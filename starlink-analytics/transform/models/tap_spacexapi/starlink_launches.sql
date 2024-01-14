
{{
  config(
    materialized='table'
  )
}}

-- launches for starlink with successful status
WITH launch AS (
  SELECT * FROM {{ source('tap_spacexapi', 'launches') }}
  WHERE name LIKE 'Starlink%' AND success = true
),

-- starlink satellites for real launch purpose
-- there are some with prototype or other purposes
starlink AS (
  SELECT
  	id,
  	launch,
  	trim(cast("spaceTrack"::json -> 'OBJECT_NAME' as VARCHAR), '"') as satellite_name
  FROM {{ source('tap_spacexapi', 'starlink') }}
  WHERE trim(cast("spaceTrack"::json -> 'OBJECT_NAME' as VARCHAR), '"') LIKE 'STARLINK%'
),

-- avg. launch duration in days
duration AS (
  SELECT 
    CEILING((DATE(MAX(date_utc)) - DATE(MIN(date_utc))) / COUNT(DISTINCT id)) as avg_launch_interval
  FROM launch
),

starlink_by_launch AS (
  select launch.id as launch_id, 
  	count(distinct starlink.id) as satellites
  FROM launch
  LEFT JOIN starlink ON launch.id = starlink.launch
  GROUP BY 1
),

-- total launches, and total satellites launches
starlink_lauched AS (
  SELECT 
    COUNT(DISTINCT launch_id) as total_launches,
    COALESCE(SUM(satellites), 0) AS total_satellites
  FROM starlink_by_launch
),

-- calculate remaining launches
starlink_analytics as (
  SELECT 
    total_launches,
    total_satellites,
    (42000 - total_satellites) AS remaining_satellites,
    CEILING((42000 - total_satellites) / (total_satellites/total_launches)) AS remaining_launches
  FROM starlink_lauched
),

-- with target date to achieve 42000 satellite launch and other metadata columns
final as (
	SELECT 
		sta.*,
		date(current_date + (dur.avg_launch_interval*remaining_launches) * interval '1 day') as remaining_launches_target_date,
	  (current_timestamp at time zone 'UTC') as transformation_updated_at
	FROM starlink_analytics as sta, duration as dur
)

select * from final

"""SpaceXAPI tap class."""

from __future__ import annotations

from singer_sdk import Tap
from singer_sdk import typing as th  # JSON schema typing helpers

from tap_spacexapi import streams


class TapSpaceXAPI(Tap):
    """SpaceXAPI tap class."""

    name = "tap-spacexapi"

    config_jsonschema = th.PropertiesList().to_dict()

    def discover_streams(self) -> list[streams.SpaceXAPIStream]:
        """Return a list of discovered streams.

        Returns:
            A list of discovered streams.
        """
        return [
            streams.StarlinkStream(self),
            streams.LaunchesStream(self),
        ]


if __name__ == "__main__":
    TapSpaceXAPI.cli()

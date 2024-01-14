"""Stream type classes for tap-spacexapi."""

from __future__ import annotations

import typing as t
from pathlib import Path

from tap_spacexapi.client import SpaceXAPIStream

SCHEMAS_DIR = Path(__file__).parent / Path("./schemas")

class StarlinkStream(SpaceXAPIStream):
    """Define custom stream."""

    name = "starlink"
    path = "/v4/starlink"
    primary_keys: t.ClassVar[list[str]] = ["id"]
    replication_key = None
    schema_filepath = SCHEMAS_DIR / "starlink.json"  # noqa: ERA001


class LaunchesStream(SpaceXAPIStream):
    """Define custom stream."""

    name = "launches"
    path = "/v5/launches"
    primary_keys: t.ClassVar[list[str]] = ["id"]
    replication_key = None
    schema_filepath = SCHEMAS_DIR / "launch.json"  # noqa: ERA001


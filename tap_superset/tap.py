"""Superset tap class."""

from __future__ import annotations

from singer_sdk import Tap
from singer_sdk import typing as th  # JSON schema typing helpers

from tap_superset import streams


class TapSuperset(Tap):
    """Superset tap class."""

    name = "tap-superset"

    config_jsonschema = th.PropertiesList(
        th.Property(
            "username",
            th.StringType,
            required=True,
            secret=False,
            description="Username of the db user that has access to superset api",
        ),
        th.Property(
            "password",
            th.StringType,
            required=True,
            secret=True,
            description="Password",
        ),
        th.Property(
            "start_date",
            th.DateTimeType,
            required=False,
            description="The earliest record date to sync",
        ),
        th.Property(
            "base_url",
            th.StringType,
            required=True,
            default="https://superset.com",
            description="The url for the API service",
        ),
    ).to_dict()

    def discover_streams(self) -> list[streams.SupersetStream]:
        """Return a list of discovered streams.

        Returns:
            A list of discovered streams.
        """
        return [
            # streams.UsersStream(self),
            # streams.ChartsStream(self),
            streams.LogsStream(self),
            # streams.DashboardsStream(self),
        ]


if __name__ == "__main__":
    TapSuperset.cli()

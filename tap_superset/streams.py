"""Stream type classes for tap-superset."""

from __future__ import annotations

import sys
import typing as t

from singer_sdk import typing as th  # JSON Schema typing helpers

from tap_superset.client import SupersetStream

if sys.version_info >= (3, 9):
    import importlib.resources as importlib_resources
else:
    import importlib_resources


class UsersStream(SupersetStream):
    """Users stream."""

    name = "users"
    path = "/api/v1/security/users"
    primary_keys: t.List[str] = ["id"]
    schema: t.Any = th.PropertiesList(
        th.Property("username", th.StringType),
        th.Property("email", th.StringType),
        th.Property("last_login", th.StringType),
        th.Property("username", th.StringType),
        th.Property("active", th.BooleanType),
        th.Property("changed_on", th.StringType),
        th.Property("id", th.IntegerType),
    ).to_dict()


class DashboardsStream(SupersetStream):
    """Dashboards stream."""

    name = "dashboards"
    path = "/api/v1/dashboard/"
    primary_keys: t.List[str] = ["id"]
    schema: t.Any = th.PropertiesList(
        th.Property("owners", th.ArrayType(th.AnyType)),
        th.Property("certification_details", th.StringType),
        th.Property("changed_on_utc", th.StringType),
        th.Property("certified_by", th.StringType),
        th.Property("url", th.StringType),
        th.Property("slug", th.StringType),
        th.Property("status", th.StringType),
        th.Property("published", th.BooleanType),
        th.Property("dashboard_title", th.StringType),
        th.Property("id", th.IntegerType),
    ).to_dict()


class ChartsStream(SupersetStream):
    """Charts stream."""

    name = "charts"
    path = "/api/v1/chart/"
    primary_keys: t.List[str] = ["id"]
    replication_key: str = "last_saved_at"
    schema: t.Any = th.PropertiesList(
        th.Property("is_managed_externally", th.BooleanType),
        th.Property("certified_by", th.StringType),
        th.Property("certification_details", th.StringType),
        th.Property("cache_timeout", th.StringType),
        th.Property("changed_by_name", th.StringType),
        th.Property("changed_on_utc", th.StringType),
        th.Property("created_by_name", th.StringType),
        th.Property("datasource_id", th.IntegerType),
        th.Property("datasource_name_text", th.StringType),
        th.Property("datasource_type", th.StringType),
        th.Property("description", th.StringType),
        th.Property("id", th.IntegerType),
        th.Property("last_saved_at", th.DateTimeType),
        th.Property("owners", th.ArrayType(th.AnyType)),
        th.Property("dashboards", th.ArrayType(th.AnyType)),
        th.Property("slice_name", th.StringType),
        th.Property("slice_url", th.StringType),
        th.Property("url", th.StringType),
        th.Property("viz_type", th.StringType),
    ).to_dict()


class LogsStream(SupersetStream):
    """Logs stream."""

    name = "logs"
    path = "/api/v1/log/"
    primary_keys: t.List[str] = ["id"]
    replication_key: str = "dttm"
    schema: t.Any = th.PropertiesList(
        th.Property("action", th.StringType),
        th.Property("dttm", th.DateTimeType),
        th.Property("slice_id", th.IntegerType),
        th.Property("dashboard_id", th.IntegerType),
        th.Property("user_id", th.IntegerType),
        th.Property("duration_ms", th.IntegerType),
        th.Property("id", th.IntegerType),
        th.Property("referrer", th.StringType),
    ).to_dict()

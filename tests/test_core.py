"""Tests standard tap features using the built-in SDK tests library."""

import datetime
import os

from singer_sdk.testing import get_tap_test_class

from tap_superset.tap import TapSuperset

SAMPLE_CONFIG = {
    "start_date": (datetime.datetime.now() - datetime.timedelta(hours=6)).strftime(
        "%Y-%m-%d %H:%M:%S"
    ),
    "username": os.environ.get("TAP_SUPERSET_USERNAME"),
    "password": os.environ.get("TAP_SUPERSET_PASSWORD"),
    "base_url": os.environ.get("TAP_SUPERSET_BASE_URL"),
}


TestTapSuperset = get_tap_test_class(
    tap_class=TapSuperset,
    config=SAMPLE_CONFIG,
)

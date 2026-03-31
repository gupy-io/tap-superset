"""Tests standard tap features using the built-in SDK tests library."""

import datetime
import os
import pytest

from singer_sdk.testing import get_tap_test_class

from tap_superset.tap import TapSuperset

username = os.environ.get("TAP_SUPERSET_USERNAME")
password = os.environ.get("TAP_SUPERSET_PASSWORD")
base_url = os.environ.get("TAP_SUPERSET_BASE_URL")

if username and password and base_url:
    SAMPLE_CONFIG = {
        "start_date": (datetime.datetime.now() - datetime.timedelta(hours=6)).strftime(
            "%Y-%m-%d %H:%M:%S"
        ),
        "username": username,
        "password": password,
        "base_url": base_url,
    }

    TestTapSuperset = get_tap_test_class(
        tap_class=TapSuperset,
        config=SAMPLE_CONFIG,
    )
else:
    # Skip tests if no config is provided
    pytest.skip("Missing TAP_SUPERSET_USERNAME, TAP_SUPERSET_PASSWORD, or TAP_SUPERSET_BASE_URL", allow_module_level=True)

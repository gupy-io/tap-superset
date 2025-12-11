"""Tests for ChartsStream in tap-superset."""

import copy
from unittest.mock import Mock, patch
import pytest
from requests import Response
import jsonschema

from tap_superset.streams import ChartsStream
from tap_superset.tap import TapSuperset


@pytest.fixture
def tap_instance():
    """Create a tap instance for testing."""
    config = {
        "username": "test_user",
        "password": "test_password",
        "base_url": "https://test-superset.com",
    }
    return TapSuperset(config=config)


@pytest.fixture
def charts_stream(tap_instance):
    """Create a ChartsStream instance for testing."""
    return ChartsStream(tap_instance)


def create_mock_response(data: dict) -> Response:
    """Create a mocked API response."""
    from datetime import timedelta
    
    response = Mock(spec=Response)
    response.json.return_value = data
    response.status_code = 200
    response.elapsed = timedelta(seconds=0.1)
    return response


def get_base_chart_data():
    """Return base chart data for reuse."""
    return {
        "count": 1,
        "description_columns": {},
        "ids": [22186],
        "label_columns": {
            "cache_timeout": "Cache Timeout",
            "slice_name": "Slice Name",
        },
        "list_columns": ["cache_timeout", "slice_name", "id"],
        "list_title": "List Slice",
        "order_columns": ["slice_name"],
        "result": [
            {
                "id": 22186,
                "slice_name": "Test Chart",
                "viz_type": "bar",
                "datasource_id": 17755,
                "datasource_name_text": "test_table",
                "datasource_type": "table",
                "last_saved_at": "2025-12-10T20:10:16.917420",
                "is_managed_externally": False,
                "certified_by": None,
                "certification_details": None,
                "changed_by_name": "Test User",
                "changed_on_utc": "2025-12-10T20:10:16.929063+0000",
                "created_by_name": "Test User",
                "description": None,
                "owners": [],
                "dashboards": [],
                "slice_url": "/explore/?slice_id=22186",
                "url": "/explore/?slice_id=22186",
            }
        ],
    }


def get_empty_response_data():
    """Return empty response data for subsequent pages to prevent infinite pagination loop."""
    return {
        "count": 0,
        "description_columns": {},
        "ids": [],
        "label_columns": {},
        "list_columns": [],
        "list_title": "List Slice",
        "order_columns": [],
        "result": [],
    }


def create_paginated_mock_send(data_with_records):
    """Create a mock send that returns data on first call and empty on subsequent calls."""
    call_count = {"count": 0}
    empty_data = get_empty_response_data()
    
    def mock_send_side_effect(request, **kwargs):
        call_count["count"] += 1
        if call_count["count"] == 1:
            return create_mock_response(data_with_records)
        else:
            return create_mock_response(empty_data)
    
    return mock_send_side_effect, call_count


def test_charts_stream_cache_timeout_null_or_int(charts_stream):
    """Test that cache_timeout null or int should pass schema validation."""
    base_data = get_base_chart_data()
    schema = charts_stream.schema

    mock_data_null = copy.deepcopy(base_data)
    mock_data_null["result"][0]["cache_timeout"] = None

    mock_data_int = copy.deepcopy(base_data)
    mock_data_int["result"][0]["cache_timeout"] = 3600
    mock_data_int["ids"] = [22187]
    mock_data_int["result"][0]["id"] = 22187

    mock_auth_response = Mock()
    mock_auth_response.json.return_value = {"access_token": "mock_token"}

    with patch("tap_superset.auth.requests.post", return_value=mock_auth_response):
        mock_send_null, _ = create_paginated_mock_send(mock_data_null)
        with patch.object(charts_stream.requests_session, "send", side_effect=mock_send_null):
            with patch.object(charts_stream, "post_process", wraps=charts_stream.post_process) as mock_post_process:
                records = list(charts_stream.get_records({}))
                assert len(records) == 1
                record = records[0]
                assert record["cache_timeout"] is None
                assert record["id"] == 22186
                
                assert mock_post_process.called, "post_process should be called to transform records"
                assert mock_post_process.call_count == 1, "post_process should be called once per record"
                
                jsonschema.validate(instance=record, schema=schema)

        mock_send_int, _ = create_paginated_mock_send(mock_data_int)
        with patch.object(charts_stream.requests_session, "send", side_effect=mock_send_int):
            with patch.object(charts_stream, "post_process", wraps=charts_stream.post_process) as mock_post_process:
                records = list(charts_stream.get_records({}))
                assert len(records) == 1
                record = records[0]
                assert record["cache_timeout"] == 3600
                assert isinstance(record["cache_timeout"], int)
                assert record["id"] == 22187
                
                assert mock_post_process.called, "post_process should be called to transform records"
                assert mock_post_process.call_count == 1, "post_process should be called once per record"
                
                jsonschema.validate(instance=record, schema=schema)


def test_charts_stream_cache_timeout_string_should_fail(charts_stream):
    """Test that cache_timeout as string should raise exception in schema validation."""
    base_data = get_base_chart_data()

    mock_data_string = copy.deepcopy(base_data)
    mock_data_string["result"][0]["cache_timeout"] = "3600"

    mock_auth_response = Mock()
    mock_auth_response.json.return_value = {"access_token": "mock_token"}

    mock_send, call_count = create_paginated_mock_send(mock_data_string)

    with patch("tap_superset.auth.requests.post", return_value=mock_auth_response):
        call_count["count"] = 0
        with patch.object(charts_stream.requests_session, "send", side_effect=mock_send):
            with patch.object(charts_stream, "post_process", wraps=charts_stream.post_process) as mock_post_process:
                records = list(charts_stream.get_records({}))
                assert len(records) == 1

                record = records[0]
                assert isinstance(record["cache_timeout"], str)
                assert record["cache_timeout"] == "3600"

                assert mock_post_process.called, "post_process should be called to transform records"
                assert mock_post_process.call_count == 1, "post_process should be called once per record"

                schema = charts_stream.schema
                
                with pytest.raises(jsonschema.ValidationError) as exc_info:
                    jsonschema.validate(instance=record, schema=schema)
                
                assert "cache_timeout" in str(exc_info.value).lower() or "3600" in str(exc_info.value)


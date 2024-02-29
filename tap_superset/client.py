"""REST client handling, including SupersetStream base class."""

from __future__ import annotations

import sys
import json
import logging
from typing import Any, Callable, Iterable, List

import requests
from singer_sdk.authenticators import BearerTokenAuthenticator
from singer_sdk.helpers.jsonpath import extract_jsonpath
from singer_sdk.pagination import BaseAPIPaginator  # noqa: TCH002
from singer_sdk.streams import RESTStream
from singer_sdk.pagination import BasePageNumberPaginator
from tap_superset.auth import get_auth_token
from tap_superset.client_helper import update_dict_with, get_start_timestamp

if sys.version_info >= (3, 9):
    import importlib.resources as importlib_resources
else:
    import importlib_resources

_Auth = Callable[[requests.PreparedRequest], requests.PreparedRequest]


class SupersetStream(RESTStream):
    """Superset stream class."""

    @property
    def url_base(self) -> str:
        """Return the API URL root, configurable via tap settings."""
        return self.config["base_url"]

    records_jsonpath = "$[*]"  # Or override `parse_response`.

    # Set this value or override `get_new_paginator`.
    next_page_token_jsonpath = "$.next_page"  # noqa: S105

    @property
    def authenticator(self) -> BearerTokenAuthenticator:
        """Return a new authenticator object.

        Returns:
            An authenticator instance.
        """
        auth_token = get_auth_token(
            base_url=self.config.get("base_url"),
            username=self.config.get("username"),
            password=self.config.get("password"),
        )
        return BearerTokenAuthenticator.create_for_stream(
            self,
            token=auth_token,
        )

    @property
    def http_headers(self) -> dict:
        """Return the http headers needed.

        Returns:
            A dictionary of HTTP headers.
        """
        headers = {"accept": "application/json"}
        return headers

    def get_new_paginator(self) -> BaseAPIPaginator:
        """Create a new pagination helper instance.

        If the source API can make use of the `next_page_token_jsonpath`
        attribute, or it contains a `X-Next-Page` header in the response
        then you can remove this method.

        If you need custom pagination that uses page numbers, "next" links, or
        other approaches, please read the guide: https://sdk.meltano.com/en/v0.25.0/guides/pagination-classes.html.

        Returns:
            A pagination helper instance.
        """
        return BasePageNumberPaginator(0)

    def get_url_params(
        self,
        context: dict | None,  # noqa: ARG002
        next_page_token: Any | None,  # noqa: ANN401
    ) -> dict[str, Any]:
        """Return a dictionary of values to be used in URL parameterization.

        Args:
            context: The stream context.
            next_page_token: The next page index or value.

        Returns:
            A dictionary of URL query parameters.
        """
        params = {
            "columns": [],
            "page": 0,
            "page_size": 50,
            "filters": [],
        }
        start_timestamp = get_start_timestamp(
            self.get_starting_replication_key_value(context)
        )
        if next_page_token:
            params["page"] = next_page_token
        if self.replication_key:
            params["order_direction"] = "asc"
            params["order_column"] = self.replication_key
        if start_timestamp:
            params["filters"] = [
                {
                    "col": self.replication_key,
                    "opr": "gt",
                    "value": start_timestamp,
                }
            ]

        return {"q": json.dumps(params)}

    def parse_response(self, response: requests.Response) -> Iterable[dict]:
        """Parse the response and return an iterator of result records.

        Args:
            response: The HTTP ``requests.Response`` object.

        Yields:
            Each record from the source.
        """
        res = response.json()
        result = res["result"]
        if "ids" not in result:
            result = update_dict_with(result, "id", res["ids"])

        yield from extract_jsonpath(self.records_jsonpath, input=result)

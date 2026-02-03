#!/usr/bin/env python3
"""Store Marketing API tools for Sensor Tower MCP Server."""

from typing import Annotated, Literal, Optional, Union

from fastmcp import FastMCP
from pydantic import Field

from ..base import SensorTowerTool, validate_date_format, validate_os_parameter


class StoreMarketingTools(SensorTowerTool):
    """Tools for Store Marketing API endpoints."""

    category = "StoreMarketing"

    def register_tools(self, mcp: FastMCP) -> None:
        """Register all store marketing tools with FastMCP."""

        @self.tool(
            mcp,
            name="get_featured_today_stories",
            title="Get Featured Today Stories",
        )
        async def get_featured_today_stories(
            country: Annotated[
                str,
                Field(description="ISO country code", min_length=2, max_length=2),
            ] = "US",
            start_date: Annotated[
                Optional[str],
                Field(description="Start date in YYYY-MM-DD format", default=None),
            ] = None,
            end_date: Annotated[
                Optional[str],
                Field(description="End date in YYYY-MM-DD format", default=None),
            ] = None,
        ) -> dict:
            """Retrieve featured Today stories from the App Store."""

            params = {"country": country}
            if start_date:
                params["start_date"] = validate_date_format(start_date)
            if end_date:
                params["end_date"] = validate_date_format(end_date)

            return await self.make_request("/v1/ios/featured/today/stories", params)

        @self.tool(
            mcp,
            name="get_featured_apps",
            title="Get Featured Apps",
        )
        async def get_featured_apps(
            category: Annotated[
                Union[int, str],
                Field(description="Category identifier"),
            ],
            country: Annotated[
                str,
                Field(description="ISO country code", min_length=2, max_length=2),
            ] = "US",
            start_date: Annotated[
                Optional[str],
                Field(description="Start date in YYYY-MM-DD format", default=None),
            ] = None,
            end_date: Annotated[
                Optional[str],
                Field(description="End date in YYYY-MM-DD format", default=None),
            ] = None,
        ) -> dict:
            """Retrieve featured apps on the App Store's Apps & Games pages."""

            params = {
                "category": category,
                "country": country,
            }
            if start_date:
                params["start_date"] = validate_date_format(start_date)
            if end_date:
                params["end_date"] = validate_date_format(end_date)

            return await self.make_request("/v1/ios/featured/apps", params)

        @self.tool(
            mcp,
            name="get_featured_creatives",
            title="Get Featured Creatives",
        )
        async def get_featured_creatives(
            os: Annotated[
                Literal["ios", "android"],
                Field(description="Operating system"),
            ],
            app_id: Annotated[str, Field(description="App identifier", min_length=1)],
            countries: Annotated[
                Optional[str],
                Field(description="Comma-separated country codes", default=None),
            ] = None,
            types: Annotated[
                Optional[str],
                Field(description="Comma-separated creative types", default=None),
            ] = None,
            start_date: Annotated[
                Optional[str],
                Field(description="Start date in YYYY-MM-DD format", default=None),
            ] = None,
            end_date: Annotated[
                Optional[str],
                Field(description="End date in YYYY-MM-DD format", default=None),
            ] = None,
        ) -> dict:
            """Retrieve featured creatives and their positions over time.

            Note: app_id is required. The API will return 422 if not provided.
            """

            os_value = validate_os_parameter(os, ["ios", "android"])
            params = {"app_id": app_id}

            optional_params = {
                "countries": countries,
                "types": types,
                "start_date": validate_date_format(start_date) if start_date else None,
                "end_date": validate_date_format(end_date) if end_date else None,
            }

            for key, value in optional_params.items():
                if value:
                    params[key] = value

            return await self.make_request(
                f"/v1/{os_value}/featured/creatives",
                params,
            )

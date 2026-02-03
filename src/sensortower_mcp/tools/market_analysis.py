#!/usr/bin/env python3
"""Market Analysis API tools for Sensor Tower MCP Server."""

import warnings
from typing import Annotated, Literal, Optional, Union

from fastmcp import FastMCP
from pydantic import Field

from ..base import SensorTowerTool, validate_date_format, validate_os_parameter


class MarketAnalysisTools(SensorTowerTool):
    """Tools for Market Analysis API endpoints."""

    category = "MarketAnalysis"

    def register_tools(self, mcp: FastMCP) -> None:
        """Register all market analysis tools with FastMCP."""

        @self.tool(
            mcp,
            name="get_store_summary",
            title="Get Store Summary",
        )
        async def get_store_summary(
            os: Annotated[
                Literal["ios", "android"],
                Field(description="Operating system"),
            ],
            categories: Annotated[
                str,
                Field(description="Comma-separated category identifiers", min_length=1),
            ],
            start_date: Annotated[str, Field(description="Start date in YYYY-MM-DD format")],
            end_date: Annotated[str, Field(description="End date in YYYY-MM-DD format")],
            date_granularity: Annotated[
                Literal["daily", "weekly", "monthly", "quarterly"],
                Field(description="Granularity of aggregated data"),
            ] = "daily",
            countries: Annotated[
                str,
                Field(description="Comma-separated country codes"),
            ] = "US",
        ) -> dict:
            """Get app store summary statistics.

            ⚠️ TEMPORARILY DISABLED: This endpoint is currently returning 500 Internal
            Server Error from Sensor Tower's API. This is a server-side issue.
            Please contact Sensor Tower support or try again later.
            """

            warnings.warn(
                "get_store_summary is experiencing API server errors (500). "
                "Contact Sensor Tower support if this persists.",
                UserWarning
            )

            os_value = validate_os_parameter(os, ["ios", "android"])
            start_value = validate_date_format(start_date)
            end_value = validate_date_format(end_date)

            params = {
                "categories": categories,
                "start_date": start_value,
                "end_date": end_value,
                "date_granularity": date_granularity,
                "countries": countries,
            }

            return await self.make_request(
                f"/v1/{os_value}/store_summary",
                params,
            )

        @self.tool(
            mcp,
            name="top_apps",
            title="Top Apps",
        )
        async def top_apps(
            os: Annotated[
                Literal["ios", "android", "unified"],
                Field(description="Operating system scope"),
            ],
            role: Annotated[
                Literal["advertisers", "publishers"],
                Field(description="Role to rank"),
            ],
            date: Annotated[str, Field(description="Start date in YYYY-MM-DD format")],
            period: Annotated[
                Literal["week", "month", "quarter"],
                Field(description="Aggregation period"),
            ],
            category: Annotated[
                Union[int, str],
                Field(description="Category identifier"),
            ],
            country: Annotated[
                str,
                Field(description="ISO country code"),
            ],
            network: Annotated[
                str,
                Field(description="Ad network name"),
            ],
            custom_fields_filter_id: Annotated[
                Optional[str],
                Field(description="Optional custom fields filter", default=None),
            ] = None,
            limit: Annotated[
                int,
                Field(description="Maximum number of apps", ge=1, le=250),
            ] = 25,
            page: Annotated[
                int,
                Field(description="Page number", ge=1),
            ] = 1,
        ) -> dict:
            """Fetch Share of Voice for top advertisers or publishers."""

            os_value = validate_os_parameter(os, ["ios", "android", "unified"])
            date_value = validate_date_format(date)

            params = {
                "role": role,
                "date": date_value,
                "period": period,
                "category": category,
                "country": country,
                "network": network,
                "limit": limit,
                "page": page,
            }
            if custom_fields_filter_id:
                params["custom_fields_filter_id"] = custom_fields_filter_id

            return await self.make_request(
                f"/v1/{os_value}/ad_intel/top_apps",
                params,
            )

        @self.tool(
            mcp,
            name="top_apps_search",
            title="Top Apps Search",
        )
        async def top_apps_search(
            os: Annotated[
                Literal["ios", "android", "unified"],
                Field(description="Operating system scope"),
            ],
            app_id: Annotated[str, Field(description="App identifier to search", min_length=1)],
            role: Annotated[
                Literal["advertisers", "publishers"],
                Field(description="Role to rank"),
            ],
            date: Annotated[str, Field(description="Date in YYYY-MM-DD format")],
            period: Annotated[
                Literal["week", "month", "quarter"],
                Field(description="Aggregation period"),
            ],
            category: Annotated[
                Union[int, str],
                Field(description="Category identifier"),
            ],
            country: Annotated[
                str,
                Field(description="ISO country code"),
            ],
            network: Annotated[
                str,
                Field(description="Ad network name"),
            ],
        ) -> dict:
            """Fetch the rank of a top advertiser or publisher for the given filters."""

            os_value = validate_os_parameter(os, ["ios", "android", "unified"])
            date_value = validate_date_format(date)

            valid_networks = {
                "Adcolony",
                "Admob",
                "Apple Search Ads",
                "Applovin",
                "Chartboost",
                "Instagram",
                "Mopub",
                "Pinterest",
                "Snapchat",
                "Supersonic",
                "Tapjoy",
                "TikTok",
                "Unity",
                "Vungle",
                "Youtube",
            }
            network_mapping = {
                "unity": "Unity",
                "google": "Youtube",
                "youtube": "Youtube",
                "admob": "Admob",
                "applovin": "Applovin",
                "chartboost": "Chartboost",
                "instagram": "Instagram",
                "snapchat": "Snapchat",
                "tiktok": "TikTok",
                "mopub": "Mopub",
                "tapjoy": "Tapjoy",
                "vungle": "Vungle",
                "pinterest": "Pinterest",
                "apple search ads": "Apple Search Ads",
                "adcolony": "Adcolony",
                "supersonic": "Supersonic",
            }

            normalized_network = network
            if isinstance(network, str):
                if network in valid_networks:
                    normalized_network = network
                elif network.lower() in network_mapping:
                    normalized_network = network_mapping[network.lower()]
                elif network.lower() == "facebook":
                    normalized_network = "Instagram"

            params = {
                "app_id": app_id,
                "role": role,
                "date": date_value,
                "period": period,
                "category": str(category),
                "country": country,
                "network": normalized_network,
            }

            return await self.make_request(
                f"/v1/{os_value}/ad_intel/top_apps/search",
                params,
            )

        @self.tool(
            mcp,
            name="games_breakdown",
            title="Games Breakdown",
        )
        async def games_breakdown(
            os: Annotated[
                Literal["ios", "android"],
                Field(description="Operating system"),
            ],
            categories: Annotated[
                str,
                Field(description="Comma-separated game categories", min_length=1),
            ],
            start_date: Annotated[str, Field(description="Start date in YYYY-MM-DD format")],
            end_date: Annotated[str, Field(description="End date in YYYY-MM-DD format")],
            date_granularity: Annotated[
                Literal["daily", "weekly", "monthly", "quarterly"],
                Field(description="Granularity for the estimates"),
            ] = "daily",
            countries: Annotated[
                Optional[str],
                Field(description="Comma-separated country codes", default=None),
            ] = None,
        ) -> dict:
            """Retrieve aggregated download and revenue estimates of game categories."""

            os_value = validate_os_parameter(os, ["ios", "android"])
            start_value = validate_date_format(start_date)
            end_value = validate_date_format(end_date)

            params = {
                "categories": categories,
                "start_date": start_value,
                "end_date": end_value,
                "date_granularity": date_granularity,
            }
            if countries:
                params["countries"] = countries

            return await self.make_request(
                f"/v1/{os_value}/games_breakdown",
                params,
            )

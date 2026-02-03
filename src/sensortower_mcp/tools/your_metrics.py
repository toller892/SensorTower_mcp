#!/usr/bin/env python3
"""Your Metrics API tools for Sensor Tower MCP Server (Connected Apps)."""

from typing import Annotated, Literal, Optional

from fastmcp import FastMCP
from fastmcp.exceptions import ToolError
from pydantic import Field

from ..base import SensorTowerTool, validate_date_format


class YourMetricsTools(SensorTowerTool):
    """Tools for Your Metrics API endpoints (Connected Apps)."""

    category = "YourMetrics"

    def register_tools(self, mcp: FastMCP) -> None:
        """Register all your metrics tools with FastMCP."""

        @self.tool(
            mcp,
            name="sales_reports",
            title="Sales Reports",
        )
        async def sales_reports(
            os: Annotated[
                Literal["ios", "android"],
                Field(description="Operating system for the report"),
            ],
            app_ids: Annotated[
                str,
                Field(description="Comma-separated app IDs you manage", min_length=1),
            ],
            countries: Annotated[
                str,
                Field(description="Comma-separated country codes", min_length=2),
            ],
            date_granularity: Annotated[
                Literal["daily", "weekly", "monthly", "quarterly"],
                Field(description="Granularity for aggregation"),
            ],
            start_date: Annotated[str, Field(description="Start date in YYYY-MM-DD format")],
            end_date: Annotated[str, Field(description="End date in YYYY-MM-DD format")],
        ) -> dict:
            """Get downloads and revenue sales report for connected apps."""

            params = {
                "app_ids": app_ids,
                "countries": countries,
                "date_granularity": date_granularity,
                "start_date": validate_date_format(start_date),
                "end_date": validate_date_format(end_date),
            }

            return await self.make_request(
                f"/v1/{os}/sales_reports",
                params,
            )

        @self.tool(
            mcp,
            name="unified_sales_reports",
            title="Unified Sales Reports",
        )
        async def unified_sales_reports(
            unified_app_ids: Annotated[
                str,
                Field(description="Comma-separated unified app IDs", min_length=1),
            ],
            start_date: Annotated[str, Field(description="Start date in YYYY-MM-DD format")],
            end_date: Annotated[str, Field(description="End date in YYYY-MM-DD format")],
            date_granularity: Annotated[
                Literal["daily", "weekly", "monthly", "quarterly"],
                Field(description="Granularity for aggregation"),
            ],
            countries: Annotated[
                Optional[str],
                Field(description="Comma-separated country codes", default=None),
            ] = None,
        ) -> dict:
            """Get unified downloads and revenue sales report for connected apps."""

            params = {
                "unified_app_ids": unified_app_ids,
                "date_granularity": date_granularity,
                "start_date": validate_date_format(start_date),
                "end_date": validate_date_format(end_date),
            }

            if countries:
                params["countries"] = countries

            return await self.make_request(
                "/v1/unified/sales_reports",
                params,
            )

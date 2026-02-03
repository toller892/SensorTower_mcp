# MCP Tool Optimization Summary

**Date:** 2026-02-03
**Based on:** Sensor Tower MCP Compatibility Test Report (Updated Version)

## Overview

This document summarizes the optimization work performed on the Sensor Tower MCP tool collection to align with official API documentation and remove deprecated endpoints.

## Changes Made

### Removed Tools (11 total)

The following tools were removed because their API endpoints return 404 and are not documented in the official Sensor Tower API:

#### SearchDiscoveryTools (1 tool)
- `search_entities` - `/v1/ios/search`

#### MarketAnalysisTools (5 tools)
- `get_top_and_trending` - `/v1/unified/top_and_trending`
- `get_top_publishers` - `/v1/unified/top_publishers`
- `usage_top_apps` - `/v1/unified/usage/top_apps`
- `get_category_rankings` - `/v1/ios/rankings`
- `top_creatives` - `/v1/ios/ad_intel/top_creatives`

#### YourMetricsTools (2 tools)
- `analytics_metrics` - `/v1/ios/analytics/metrics`
- `sources_metrics` - `/v1/ios/analytics/sources`

#### StoreMarketingTools (3 tools)
- `get_keywords` - `/v1/ios/keywords`
- `get_reviews` - `/v1/ios/reviews`
- `research_keyword` - `/v1/ios/keywords/research`

### Fixed Tools (2 total)

#### Parameter Fixes
- `get_featured_creatives` - Clarified that `app_id` is required (was already enforced)
- `unified_sales_reports` - Added required `unified_app_ids` parameter

### Documented Tools (4 total)

#### Permission Requirements
- `sales_reports` - Added warning about special API authorization requirement (returns 401)

#### Server Issues
- `get_store_summary` - Added warning about server-side 500 errors

#### Unofficial APIs (Shadow APIs)
- `top_apps` - Marked as unofficial but working
- `top_apps_search` - Marked as unofficial but working
- `games_breakdown` - Marked as unofficial but working

## Tool Count

- **Before:** 40 tools
- **After:** 29 tools
- **Removed:** 11 tools

## Recommendations

### For Users

1. **Avoid removed tools** - They will no longer be available
2. **Check permissions** - If `sales_reports` returns 401, contact Sensor Tower support
3. **Monitor unofficial tools** - The 3 "shadow API" tools may stop working without notice
4. **Report issues** - If `get_store_summary` continues to fail, contact Sensor Tower

### For Maintainers

1. **Phase 3 work** - Audit remaining 29 tools against official documentation
2. **Add missing tools** - Implement any official API endpoints not yet in MCP
3. **Monitor shadow APIs** - Track if unofficial endpoints become documented or deprecated
4. **Update tests** - Remove tests for deprecated tools, add tests for fixed tools

## References

- Original Report: `Sensor Tower MCP 工具兼容性测试与优化报告 (更新版).md`
- Implementation Plan: `docs/plans/2026-02-03-mcp-tool-optimization.md`

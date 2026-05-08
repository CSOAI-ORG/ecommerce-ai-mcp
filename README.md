<div align="center">

# Ecommerce Ai MCP

**E-Commerce AI MCP Server - Online Retail Intelligence**

[![PyPI](https://img.shields.io/pypi/v/meok-ecommerce-ai-mcp)](https://pypi.org/project/meok-ecommerce-ai-mcp/)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![MEOK AI Labs](https://img.shields.io/badge/MEOK_AI_Labs-MCP_Server-purple)](https://meok.ai)

</div>

## Overview

E-Commerce AI MCP Server - Online Retail Intelligence
Built by MEOK AI Labs | https://meok.ai

Product description writing, pricing optimization, review summarization,
inventory forecasting, and SEO meta generation.

## Tools

| Tool | Description |
|------|-------------|
| `write_product_description` | Generate a compelling product description for an e-commerce listing. |
| `optimize_pricing` | Optimize product pricing using market data and strategy. |
| `summarize_reviews` | Summarize product reviews into actionable insights. |
| `forecast_inventory` | Forecast inventory needs and generate reorder recommendations. |
| `generate_seo_meta` | Generate SEO-optimized meta tags for product pages. |

## Installation

```bash
pip install meok-ecommerce-ai-mcp
```

## Usage with Claude Desktop

Add to your Claude Desktop MCP config (`claude_desktop_config.json`):

```json
{
  "mcpServers": {
    "ecommerce-ai": {
      "command": "python",
      "args": ["-m", "meok_ecommerce_ai_mcp.server"]
    }
  }
}
```

## Usage with FastMCP

```python
from mcp.server.fastmcp import FastMCP

# This server exposes 5 tool(s) via MCP
# See server.py for full implementation
```

## License

MIT © [MEOK AI Labs](https://meok.ai)

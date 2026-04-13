# E-Commerce AI MCP Server

**Online Retail Intelligence**

Built by [MEOK AI Labs](https://meok.ai)

---

An MCP server for e-commerce businesses. Write compelling product descriptions, optimize pricing with competitor analysis, summarize product reviews into actionable insights, forecast inventory with reorder alerts, and generate SEO-optimized meta tags.

## Tools

| Tool | Description |
|------|-------------|
| `write_product_description` | Generate compelling product descriptions with audience-targeted tone |
| `optimize_pricing` | Pricing optimization using market data and strategy selection |
| `summarize_reviews` | Summarize reviews into aspect-based insights with pros and cons |
| `forecast_inventory` | Inventory forecasting with reorder points and stockout projections |
| `generate_seo_meta` | Generate SEO meta tags, Open Graph, and Schema.org markup |

## Quick Start

```bash
pip install ecommerce-ai-mcp
```

### Claude Desktop

```json
{
  "mcpServers": {
    "ecommerce-ai": {
      "command": "python",
      "args": ["-m", "server"],
      "cwd": "/path/to/ecommerce-ai-mcp"
    }
  }
}
```

### Direct Usage

```bash
python server.py
```

## Rate Limits

| Tier | Requests/Hour |
|------|--------------|
| Free | 60 |
| Pro | 5,000 |

## License

MIT - see [LICENSE](LICENSE)

---

*Part of the MEOK AI Labs MCP Marketplace*

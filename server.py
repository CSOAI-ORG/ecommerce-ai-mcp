"""
E-Commerce AI MCP Server - Online Retail Intelligence
Built by MEOK AI Labs | https://meok.ai

Product description writing, pricing optimization, review summarization,
inventory forecasting, and SEO meta generation.
"""

import time
import math
from datetime import datetime, timezone
from typing import Optional

from mcp.server.fastmcp import FastMCP

mcp = FastMCP(
    "ecommerce-ai",
    version="1.0.0",
    description="E-commerce AI - product copy, pricing, review summaries, inventory, SEO",
)

# ---------------------------------------------------------------------------
# Rate limiting
# ---------------------------------------------------------------------------
_RATE_LIMITS = {"free": {"requests_per_hour": 60}, "pro": {"requests_per_hour": 5000}}
_request_log: list[float] = []
_tier = "free"


def _check_rate_limit() -> bool:
    now = time.time()
    _request_log[:] = [t for t in _request_log if now - t < 3600]
    if len(_request_log) >= _RATE_LIMITS[_tier]["requests_per_hour"]:
        return False
    _request_log.append(now)
    return True


# ---------------------------------------------------------------------------
# Data
# ---------------------------------------------------------------------------
_PRICE_STRATEGIES = {
    "penetration": {"description": "Low price to gain market share", "margin_range": (5, 15)},
    "premium": {"description": "High price signaling quality", "margin_range": (40, 70)},
    "competitive": {"description": "Match market average", "margin_range": (20, 35)},
    "economy": {"description": "Lowest cost positioning", "margin_range": (3, 10)},
    "skimming": {"description": "High initial price, reduce over time", "margin_range": (50, 80)},
    "bundle": {"description": "Discount for multi-item purchase", "margin_range": (15, 30)},
}

_CATEGORY_KEYWORDS: dict[str, list[str]] = {
    "electronics": ["tech", "smart", "wireless", "bluetooth", "usb", "digital", "powered", "rechargeable"],
    "clothing": ["comfortable", "breathable", "stylish", "fitted", "casual", "premium", "soft", "durable"],
    "home": ["elegant", "modern", "practical", "space-saving", "easy-clean", "decorative", "functional"],
    "beauty": ["natural", "organic", "nourishing", "gentle", "radiant", "hydrating", "refreshing"],
    "sports": ["performance", "lightweight", "grip", "aerodynamic", "sweat-resistant", "training", "pro"],
    "food": ["artisan", "organic", "handcrafted", "fresh", "gourmet", "traditional", "natural"],
}


@mcp.tool()
def write_product_description(
    product_name: str,
    category: str,
    features: list[str],
    target_audience: str = "general",
    tone: str = "professional",
    price: Optional[float] = None,
    include_bullet_points: bool = True,
) -> dict:
    """Generate a compelling product description for an e-commerce listing.

    Args:
        product_name: Name of the product.
        category: electronics | clothing | home | beauty | sports | food.
        features: List of key product features.
        target_audience: general | young_adults | professionals | parents | luxury | budget.
        tone: professional | casual | luxury | minimalist | energetic.
        price: Product price (for value messaging).
        include_bullet_points: Whether to include formatted bullet points.
    """
    if not _check_rate_limit():
        return {"error": "Rate limit exceeded. Upgrade to pro tier."}

    power_words = _CATEGORY_KEYWORDS.get(category, ["quality", "premium", "reliable"])

    audience_hooks = {
        "general": "Designed for everyday use",
        "young_adults": "Made for the modern lifestyle",
        "professionals": "Engineered for professionals who demand the best",
        "parents": "Built with families in mind",
        "luxury": "For those who accept nothing less than excellence",
        "budget": "Premium quality without the premium price tag",
    }

    tone_style = {
        "professional": {"opener": "Introducing", "quality": "exceptional", "verb": "delivers"},
        "casual": {"opener": "Meet", "quality": "awesome", "verb": "brings"},
        "luxury": {"opener": "Presenting", "quality": "exquisite", "verb": "embodies"},
        "minimalist": {"opener": "The", "quality": "essential", "verb": "offers"},
        "energetic": {"opener": "Get ready for", "quality": "incredible", "verb": "powers"},
    }

    style = tone_style.get(tone, tone_style["professional"])
    hook = audience_hooks.get(target_audience, audience_hooks["general"])

    headline = f"{style['opener']} the {product_name}"
    intro = f"{hook}. The {product_name} {style['verb']} {style['quality']} performance with features you'll love."

    bullet_points = []
    if include_bullet_points:
        for feature in features[:6]:
            pw = power_words[len(bullet_points) % len(power_words)]
            bullet_points.append(f"{pw.title()} {feature}")

    cta = "Add to cart today" if not price else f"Get yours for just ${price:.2f}"
    if target_audience == "luxury":
        cta = "Experience the difference"

    full_description = f"{intro}\n\n" + "\n".join(f"- {bp}" for bp in bullet_points) + f"\n\n{cta}"

    return {
        "headline": headline,
        "description": full_description,
        "intro": intro,
        "bullet_points": bullet_points,
        "call_to_action": cta,
        "seo_title": f"{product_name} | {category.title()} | Shop Now",
        "word_count": len(full_description.split()),
        "generated_at": datetime.now(timezone.utc).isoformat(),
    }


@mcp.tool()
def optimize_pricing(
    cost: float,
    competitor_prices: Optional[list[float]] = None,
    strategy: str = "competitive",
    target_margin_pct: Optional[float] = None,
    demand_level: str = "medium",
) -> dict:
    """Optimize product pricing using market data and strategy.

    Args:
        cost: Product cost (COGS).
        competitor_prices: List of competitor prices for the same/similar product.
        strategy: penetration | premium | competitive | economy | skimming | bundle.
        target_margin_pct: Target gross margin percentage (overrides strategy default).
        demand_level: low | medium | high (affects pricing recommendations).
    """
    if not _check_rate_limit():
        return {"error": "Rate limit exceeded. Upgrade to pro tier."}

    strat = _PRICE_STRATEGIES.get(strategy, _PRICE_STRATEGIES["competitive"])

    if target_margin_pct is not None:
        margin_pct = target_margin_pct
    else:
        margin_pct = sum(strat["margin_range"]) / 2

    base_price = cost / (1 - margin_pct / 100)

    # Competitor analysis
    comp_analysis = None
    if competitor_prices and len(competitor_prices) > 0:
        avg_comp = sum(competitor_prices) / len(competitor_prices)
        min_comp = min(competitor_prices)
        max_comp = max(competitor_prices)

        comp_analysis = {
            "average": round(avg_comp, 2),
            "min": round(min_comp, 2),
            "max": round(max_comp, 2),
            "your_position": "below_average" if base_price < avg_comp else "above_average" if base_price > avg_comp else "at_average",
        }

        # Adjust based on strategy and competitors
        if strategy == "competitive":
            base_price = avg_comp * 0.98  # Slightly below average
        elif strategy == "penetration":
            base_price = min_comp * 0.95
        elif strategy == "premium":
            base_price = max_comp * 1.10

    # Demand adjustment
    demand_mult = {"low": 0.92, "medium": 1.0, "high": 1.08}
    adjusted_price = base_price * demand_mult.get(demand_level, 1.0)

    actual_margin = round(((adjusted_price - cost) / adjusted_price) * 100, 1) if adjusted_price > 0 else 0
    profit_per_unit = round(adjusted_price - cost, 2)

    # Psychological pricing
    charm_price = math.floor(adjusted_price) - 0.01 if adjusted_price > 10 else round(adjusted_price, 2)
    rounded_price = round(adjusted_price / 5) * 5 if adjusted_price > 50 else round(adjusted_price, 0)

    return {
        "cost": cost,
        "strategy": strategy,
        "recommended_price": round(adjusted_price, 2),
        "pricing_options": {
            "calculated": round(adjusted_price, 2),
            "charm_pricing": charm_price,
            "round_pricing": rounded_price,
        },
        "margin": {
            "target_pct": round(margin_pct, 1),
            "actual_pct": actual_margin,
            "profit_per_unit": profit_per_unit,
        },
        "competitor_analysis": comp_analysis,
        "demand_adjustment": demand_level,
        "strategy_description": strat["description"],
        "generated_at": datetime.now(timezone.utc).isoformat(),
    }


@mcp.tool()
def summarize_reviews(
    reviews: list[dict],
) -> dict:
    """Summarize product reviews into actionable insights.

    Args:
        reviews: List with keys: rating (1-5), text, verified (bool, optional).
    """
    if not _check_rate_limit():
        return {"error": "Rate limit exceeded. Upgrade to pro tier."}

    if not reviews:
        return {"error": "Provide at least one review."}

    ratings = [r.get("rating", 3) for r in reviews]
    avg_rating = round(sum(ratings) / len(ratings), 1)
    verified_count = sum(1 for r in reviews if r.get("verified", False))

    distribution = {i: ratings.count(i) for i in range(1, 6)}

    # Aspect extraction
    aspects = {
        "quality": {"positive": 0, "negative": 0, "keywords": ["quality", "well-made", "durable", "sturdy", "flimsy", "cheap", "broke"]},
        "value": {"positive": 0, "negative": 0, "keywords": ["value", "worth", "price", "expensive", "bargain", "overpriced", "deal"]},
        "shipping": {"positive": 0, "negative": 0, "keywords": ["shipping", "delivery", "arrived", "fast", "slow", "packaging", "damaged"]},
        "design": {"positive": 0, "negative": 0, "keywords": ["design", "look", "beautiful", "ugly", "color", "size", "fit"]},
        "usability": {"positive": 0, "negative": 0, "keywords": ["easy", "difficult", "intuitive", "confusing", "setup", "instructions", "use"]},
    }

    pos_words = {"great", "excellent", "love", "perfect", "amazing", "best", "good", "fantastic"}
    neg_words = {"terrible", "awful", "worst", "hate", "broken", "disappointed", "poor", "bad"}

    pros = []
    cons = []

    for review in reviews:
        text = review.get("text", "").lower()
        words = set(text.split())
        rating = review.get("rating", 3)

        for aspect, data in aspects.items():
            if any(kw in text for kw in data["keywords"]):
                if rating >= 4 or (words & pos_words):
                    data["positive"] += 1
                elif rating <= 2 or (words & neg_words):
                    data["negative"] += 1

        if rating >= 4:
            for w in words & pos_words:
                ctx = text[max(0, text.index(w) - 30):text.index(w) + 40].strip()
                if ctx and ctx not in pros:
                    pros.append(ctx)
        elif rating <= 2:
            for w in words & neg_words:
                ctx = text[max(0, text.index(w) - 30):text.index(w) + 40].strip()
                if ctx and ctx not in cons:
                    cons.append(ctx)

    aspect_summary = {}
    for aspect, data in aspects.items():
        total = data["positive"] + data["negative"]
        if total > 0:
            aspect_summary[aspect] = {
                "sentiment": "positive" if data["positive"] > data["negative"] else "negative" if data["negative"] > data["positive"] else "mixed",
                "positive_mentions": data["positive"],
                "negative_mentions": data["negative"],
            }

    return {
        "total_reviews": len(reviews),
        "average_rating": avg_rating,
        "verified_reviews": verified_count,
        "rating_distribution": distribution,
        "aspect_analysis": aspect_summary,
        "top_pros": pros[:5],
        "top_cons": cons[:5],
        "recommendation": "Highly rated" if avg_rating >= 4.0 else "Mixed reviews" if avg_rating >= 3.0 else "Needs improvement",
        "generated_at": datetime.now(timezone.utc).isoformat(),
    }


@mcp.tool()
def forecast_inventory(
    product_name: str,
    current_stock: int,
    daily_sales_avg: float,
    lead_time_days: int = 14,
    safety_stock_days: int = 7,
    sales_history: Optional[list[float]] = None,
    seasonal_factor: float = 1.0,
) -> dict:
    """Forecast inventory needs and generate reorder recommendations.

    Args:
        product_name: Product name.
        current_stock: Current units in stock.
        daily_sales_avg: Average daily unit sales.
        lead_time_days: Supplier lead time in days.
        safety_stock_days: Days of safety stock to maintain.
        sales_history: Optional list of recent daily sales for trend analysis.
        seasonal_factor: Seasonal demand multiplier (1.0 = normal, 1.5 = 50% higher).
    """
    if not _check_rate_limit():
        return {"error": "Rate limit exceeded. Upgrade to pro tier."}

    adjusted_daily = daily_sales_avg * seasonal_factor

    # Days of stock remaining
    days_remaining = current_stock / adjusted_daily if adjusted_daily > 0 else 999

    # Reorder point
    safety_stock = math.ceil(adjusted_daily * safety_stock_days)
    reorder_point = math.ceil(adjusted_daily * lead_time_days) + safety_stock

    # Optimal order quantity (simplified EOQ)
    annual_demand = adjusted_daily * 365
    ordering_cost = 50  # Fixed cost per order
    holding_cost_pct = 0.25
    unit_cost = 10  # Placeholder
    eoq = round(math.sqrt((2 * annual_demand * ordering_cost) / (unit_cost * holding_cost_pct)))

    needs_reorder = current_stock <= reorder_point

    # Trend analysis
    trend = "stable"
    if sales_history and len(sales_history) >= 7:
        first_half = sum(sales_history[:len(sales_history)//2]) / (len(sales_history)//2)
        second_half = sum(sales_history[len(sales_history)//2:]) / (len(sales_history) - len(sales_history)//2)
        if second_half > first_half * 1.1:
            trend = "increasing"
        elif second_half < first_half * 0.9:
            trend = "decreasing"

    # 30/60/90 day projections
    projections = {}
    for days in [30, 60, 90]:
        projected_sales = round(adjusted_daily * days)
        projected_stock = current_stock - projected_sales
        projections[f"{days}_days"] = {
            "projected_sales": projected_sales,
            "projected_stock": max(0, projected_stock),
            "stockout_risk": projected_stock < 0,
        }

    return {
        "product": product_name,
        "current_stock": current_stock,
        "daily_sales_adjusted": round(adjusted_daily, 1),
        "days_of_stock_remaining": round(days_remaining, 1),
        "reorder_point": reorder_point,
        "safety_stock": safety_stock,
        "needs_reorder": needs_reorder,
        "recommended_order_qty": eoq,
        "urgency": "critical" if days_remaining < lead_time_days else "soon" if needs_reorder else "no_action",
        "sales_trend": trend,
        "seasonal_factor": seasonal_factor,
        "projections": projections,
        "generated_at": datetime.now(timezone.utc).isoformat(),
    }


@mcp.tool()
def generate_seo_meta(
    product_name: str,
    category: str,
    features: list[str],
    brand: Optional[str] = None,
    target_keywords: Optional[list[str]] = None,
) -> dict:
    """Generate SEO-optimized meta tags for product pages.

    Args:
        product_name: Product name.
        category: Product category.
        features: Key product features.
        brand: Brand name.
        target_keywords: Specific keywords to target.
    """
    if not _check_rate_limit():
        return {"error": "Rate limit exceeded. Upgrade to pro tier."}

    target_keywords = target_keywords or []

    # Title tag (50-60 chars optimal)
    brand_suffix = f" | {brand}" if brand else ""
    title_options = [
        f"{product_name} - {category.title()}{brand_suffix}",
        f"Buy {product_name} | {category.title()} | Free Shipping",
        f"{product_name} | Best {category.title()} | Shop Now",
    ]
    # Pick shortest that's under 60 chars
    title = min(title_options, key=lambda t: abs(len(t) - 55))

    # Meta description (150-160 chars)
    features_text = ", ".join(features[:3])
    desc_options = [
        f"Shop the {product_name}. Features {features_text}. Free shipping on orders over $50. Buy now!",
        f"Discover the {product_name} - {features_text}. Top-rated {category}. Order today with free returns.",
    ]
    description = min(desc_options, key=lambda d: abs(len(d) - 155))
    if len(description) > 160:
        description = description[:157] + "..."

    # Keywords
    auto_keywords = [product_name.lower(), category.lower(), f"buy {product_name.lower()}", f"best {category.lower()}"]
    if brand:
        auto_keywords.append(brand.lower())
    all_keywords = list(dict.fromkeys(target_keywords + auto_keywords))[:10]

    # Schema.org structured data
    schema = {
        "@context": "https://schema.org",
        "@type": "Product",
        "name": product_name,
        "category": category,
        "brand": {"@type": "Brand", "name": brand or ""},
        "description": description,
    }

    # URL slug
    slug = product_name.lower().replace(" ", "-").replace("'", "")
    slug = "".join(c for c in slug if c.isalnum() or c == "-")

    # Open Graph tags
    og_tags = {
        "og:title": title,
        "og:description": description,
        "og:type": "product",
        "og:url": f"https://example.com/products/{slug}",
    }

    return {
        "title_tag": {"text": title, "length": len(title), "optimal": 50 <= len(title) <= 60},
        "meta_description": {"text": description, "length": len(description), "optimal": 150 <= len(description) <= 160},
        "keywords": all_keywords,
        "url_slug": slug,
        "og_tags": og_tags,
        "schema_markup": schema,
        "seo_checklist": {
            "title_length_ok": 50 <= len(title) <= 60,
            "description_length_ok": 150 <= len(description) <= 160,
            "primary_keyword_in_title": any(kw in title.lower() for kw in all_keywords[:2]),
            "primary_keyword_in_description": any(kw in description.lower() for kw in all_keywords[:2]),
            "has_call_to_action": any(cta in description.lower() for cta in ["buy", "shop", "order", "get"]),
        },
        "generated_at": datetime.now(timezone.utc).isoformat(),
    }


if __name__ == "__main__":
    mcp.run()

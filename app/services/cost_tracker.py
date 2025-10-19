import logging
from datetime import datetime
from typing import Any

from pydantic import BaseModel

logger = logging.getLogger(__name__)


class UsageMetrics(BaseModel):
    """Usage metrics for API calls"""

    total_calls: int = 0
    total_input_tokens: int = 0
    total_output_tokens: int = 0
    total_cost: float = 0.0
    last_updated: datetime = datetime.utcnow()


class CostTracker:
    """
    Track and monitor API usage costs
    Helps manage budget and optimize usage
    """

    # Pricing per 1K tokens (as of 2024 - update as needed)
    PRICING = {
        "gpt-4": {"input": 0.03, "output": 0.06},
        "gpt-4-turbo": {"input": 0.01, "output": 0.03},
        "gpt-3.5-turbo": {"input": 0.001, "output": 0.002},
        "text-embedding-3-small": {"input": 0.00002, "output": 0.0},
        "text-embedding-3-large": {"input": 0.00013, "output": 0.0},
    }

    def __init__(self):
        self.daily_metrics: dict[str, UsageMetrics] = {}
        self.session_metrics = UsageMetrics()

    async def track_chat_completion(
        self, input_tokens: int, output_tokens: int, model: str
    ) -> float:
        """Track chat completion usage and cost"""

        cost = self._calculate_cost(input_tokens, output_tokens, model)

        # Update session metrics
        self.session_metrics.total_calls += 1
        self.session_metrics.total_input_tokens += input_tokens
        self.session_metrics.total_output_tokens += output_tokens
        self.session_metrics.total_cost += cost
        self.session_metrics.last_updated = datetime.utcnow()

        # Update daily metrics
        today = datetime.utcnow().date().isoformat()
        if today not in self.daily_metrics:
            self.daily_metrics[today] = UsageMetrics()

        daily = self.daily_metrics[today]
        daily.total_calls += 1
        daily.total_input_tokens += input_tokens
        daily.total_output_tokens += output_tokens
        daily.total_cost += cost
        daily.last_updated = datetime.utcnow()

        # Log if cost is significant
        if cost > 0.10:  # Log costs over 10 cents
            logger.info(
                rf"High cost API call: \ ({model}, {input_tokens+output_tokens} tokens)"
            )

        return cost

    async def track_embedding(
        self, input_tokens: int, model: str = "text-embedding-3-small"
    ) -> float:
        """Track embedding usage and cost"""

        cost = self._calculate_cost(input_tokens, 0, model)

        # Update metrics (similar to chat completion)
        self.session_metrics.total_calls += 1
        self.session_metrics.total_input_tokens += input_tokens
        self.session_metrics.total_cost += cost

        today = datetime.utcnow().date().isoformat()
        if today not in self.daily_metrics:
            self.daily_metrics[today] = UsageMetrics()

        daily = self.daily_metrics[today]
        daily.total_calls += 1
        daily.total_input_tokens += input_tokens
        daily.total_cost += cost

        return cost

    def _calculate_cost(
        self, input_tokens: int, output_tokens: int, model: str
    ) -> float:
        """Calculate cost for API usage"""

        if model not in self.PRICING:
            logger.warning(f"Unknown model for pricing: {model}")
            return 0.0

        pricing = self.PRICING[model]

        input_cost = (input_tokens / 1000) * pricing["input"]
        output_cost = (output_tokens / 1000) * pricing["output"]

        return input_cost + output_cost

    def get_daily_summary(self, date: str | None = None) -> dict[str, Any]:
        """Get daily usage summary"""

        if date is None:
            date = datetime.utcnow().date().isoformat()

        metrics = self.daily_metrics.get(date, UsageMetrics())

        return {
            "date": date,
            "total_calls": metrics.total_calls,
            "total_tokens": metrics.total_input_tokens + metrics.total_output_tokens,
            "input_tokens": metrics.total_input_tokens,
            "output_tokens": metrics.total_output_tokens,
            "total_cost": round(metrics.total_cost, 4),
            "average_cost_per_call": round(
                metrics.total_cost / max(metrics.total_calls, 1), 4
            ),
        }

    def get_session_summary(self) -> dict[str, Any]:
        """Get current session usage summary"""

        return {
            "session_start": self.session_metrics.last_updated.isoformat(),
            "total_calls": self.session_metrics.total_calls,
            "total_tokens": (
                self.session_metrics.total_input_tokens
                + self.session_metrics.total_output_tokens
            ),
            "total_cost": round(self.session_metrics.total_cost, 4),
        }

    def check_budget_alerts(self, daily_budget: float = 5.0) -> dict[str, Any]:
        """Check if usage is approaching budget limits"""

        today = datetime.utcnow().date().isoformat()
        daily_cost = self.daily_metrics.get(today, UsageMetrics()).total_cost

        alerts = []

        if daily_cost > daily_budget * 0.8:
            alerts.append(
                f"Daily budget 80% reached: {daily_cost:.2f} / {daily_budget:.2f}"
            )

        if daily_cost > daily_budget:
            alerts.append(
                f"Daily budget exceeded: {daily_cost:.2f} / {daily_budget:.2f}"
            )

        return {
            "alerts": alerts,
            "daily_cost": daily_cost,
            "daily_budget": daily_budget,
            "budget_remaining": max(0, daily_budget - daily_cost),
        }

"""
Insight interpreter that generates human-readable explanations from calculated metrics.
"""

import logging
from typing import Optional

from models.metrics import Metrics, RiskLevel, TrendIndicator, TrendStrength

logger = logging.getLogger(__name__)


class InsightInterpreter:
    """Generates human-readable interpretations of groundwater metrics."""
    
    def generate_insight(self, metrics: Metrics) -> str:
        """
        Generate a human-readable insight explanation for the given metrics.
        
        Args:
            metrics: Calculated Metrics object
        
        Returns:
            Plain-language explanation string
        """
        if metrics.trend_indicator == TrendIndicator.INSUFFICIENT_DATA:
            return self._insufficient_data_message(metrics)
        
        # Build insight from components
        trend_text = self._trend_explanation(metrics)
        seasonal_text = self._seasonal_explanation(metrics)
        risk_text = self._risk_explanation(metrics)
        
        # Combine into coherent narrative
        insight = f"{trend_text}"
        
        if seasonal_text:
            insight += f" {seasonal_text}"
        
        if risk_text:
            insight += f" {risk_text}"
        
        return insight
    
    def _trend_explanation(self, metrics: Metrics) -> str:
        """Generate explanation for trend indicator."""
        # Use detailed trend_metrics if available, otherwise fall back to basic metrics
        if metrics.trend_metrics:
            trend_metrics = metrics.trend_metrics
            strength_text = f"**{trend_metrics.strength.value.lower()}-strength** " if trend_metrics.strength != TrendStrength.LOW else ""
            magnitude_text = f" by {abs(trend_metrics.magnitude):.2f} meters" if trend_metrics.magnitude else ""
            
            if trend_metrics.status == TrendIndicator.RECHARGING:
                return f"Groundwater levels show a {strength_text}recharging trend{magnitude_text} over the past {trend_metrics.window_days} days."
            elif trend_metrics.status == TrendIndicator.DEPLETING:
                return f"Groundwater levels show a {strength_text}depleting trend{magnitude_text} over the past {trend_metrics.window_days} days."
            elif trend_metrics.status == TrendIndicator.STABLE:
                return f"Groundwater levels have remained relatively stable over the past {trend_metrics.window_days} days."
        
        # Fallback to basic metrics if trend_metrics not available
        if metrics.trend_indicator == TrendIndicator.RECHARGING:
            magnitude_text = f" by {abs(metrics.trend_magnitude):.2f} meters" if metrics.trend_magnitude else ""
            return f"Groundwater levels show a recharging trend{magnitude_text} over the past {metrics.trend_period_days} days."
        
        elif metrics.trend_indicator == TrendIndicator.DEPLETING:
            magnitude_text = f" by {abs(metrics.trend_magnitude):.2f} meters" if metrics.trend_magnitude else ""
            return f"Groundwater levels show a depleting trend{magnitude_text} over the past {metrics.trend_period_days} days."
        
        elif metrics.trend_indicator == TrendIndicator.STABLE:
            return f"Groundwater levels have remained relatively stable over the past {metrics.trend_period_days} days."
        
        else:
            return "Trend analysis could not be completed due to insufficient data."
    
    def _seasonal_explanation(self, metrics: Metrics) -> Optional[str]:
        """Generate explanation for seasonal deviation."""
        if metrics.seasonal_deviation is None:
            return None
        
        deviation = metrics.seasonal_deviation
        baseline = metrics.seasonal_baseline
        
        if abs(deviation) < 0.5:
            return f"Current levels are consistent with seasonal expectations (baseline: {baseline:.2f}m)."
        elif deviation < 0:
            return f"Current levels are {abs(deviation):.2f}m below the seasonal baseline ({baseline:.2f}m), indicating lower than expected recharge."
        else:
            return f"Current levels are {deviation:.2f}m above the seasonal baseline ({baseline:.2f}m), indicating favorable recharge conditions."
    
    def _risk_explanation(self, metrics: Metrics) -> Optional[str]:
        """Generate explanation for risk level."""
        if metrics.risk_level is None or metrics.risk_index is None:
            return None
        
        risk_index = metrics.risk_index
        
        if metrics.risk_level == RiskLevel.LOW:
            return f"Overall groundwater stress risk is LOW (index: {risk_index:.1f}/100), indicating sustainable conditions."
        
        elif metrics.risk_level == RiskLevel.MODERATE:
            return f"Overall groundwater stress risk is MODERATE (index: {risk_index:.1f}/100), suggesting careful monitoring is warranted."
        
        elif metrics.risk_level == RiskLevel.HIGH:
            return f"Overall groundwater stress risk is HIGH (index: {risk_index:.1f}/100), indicating potential sustainability concerns."
        
        elif metrics.risk_level == RiskLevel.CRITICAL:
            return f"Overall groundwater stress risk is CRITICAL (index: {risk_index:.1f}/100), requiring immediate attention and management intervention."
        
        return None
    
    def _insufficient_data_message(self, metrics: Metrics) -> str:
        """Message when data is insufficient for analysis."""
        return (
            f"Insufficient data available for station {metrics.station_id}. "
            f"Only {metrics.data_points_used} data points were found. "
            "Please ensure adequate historical data is available for meaningful analysis."
        )


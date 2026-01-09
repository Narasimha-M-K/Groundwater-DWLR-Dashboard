"""
Metrics model representing calculated analytics for a station.
"""

from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from typing import Optional


class TrendIndicator(str, Enum):
    """Trend classification for groundwater levels."""
    
    RECHARGING = "Recharging"
    STABLE = "Stable"
    DEPLETING = "Depleting"
    INSUFFICIENT_DATA = "Insufficient Data"


class RiskLevel(str, Enum):
    """Risk level classification."""
    
    LOW = "Low Risk"
    MODERATE = "Moderate Risk"
    HIGH = "High Risk"
    CRITICAL = "Critical Risk"


class TrendStrength(str, Enum):
    """Trend strength classification."""
    
    LOW = "Low"
    MEDIUM = "Medium"
    STRONG = "Strong"


@dataclass
class TrendMetrics:
    """
    Detailed trend analysis metrics from linear regression.
    
    Attributes:
        status: Trend classification (Recharging/Stable/Depleting)
        slope: Linear regression slope in m/day
        strength: Trend strength classification (Low/Medium/Strong)
        magnitude: Total change in meters over the analysis window.
                  Calculated as: magnitude = slope * window_days
        window_days: Analysis window size in days
        data_points_used: Number of readings used in calculation
    """
    
    status: TrendIndicator
    slope: float  # m/day
    strength: TrendStrength
    magnitude: float  # meters over window (slope * window_days)
    window_days: int
    data_points_used: int


@dataclass
class Metrics:
    """Calculated metrics for a groundwater monitoring station."""
    
    station_id: str
    calculation_date: datetime
    
    # Trend metrics
    trend_indicator: TrendIndicator
    trend_magnitude: Optional[float] = None  # Change in meters over trend window
    trend_period_days: Optional[int] = None
    trend_metrics: Optional[TrendMetrics] = None  # Detailed trend analysis
    
    # Seasonal metrics
    seasonal_deviation: Optional[float] = None  # Deviation from seasonal baseline
    seasonal_baseline: Optional[float] = None
    
    # Risk index
    risk_index: Optional[float] = None  # 0-100 composite risk score
    risk_level: Optional[RiskLevel] = None
    
    # Metadata
    data_points_used: Optional[int] = None
    calculation_notes: Optional[str] = None
    
    def __str__(self) -> str:
        return f"Metrics({self.station_id}, {self.trend_indicator}, Risk: {self.risk_level})"


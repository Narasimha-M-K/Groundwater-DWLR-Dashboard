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


@dataclass
class Metrics:
    """Calculated metrics for a groundwater monitoring station."""
    
    station_id: str
    calculation_date: datetime
    
    # Trend metrics
    trend_indicator: TrendIndicator
    trend_magnitude: Optional[float] = None  # Change in meters over trend window
    trend_period_days: Optional[int] = None
    
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


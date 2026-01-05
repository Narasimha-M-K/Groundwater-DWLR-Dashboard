"""
Reading model representing a single groundwater level measurement.
"""

from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class Reading:
    """Represents a single groundwater level reading from a DWLR station."""
    
    station_id: str
    timestamp: datetime
    water_level_m: float
    quality_flag: Optional[str] = None
    source: Optional[str] = None
    
    def __str__(self) -> str:
        return f"Reading({self.station_id}, {self.timestamp.date()}, {self.water_level_m}m)"


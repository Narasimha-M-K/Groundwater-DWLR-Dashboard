"""
Station model representing a groundwater monitoring well.
"""

from dataclasses import dataclass
from typing import Optional


@dataclass
class Station:
    """Represents a groundwater monitoring station (DWLR well)."""
    
    station_id: str
    name: str
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    district: Optional[str] = None
    state: Optional[str] = None
    elevation_m: Optional[float] = None
    description: Optional[str] = None
    
    def __str__(self) -> str:
        return f"Station({self.station_id}: {self.name})"


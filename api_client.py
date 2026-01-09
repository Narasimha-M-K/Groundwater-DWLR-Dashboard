"""
API client for NWDP (National Water Data Portal) data ingestion.
Supports both live API access and mock data mode.
"""

import logging
import random
from datetime import datetime, timedelta
from typing import List, Optional

import numpy as np
import requests

from config import config
from models.reading import Reading
from models.station import Station

logger = logging.getLogger(__name__)


class NWDPClient:
    """Client for fetching groundwater data from NWDP API or mock sources."""
    
    def __init__(self, api_base_url: Optional[str] = None, api_key: Optional[str] = None):
        """
        Initialize NWDP client.
        
        Args:
            api_base_url: Base URL for NWDP API (defaults to config)
            api_key: API key for authentication (defaults to config)
        """
        self.api_base_url = api_base_url or config.nwdp_api_base_url
        self.api_key = api_key or config.nwdp_api_key
        self.timeout = config.nwdp_api_timeout
    
    def fetch_stations(self) -> List[Station]:
        """
        Fetch list of available monitoring stations.
        
        Returns:
            List of Station objects
        """
        if config.is_mock_mode():
            return self._fetch_mock_stations()
        else:
            return self._fetch_api_stations()
    
    def fetch_readings(
        self,
        station_id: str,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None
    ) -> List[Reading]:
        """
        Fetch groundwater level readings for a specific station.
        
        Args:
            station_id: Unique identifier for the station
            start_date: Start date for data range (defaults to 1 year ago)
            end_date: End date for data range (defaults to today)
        
        Returns:
            List of Reading objects
        """
        if config.is_mock_mode():
            return self._fetch_mock_readings(station_id, start_date, end_date)
        else:
            return self._fetch_api_readings(station_id, start_date, end_date)
    
    def _fetch_api_stations(self) -> List[Station]:
        """Fetch stations from NWDP API."""
        # TODO: Implement API call
        logger.warning("API mode not yet implemented, returning empty list")
        return []
    
    def _fetch_api_readings(
        self,
        station_id: str,
        start_date: Optional[datetime],
        end_date: Optional[datetime]
    ) -> List[Reading]:
        """Fetch readings from NWDP API."""
        # TODO: Implement API call
        logger.warning("API mode not yet implemented, returning empty list")
        return []
    
    def _fetch_mock_stations(self) -> List[Station]:
        """Generate mock station data for development/testing."""
        return [
            Station(
                station_id="DWLR-001",
                name="Village Well Alpha",
                state="Maharashtra",
                district="Pune"
            ),
            Station(
                station_id="DWLR-002",
                name="Village Well Beta",
                state="Maharashtra",
                district="Nashik"
            ),
            Station(
                station_id="DWLR-003",
                name="Village Well Gamma",
                state="Maharashtra",
                district="Aurangabad"
            )
        ]
    
    def _fetch_mock_readings(
        self,
        station_id: str,
        start_date: Optional[datetime],
        end_date: Optional[datetime]
    ) -> List[Reading]:
        """Generate mock reading data for development/testing."""
        from datetime import timedelta
        
        # Seasonal variation amplitude (configurable constant)
        SEASONAL_AMPLITUDE = 0.05  # ±0.05m seasonal variation
        
        # Stable seed mapping for deterministic generation
        STATION_SEED_MAP = {
            "DWLR-001": 101,
            "DWLR-002": 202,
            "DWLR-003": 303
        }
        
        # Set defaults if dates not provided
        if end_date is None:
            end_date = datetime.now()
        if start_date is None:
            start_date = end_date - timedelta(days=365)
        
        # Always generate exactly 365 days of data
        days = 365
        actual_start = end_date - timedelta(days=days - 1)
        
        # Get deterministic seed for this station (default to 999 if unknown)
        station_seed = STATION_SEED_MAP.get(station_id, 999)
        random.seed(station_seed)
        
        readings = []
        baseline_depth = None
        trend_direction = None
        
        # Assign patterns per station
        if station_id == "DWLR-001":
            # Recharging station: slow improvement (depth decreasing)
            baseline_depth = 12.0  # Start at 12m below ground
            trend_direction = -0.0003  # ~0.1m improvement per year
        elif station_id == "DWLR-002":
            # Depleting station: slow decline (depth increasing)
            baseline_depth = 10.0  # Start at 10m below ground
            trend_direction = 0.0004  # ~0.15m decline per year
        else:  # DWLR-003 or any other
            # Stable station: minimal change
            baseline_depth = 11.5  # Start at 11.5m below ground
            trend_direction = 0.00005  # Very slight variation
        
        # Generate daily readings for exactly 365 days
        current_date = actual_start
        day_count = 0
        
        while day_count < days:
            # Calculate trend component (linear over time)
            days_elapsed = day_count
            trend_component = trend_direction * days_elapsed
            
            # Add seasonal variation (sinusoidal, ~6 month cycle)
            seasonal_phase = (days_elapsed / 365.0) * 2 * np.pi
            seasonal_component = SEASONAL_AMPLITUDE * np.sin(seasonal_phase)
            
            # Add small daily random variation (±0.05m)
            daily_variation = random.uniform(-0.05, 0.05)
            
            # Calculate final water level depth
            water_level = baseline_depth + trend_component + seasonal_component + daily_variation
            
            # Ensure realistic bounds (5-20m below ground)
            water_level = max(5.0, min(20.0, water_level))
            
            reading = Reading(
                station_id=station_id,
                timestamp=current_date,
                water_level_m=round(water_level, 3),
                quality_flag="GOOD",
                source="MOCK"
            )
            readings.append(reading)
            
            current_date += timedelta(days=1)
            day_count += 1
        
        return readings


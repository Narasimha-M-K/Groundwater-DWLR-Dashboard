"""
API client for NWDP (National Water Data Portal) data ingestion.
Supports both live API access and mock data mode.
"""

import logging
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
        """
        Generate deterministic mock reading data for development/testing.
        
        Generates a fixed historical window (2019-01-01 to 2024-01-01, 5 years)
        with one reading per calendar day. Uses index-based regime mapping
        to assign numerical drift parameters per station.
        """
        # Fixed historical window: 5 years of data
        FIXED_START_DATE = datetime(2019, 1, 1)
        FIXED_END_DATE = datetime(2024, 1, 1)
        TOTAL_DAYS = (FIXED_END_DATE - FIXED_START_DATE).days  # 1825 days
        
        # Get station index for deterministic regime mapping
        stations = self._fetch_mock_stations()
        station_ids = [s.station_id for s in stations]
        try:
            station_index = station_ids.index(station_id)
        except ValueError:
            # Unknown station: use hash-based index for determinism
            station_index = hash(station_id) % 3
        
        # Numerical regime parameters (no semantic labels)
        # Regime 0: Positive drift (depth increasing over time)
        # Regime 1: Negative drift (depth decreasing over time)
        # Regime 2: Near-zero drift (stable)
        REGIME_INDEX = station_index % 3
        
        REGIME_PARAMS = [
            {"baseline_depth": 10.0, "drift_per_day": 0.0015, "seasonal_amplitude": 0.03},  # Regime 0
            {"baseline_depth": 12.0, "drift_per_day": -0.0015, "seasonal_amplitude": 0.03},  # Regime 1
            {"baseline_depth": 11.5, "drift_per_day": 0.0001, "seasonal_amplitude": 0.0}   # Regime 2
        ]
        
        regime = REGIME_PARAMS[REGIME_INDEX]
        baseline_depth = regime["baseline_depth"]
        drift_per_day = regime["drift_per_day"]
        seasonal_amplitude = regime["seasonal_amplitude"]
        
        # Deterministic seed: global seed + station index
        GLOBAL_SEED = 42
        station_seed = GLOBAL_SEED + station_index * 1000
        rng = np.random.RandomState(station_seed)
        
        # Generate one reading per calendar day
        readings = []
        current_date = FIXED_START_DATE
        
        for day_index in range(TOTAL_DAYS):
            # Days elapsed from start
            days_elapsed = day_index
            
            # Trend component: linear drift over time
            trend_component = drift_per_day * days_elapsed
            
            # Seasonal variation (sinusoidal, annual cycle)
            seasonal_phase = (days_elapsed / 365.25) * 2 * np.pi
            seasonal_component = seasonal_amplitude * np.sin(seasonal_phase)
            
            # Bounded pseudo-noise (order of magnitude smaller than cumulative drift)
            # Over 5 years, max cumulative drift is |0.0015 * 1825| = 2.74m
            # Noise magnitude: ±0.005m (5mm) per day, much smaller than drift
            noise = rng.uniform(-0.005, 0.005)
            
            # Calculate final water level depth
            water_level = baseline_depth + trend_component + seasonal_component + noise
            
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
        
        return readings


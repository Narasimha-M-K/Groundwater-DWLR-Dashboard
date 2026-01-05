"""
Streamlit dashboard application for Groundwater Recharge Insight Dashboard.
"""

import logging
from datetime import datetime, timedelta

import streamlit as st

from api_client import NWDPClient
from config import config
from data_store import DataStore
from insights import InsightInterpreter
from models.station import Station
from processing import ProcessingEngine

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Page configuration
st.set_page_config(
    page_title="Groundwater Recharge Insight Dashboard",
    page_icon="💧",
    layout="wide",
    initial_sidebar_state="expanded"
)


def initialize_components():
    """Initialize application components."""
    if "data_store" not in st.session_state:
        st.session_state.data_store = DataStore()
    
    if "api_client" not in st.session_state:
        st.session_state.api_client = NWDPClient()
    
    if "processing_engine" not in st.session_state:
        st.session_state.processing_engine = ProcessingEngine()
    
    if "insight_interpreter" not in st.session_state:
        st.session_state.insight_interpreter = InsightInterpreter()


def main():
    """Main application entry point."""
    st.title("💧 Groundwater Recharge Insight Dashboard")
    st.markdown("**DWLR – NWDP Data Analysis**")
    
    # Initialize components
    initialize_components()
    
    # Sidebar
    with st.sidebar:
        st.header("Configuration")
        st.info(f"Data Mode: **{config.data_mode.upper()}**")
        
        if st.button("🔄 Refresh Data"):
            st.session_state.refresh_triggered = True
    
    # Main content
    data_store = st.session_state.data_store
    
    # Get list of stations
    stations = data_store.get_all_stations()
    
    if not stations:
        st.warning("No stations found. Please fetch data from NWDP API or load mock data.")
        if st.button("Load Sample Stations"):
            with st.spinner("Loading sample stations and generating mock data..."):
                try:
                    api_client = st.session_state.api_client
                    data_store = st.session_state.data_store
                    
                    # Fetch mock stations
                    mock_stations = api_client.fetch_stations()
                    
                    if not mock_stations:
                        st.error("Failed to generate mock stations.")
                    else:
                        # Save each station (will update if already exists)
                        for station in mock_stations:
                            data_store.save_station(station)
                        
                        st.success(f"Loaded {len(mock_stations)} stations.")
                        
                        # Generate and save readings for each station (only if not already present)
                        progress_bar = st.progress(0)
                        total_stations = len(mock_stations)
                        
                        for idx, station in enumerate(mock_stations):
                            # Check if readings already exist for this station
                            existing_readings = data_store.get_readings(station.station_id)
                            
                            if existing_readings:
                                st.info(f"⏭️  Skipping {station.name} - {len(existing_readings)} readings already exist")
                            else:
                                # Generate readings (exactly 365 days)
                                end_date = datetime.now()
                                start_date = end_date - timedelta(days=365)
                                
                                readings = api_client.fetch_readings(
                                    station.station_id,
                                    start_date,
                                    end_date
                                )
                                
                                if readings:
                                    data_store.save_readings(readings)
                                    st.info(f"✅ Generated {len(readings)} readings for {station.name}")
                                else:
                                    st.warning(f"⚠️  No readings generated for {station.name}")
                            
                            progress_bar.progress((idx + 1) / total_stations)
                        
                        st.success("✅ Sample data loading complete! Refresh the page to see stations.")
                        st.rerun()  # Refresh the app to show new stations
                        
                except Exception as e:
                    st.error(f"Error loading sample data: {str(e)}")
                    logger.exception("Error in load sample stations")
    else:
        # Station selection
        station_options = {f"{s.name} ({s.station_id})": s.station_id for s in stations}
        selected_station_name = st.selectbox(
            "Select Station",
            options=list(station_options.keys()),
            index=0
        )
        selected_station_id = station_options[selected_station_name]
        
        # Display station details
        station = data_store.get_station(selected_station_id)
        if station:
            display_station_summary(station, data_store)
            display_station_details(station, data_store)


def display_station_summary(station: Station, data_store: DataStore):
    """Display summary card for selected station."""
    st.header(f"📊 {station.name}")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Station ID", station.station_id)
    
    with col2:
        if station.district:
            st.metric("District", station.district)
    
    with col3:
        if station.state:
            st.metric("State", station.state)
    
    with col4:
        # Get latest metrics
        metrics = data_store.get_latest_metrics(station.station_id)
        if metrics and metrics.risk_level:
            risk_color = {
                "Low Risk": "🟢",
                "Moderate Risk": "🟡",
                "High Risk": "🟠",
                "Critical Risk": "🔴"
            }.get(metrics.risk_level.value, "⚪")
            st.metric("Risk Level", f"{risk_color} {metrics.risk_level.value}")


def display_station_details(station: Station, data_store: DataStore):
    """Display detailed analysis for selected station."""
    st.subheader("Detailed Analysis")
    
    # Get readings
    end_date = datetime.now()
    start_date = end_date - timedelta(days=365)
    readings = data_store.get_readings(station.station_id, start_date, end_date)
    
    if not readings:
        st.warning(f"No readings found for station {station.station_id}")
        return
    
    # Calculate metrics
    processing_engine = st.session_state.processing_engine
    metrics = processing_engine.calculate_metrics(readings)
    
    # Display metrics
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Trend Analysis")
        st.metric("Trend", metrics.trend_indicator.value)
        if metrics.trend_magnitude:
            st.metric("Change", f"{metrics.trend_magnitude:.2f} m")
    
    with col2:
        st.subheader("Risk Assessment")
        if metrics.risk_index is not None:
            st.metric("Risk Index", f"{metrics.risk_index:.1f}/100")
        if metrics.risk_level:
            st.metric("Risk Level", metrics.risk_level.value)
    
    # Generate and display insight
    insight_interpreter = st.session_state.insight_interpreter
    insight = insight_interpreter.generate_insight(metrics)
    
    st.subheader("📝 Interpretation")
    st.info(insight)
    
    # Display chart
    st.subheader("Groundwater Level Chart")
    # TODO: Implement chart visualization
    st.info("Chart visualization not yet implemented.")


if __name__ == "__main__":
    main()


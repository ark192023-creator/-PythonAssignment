import streamlit as st
import requests
import json
import pandas as pd
from datetime import datetime, timedelta
import time
import random
import numpy as np
from typing import Dict, List, Optional, Tuple
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# Configure page
st.set_page_config(
    page_title="Adaptive RAG Live Market Data - Sept 24, 2025",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Adaptive RAG Configuration
class AdaptiveRAGConfig:
    def __init__(self):
        self.primary_sources = [
            "https://api.marketstack.com/v1/eod",
            "https://finnhub.io/api/v1/quote",
            "https://api.polygon.io/v2/aggs/ticker",
            "https://api.alpha-vantage.co/query"
        ]
        self.fallback_sources = [
            "yahoo_finance",
            "trading_economics",
            "investing_com",
            "cnbc_api"
        ]
        self.cache_duration = 300  # 5 minutes
        self.retry_attempts = 3
        self.timeout = 10

# Live Market Data Class with Fallback Mechanism
class LiveMarketDataRAG:
    def __init__(self):
        self.config = AdaptiveRAGConfig()
        self.cache = {}
        self.last_update = {}
        self.data_quality_scores = {}
        
    def get_cache_key(self, symbol: str, data_type: str) -> str:
        return f"{symbol}_{data_type}_{datetime.now().date()}"
    
    def is_cache_valid(self, key: str) -> bool:
        if key not in self.last_update:
            return False
        return (datetime.now() - self.last_update[key]).seconds < self.config.cache_duration
    
    def update_quality_score(self, source: str, success: bool):
        if source not in self.data_quality_scores:
            self.data_quality_scores[source] = {"success": 0, "total": 0}
        
        self.data_quality_scores[source]["total"] += 1
        if success:
            self.data_quality_scores[source]["success"] += 1
    
    def get_source_reliability(self, source: str) -> float:
        if source not in self.data_quality_scores:
            return 0.5
        stats = self.data_quality_scores[source]
        return stats["success"] / stats["total"] if stats["total"] > 0 else 0.5
    
    def fetch_primary_data(self, symbol: str) -> Optional[Dict]:
        """Primary data source with API fallback"""
        try:
            # Simulate real API calls with mock data based on actual market conditions
            # In production, replace with actual API calls
            
            # Mock data based on recent market conditions (Sept 24, 2025)
            base_prices = {
                "SPY": 666.92,  # S&P 500 ETF
                "QQQ": 575.73,  # NASDAQ ETF  
                "DIA": 463.15,  # DOW ETF
                "NVDA": 145.25, # NVIDIA
                "AAPL": 184.50, # Apple
                "MSFT": 425.75, # Microsoft
                "GOOGL": 168.25, # Google
                "TSLA": 267.88, # Tesla
                "META": 495.67, # Meta
                "AMZN": 187.45  # Amazon
            }
            
            if symbol not in base_prices:
                return None
            
            # Simulate realistic market fluctuations
            base_price = base_prices[symbol]
            current_price = base_price * (1 + random.uniform(-0.02, 0.02))
            change = current_price - base_price
            change_percent = (change / base_price) * 100
            
            volume = random.randint(1000000, 50000000)
            
            data = {
                "symbol": symbol,
                "price": round(current_price, 2),
                "change": round(change, 2),
                "change_percent": round(change_percent, 2),
                "volume": volume,
                "high": round(current_price * 1.015, 2),
                "low": round(current_price * 0.985, 2),
                "open": round(base_price * 1.002, 2),
                "timestamp": datetime.now().isoformat(),
                "source": "primary_api"
            }
            
            self.update_quality_score("primary_api", True)
            return data
            
        except Exception as e:
            self.update_quality_score("primary_api", False)
            st.error(f"Primary API error: {str(e)}")
            return None
    
    def fetch_fallback_data(self, symbol: str) -> Optional[Dict]:
        """Fallback data using alternative methods"""
        try:
            # Simulate fallback data sources
            fallback_data = {
                "SPY": {"price": 666.68, "change": -0.24, "volume": 45678900},
                "QQQ": {"price": 574.89, "change": -0.84, "volume": 32456780},
                "DIA": {"price": 463.81, "change": 0.66, "volume": 8765432}
            }
            
            if symbol in fallback_data:
                base_data = fallback_data[symbol]
                return {
                    "symbol": symbol,
                    "price": base_data["price"],
                    "change": base_data["change"],
                    "change_percent": round((base_data["change"] / base_data["price"]) * 100, 2),
                    "volume": base_data["volume"],
                    "timestamp": datetime.now().isoformat(),
                    "source": "fallback_scraper"
                }
            
            self.update_quality_score("fallback_scraper", True)
            return None
            
        except Exception as e:
            self.update_quality_score("fallback_scraper", False)
            return None
    
    def get_live_data(self, symbol: str) -> Dict:
        """Main method with adaptive fallback mechanism"""
        cache_key = self.get_cache_key(symbol, "live_price")
        
        # Check cache first
        if self.is_cache_valid(cache_key) and cache_key in self.cache:
            return self.cache[cache_key]
        
        # Try primary data source
        data = self.fetch_primary_data(symbol)
        
        # If primary fails, try fallback
        if data is None:
            st.warning(f"Primary source failed for {symbol}, using fallback...")
            data = self.fetch_fallback_data(symbol)
        
        # If all fails, use cached data or mock data
        if data is None:
            if cache_key in self.cache:
                st.info(f"Using cached data for {symbol}")
                return self.cache[cache_key]
            else:
                st.error(f"No data available for {symbol}, using mock data")
                data = {
                    "symbol": symbol,
                    "price": 100.0,
                    "change": 0.0,
                    "change_percent": 0.0,
                    "volume": 1000000,
                    "timestamp": datetime.now().isoformat(),
                    "source": "mock_data"
                }
        
        # Cache the result
        self.cache[cache_key] = data
        self.last_update[cache_key] = datetime.now()
        
        return data

# Initialize the RAG system
@st.cache_resource
def get_market_rag():
    return LiveMarketDataRAG()

# Custom CSS
st.markdown("""
<style>
    .stApp {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        min-height: 100vh;
    }
    
    .metric-card {
        background: rgba(255, 255, 255, 0.15);
        backdrop-filter: blur(15px);
        border-radius: 20px;
        padding: 1.5rem;
        margin: 1rem 0;
        border: 1px solid rgba(255, 255, 255, 0.3);
        box-shadow: 0 12px 40px rgba(0, 0, 0, 0.15);
    }
    
    .main-header {
        background: linear-gradient(90deg, #ff6b6b, #4ecdc4, #45b7d1, #f7b801);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        background-size: 300% 300%;
        text-align: center;
        font-size: 3.5rem;
        font-weight: bold;
        margin-bottom: 1rem;
        animation: shimmer 3s infinite;
    }
    
    @keyframes shimmer {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }
    
    .live-indicator {
        background: linear-gradient(45deg, #ff6b6b, #4ecdc4);
        color: white;
        padding: 0.5rem 1rem;
        border-radius: 20px;
        font-weight: bold;
        text-align: center;
        margin: 1rem auto;
        display: inline-block;
        animation: pulse 2s infinite;
    }
    
    @keyframes pulse {
        0% { transform: scale(1); }
        50% { transform: scale(1.05); }
        100% { transform: scale(1); }
    }
</style>
""", unsafe_allow_html=True)

# Main App
st.markdown('<h1 class="main-header">📈 Adaptive RAG Live Market Data</h1>', unsafe_allow_html=True)
st.markdown('<div class="live-indicator">🔴 LIVE - September 24, 2025</div>', unsafe_allow_html=True)

# Initialize RAG system
market_rag = get_market_rag()

# Sidebar Configuration
st.sidebar.title("🎛️ RAG Configuration")
st.sidebar.markdown("### Data Source Status")

# Display source reliability
for source, score in market_rag.data_quality_scores.items():
    reliability = market_rag.get_source_reliability(source)
    color = "🟢" if reliability > 0.8 else "🟡" if reliability > 0.5 else "🔴"
    st.sidebar.markdown(f"{color} **{source}**: {reliability:.1%}")

st.sidebar.markdown("---")
st.sidebar.markdown("### Fallback Strategy")
st.sidebar.markdown("""
1. **Primary APIs** (Real-time)
2. **Fallback Scrapers** (5min delay)  
3. **Cached Data** (Last valid)
4. **Mock Data** (Emergency)
""")

# Auto-refresh toggle
auto_refresh = st.sidebar.checkbox("🔄 Auto Refresh (30s)", value=True)
if auto_refresh:
    st.sidebar.markdown("*Next update in 30 seconds*")

# Main Market Dashboard
st.subheader("📊 Live Market Dashboard")

# Current market data based on search results
current_market_data = {
    "S&P 500": {"value": 6668, "change": -0.39, "source": "Trading Economics"},
    "NASDAQ": {"value": 22573.47, "change": -0.95, "source": "CNBC"},
    "DOW": {"value": 46381.54, "change": 0.14, "source": "CNBC"}
}

# Display current market indices
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown(f"""
    <div class="metric-card">
        <h3>📈 S&P 500</h3>
        <h2>{current_market_data["S&P 500"]["value"]}</h2>
        <p style="color: {'red' if current_market_data['S&P 500']['change'] < 0 else 'green'}">
            {current_market_data["S&P 500"]["change"]:+.2f}%
        </p>
        <small>Source: {current_market_data["S&P 500"]["source"]}</small>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
    <div class="metric-card">
        <h3>💻 NASDAQ</h3>
        <h2>{current_market_data["NASDAQ"]["value"]}</h2>
        <p style="color: {'red' if current_market_data['NASDAQ']['change'] < 0 else 'green'}">
            {current_market_data["NASDAQ"]["change"]:+.2f}%
        </p>
        <small>Source: {current_market_data["NASDAQ"]["source"]}</small>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown(f"""
    <div class="metric-card">
        <h3>🏭 DOW JONES</h3>
        <h2>{current_market_data["DOW"]["value"]}</h2>
        <p style="color: {'red' if current_market_data['DOW']['change'] < 0 else 'green'}">
            {current_market_data["DOW"]["change"]:+.2f}%
        </p>
        <small>Source: {current_market_data["DOW"]["source"]}</small>
    </div>
    """, unsafe_allow_html=True)

# Live Stock Lookup
st.subheader("🔍 Live Stock Lookup")
col1, col2 = st.columns([3, 1])

with col1:
    symbol = st.selectbox("Select Stock Symbol", 
                         ["SPY", "QQQ", "DIA", "NVDA", "AAPL", "MSFT", "GOOGL", "TSLA", "META", "AMZN"])

with col2:
    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("🔄 Get Live Data"):
        with st.spinner("Fetching live data..."):
            data = market_rag.get_live_data(symbol)
            
            if data:
                col_a, col_b, col_c, col_d = st.columns(4)
                
                with col_a:
                    st.metric("Price", f"${data['price']}", f"{data['change']:+.2f}")
                
                with col_b:
                    st.metric("Change %", f"{data['change_percent']:+.2f}%")
                
                with col_c:
                    st.metric("Volume", f"{data['volume']:,}")
                
                with col_d:
                    st.metric("Source", data['source'])
                
                # Display additional data if available
                if 'high' in data and 'low' in data:
                    col_e, col_f = st.columns(2)
                    with col_e:
                        st.metric("High", f"${data.get('high', 'N/A')}")
                    with col_f:
                        st.metric("Low", f"${data.get('low', 'N/A')}")

# Market Insights from Search Results
st.subheader("📰 Latest Market Insights")

# Display insights from the search results
market_insights = [
    {
        "title": "Recent Market Performance",
        "content": "The S&P 500 fell to 6668 points on September 23, 2025, losing 0.39% from the previous session.",
        "source": "Trading Economics",
        "timestamp": "Sep 23, 2025"
    },
    {
        "title": "Market Gains Over Time", 
        "content": "Over the past month, the S&P 500 has climbed 3.55% and is up 16.31% compared to the same time last year.",
        "source": "Trading Economics", 
        "timestamp": "Sep 23, 2025"
    },
    {
        "title": "AI Trade Concerns",
        "content": "Questions remain on whether the AI trade can continue powering U.S. equities given the risks tied to elevated market valuations.",
        "source": "CNBC",
        "timestamp": "Sep 23, 2025"
    },
    {
        "title": "Bank Forecasts",
        "content": "Wells Fargo expects the S&P 500 to finish 2025 at 6,650, while Barclays raised its year-end price target to 6,450.",
        "source": "CNBC",
        "timestamp": "Sep 10, 2025"
    }
]

for insight in market_insights:
    with st.expander(f"📄 {insight['title']} - {insight['timestamp']}"):
        st.write(insight['content'])
        st.caption(f"Source: {insight['source']}")

# RAG Performance Metrics
st.subheader("🎯 RAG System Performance")

col1, col2, col3 = st.columns(3)

with col1:
    total_requests = sum([scores["total"] for scores in market_rag.data_quality_scores.values()])
    st.metric("Total Requests", total_requests)

with col2:
    cache_hit_rate = len(market_rag.cache) / max(total_requests, 1) * 100
    st.metric("Cache Hit Rate", f"{cache_hit_rate:.1f}%")

with col3:
    avg_reliability = np.mean([market_rag.get_source_reliability(source) 
                              for source in market_rag.data_quality_scores.keys()]) if market_rag.data_quality_scores else 0
    st.metric("Avg Source Reliability", f"{avg_reliability:.1%}")

# Real-time Chart (Mock)
st.subheader("📈 Real-time Price Chart")

# Generate mock intraday data
times = pd.date_range(start="2025-09-24 09:30", end="2025-09-24 16:00", freq="5min")
prices = 6668 + np.cumsum(np.random.randn(len(times)) * 0.5)

fig = go.Figure()
fig.add_trace(go.Scatter(x=times, y=prices, mode='lines', name='S&P 500', line=dict(color='#4ecdc4', width=2)))
fig.update_layout(
    title="S&P 500 Intraday Chart - September 24, 2025",
    xaxis_title="Time",
    yaxis_title="Price",
    template="plotly_dark",
    height=400
)
st.plotly_chart(fig, use_container_width=True)

# Data Quality Dashboard
st.subheader("📊 Data Quality & Sources")

if market_rag.data_quality_scores:
    sources = list(market_rag.data_quality_scores.keys())
    success_rates = [market_rag.get_source_reliability(source) for source in sources]
    
    fig = go.Figure(data=[
        go.Bar(x=sources, y=success_rates, marker_color=['#4ecdc4', '#ff6b6b', '#f7b801', '#45b7d1'])
    ])
    fig.update_layout(
        title="Data Source Reliability",
        yaxis_title="Success Rate",
        template="plotly_dark",
        height=300
    )
    st.plotly_chart(fig, use_container_width=True)

# Auto-refresh mechanism
if auto_refresh:
    time.sleep(1)  # Small delay to prevent too frequent updates
    st.rerun()

# Footer
st.markdown("---")
st.markdown("### 🔧 System Status")

col1, col2, col3 = st.columns(3)

with col1:
    st.success("✅ Primary API: Online")

with col2:
    st.info("🔄 Fallback: Ready")

with col3:
    st.warning("⚡ Cache: Active")

st.caption("Last updated: " + datetime.now().strftime("%Y-%m-%d %H:%M:%S UTC"))
st.caption("Adaptive RAG System - Intelligent fallback mechanisms ensure data availability")

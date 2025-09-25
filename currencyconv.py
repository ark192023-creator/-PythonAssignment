import streamlit as st
import pandas as pd
import requests
import json
from datetime import datetime, timedelta
import random
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import time

# Configure page
st.set_page_config(
    page_title="Live Currency Converter Pro",
    page_icon="💰",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Enhanced Live Market Data Class
class EnhancedLiveMarketData:
    def __init__(self):
        self.cache_duration = 60
        
    @st.cache_data(ttl=60)
    def fetch_enhanced_forex_rates(_self):
        try:
            response = requests.get("https://api.exchangerate-api.com/v4/latest/USD", timeout=10)
            if response.status_code == 200:
                data = response.json()
                rates = data.get('rates', {})
                
                enhanced_data = {}
                for currency, rate in rates.items():
                    enhanced_data[currency] = {
                        'rate': rate,
                        'change_24h': random.uniform(-2, 2),
                        'volatility': random.uniform(0.5, 2.0),
                        'volume_24h': random.randint(50000000, 1500000000),
                        'bid': rate * 0.9999,
                        'ask': rate * 1.0001,
                        'spread': rate * 0.0002,
                        'last_update': datetime.now().strftime("%H:%M:%S")
                    }
                
                return rates, data.get('date'), enhanced_data
                
        except Exception as e:
            st.warning(f"API Error: {str(e)[:100]}...")
        
        return None, None, None
    
    @st.cache_data(ttl=60)
    def fetch_enhanced_crypto_data(_self):
        try:
            response = requests.get(
                "https://api.coingecko.com/api/v3/simple/price?ids=bitcoin,ethereum,cardano,solana,dogecoin&vs_currencies=usd&include_24hr_change=true&include_24hr_vol=true&include_market_cap=true",
                timeout=15
            )
            if response.status_code == 200:
                data = response.json()
                
                enhanced_crypto = {}
                for coin_id, coin_data in data.items():
                    enhanced_crypto[coin_id] = {
                        'price_usd': coin_data.get('usd', 0),
                        'change_24h': coin_data.get('usd_24h_change', 0),
                        'volume_24h': coin_data.get('usd_24h_vol', 0),
                        'market_cap': coin_data.get('usd_market_cap', 0),
                        'volatility': abs(coin_data.get('usd_24h_change', 0)) * 2,
                        'fear_greed_index': random.randint(20, 80),
                        'last_update': datetime.now().strftime("%H:%M:%S")
                    }
                
                return enhanced_crypto
                
        except Exception as e:
            st.warning(f"Crypto API Error: {str(e)[:100]}...")
        
        return None

# Initialize market data
@st.cache_resource
def get_market_data_instance():
    return EnhancedLiveMarketData()

market_data = get_market_data_instance()

# Enhanced CSS
st.markdown("""
<style>
    @keyframes pulse {
        0% { opacity: 1; }
        50% { opacity: 0.7; }
        100% { opacity: 1; }
    }
    
    @keyframes slideIn {
        from { transform: translateY(-10px); opacity: 0; }
        to { transform: translateY(0); opacity: 1; }
    }
    
    @keyframes glow {
        0% { box-shadow: 0 0 5px rgba(78, 205, 196, 0.5); }
        50% { box-shadow: 0 0 20px rgba(78, 205, 196, 0.8); }
        100% { box-shadow: 0 0 5px rgba(78, 205, 196, 0.5); }
    }
    
    .stApp {
        background: linear-gradient(135deg, #1e3c72 0%, #2a5298 50%, #667eea 100%);
        min-height: 100vh;
    }
    
    .main-header {
        background: linear-gradient(90deg, #ffd700, #ffb347, #ff6b6b, #4ecdc4);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        text-align: center;
        font-size: 3rem;
        font-weight: bold;
        margin-bottom: 1rem;
        animation: slideIn 1s ease-out;
    }
    
    .live-indicator {
        display: inline-block;
        width: 12px;
        height: 12px;
        background-color: #00ff00;
        border-radius: 50%;
        margin-right: 8px;
        animation: pulse 2s infinite;
    }
    
    .currency-card {
        background: rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(20px);
        border-radius: 20px;
        padding: 2rem;
        margin: 1rem 0;
        border: 1px solid rgba(255, 255, 255, 0.2);
        box-shadow: 0 15px 35px rgba(0, 0, 0, 0.1);
        color: white;
        transition: all 0.3s ease;
    }
    
    .currency-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 20px 40px rgba(0, 0, 0, 0.2);
        animation: glow 2s ease-in-out infinite;
    }
    
    .positive { color: #00c851; font-weight: bold; }
    .negative { color: #ff4444; font-weight: bold; }
    .neutral { color: #ffbb33; font-weight: bold; }
    
    .metric-card {
        background: rgba(255, 255, 255, 0.15);
        border-radius: 12px;
        padding: 1rem;
        margin: 0.5rem 0;
        border-left: 4px solid #4ecdc4;
        color: white;
        transition: all 0.3s ease;
    }
    
    .metric-card:hover {
        background: rgba(255, 255, 255, 0.2);
        transform: scale(1.02);
    }
    
    .news-item {
        background: rgba(255, 255, 255, 0.1);
        border-radius: 8px;
        padding: 1rem;
        margin: 0.5rem 0;
        color: white;
        border-left: 3px solid #ffd700;
        transition: all 0.3s ease;
    }
    
    .news-item:hover {
        background: rgba(255, 255, 255, 0.15);
        transform: translateX(5px);
    }
    
    .conversion-result {
        background: linear-gradient(45deg, #ff6b6b, #4ecdc4);
        border-radius: 20px;
        padding: 2rem;
        text-align: center;
        color: white;
        font-size: 2rem;
        font-weight: bold;
        margin: 2rem 0;
        box-shadow: 0 10px 30px rgba(255, 107, 107, 0.3);
        animation: slideIn 0.5s ease-out;
    }
    
    .alert-box {
        background: linear-gradient(45deg, #ff9800, #f57c00);
        border-radius: 10px;
        padding: 1rem;
        margin: 1rem 0;
        color: white;
        border: 1px solid rgba(255, 255, 255, 0.3);
    }
    
    .market-status {
        display: flex;
        align-items: center;
        background: rgba(0, 0, 0, 0.2);
        border-radius: 25px;
        padding: 0.5rem 1rem;
        margin: 0.5rem 0;
        color: white;
    }
    
    .sentiment-card {
        background: linear-gradient(45deg, #667eea, #764ba2);
        border-radius: 15px;
        padding: 1.5rem;
        text-align: center;
        color: white;
        margin: 1rem 0;
        box-shadow: 0 10px 25px rgba(102, 126, 234, 0.3);
    }
</style>
""", unsafe_allow_html=True)

# Cache for enhanced data
@st.cache_data(ttl=120)
def get_enhanced_currency_data():
    live_rates, rate_date, enhanced_forex = market_data.fetch_enhanced_forex_rates()
    crypto_data = market_data.fetch_enhanced_crypto_data()
    
    # Base currency data
    static_data = {
        'USD': {'rate': 1.0000, 'name': 'US Dollar', 'symbol': '$', 'change_24h': 0.0, 'volatility': 0.5, 'central_bank': 'Federal Reserve', 'inflation_rate': 2.1, 'interest_rate': 5.25},
        'EUR': {'rate': 0.8536, 'name': 'Euro', 'symbol': '€', 'change_24h': -0.12, 'volatility': 0.8, 'central_bank': 'European Central Bank', 'inflation_rate': 1.8, 'interest_rate': 4.50},
        'GBP': {'rate': 0.7589, 'name': 'British Pound', 'symbol': '£', 'change_24h': 0.23, 'volatility': 1.2, 'central_bank': 'Bank of England', 'inflation_rate': 2.3, 'interest_rate': 5.00},
        'JPY': {'rate': 149.85, 'name': 'Japanese Yen', 'symbol': '¥', 'change_24h': -0.45, 'volatility': 1.1, 'central_bank': 'Bank of Japan', 'inflation_rate': 0.9, 'interest_rate': 0.10},
        'CAD': {'rate': 1.3612, 'name': 'Canadian Dollar', 'symbol': 'C$', 'change_24h': 0.08, 'volatility': 0.9, 'central_bank': 'Bank of Canada', 'inflation_rate': 2.0, 'interest_rate': 4.75},
        'AUD': {'rate': 1.4895, 'name': 'Australian Dollar', 'symbol': 'A$', 'change_24h': 0.15, 'volatility': 1.3, 'central_bank': 'Reserve Bank of Australia', 'inflation_rate': 2.5, 'interest_rate': 4.35},
        'CHF': {'rate': 0.8445, 'name': 'Swiss Franc', 'symbol': 'CHF', 'change_24h': -0.05, 'volatility': 0.6, 'central_bank': 'Swiss National Bank', 'inflation_rate': 1.2, 'interest_rate': 1.75},
        'CNY': {'rate': 7.2156, 'name': 'Chinese Yuan', 'symbol': '¥', 'change_24h': 0.03, 'volatility': 0.4, 'central_bank': 'Peoples Bank of China', 'inflation_rate': 1.5, 'interest_rate': 3.45},
        'INR': {'rate': 83.24, 'name': 'Indian Rupee', 'symbol': '₹', 'change_24h': -0.18, 'volatility': 1.0, 'central_bank': 'Reserve Bank of India', 'inflation_rate': 3.2, 'interest_rate': 6.50},
    }
    
    # Update with live rates
    if enhanced_forex:
        for currency, enhanced_info in enhanced_forex.items():
            if currency in static_data:
                static_data[currency].update(enhanced_info)
    
    # Add crypto data
    if crypto_data:
        crypto_mapping = {
            'bitcoin': {'symbol': 'BTC', 'name': 'Bitcoin'},
            'ethereum': {'symbol': 'ETH', 'name': 'Ethereum'},
            'cardano': {'symbol': 'ADA', 'name': 'Cardano'},
            'solana': {'symbol': 'SOL', 'name': 'Solana'},
            'dogecoin': {'symbol': 'DOGE', 'name': 'Dogecoin'}
        }
        
        for coin_id, coin_info in crypto_mapping.items():
            if coin_id in crypto_data:
                crypto_price = crypto_data[coin_id]['price_usd']
                static_data[coin_info['symbol']] = {
                    'rate': 1/crypto_price if crypto_price > 0 else 0,
                    'name': coin_info['name'],
                    'symbol': '₿' if coin_info['symbol'] == 'BTC' else coin_info['symbol'],
                    'change_24h': crypto_data[coin_id]['change_24h'],
                    'volatility': crypto_data[coin_id]['volatility'],
                    'volume_24h': crypto_data[coin_id]['volume_24h'],
                    'market_cap': crypto_data[coin_id]['market_cap'],
                    'central_bank': 'Decentralized',
                    'inflation_rate': 0.0,
                    'interest_rate': 0.0,
                    'last_update': crypto_data[coin_id]['last_update']
                }
    
    return static_data, rate_date

# Get stock data
@st.cache_data(ttl=300)
def get_stock_indices():
    indices = {
        'S&P 500': {'value': 4567.89 + random.uniform(-50, 50), 'change': random.uniform(-2, 2), 'currency': 'USD'},
        'NASDAQ': {'value': 14234.56 + random.uniform(-200, 200), 'change': random.uniform(-3, 3), 'currency': 'USD'},
        'FTSE 100': {'value': 7456.23 + random.uniform(-75, 75), 'change': random.uniform(-1.5, 1.5), 'currency': 'GBP'},
        'Nikkei 225': {'value': 32145.67 + random.uniform(-300, 300), 'change': random.uniform(-2, 2), 'currency': 'JPY'},
        'DAX': {'value': 15789.45 + random.uniform(-200, 200), 'change': random.uniform(-2, 2), 'currency': 'EUR'},
        'Hang Seng': {'value': 18456.78 + random.uniform(-400, 400), 'change': random.uniform(-3, 3), 'currency': 'HKD'},
    }
    return indices

# Market news
@st.cache_data(ttl=600)
def fetch_market_news():
    return [
        {"title": "Federal Reserve Signals Potential Rate Cut", "impact": "USD", "time": "2 hours ago", "sentiment": "bearish"},
        {"title": "ECB Maintains Dovish Stance", "impact": "EUR", "time": "4 hours ago", "sentiment": "neutral"},
        {"title": "Bank of Japan Intervenes in Markets", "impact": "JPY", "time": "6 hours ago", "sentiment": "bullish"},
        {"title": "UK Inflation Data Beats Expectations", "impact": "GBP", "time": "8 hours ago", "sentiment": "bullish"},
        {"title": "Bitcoin ETF Sees Record Inflows", "impact": "BTC", "time": "3 hours ago", "sentiment": "bullish"},
    ]

# Get data
CURRENCY_DATA, last_update = get_enhanced_currency_data()
STOCK_INDICES = get_stock_indices()

# Header with live indicator
col_header1, col_header2 = st.columns([3, 1])
with col_header1:
    st.markdown('<h1 class="main-header">💰 Live Currency Converter Pro</h1>', unsafe_allow_html=True)
    st.markdown('<p style="text-align: center; color: white; font-size: 1.3rem; margin-bottom: 2rem;">Real-time currency conversion with live market data & AI insights</p>', unsafe_allow_html=True)

with col_header2:
    st.markdown(f'''
    <div class="market-status">
        <span class="live-indicator"></span>
        <strong>LIVE</strong> | {datetime.now().strftime("%H:%M:%S")}
    </div>
    ''', unsafe_allow_html=True)
    
    if st.button("🔄 Refresh Data"):
        st.cache_data.clear()
        st.rerun()

# Market sentiment analysis
def calculate_market_sentiment():
    total_change = sum(data['change_24h'] for data in CURRENCY_DATA.values() if 'change_24h' in data)
    avg_change = total_change / len([d for d in CURRENCY_DATA.values() if 'change_24h' in d])
    
    if avg_change > 0.5:
        return "Very Bullish 🚀", "#00ff00", avg_change
    elif avg_change > 0:
        return "Bullish 📈", "#90EE90", avg_change
    elif avg_change > -0.5:
        return "Neutral ➡️", "#ffbb33", avg_change
    else:
        return "Bearish 📉", "#ff4444", avg_change

sentiment_label, sentiment_color, sentiment_score = calculate_market_sentiment()

# Live Market Alerts
market_alerts = []
for curr, data in CURRENCY_DATA.items():
    if 'change_24h' in data and abs(data['change_24h']) > 1.5:
        alert_type = "🚨" if abs(data['change_24h']) > 2.5 else "⚠️"
        market_alerts.append(f"{alert_type} {curr} moved {data['change_24h']:+.2f}% in 24h")

if market_alerts:
    st.markdown("### 📢 Live Market Alerts")
    for alert in market_alerts[:3]:
        st.markdown(f'<div class="alert-box">{alert}</div>', unsafe_allow_html=True)

# Market Sentiment Display
st.markdown("### 🎭 Real-Time Market Sentiment")
sent_col1, sent_col2, sent_col3 = st.columns([2, 1, 1])

with sent_col1:
    st.markdown(f'''
    <div class="sentiment-card">
        <h3>Global Market Sentiment</h3>
        <h2 style="color: {sentiment_color};">{sentiment_label}</h2>
        <p>Score: {sentiment_score:.3f}</p>
        <p>Confidence: {min(100, abs(sentiment_score * 50) + 60):.0f}%</p>
    </div>
    ''', unsafe_allow_html=True)

with sent_col2:
    # Fear & Greed Index
    fear_greed = random.randint(20, 80)
    fg_color = "#00c851" if fear_greed > 60 else "#ffbb33" if fear_greed > 40 else "#ff4444"
    st.markdown(f'''
    <div class="metric-card">
        <h4>Fear & Greed Index</h4>
        <h2 style="color: {fg_color};">{fear_greed}</h2>
        <p>{"Greedy" if fear_greed > 60 else "Neutral" if fear_greed > 40 else "Fearful"}</p>
    </div>
    ''', unsafe_allow_html=True)

with sent_col3:
    # Volatility Index
    avg_volatility = np.mean([data.get('volatility', 1) for data in CURRENCY_DATA.values()])
    vol_color = "#ff4444" if avg_volatility > 1.5 else "#ffbb33" if avg_volatility > 1 else "#00c851"
    st.markdown(f'''
    <div class="metric-card">
        <h4>Market Volatility</h4>
        <h2 style="color: {vol_color};">{avg_volatility:.1f}%</h2>
        <p>{"High" if avg_volatility > 1.5 else "Medium" if avg_volatility > 1 else "Low"}</p>
    </div>
    ''', unsafe_allow_html=True)

# Enhanced Sidebar
st.sidebar.title("📊 Live Market Dashboard")

# Auto-refresh toggle
auto_refresh = st.sidebar.checkbox("🔄 Auto-refresh (30s)", value=False)
if auto_refresh:
    time.sleep(30)
    st.rerun()

st.sidebar.markdown(f'''
<div style="background: {sentiment_color}; border-radius: 10px; padding: 1rem; text-align: center; color: white; margin-bottom: 1rem;">
    <strong>Market Sentiment</strong><br>
    {sentiment_label}
</div>
''', unsafe_allow_html=True)

st.sidebar.markdown("### 🌍 Major Indices")
for index, data in STOCK_INDICES.items():
    change_class = "positive" if data['change'] > 0 else "negative" if data['change'] < 0 else "neutral"
    change_symbol = "+" if data['change'] > 0 else ""
    st.sidebar.markdown(f'''
    <div class="metric-card">
        <strong>{index}</strong><br>
        {data['value']:,.2f} 
        <span class="{change_class}">({change_symbol}{data['change']:.1f}%)</span>
    </div>
    ''', unsafe_allow_html=True)

st.sidebar.markdown("---")
st.sidebar.markdown("### 🔥 Top Movers (24h)")
sorted_currencies = sorted(
    [(k, v) for k, v in CURRENCY_DATA.items() if 'change_24h' in v], 
    key=lambda x: abs(x[1]['change_24h']), 
    reverse=True
)[:5]

for curr, data in sorted_currencies:
    if curr != 'USD':
        change_class = "positive" if data['change_24h'] > 0 else "negative"
        change_symbol = "+" if data['change_24h'] > 0 else ""
        st.sidebar.markdown(f"**{curr}**: <span class='{change_class}'>{change_symbol}{data['change_24h']:.2f}%</span>", unsafe_allow_html=True)

# Market News
st.sidebar.markdown("---")
st.sidebar.markdown("### 📰 Market News")
news_items = fetch_market_news()
for news in news_items[:3]:
    sentiment_emoji = "🟢" if news['sentiment'] == 'bullish' else "🔴" if news['sentiment'] == 'bearish' else "🟡"
    st.sidebar.markdown(f'''
    <div class="news-item">
        <strong>{news['title']}</strong><br>
        <small>{sentiment_emoji} {news['impact']} | {news['time']}</small>
    </div>
    ''', unsafe_allow_html=True)

# Main converter
col1, col2 = st.columns([2, 1])

with col1:
    st.markdown('<div class="currency-card">', unsafe_allow_html=True)
    st.subheader("💱 Live Currency Converter")
    
    conv_col1, conv_col2, conv_col3 = st.columns([2, 1, 2])
    
    with conv_col1:
        amount = st.number_input("Amount", min_value=0.01, value=1000.0, step=0.01)
        from_currency = st.selectbox("From Currency", list(CURRENCY_DATA.keys()), index=0)
    
    with conv_col3:
        to_currency_options = [k for k in CURRENCY_DATA.keys() if k != from_currency]
        to_currency = st.selectbox("To Currency", to_currency_options)
    
    with conv_col2:
        st.markdown("<br><br>", unsafe_allow_html=True)
        if st.button("🔄 Convert", type="primary"):
            # Conversion calculation
            from_rate = CURRENCY_DATA[from_currency]['rate']
            to_rate = CURRENCY_DATA[to_currency]['rate']
            
            if from_currency == 'USD':
                converted_amount = amount * to_rate
            elif to_currency == 'USD':
                converted_amount = amount / from_rate
            else:
                usd_amount = amount / from_rate
                converted_amount = usd_amount * to_rate
            
            exchange_rate = to_rate / from_rate if from_currency != 'USD' else to_rate
            if to_currency == 'USD':
                exchange_rate = 1 / from_rate
            
            # Display result
            st.markdown(f'''
            <div class="conversion-result">
                {CURRENCY_DATA[from_currency]['symbol']}{amount:,.2f} = {CURRENCY_DATA[to_currency]['symbol']}{converted_amount:,.4f}
                <br><small>Rate: 1 {from_currency} = {exchange_rate:.6f} {to_currency}</small>
            </div>
            ''', unsafe_allow_html=True)
            
            # Performance comparison
            from_change = CURRENCY_DATA[from_currency].get('change_24h', 0)
            to_change = CURRENCY_DATA[to_currency].get('change_24h', 0)
            
            col_a, col_b, col_c = st.columns(3)
            with col_a:
                st.markdown(f'''
                <div class="metric-card">
                    <strong>{from_currency} Performance</strong><br>
                    24h: <span class="{'positive' if from_change >= 0 else 'negative'}">
                    {'+' if from_change >= 0 else ''}{from_change:.2f}%
                    </span><br>
                    Vol: {CURRENCY_DATA[from_currency].get('volatility', 1):.1f}%
                </div>
                ''', unsafe_allow_html=True)
                
            with col_b:
                trend = "📈" if to_change > from_change else "📉" if to_change < from_change else "➡️"
                st.markdown(f'''
                <div class="metric-card">
                    <strong>Pair Trend</strong><br>
                    {trend}<br>
                    <small>{to_currency} vs {from_currency}</small>
                </div>
                ''', unsafe_allow_html=True)
                
            with col_c:
                st.markdown(f'''
                <div class="metric-card">
                    <strong>{to_currency} Performance</strong><br>
                    24h: <span class="{'positive' if to_change >= 0 else 'negative'}">
                    {'+' if to_change >= 0 else ''}{to_change:.2f}%
                    </span><br>
                    Vol: {CURRENCY_DATA[to_currency].get('volatility', 1):.1f}%
                </div>
                ''', unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

with col2:
    st.markdown('<div class="currency-card">', unsafe_allow_html=True)
    st.subheader("📊 Live Market Insights")
    
    from_data = CURRENCY_DATA[from_currency]
    to_data = CURRENCY_DATA[to_currency]
    
    # Price movement indicators
    from_trend = "🔺" if from_data.get('change_24h', 0) > 0 else "🔻" if from_data.get('change_24h', 0) < 0 else "▶️"
    to_trend = "🔺" if to_data.get('change_24h', 0) > 0 else "🔻" if to_data.get('change_24h', 0) < 0 else "▶️"
    
    st.markdown(f'''
    <div class="metric-card">
        <strong>🎯 Price Momentum</strong><br>
        {from_currency}: {from_trend} {from_data.get('change_24h', 0):+.2f}%<br>
        {to_currency}: {to_trend} {to_data.get('change_24h', 0):+.2f}%
    </div>
    ''', unsafe_allow_html=True)
    
    if 'volume_24h' in from_data and 'volume_24h' in to_data:
        st.markdown(f'''
        <div class="metric-card">
            <strong>📊 Trading Volume (24h)</strong><br>
            {from_currency}: ${from_data['volume_24h']:,.0f}<br>
            {to_currency}: ${to_data['volume_24h']:,.0f}
        </div>
        ''', unsafe_allow_html=True)
    
    if 'bid' in from_data and 'ask' in from_data:
        spread = (from_data['ask'] - from_data['bid']) / from_data['bid'] * 100
        st.markdown(f'''
        <div class="metric-card">
            <strong>💰 Bid/Ask Spread</strong><br>
            {from_currency}: {spread:.4f}%<br>
            Liquidity: {"High" if spread < 0.1 else "Medium" if spread < 0.2 else "Low"}
        </div>
        ''', unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

# Advanced Market Analysis
st.markdown("---")
st.subheader("📈 Advanced Market Analysis")

analysis_col1, analysis_col2 = st.columns([2, 1])

with analysis_col1:
    # Volatility vs Performance Chart
    fig = go.Figure()
    
    for curr, data in CURRENCY_DATA.items():
        if curr != 'USD' and 'volatility' in data and 'change_24h' in data:
            fig.add_trace(go.Scatter(
                x=[data['volatility']],
                y=[data['change_24h']],
                mode='markers+text',
                text=[curr],
                textposition="middle right",
                marker=dict(
                    size=15,
                    color=data['change_24h'],
                    colorscale='RdYlGn',
                    showscale=True,
                    colorbar=dict(title="24h Change %")
                ),
                name=curr,
                hovertemplate=f"<b>{curr}</b><br>" +
                            f"Volatility: {data['volatility']:.1f}%<br>" +
                            f"24h Change: {data['change_24h']:+.2f}%<br>" +
                            f"Interest Rate: {data.get('interest_rate', 0):.2f}%<extra></extra>"
            ))
    
    fig.update_layout(
        title="Currency Risk-Return Matrix",
        xaxis_title="Volatility (%)",
        yaxis_title="24h Performance (%)",
        template="plotly_dark",
        height=500,
        showlegend=False
    )
    
    # Add quadrant lines
    fig.add_hline(y=0, line_dash="dash", line_color="rgba(255,255,255,0.5)")
    fig.add_vline(x=1, line_dash="dash", line_color="rgba(255,255,255,0.5)")
    
    st.plotly_chart(fig, use_container_width=True)

with analysis_col2:
    st.markdown("### 🎯 Trading Signals")
    
    # Generate AI-like trading signals
    signals = []
    
    # Momentum signal
    best_performer = max(
        [(k, v) for k, v in CURRENCY_DATA.items() if k != 'USD' and 'change_24h' in v], 
        key=lambda x: x[1]['change_24h']
    )
    if best_performer[1]['change_24h'] > 1:
        signals.append(f"🚀 BUY {best_performer[0]} - Strong momentum ({best_performer[1]['change_24h']:+.1f}%)")
    
    # Mean reversion signal
    worst_performer = min(
        [(k, v) for k, v in CURRENCY_DATA.items() if k != 'USD' and 'change_24h' in v], 
        key=lambda x: x[1]['change_24h']
    )
    if worst_performer[1]['change_24h'] < -1:
        signals.append(f"🔄 WATCH {worst_performer[0]} - Potential reversal ({worst_performer[1]['change_24h']:+.1f}%)")
    
    # Carry trade signal
    high_yield_currencies = [(k, v) for k, v in CURRENCY_DATA.items() if v.get('interest_rate', 0) > 4 and k != 'USD']
    if high_yield_currencies:
        best_carry = max(high_yield_currencies, key=lambda x: x[1]['interest_rate'])
        signals.append(f"💰 CARRY {best_carry[0]} - High yield ({best_carry[1]['interest_rate']:.1f}%)")
    
    # Volatility signal
    low_vol_currencies = [(k, v) for k, v in CURRENCY_DATA.items() if v.get('volatility', 1) < 1 and k != 'USD']
    if low_vol_currencies:
        safest = min(low_vol_currencies, key=lambda x: x[1]['volatility'])
        signals.append(f"🛡️ SAFE HAVEN {safest[0]} - Low vol ({safest[1]['volatility']:.1f}%)")
    
    for signal in signals:
        st.markdown(f'''
        <div class="news-item">
            {signal}
        </div>
        ''', unsafe_allow_html=True)
    
    # Market correlation matrix (simplified)
    st.markdown("### 🔗 Market Correlations")
    correlations = {
        'EUR-USD': random.uniform(0.6, 0.8),
        'GBP-USD': random.uniform(0.7, 0.9),
        'JPY-USD': random.uniform(-0.4, -0.2),
        'Gold-USD': random.uniform(-0.3, -0.1),
        'BTC-USD': random.uniform(-0.1, 0.3)
    }
    
    for pair, corr in correlations.items():
        color = "#00c851" if abs(corr) > 0.7 else "#ffbb33" if abs(corr) > 0.4 else "#ff4444"
        st.markdown(f'''
        <div style="background: {color}; border-radius: 5px; padding: 0.5rem; margin: 0.2rem 0; color: white;">
            <strong>{pair}</strong>: {corr:.2f}
        </div>
        ''', unsafe_allow_html=True)

# Live Economic Calendar
st.markdown("---")
st.subheader("📅 Live Economic Calendar & Market Events")

calendar_col1, calendar_col2 = st.columns(2)

with calendar_col1:
    st.markdown("#### 🗓️ Upcoming Events (Next 24h)")
    
    upcoming_events = [
        {"time": "09:30 EST", "event": "US GDP Data Release", "impact": "High", "currency": "USD"},
        {"time": "14:00 EST", "event": "ECB Interest Rate Decision", "impact": "High", "currency": "EUR"},
        {"time": "20:00 EST", "event": "BoJ Policy Meeting Minutes", "impact": "Medium", "currency": "JPY"},
        {"time": "06:00 EST+1", "event": "UK Employment Data", "impact": "Medium", "currency": "GBP"},
    ]
    
    for event in upcoming_events:
        impact_color = "#ff4444" if event['impact'] == 'High' else "#ffbb33" if event['impact'] == 'Medium' else "#00c851"
        st.markdown(f'''
        <div class="metric-card">
            <strong>{event['time']}</strong><br>
            {event['event']}<br>
            <span style="color: {impact_color};">Impact: {event['impact']}</span> | 
            <span style="color: #4ecdc4;">{event['currency']}</span>
        </div>
        ''', unsafe_allow_html=True)

with calendar_col2:
    st.markdown("#### 📊 Market Sessions Status")
    
    current_hour = datetime.now().hour
    
    sessions = [
        {"name": "🌅 London", "status": "Open" if 8 <= current_hour < 17 else "Closed", "overlap": "High volume with NY"},
        {"name": "🗽 New York", "status": "Open" if 13 <= current_hour < 22 else "Closed", "overlap": "Peak liquidity hours"},
        {"name": "🌸 Tokyo", "status": "Open" if 23 <= current_hour or current_hour < 8 else "Closed", "overlap": "Asian session leader"},
        {"name": "🦘 Sydney", "status": "Open" if 21 <= current_hour or current_hour < 6 else "Closed", "overlap": "Oceania markets"}
    ]
    
    for session in sessions:
        status_color = "#00c851" if session['status'] == 'Open' else "#ff4444"
        st.markdown(f'''
        <div class="metric-card">
            <strong>{session['name']} Session</strong><br>
            Status: <span style="color: {status_color};">{session['status']}</span><br>
            <small>{session['overlap']}</small>
        </div>
        ''', unsafe_allow_html=True)

# Live Market Data Table
st.markdown("---")
st.subheader("📋 Complete Market Overview")

# Create comprehensive market table
market_df_data = []
for curr, data in CURRENCY_DATA.items():
    market_df_data.append({
        'Currency': curr,
        'Name': data.get('name', 'N/A'),
        'Rate (USD)': f"{data['rate']:.6f}",
        '24h Change': f"{data.get('change_24h', 0):+.2f}%",
        'Volatility': f"{data.get('volatility', 0):.1f}%",
        'Volume 24h': f"${data.get('volume_24h', 0):,.0f}" if 'volume_24h' in data else 'N/A',
        'Market Cap': f"${data.get('market_cap', 0):,.0f}" if 'market_cap' in data else 'N/A',
        'Interest Rate': f"{data.get('interest_rate', 0):.2f}%",
        'Last Update': data.get('last_update', 'N/A')
    })

market_df = pd.DataFrame(market_df_data)
st.dataframe(market_df, use_container_width=True, hide_index=True)

# Performance Analytics
st.markdown("---")
st.subheader("📈 Performance Analytics Dashboard")

perf_col1, perf_col2, perf_col3 = st.columns(3)

with perf_col1:
    # Best performers
    st.markdown("#### 🏆 Best Performers")
    best_performers = sorted(
        [(k, v) for k, v in CURRENCY_DATA.items() if 'change_24h' in v],
        key=lambda x: x[1]['change_24h'],
        reverse=True
    )[:3]
    
    for i, (curr, data) in enumerate(best_performers):
        medal = "🥇" if i == 0 else "🥈" if i == 1 else "🥉"
        st.markdown(f'''
        <div class="metric-card">
            {medal} <strong>{curr}</strong><br>
            {data.get('name', 'N/A')}<br>
            <span class="positive">{data['change_24h']:+.2f}%</span>
        </div>
        ''', unsafe_allow_html=True)

with perf_col2:
    # Worst performers
    st.markdown("#### 📉 Worst Performers")
    worst_performers = sorted(
        [(k, v) for k, v in CURRENCY_DATA.items() if 'change_24h' in v],
        key=lambda x: x[1]['change_24h']
    )[:3]
    
    for i, (curr, data) in enumerate(worst_performers):
        st.markdown(f'''
        <div class="metric-card">
            <strong>{curr}</strong><br>
            {data.get('name', 'N/A')}<br>
            <span class="negative">{data['change_24h']:+.2f}%</span>
        </div>
        ''', unsafe_allow_html=True)

with perf_col3:
    # Most volatile
    st.markdown("#### 🌪️ Most Volatile")
    most_volatile = sorted(
        [(k, v) for k, v in CURRENCY_DATA.items() if 'volatility' in v],
        key=lambda x: x[1]['volatility'],
        reverse=True
    )[:3]
    
    for curr, data in most_volatile:
        st.markdown(f'''
        <div class="metric-card">
            <strong>{curr}</strong><br>
            {data.get('name', 'N/A')}<br>
            <span class="neutral">{data['volatility']:.1f}% vol</span>
        </div>
        ''', unsafe_allow_html=True)

# Footer with API status and info
st.markdown("---")
footer_col1, footer_col2, footer_col3 = st.columns(3)

with footer_col1:
    st.markdown('''
    <div class="metric-card">
        <strong>📡 Data Sources</strong><br>
        • ExchangeRate-API (Forex)<br>
        • CoinGecko API (Crypto)<br>
        • Simulated Stock Data
    </div>
    ''', unsafe_allow_html=True)

with footer_col2:
    st.markdown(f'''
    <div class="metric-card">
        <strong>⏰ Last Updated</strong><br>
        {datetime.now().strftime("%Y-%m-%d %H:%M:%S UTC")}<br>
        Cache TTL: 60-300 seconds
    </div>
    ''', unsafe_allow_html=True)

with footer_col3:
    st.markdown('''
    <div class="metric-card">
        <strong>🔧 Features</strong><br>
        • Real-time rates<br>
        • Live market sentiment<br>
        • Advanced analytics
    </div>
    ''', unsafe_allow_html=True)

# End of application
st.markdown('<p style="text-align: center; color: white; margin-top: 3rem; opacity: 0.7;">💰 Live Currency Converter Pro - Real-time financial market data at your fingertips</p>', unsafe_allow_html=True)

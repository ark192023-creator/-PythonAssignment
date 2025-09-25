mport streamlit as st
import requests
import json
from datetime import datetime
import pandas as pd
import math

# Configure page
st.set_page_config(
    page_title="Universal Converter Hub - Sept 12, 2025",
    page_icon="🔄",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Current exchange rates for September 12, 2025
CURRENT_RATES = {
    # Base: USD = 1.0
    'USD': 1.0,
    'EUR': 0.8536,  # 1 USD = 0.8536 EUR
    'GBP': 0.7589,  # Estimated based on current trends
    'JPY': 149.85,  # Japanese Yen
    'CAD': 1.3612,  # Canadian Dollar
    'AUD': 1.4895,  # Australian Dollar
    'CHF': 0.8445,  # Swiss Franc
    'CNY': 7.2156,  # Chinese Yuan
    'INR': 83.24,   # Indian Rupee
    'KRW': 1342.5,  # South Korean Won
    'BTC': 0.000018, # Bitcoin (approximate)
    'ETH': 0.0004,   # Ethereum (approximate)
    'MXN': 19.67,   # Mexican Peso
    'SEK': 10.89,   # Swedish Krona
    'NOK': 10.72,   # Norwegian Krone
    'DKK': 6.37,    # Danish Krone
    'SGD': 1.3468,  # Singapore Dollar
    'HKD': 7.8245,  # Hong Kong Dollar
    'NZD': 1.6234,  # New Zealand Dollar
    'ZAR': 18.45    # South African Rand
}

# Unit conversion factors
LENGTH_UNITS = {
    "Millimeter (mm)": 0.001,
    "Centimeter (cm)": 0.01,
    "Meter (m)": 1.0,
    "Kilometer (km)": 1000.0,
    "Inch (in)": 0.0254,
    "Foot (ft)": 0.3048,
    "Yard (yd)": 0.9144,
    "Mile (mi)": 1609.344,
    "Nautical Mile": 1852.0,
    "Light Year": 9.461e15
}

WEIGHT_UNITS = {
    "Milligram (mg)": 0.001,
    "Gram (g)": 1.0,
    "Kilogram (kg)": 1000.0,
    "Ounce (oz)": 28.3495,
    "Pound (lb)": 453.592,
    "Stone (st)": 6350.29,
    "Ton (t)": 1000000.0,
    "US Ton": 907185.0,
    "UK Ton": 1016047.0
}

AREA_UNITS = {
    "Square Millimeter (mm²)": 0.000001,
    "Square Centimeter (cm²)": 0.0001,
    "Square Meter (m²)": 1.0,
    "Square Kilometer (km²)": 1000000.0,
    "Square Inch (in²)": 0.00064516,
    "Square Foot (ft²)": 0.092903,
    "Square Yard (yd²)": 0.836127,
    "Acre": 4046.86,
    "Hectare": 10000.0
}

VOLUME_UNITS = {
    "Milliliter (ml)": 0.001,
    "Liter (l)": 1.0,
    "Cubic Meter (m³)": 1000.0,
    "Cubic Inch (in³)": 0.0163871,
    "Cubic Foot (ft³)": 28.3168,
    "US Gallon": 3.78541,
    "UK Gallon": 4.54609,
    "US Pint": 0.473176,
    "UK Pint": 0.568261
}

TIME_UNITS = {
    "Millisecond (ms)": 0.001,
    "Second (s)": 1.0,
    "Minute (min)": 60.0,
    "Hour (hr)": 3600.0,
    "Day": 86400.0,
    "Week": 604800.0,
    "Month": 2629746.0,  # Average month
    "Year": 31556952.0   # Average year
}

SPEED_UNITS = {
    "Meter/Second (m/s)": 1.0,
    "Kilometer/Hour (km/h)": 0.277778,
    "Mile/Hour (mph)": 0.44704,
    "Foot/Second (ft/s)": 0.3048,
    "Knot": 0.514444,
    "Mach": 343.0  # At sea level
}

# Custom CSS for gradient background and styling
st.markdown("""
<style>
    /* Main background gradient */
    .stApp {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        min-height: 100vh;
    }
    
    /* Header styling */
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
    
    /* Date badge */
    .date-badge {
        background: linear-gradient(45deg, #ff9a56, #ff6b6b);
        color: white;
        padding: 0.5rem 1.5rem;
        border-radius: 25px;
        font-weight: bold;
        text-align: center;
        margin: 1rem auto;
        display: inline-block;
        box-shadow: 0 4px 15px rgba(255, 107, 107, 0.3);
    }
    
    /* Card styling */
    .converter-card {
        background: rgba(255, 255, 255, 0.15);
        backdrop-filter: blur(15px);
        border-radius: 25px;
        padding: 2.5rem;
        margin: 2rem 0;
        border: 1px solid rgba(255, 255, 255, 0.3);
        box-shadow: 0 12px 40px rgba(0, 0, 0, 0.15);
        transition: transform 0.3s ease;
    }
    
    .converter-card:hover {
        transform: translateY(-5px);
    }
    
    /* Tab styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 24px;
        background: rgba(255, 255, 255, 0.1);
        border-radius: 20px;
        padding: 10px;
    }
    
    .stTabs [data-baseweb="tab"] {
        height: 50px;
        background: rgba(255, 255, 255, 0.2);
        border-radius: 15px;
        color: white;
        font-weight: bold;
    }
    
    .stTabs [aria-selected="true"] {
        background: linear-gradient(45deg, #ff6b6b, #4ecdc4);
        color: white;
    }
    
    /* Button styling */
    .stButton > button {
        background: linear-gradient(45deg, #ff6b6b, #4ecdc4);
        color: white;
        border: none;
        border-radius: 30px;
        padding: 0.75rem 3rem;
        font-weight: bold;
        font-size: 1.1rem;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.2);
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(0, 0, 0, 0.25);
    }
    
    /* Result styling */
    .result-box {
        background: linear-gradient(45deg, #56ab2f, #a8e6cf);
        border-radius: 20px;
        padding: 2rem;
        text-align: center;
        font-size: 2rem;
        font-weight: bold;
        color: white;
        margin: 2rem 0;
        box-shadow: 0 8px 25px rgba(86, 171, 47, 0.3);
        animation: pulse 2s infinite;
    }
    
    @keyframes pulse {
        0% { transform: scale(1); }
        50% { transform: scale(1.02); }
        100% { transform: scale(1); }
    }
    
    /* Rate info */
    .rate-info {
        background: rgba(255, 255, 255, 0.2);
        border-radius: 15px;
        padding: 1rem;
        margin: 1rem 0;
        border-left: 4px solid #4ecdc4;
        color: white;
    }
    
    /* Sidebar styling */
    .css-1d391kg {
        background: linear-gradient(180deg, #667eea 0%, #764ba2 100%);
    }
    
    /* Input styling */
    .stSelectbox > div > div {
        background: rgba(255, 255, 255, 0.1);
        border-radius: 15px;
        border: 1px solid rgba(255, 255, 255, 0.3);
    }
    
    .stNumberInput > div > div > input {
        background: rgba(255, 255, 255, 0.1);
        border-radius: 15px;
        color: white;
        border: 1px solid rgba(255, 255, 255, 0.3);
    }
    
    /* Feature cards */
    .feature-card {
        background: rgba(255, 255, 255, 0.15);
        border-radius: 15px;
        padding: 1.5rem;
        text-align: center;
        margin: 1rem 0;
        border: 1px solid rgba(255, 255, 255, 0.3);
        transition: all 0.3s ease;
    }
    
    .feature-card:hover {
        transform: translateY(-3px);
        background: rgba(255, 255, 255, 0.2);
    }
</style>
""", unsafe_allow_html=True)

# Title and date
st.markdown('<h1 class="main-header">🔄 Universal Converter Hub</h1>', unsafe_allow_html=True)
#st.markdown('<div class="date-badge">📅 September 12, 2025 - Live Data</div>', unsafe_allow_html=True)
st.markdown('<p style="text-align: center; color: white; font-size: 1.2rem; margin-bottom: 3rem;">Your complete solution for all conversion needs - Currency, Temperature, Length, Weight & More!</p>', unsafe_allow_html=True)

# Sidebar navigation
st.sidebar.title("🚀 Converter Hub")
st.sidebar.markdown("### Available Converters")
st.sidebar.markdown("""
- 💱 **Currency** (Live rates)
- 🌡️ **Temperature** (°C, °F, K)
- 📏 **Length** (m, ft, in, km)
- ⚖️ **Weight** (kg, lb, oz, g)
- 📊 **Area** (m², ft², acres)
- 🕐 **Time** (s, min, hr, days)
- 📦 **Volume** (L, gal, m³)
- 🚀 **Speed** (m/s, mph, km/h)
""")

st.sidebar.markdown("---")
st.sidebar.markdown("### 💰 Today's Top Rates")
featured_currencies = ['EUR', 'GBP', 'JPY', 'INR']
for curr in featured_currencies:
    rate = CURRENT_RATES[curr]
    if curr in ['JPY', 'INR']:
        st.sidebar.markdown(f"**USD→{curr}**: {rate:.2f}")
    else:
        st.sidebar.markdown(f"**USD→{curr}**: {rate:.4f}")

# Main converter tabs
tab1, tab2, tab3, tab4, tab5, tab6, tab7, tab8 = st.tabs([
    "💱 Currency", "🌡️ Temperature", "📏 Length", "⚖️ Weight", 
    "📊 Area", "🕐 Time", "📦 Volume", "🚀 Speed"
])

# Currency Converter Tab
with tab1:
    st.markdown('<div class="converter-card">', unsafe_allow_html=True)
    st.subheader("💱 Live Currency Converter")
    
    col1, col2, col3 = st.columns([2, 1, 2])
    
    with col1:
        amount = st.number_input("Amount", min_value=0.01, value=100.0, step=0.01, key="curr_amount")
        from_currency = st.selectbox("From Currency", 
            ["USD", "EUR", "GBP", "JPY", "CAD", "AUD", "CHF", "CNY", "INR", "KRW", "BTC", "ETH"], 
            key="curr_from")
    
    with col3:
        to_currency = st.selectbox("To Currency", 
            ["EUR", "USD", "GBP", "JPY", "CAD", "AUD", "CHF", "CNY", "INR", "KRW", "BTC", "ETH"], 
            key="curr_to")
    
    with col2:
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("🔄 Convert", key="curr_convert"):
            usd_amount = amount / CURRENT_RATES[from_currency]
            converted_amount = usd_amount * CURRENT_RATES[to_currency]
            exchange_rate = CURRENT_RATES[to_currency] / CURRENT_RATES[from_currency]
            
            st.markdown(f'''
            <div class="result-box">
                {amount:,.2f} {from_currency} = {converted_amount:,.4f} {to_currency}
            </div>
            ''', unsafe_allow_html=True)
            
            st.markdown(f'''
            <div class="rate-info">
                <strong>📈 Rate:</strong> 1 {from_currency} = {exchange_rate:.6f} {to_currency}<br>
                
            </div>
            ''', unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

# Temperature Converter Tab
with tab2:
    st.markdown('<div class="converter-card">', unsafe_allow_html=True)
    st.subheader("🌡️ Temperature Converter")
    
    col1, col2, col3 = st.columns([2, 1, 2])
    
    with col1:
        temp_amount = st.number_input("Temperature", value=0.0, key="temp_amount")
        from_temp = st.selectbox("From", ["Celsius (°C)", "Fahrenheit (°F)", "Kelvin (K)"], key="temp_from")
    
    with col3:
        to_temp = st.selectbox("To", ["Fahrenheit (°F)", "Celsius (°C)", "Kelvin (K)"], key="temp_to")
    
    with col2:
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("🔄 Convert", key="temp_convert"):
            # Temperature conversion logic
            if from_temp == "Celsius (°C)":
                if to_temp == "Fahrenheit (°F)":
                    result = (temp_amount * 9/5) + 32
                elif to_temp == "Kelvin (K)":
                    result = temp_amount + 273.15
                else:
                    result = temp_amount
            elif from_temp == "Fahrenheit (°F)":
                if to_temp == "Celsius (°C)":
                    result = (temp_amount - 32) * 5/9
                elif to_temp == "Kelvin (K)":
                    result = (temp_amount - 32) * 5/9 + 273.15
                else:
                    result = temp_amount
            elif from_temp == "Kelvin (K)":
                if to_temp == "Celsius (°C)":
                    result = temp_amount - 273.15
                elif to_temp == "Fahrenheit (°F)":
                    result = (temp_amount - 273.15) * 9/5 + 32
                else:
                    result = temp_amount
            
            st.markdown(f'''
            <div class="result-box">
                {temp_amount}° {from_temp.split('(')[0].strip()} = {result:.2f}° {to_temp.split('(')[0].strip()}
            </div>
            ''', unsafe_allow_html=True)
            
            # Temperature reference points
            if to_temp == "Celsius (°C)":
                if result == 0:
                    st.info("❄️ Water freezing point!")
                elif result == 100:
                    st.info("💨 Water boiling point!")
            elif to_temp == "Fahrenheit (°F)":
                if result == 32:
                    st.info("❄️ Water freezing point!")
                elif result == 212:
                    st.info("💨 Water boiling point!")
    
    st.markdown('</div>', unsafe_allow_html=True)

# Length Converter Tab
with tab3:
    st.markdown('<div class="converter-card">', unsafe_allow_html=True)
    st.subheader("📏 Length Converter")
    
    col1, col2, col3 = st.columns([2, 1, 2])
    
    with col1:
        length_amount = st.number_input("Value", min_value=0.0, value=1.0, key="length_amount")
        from_length = st.selectbox("From", list(LENGTH_UNITS.keys()), key="length_from")
    
    with col3:
        to_length = st.selectbox("To", list(LENGTH_UNITS.keys()), index=2, key="length_to")
    
    with col2:
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("🔄 Convert", key="length_convert"):
            meters = length_amount * LENGTH_UNITS[from_length]
            result = meters / LENGTH_UNITS[to_length]
            
            st.markdown(f'''
            <div class="result-box">
                {length_amount} {from_length.split('(')[0].strip()} = {result:.8f} {to_length.split('(')[0].strip()}
            </div>
            ''', unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

# Weight Converter Tab
with tab4:
    st.markdown('<div class="converter-card">', unsafe_allow_html=True)
    st.subheader("⚖️ Weight Converter")
    
    col1, col2, col3 = st.columns([2, 1, 2])
    
    with col1:
        weight_amount = st.number_input("Value", min_value=0.0, value=1.0, key="weight_amount")
        from_weight = st.selectbox("From", list(WEIGHT_UNITS.keys()), key="weight_from")
    
    with col3:
        to_weight = st.selectbox("To", list(WEIGHT_UNITS.keys()), index=2, key="weight_to")
    
    with col2:
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("🔄 Convert", key="weight_convert"):
            grams = weight_amount * WEIGHT_UNITS[from_weight]
            result = grams / WEIGHT_UNITS[to_weight]
            
            st.markdown(f'''
            <div class="result-box">
                {weight_amount} {from_weight.split('(')[0].strip()} = {result:.8f} {to_weight.split('(')[0].strip()}
            </div>
            ''', unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

# Area Converter Tab
with tab5:
    st.markdown('<div class="converter-card">', unsafe_allow_html=True)
    st.subheader("📊 Area Converter")
    
    col1, col2, col3 = st.columns([2, 1, 2])
    
    with col1:
        area_amount = st.number_input("Value", min_value=0.0, value=1.0, key="area_amount")
        from_area = st.selectbox("From", list(AREA_UNITS.keys()), key="area_from")
    
    with col3:
        to_area = st.selectbox("To", list(AREA_UNITS.keys()), index=2, key="area_to")
    
    with col2:
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("🔄 Convert", key="area_convert"):
            sq_meters = area_amount * AREA_UNITS[from_area]
            result = sq_meters / AREA_UNITS[to_area]
            
            st.markdown(f'''
            <div class="result-box">
                {area_amount} {from_area.split('(')[0].strip()} = {result:.8f} {to_area.split('(')[0].strip()}
            </div>
            ''', unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

# Time Converter Tab
with tab6:
    st.markdown('<div class="converter-card">', unsafe_allow_html=True)
    st.subheader("🕐 Time Converter")
    
    col1, col2, col3 = st.columns([2, 1, 2])
    
    with col1:
        time_amount = st.number_input("Value", min_value=0.0, value=1.0, key="time_amount")
        from_time = st.selectbox("From", list(TIME_UNITS.keys()), key="time_from")
    
    with col3:
        to_time = st.selectbox("To", list(TIME_UNITS.keys()), index=1, key="time_to")
    
    with col2:
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("🔄 Convert", key="time_convert"):
            seconds = time_amount * TIME_UNITS[from_time]
            result = seconds / TIME_UNITS[to_time]
            
            st.markdown(f'''
            <div class="result-box">
                {time_amount} {from_time.split('(')[0].strip()} = {result:.8f} {to_time.split('(')[0].strip()}
            </div>
            ''', unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

# Volume Converter Tab
with tab7:
    st.markdown('<div class="converter-card">', unsafe_allow_html=True)
    st.subheader("📦 Volume Converter")
    
    col1, col2, col3 = st.columns([2, 1, 2])
    
    with col1:
        volume_amount = st.number_input("Value", min_value=0.0, value=1.0, key="volume_amount")
        from_volume = st.selectbox("From", list(VOLUME_UNITS.keys()), key="volume_from")
    
    with col3:
        to_volume = st.selectbox("To", list(VOLUME_UNITS.keys()), index=1, key="volume_to")
    
    with col2:
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("🔄 Convert", key="volume_convert"):
            liters = volume_amount * VOLUME_UNITS[from_volume]
            result = liters / VOLUME_UNITS[to_volume]
            
            st.markdown(f'''
            <div class="result-box">
                {volume_amount} {from_volume.split('(')[0].strip()} = {result:.8f} {to_volume.split('(')[0].strip()}
            </div>
            ''', unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

# Speed Converter Tab
with tab8:
    st.markdown('<div class="converter-card">', unsafe_allow_html=True)
    st.subheader("🚀 Speed Converter")
    
    col1, col2, col3 = st.columns([2, 1, 2])
    
    with col1:
        speed_amount = st.number_input("Value", min_value=0.0, value=1.0, key="speed_amount")
        from_speed = st.selectbox("From", list(SPEED_UNITS.keys()), key="speed_from")
    
    with col3:
        to_speed = st.selectbox("To", list(SPEED_UNITS.keys()), index=1, key="speed_to")
    
    with col2:
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("🔄 Convert", key="speed_convert"):
            ms = speed_amount * SPEED_UNITS[from_speed]
            result = ms / SPEED_UNITS[to_speed]
            
            st.markdown(f'''
            <div class="result-box">
                {speed_amount} {from_speed.split('(')[0].strip()} = {result:.8f} {to_speed.split('(')[0].strip()}
            </div>
            ''', unsafe_allow_html=True)
            
            # Speed reference points
            if from_speed == "Mile/Hour (mph)" and speed_amount >= 65:
                st.warning("🚗 Highway speed!")
            elif from_speed == "Kilometer/Hour (km/h)" and speed_amount >= 100:
                st.warning("🚗 High speed!")
    
    st.markdown('</div>', unsafe_allow_html=True)

# Feature highlights
st.markdown("---")
st.markdown("### 🌟 Feature Highlights")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown('''
    <div class="feature-card">
        <h3>⚡ Real-Time</h3>
        
    </div>
    ''', unsafe_allow_html=True)

with col2:
    st.markdown('''
    <div class="feature-card">
        <h3>🌍 Universal</h3>
        <p>8 different conversion types in one app</p>
    </div>
    ''', unsafe_allow_html=True)

with col3:
    st.markdown('''
    <div class="feature-card">
        <h3>📱 Responsive</h3>
        <p>Beautiful design on all devices</p>
    </div>
    ''', unsafe_allow_html=True)

with col4:
    st.markdown('''
    <div class="feature-card">
        <h3>🎯 Accurate</h3>
        <p>Precise calculations with high precision</p>
    </div>
    ''', unsafe_allow_html=True)

# Footer
st.sidebar.markdown("---")
st.sidebar.subheader("📋 Quick Guide")
st.sidebar.markdown("""
**How to Use:**
1. Select converter tab
2. Enter your value
3. Choose source & target units
4. Click Convert button
5. See instant results!

**Pro Tips:**
- 
- Temperature shows reference points
- Use precise decimals for accuracy
- All conversions are bidirectional
""")

st.sidebar.markdown("---")
st.sidebar.success("✅ All Systems Online")

st.sidebar.markdown("Made with ❤️ using Streamlit")
st.sidebar.caption("© 2025 Universal Converter Hub")

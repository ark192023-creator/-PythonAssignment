import streamlit as st
import math
import re

# Page configuration
st.set_page_config(
    page_title="Gradient Calculator Pro",
    page_icon="🧮",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Initialize session state
if 'display' not in st.session_state:
    st.session_state.display = '0'
if 'previous_value' not in st.session_state:
    st.session_state.previous_value = ''
if 'operator' not in st.session_state:
    st.session_state.operator = ''
if 'new_calculation' not in st.session_state:
    st.session_state.new_calculation = True
if 'history' not in st.session_state:
    st.session_state.history = []

# Enhanced Custom CSS with structured key layout
st.markdown("""
<style>
    /* Import Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;500;600&display=swap');
    
    /* Hide Streamlit elements */
    .stDeployButton {display: none;}
    header[data-testid="stHeader"] {display: none;}
    .stMainBlockContainer {padding-top: 1rem;}
    
    /* Page background with subtle pattern */
    .stApp {
        background: 
            radial-gradient(circle at 20% 50%, rgba(120, 119, 198, 0.3), transparent 50%),
            radial-gradient(circle at 80% 20%, rgba(255, 119, 198, 0.3), transparent 50%),
            radial-gradient(circle at 40% 80%, rgba(120, 219, 255, 0.3), transparent 50%),
            linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
        min-height: 100vh;
        font-family: 'Inter', sans-serif;
    }
    
    /* Main calculator container */
    .calculator-wrapper {
        max-width: 500px;
        margin: 2rem auto;
        position: relative;
        perspective: 1000px;
    }
    
    /* Calculator container with enhanced design */
    .main-container {
        position: relative;
        border-radius: 32px;
        overflow: hidden;
        box-shadow: 
            0 40px 80px rgba(0, 0, 0, 0.25),
            0 20px 40px rgba(0, 0, 0, 0.15),
            0 0 0 1px rgba(255, 255, 255, 0.1);
        transform: rotateX(2deg) rotateY(-2deg);
        transition: transform 0.3s ease;
    }
    
    .main-container:hover {
        transform: rotateX(0deg) rotateY(0deg) scale(1.02);
    }
    
    /* Gradient background box */
    .gradient-background {
        background: linear-gradient(
            135deg, 
            #667eea 0%, 
            #764ba2 20%, 
            #f093fb 40%, 
            #f5576c 60%, 
            #4facfe 80%,
            #00f2fe 100%
        );
        background-size: 400% 400%;
        animation: gradientFlow 15s ease infinite;
        padding: 35px;
        position: relative;
        border-radius: 32px;
    }
    
    @keyframes gradientFlow {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }
    
    /* Enhanced floating orbs */
    .gradient-background::before {
        content: '';
        position: absolute;
        width: 150px;
        height: 150px;
        background: radial-gradient(circle, rgba(255,255,255,0.4), rgba(255,255,255,0.1));
        border-radius: 50%;
        top: -75px;
        left: -75px;
        filter: blur(40px);
        animation: floatOrb1 12s ease-in-out infinite;
    }
    
    .gradient-background::after {
        content: '';
        position: absolute;
        width: 120px;
        height: 120px;
        background: radial-gradient(circle, rgba(255,255,255,0.3), rgba(255,255,255,0.05));
        border-radius: 50%;
        bottom: -60px;
        right: -60px;
        filter: blur(35px);
        animation: floatOrb2 10s ease-in-out infinite 3s;
    }
    
    @keyframes floatOrb1 {
        0%, 100% { transform: translate(0px, 0px) rotate(0deg); }
        33% { transform: translate(30px, -30px) rotate(120deg); }
        66% { transform: translate(-20px, 20px) rotate(240deg); }
    }
    
    @keyframes floatOrb2 {
        0%, 100% { transform: translate(0px, 0px) rotate(0deg); }
        50% { transform: translate(-25px, -25px) rotate(180deg); }
    }
    
    /* Calculator content container */
    .calculator-content {
        position: relative;
        z-index: 2;
        backdrop-filter: blur(25px);
        background: rgba(255, 255, 255, 0.15);
        border: 2px solid rgba(255, 255, 255, 0.25);
        border-radius: 24px;
        padding: 0;
        box-shadow: 
            0 8px 32px rgba(0, 0, 0, 0.15),
            inset 0 2px 0 rgba(255, 255, 255, 0.3),
            inset 0 -1px 0 rgba(0, 0, 0, 0.1);
        overflow: hidden;
    }
    
    /* Header section */
    .calculator-header {
        padding: 25px 30px 15px;
        background: linear-gradient(135deg, rgba(255,255,255,0.2), rgba(255,255,255,0.05));
        border-bottom: 1px solid rgba(255,255,255,0.1);
    }
    
    /* Enhanced title */
    .calculator-title {
        color: white;
        font-size: 1.8rem;
        font-weight: 700;
        text-align: center;
        margin: 0;
        text-shadow: 0 2px 8px rgba(0, 0, 0, 0.4);
        letter-spacing: -0.5px;
    }
    
    /* Display section */
    .display-section {
        padding: 25px 30px;
        background: rgba(0, 0, 0, 0.2);
        border-bottom: 1px solid rgba(255,255,255,0.1);
    }
    
    /* Enhanced display container */
    .display-container {
        background: linear-gradient(135deg, rgba(0, 0, 0, 0.4), rgba(0, 0, 0, 0.6));
        border-radius: 20px;
        padding: 25px;
        border: 2px solid rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(15px);
        box-shadow: 
            inset 0 2px 4px rgba(0, 0, 0, 0.3),
            0 4px 15px rgba(0, 0, 0, 0.2);
    }
    
    .display-history {
        color: rgba(255, 255, 255, 0.7);
        font-size: 1rem;
        text-align: right;
        margin-bottom: 10px;
        min-height: 1.2rem;
        font-family: 'JetBrains Mono', monospace;
        font-weight: 400;
    }
    
    .display-main {
        color: white;
        font-size: 3.2rem;
        font-weight: 600;
        text-align: right;
        font-family: 'JetBrains Mono', monospace;
        text-shadow: 0 3px 10px rgba(0, 0, 0, 0.5);
        line-height: 1.1;
        word-break: break-all;
        letter-spacing: -1px;
    }
    
    /* Keys section with structured layout */
    .keys-section {
        padding: 30px;
        background: linear-gradient(135deg, rgba(255,255,255,0.1), rgba(255,255,255,0.05));
    }
    
    /* Key grid container */
    .key-grid {
        display: grid;
        grid-template-columns: repeat(4, 1fr);
        gap: 15px;
        margin-bottom: 20px;
    }
    
    .key-row {
        display: contents;
    }
    
    /* Enhanced button styling */
    .stButton > button {
        width: 100% !important;
        height: 80px !important;
        border: none !important;
        border-radius: 20px !important;
        font-size: 1.4rem !important;
        font-weight: 600 !important;
        cursor: pointer !important;
        transition: all 0.25s cubic-bezier(0.4, 0, 0.2, 1) !important;
        backdrop-filter: blur(15px) !important;
        border: 2px solid rgba(255, 255, 255, 0.2) !important;
        position: relative !important;
        overflow: hidden !important;
        font-family: 'Inter', sans-serif !important;
        text-shadow: 0 2px 4px rgba(0, 0, 0, 0.3) !important;
        box-shadow: 
            0 8px 20px rgba(0, 0, 0, 0.15),
            0 3px 6px rgba(0, 0, 0, 0.1),
            inset 0 1px 0 rgba(255, 255, 255, 0.2) !important;
    }
    
    .stButton > button:hover {
        transform: translateY(-3px) scale(1.05) !important;
        box-shadow: 
            0 12px 30px rgba(0, 0, 0, 0.2),
            0 6px 12px rgba(0, 0, 0, 0.15),
            inset 0 1px 0 rgba(255, 255, 255, 0.3) !important;
    }
    
    .stButton > button:active {
        transform: translateY(-1px) scale(1.02) !important;
    }
    
    /* Shine effect for all buttons */
    .stButton > button::before {
        content: '' !important;
        position: absolute !important;
        top: 0 !important;
        left: -100% !important;
        width: 100% !important;
        height: 100% !important;
        background: linear-gradient(
            90deg, 
            transparent, 
            rgba(255, 255, 255, 0.4), 
            transparent
        ) !important;
        transition: left 0.6s !important;
    }
    
    .stButton > button:hover::before {
        left: 100% !important;
    }
    
    /* Number buttons - Glass effect */
    .number-btn > button {
        background: linear-gradient(135deg, rgba(255, 255, 255, 0.25), rgba(255, 255, 255, 0.1)) !important;
        color: white !important;
        border: 2px solid rgba(255, 255, 255, 0.3) !important;
    }
    
    .number-btn > button:hover {
        background: linear-gradient(135deg, rgba(255, 255, 255, 0.35), rgba(255, 255, 255, 0.2)) !important;
        border-color: rgba(255, 255, 255, 0.4) !important;
    }
    
    /* Operator buttons - Vibrant gradients */
    .operator-btn > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
        color: white !important;
        border: 2px solid rgba(102, 126, 234, 0.5) !important;
    }
    
    .operator-btn > button:hover {
        background: linear-gradient(135deg, #7c8ef4 0%, #8659b8 100%) !important;
        border-color: rgba(124, 142, 244, 0.7) !important;
    }
    
    /* Equals button - Special gradient */
    .equals-btn > button {
        background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%) !important;
        color: white !important;
        font-weight: 700 !important;
        border: 2px solid rgba(240, 147, 251, 0.5) !important;
    }
    
    .equals-btn > button:hover {
        background: linear-gradient(135deg, #f4a3fc 0%, #f7687c 100%) !important;
        border-color: rgba(244, 163, 252, 0.7) !important;
    }
    
    /* Clear buttons - Warning gradient */
    .clear-btn > button {
        background: linear-gradient(135deg, #ff6b6b 0%, #ee5a24 100%) !important;
        color: white !important;
        border: 2px solid rgba(255, 107, 107, 0.5) !important;
    }
    
    .clear-btn > button:hover {
        background: linear-gradient(135deg, #ff7979 0%, #f0683a 100%) !important;
        border-color: rgba(255, 121, 121, 0.7) !important;
    }
    
    /* Wide buttons (0 and equals) */
    .btn-wide {
        grid-column: span 2;
    }
    
    /* Enhanced focus states */
    .stButton > button:focus {
        outline: none !important;
        box-shadow: 
            0 0 0 3px rgba(255, 255, 255, 0.4),
            0 8px 20px rgba(0, 0, 0, 0.15) !important;
    }
    
    /* History section */
    .history-section {
        margin-top: 20px;
        padding: 20px;
        background: linear-gradient(135deg, rgba(255, 255, 255, 0.15), rgba(255, 255, 255, 0.05));
        border-radius: 16px;
        border: 1px solid rgba(255, 255, 255, 0.2);
        backdrop-filter: blur(10px);
    }
    
    .history-title {
        color: white;
        font-size: 1.1rem;
        font-weight: 600;
        margin-bottom: 12px;
        text-shadow: 0 1px 3px rgba(0, 0, 0, 0.3);
    }
    
    .history-item {
        color: rgba(255, 255, 255, 0.85);
        font-size: 0.95rem;
        font-family: 'JetBrains Mono', monospace;
        margin-bottom: 6px;
        padding: 8px 12px;
        background: rgba(255, 255, 255, 0.05);
        border-radius: 8px;
        border-left: 3px solid rgba(255, 255, 255, 0.3);
    }
    
    /* Responsive design */
    @media (max-width: 600px) {
        .calculator-wrapper {
            margin: 1rem;
            max-width: 95vw;
        }
        
        .main-container {
            transform: none;
        }
        
        .gradient-background {
            padding: 25px;
        }
        
        .calculator-header {
            padding: 20px 25px 15px;
        }
        
        .display-section {
            padding: 20px 25px;
        }
        
        .keys-section {
            padding: 25px;
        }
        
        .display-main {
            font-size: 2.5rem;
        }
        
        .stButton > button {
            height: 70px !important;
            font-size: 1.2rem !important;
        }
        
        .key-grid {
            gap: 12px;
        }
    }
    
    @media (max-width: 480px) {
        .calculator-title {
            font-size: 1.5rem;
        }
        
        .display-main {
            font-size: 2.2rem;
        }
        
        .stButton > button {
            height: 65px !important;
            font-size: 1.1rem !important;
        }
    }
</style>
""", unsafe_allow_html=True)

# Calculator functions
def clear_all():
    st.session_state.display = '0'
    st.session_state.previous_value = ''
    st.session_state.operator = ''
    st.session_state.new_calculation = True

def clear_entry():
    st.session_state.display = '0'
    st.session_state.new_calculation = True

def input_number(num):
    if st.session_state.new_calculation or st.session_state.display == '0':
        st.session_state.display = str(num)
        st.session_state.new_calculation = False
    else:
        st.session_state.display += str(num)

def input_decimal():
    if st.session_state.new_calculation:
        st.session_state.display = '0.'
        st.session_state.new_calculation = False
    elif '.' not in st.session_state.display:
        st.session_state.display += '.'

def input_operator(op):
    if st.session_state.previous_value and not st.session_state.new_calculation:
        calculate()
    
    st.session_state.operator = op
    st.session_state.previous_value = st.session_state.display
    st.session_state.new_calculation = True

def calculate():
    if not st.session_state.previous_value or not st.session_state.operator:
        return
    
    try:
        prev = float(st.session_state.previous_value)
        current = float(st.session_state.display)
        
        if st.session_state.operator == '+':
            result = prev + current
        elif st.session_state.operator == '-':
            result = prev - current
        elif st.session_state.operator == '*':
            result = prev * current
        elif st.session_state.operator == '/':
            if current == 0:
                st.error("Cannot divide by zero!")
                return
            result = prev / current
        else:
            return
        
        # Format result
        if result == int(result):
            result_str = str(int(result))
        else:
            result_str = f"{result:.10f}".rstrip('0').rstrip('.')
        
        # Add to history
        operator_symbol = {'*': '×', '/': '÷', '-': '−'}.get(st.session_state.operator, st.session_state.operator)
        calculation = f"{st.session_state.previous_value} {operator_symbol} {st.session_state.display} = {result_str}"
        
        st.session_state.history.insert(0, calculation)
        if len(st.session_state.history) > 5:
            st.session_state.history.pop()
        
        st.session_state.display = result_str
        st.session_state.operator = ''
        st.session_state.previous_value = ''
        st.session_state.new_calculation = True
        
    except Exception as e:
        st.error(f"Calculation error: {str(e)}")

# Main app layout
st.markdown('<div class="calculator-wrapper">', unsafe_allow_html=True)
st.markdown('<div class="main-container">', unsafe_allow_html=True)
st.markdown('<div class="gradient-background">', unsafe_allow_html=True)
st.markdown('<div class="calculator-content">', unsafe_allow_html=True)

# Header section
st.markdown('<div class="calculator-header">', unsafe_allow_html=True)
st.markdown('<h1 class="calculator-title">Calculator Pro</h1>', unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

# Display section
st.markdown('<div class="display-section">', unsafe_allow_html=True)
history_text = st.session_state.history[0] if st.session_state.history else ""
st.markdown(f'''
<div class="display-container">
    <div class="display-history">{history_text}</div>
    <div class="display-main">{st.session_state.display}</div>
</div>
''', unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

# Keys section
st.markdown('<div class="keys-section">', unsafe_allow_html=True)

# Row 1: AC, CE, ÷, ×
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.markdown('<div class="clear-btn">', unsafe_allow_html=True)
    if st.button("AC", key="ac", help="Clear All"):
        clear_all()
    st.markdown('</div>', unsafe_allow_html=True)

with col2:
    st.markdown('<div class="clear-btn">', unsafe_allow_html=True)
    if st.button("CE", key="ce", help="Clear Entry"):
        clear_entry()
    st.markdown('</div>', unsafe_allow_html=True)

with col3:
    st.markdown('<div class="operator-btn">', unsafe_allow_html=True)
    if st.button("÷", key="div", help="Divide"):
        input_operator('/')
    st.markdown('</div>', unsafe_allow_html=True)

with col4:
    st.markdown('<div class="operator-btn">', unsafe_allow_html=True)
    if st.button("×", key="mul", help="Multiply"):
        input_operator('*')
    st.markdown('</div>', unsafe_allow_html=True)

# Row 2: 7, 8, 9, -
with col1:
    st.markdown('<div class="number-btn">', unsafe_allow_html=True)
    if st.button("7", key="7"):
        input_number(7)
    st.markdown('</div>', unsafe_allow_html=True)

with col2:
    st.markdown('<div class="number-btn">', unsafe_allow_html=True)
    if st.button("8", key="8"):
        input_number(8)
    st.markdown('</div>', unsafe_allow_html=True)

with col3:
    st.markdown('<div class="number-btn">', unsafe_allow_html=True)
    if st.button("9", key="9"):
        input_number(9)
    st.markdown('</div>', unsafe_allow_html=True)

with col4:
    st.markdown('<div class="operator-btn">', unsafe_allow_html=True)
    if st.button("−", key="sub", help="Subtract"):
        input_operator('-')
    st.markdown('</div>', unsafe_allow_html=True)

# Row 3: 4, 5, 6, +
with col1:
    st.markdown('<div class="number-btn">', unsafe_allow_html=True)
    if st.button("4", key="4"):
        input_number(4)
    st.markdown('</div>', unsafe_allow_html=True)

with col2:
    st.markdown('<div class="number-btn">', unsafe_allow_html=True)
    if st.button("5", key="5"):
        input_number(5)
    st.markdown('</div>', unsafe_allow_html=True)

with col3:
    st.markdown('<div class="number-btn">', unsafe_allow_html=True)
    if st.button("6", key="6"):
        input_number(6)
    st.markdown('</div>', unsafe_allow_html=True)

with col4:
    st.markdown('<div class="operator-btn">', unsafe_allow_html=True)
    if st.button("+", key="add", help="Add"):
        input_operator('+')
    st.markdown('</div>', unsafe_allow_html=True)

# Row 4: 1, 2, 3, =
with col1:
    st.markdown('<div class="number-btn">', unsafe_allow_html=True)
    if st.button("1", key="1"):
        input_number(1)
    st.markdown('</div>', unsafe_allow_html=True)

with col2:
    st.markdown('<div class="number-btn">', unsafe_allow_html=True)
    if st.button("2", key="2"):
        input_number(2)
    st.markdown('</div>', unsafe_allow_html=True)

with col3:
    st.markdown('<div class="number-btn">', unsafe_allow_html=True)
    if st.button("3", key="3"):
        input_number(3)
    st.markdown('</div>', unsafe_allow_html=True)

with col4:
    st.markdown('<div class="equals-btn">', unsafe_allow_html=True)
    if st.button("=", key="equals", help="Calculate"):
        calculate()
    st.markdown('</div>', unsafe_allow_html=True)

# Row 5: 0 (wide), .
col1_wide, col3 = st.columns([2, 1])

with col1_wide:
    st.markdown('<div class="number-btn btn-wide">', unsafe_allow_html=True)
    if st.button("0", key="0"):
        input_number(0)
    st.markdown('</div>', unsafe_allow_html=True)

with col3:
    st.markdown('<div class="number-btn">', unsafe_allow_html=True)
    if st.button(".", key="decimal", help="Decimal point"):
        input_decimal()
    st.markdown('</div>', unsafe_allow_html=True)

# History section
if st.session_state.history:
    st.markdown('<div class="history-section">', unsafe_allow_html=True)
    st.markdown('<div class="history-title">📊 Recent Calculations</div>', unsafe_allow_html=True)
    for calc in st.session_state.history[:3]:  # Show last 3 calculations
        st.markdown(f'<div class="history-item">{calc}</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)  # keys-section
st.markdown('</div>', unsafe_allow_html=True)  # calculator-content
st.markdown('</div>', unsafe_allow_html=True)  # gradient-background
st.markdown('</div>', unsafe_allow_html=True)  # main-container
st.markdown('</div>', unsafe_allow_html=True)  # calculator-wrapper

# Instructions
st.markdown("""
<div style="text-align: center; margin-top: 2rem; color: rgba(100,100,100,0.8);">
    <small>✨ Professional calculator with beautiful gradient design • Built with Streamlit</small>
</div>
""", unsafe_allow_html=True)

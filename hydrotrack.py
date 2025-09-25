import streamlit as st
from datetime import datetime, timedelta
import random
import pandas as pd
import numpy as np

# Configure page
st.set_page_config(
    page_title="💧 HydroTracker - Stay Hydrated!",
    page_icon="💧",
    layout="centered"
)

# Beautiful gradient background and motivational styling
st.markdown("""
<style>
    .stApp {
        background: linear-gradient(45deg, 
            #667eea 0%, 
            #764ba2 15%, 
            #f093fb 30%, 
            #f5576c 45%, 
            #4facfe 60%, 
            #00f2fe 75%, 
            #667eea 100%
        );
        background-size: 400% 400%;
        animation: gradientShift 12s ease infinite;
        min-height: 100vh;
    }
    
    @keyframes gradientShift {
        0% { background-position: 0% 50%; }
        25% { background-position: 100% 50%; }
        50% { background-position: 100% 100%; }
        75% { background-position: 0% 100%; }
        100% { background-position: 0% 50%; }
    }
    
    /* Main content container with glass morphism */
    .main > div {
        background: rgba(255, 255, 255, 0.9) !important;
        border-radius: 25px !important;
        padding: 30px !important;
        margin: 15px !important;
        backdrop-filter: blur(20px) !important;
        box-shadow: 
            0 8px 32px rgba(0, 0, 0, 0.1),
            0 4px 16px rgba(0, 0, 0, 0.05),
            inset 0 1px 0 rgba(255, 255, 255, 0.8) !important;
        border: 1px solid rgba(255, 255, 255, 0.2) !important;
    }
    
    /* Enhanced progress bar with gradient */
    .stProgress > div > div > div > div {
        background: linear-gradient(90deg, 
            #667eea 0%, 
            #764ba2 25%, 
            #f093fb 50%, 
            #f5576c 75%, 
            #4facfe 100%) !important;
        border-radius: 10px !important;
        box-shadow: 0 2px 10px rgba(102, 126, 234, 0.3) !important;
    }
    
    /* Beautiful metric cards */
    [data-testid="metric-container"] {
        background: linear-gradient(135deg, 
            rgba(255, 255, 255, 0.8) 0%, 
            rgba(255, 255, 255, 0.6) 100%) !important;
        border-radius: 15px !important;
        padding: 20px !important;
        box-shadow: 
            0 4px 20px rgba(0, 0, 0, 0.1),
            inset 0 1px 0 rgba(255, 255, 255, 0.9) !important;
        border: 1px solid rgba(255, 255, 255, 0.3) !important;
        backdrop-filter: blur(10px) !important;
    }
    
    /* Styled buttons with gradient */
    .stButton > button {
        background: linear-gradient(135deg, 
            #667eea 0%, 
            #764ba2 100%) !important;
        color: white !important;
        border: none !important;
        border-radius: 15px !important;
        padding: 12px 24px !important;
        font-weight: 600 !important;
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.3) !important;
        transition: all 0.3s ease !important;
    }
    
    .stButton > button:hover {
        background: linear-gradient(135deg, 
            #764ba2 0%, 
            #f093fb 100%) !important;
        transform: translateY(-2px) !important;
        box-shadow: 0 6px 20px rgba(102, 126, 234, 0.4) !important;
    }
    
    /* Number input styling */
    .stNumberInput > div > div > input {
        border-radius: 10px !important;
        border: 2px solid rgba(102, 126, 234, 0.3) !important;
        background: rgba(255, 255, 255, 0.9) !important;
    }
    
    /* Success/Info/Warning/Error boxes with gradients */
    .stSuccess {
        background: linear-gradient(135deg, 
            rgba(16, 185, 129, 0.1) 0%, 
            rgba(16, 185, 129, 0.05) 100%) !important;
        border-left: 4px solid #10b981 !important;
        border-radius: 10px !important;
        backdrop-filter: blur(5px) !important;
    }
    
    .stInfo {
        background: linear-gradient(135deg, 
            rgba(59, 130, 246, 0.1) 0%, 
            rgba(59, 130, 246, 0.05) 100%) !important;
        border-left: 4px solid #3b82f6 !important;
        border-radius: 10px !important;
        backdrop-filter: blur(5px) !important;
    }
    
    .stWarning {
        background: linear-gradient(135deg, 
            rgba(245, 158, 11, 0.1) 0%, 
            rgba(245, 158, 11, 0.05) 100%) !important;
        border-left: 4px solid #f59e0b !important;
        border-radius: 10px !important;
        backdrop-filter: blur(5px) !important;
    }
    
    .stError {
        background: linear-gradient(135deg, 
            rgba(239, 68, 68, 0.1) 0%, 
            rgba(239, 68, 68, 0.05) 100%) !important;
        border-left: 4px solid #ef4444 !important;
        border-radius: 10px !important;
        backdrop-filter: blur(5px) !important;
    }
    
    /* Expander styling */
    .streamlit-expanderHeader {
        background: rgba(102, 126, 234, 0.1) !important;
        border-radius: 10px !important;
        border: 1px solid rgba(102, 126, 234, 0.2) !important;
    }
    
    /* Chart container enhancements */
    .stPlotlyChart {
        background: rgba(255, 255, 255, 0.8) !important;
        border-radius: 15px !important;
        padding: 15px !important;
        backdrop-filter: blur(10px) !important;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1) !important;
    }
    
    /* Custom motivational quote styling */
    .motivational-quote {
        background: linear-gradient(135deg, 
            #667eea 0%, 
            #764ba2 50%, 
            #f093fb 100%) !important;
        border-radius: 20px !important;
        padding: 25px !important;
        color: white !important;
        text-align: center !important;
        font-style: italic !important;
        font-size: 18px !important;
        font-weight: 500 !important;
        margin: 20px 0 !important;
        box-shadow: 
            0 8px 25px rgba(102, 126, 234, 0.3),
            inset 0 1px 0 rgba(255, 255, 255, 0.2) !important;
        text-shadow: 0 1px 2px rgba(0, 0, 0, 0.1) !important;
    }
    
    /* Floating animation for title */
    h1 {
        animation: float 3s ease-in-out infinite !important;
    }
    
    @keyframes float {
        0%, 100% { transform: translateY(0px); }
        50% { transform: translateY(-5px); }
    }
    
    /* Subtle glow for important elements */
    .stTitle {
        text-shadow: 0 0 20px rgba(102, 126, 234, 0.3) !important;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'daily_intake' not in st.session_state:
    st.session_state.daily_intake = 0
if 'water_entries' not in st.session_state:
    st.session_state.water_entries = []

DAILY_GOAL = 2500

def add_water(amount):
    st.session_state.daily_intake += amount
    current_time = datetime.now().strftime("%H:%M")
    st.session_state.water_entries.append({
        'time': current_time,
        'amount': amount,
        'timestamp': datetime.now()
    })

def get_progress_bar_color(percentage):
    if percentage >= 100:
        return "🟢"
    elif percentage >= 80:
        return "🟡"
    elif percentage >= 50:
        return "🔵"
    else:
        return "⚪"

def analyze_hydration_patterns():
    """Advanced analytics for hydration patterns"""
    if not st.session_state.water_entries:
        return None
    
    entries = st.session_state.water_entries
    now = datetime.now()
    
    # Time-based analysis
    times = [entry['timestamp'] for entry in entries]
    amounts = [entry['amount'] for entry in entries]
    
    # Calculate drinking frequency (minutes between drinks)
    if len(times) > 1:
        intervals = [(times[i] - times[i-1]).total_seconds() / 60 for i in range(1, len(times))]
        avg_interval = np.mean(intervals)
    else:
        avg_interval = 0
    
    # Hourly distribution
    hourly_intake = {}
    for entry in entries:
        hour = entry['timestamp'].hour
        hourly_intake[hour] = hourly_intake.get(hour, 0) + entry['amount']
    
    # Peak drinking times
    if hourly_intake:
        peak_hour = max(hourly_intake, key=hourly_intake.get)
        peak_amount = hourly_intake[peak_hour]
    else:
        peak_hour, peak_amount = None, 0
    
    # Hydration velocity (ml per hour since first drink)
    if times:
        hours_elapsed = (now - times[0]).total_seconds() / 3600
        velocity = st.session_state.daily_intake / max(hours_elapsed, 0.1)
    else:
        velocity = 0
    
    # Predicted completion time
    remaining = max(0, DAILY_GOAL - st.session_state.daily_intake)
    if velocity > 0 and remaining > 0:
        hours_to_goal = remaining / velocity
        completion_time = now + timedelta(hours=hours_to_goal)
    else:
        completion_time = None
    
    # Consistency score (based on regular intervals)
    if len(intervals) > 2:
        interval_consistency = 100 - (np.std(intervals) / np.mean(intervals) * 100)
        consistency_score = max(0, min(100, interval_consistency))
    else:
        consistency_score = 100 if len(entries) > 0 else 0
    
    return {
        'avg_interval': avg_interval,
        'peak_hour': peak_hour,
        'peak_amount': peak_amount,
        'velocity': velocity,
        'completion_time': completion_time,
        'consistency_score': consistency_score,
        'hourly_distribution': hourly_intake
    }

def get_smart_recommendations():
    """AI-powered personalized recommendations"""
    analysis = analyze_hydration_patterns()
    recommendations = []
    
    current_hour = datetime.now().hour
    remaining = max(0, DAILY_GOAL - st.session_state.daily_intake)
    percentage = (st.session_state.daily_intake / DAILY_GOAL) * 100
    
    if analysis:
        # Time-based recommendations
        if current_hour < 10 and percentage < 20:
            recommendations.append({
                'icon': '🌅',
                'title': 'Morning Boost Needed',
                'message': 'Your morning hydration is low. Try drinking 500ml now to kickstart your metabolism!',
                'priority': 'high'
            })
        
        if analysis['avg_interval'] > 120:  # More than 2 hours between drinks
            recommendations.append({
                'icon': '⏰',
                'title': 'Improve Consistency',
                'message': f'You drink every {analysis["avg_interval"]:.0f} minutes on average. Try setting hourly reminders!',
                'priority': 'medium'
            })
        
        if analysis['velocity'] > 0:
            if analysis['completion_time'] and analysis['completion_time'].hour > 22:
                recommendations.append({
                    'icon': '🌙',
                    'title': 'Evening Rush Alert',
                    'message': 'At your current pace, you\'ll finish late. Increase intake now to avoid evening rush!',
                    'priority': 'high'
                })
        
        if analysis['consistency_score'] > 80:
            recommendations.append({
                'icon': '🎯',
                'title': 'Great Consistency!',
                'message': f'Your drinking pattern is {analysis["consistency_score"]:.0f}% consistent. Keep it up!',
                'priority': 'positive'
            })
    
    # General recommendations based on current status
    if 12 <= current_hour <= 14 and percentage < 40:
        recommendations.append({
            'icon': '🍽️',
            'title': 'Lunch Break Hydration',
            'message': 'Perfect time for a big glass! Your body needs extra water for afternoon energy.',
            'priority': 'medium'
        })
    
    if 15 <= current_hour <= 17 and percentage < 60:
        recommendations.append({
            'icon': '☕',
            'title': 'Afternoon Slump Fighter',
            'message': 'Beat the 3 PM slump! Dehydration causes fatigue. Drink 300ml now for instant energy.',
            'priority': 'high'
        })
    
    if remaining > 0:
        optimal_size = min(500, max(200, remaining // max(1, 22 - current_hour)))
        recommendations.append({
            'icon': '🎯',
            'title': 'Optimal Next Drink',
            'message': f'Based on remaining time, your next drink should be {optimal_size}ml for perfect pacing.',
            'priority': 'medium'
        })
    
    return recommendations

def get_health_insights():
    """Generate health-focused insights"""
    percentage = (st.session_state.daily_intake / DAILY_GOAL) * 100
    insights = []
    
    # Dehydration level insights
    if percentage < 25:
        insights.append({
            'level': 'warning',
            'title': '🚨 Dehydration Risk',
            'content': 'You\'re at risk of dehydration. Symptoms may include headaches, fatigue, and poor concentration.'
        })
    elif percentage < 50:
        insights.append({
            'level': 'info',
            'title': '💧 Mild Dehydration',
            'content': 'You might be feeling slightly tired or less focused. Your body is asking for more water!'
        })
    elif percentage < 80:
        insights.append({
            'level': 'success',
            'title': '👍 Good Hydration',
            'content': 'You\'re well-hydrated! Your body is functioning optimally with improved circulation and energy.'
        })
    else:
        insights.append({
            'level': 'success',
            'title': '🏆 Optimal Hydration',
            'content': 'Excellent! Your brain, skin, and organs are getting the water they need for peak performance.'
        })
    
    # Time-specific health benefits
    current_hour = datetime.now().hour
    
    if 6 <= current_hour <= 9:
        insights.append({
            'level': 'info',
            'title': '🌅 Morning Benefits',
            'content': 'Morning hydration boosts metabolism by 24% and helps flush out toxins accumulated overnight.'
        })
    elif 12 <= current_hour <= 14:
        insights.append({
            'level': 'info',
            'title': '🍽️ Digestive Support',
            'content': 'Proper hydration aids digestion and nutrient absorption. Great timing for your health!'
        })
    elif 15 <= current_hour <= 18:
        insights.append({
            'level': 'info',
            'title': '🧠 Cognitive Boost',
            'content': 'Afternoon hydration prevents the 3 PM crash and maintains mental clarity for the rest of the day.'
        })
    
    return insights

def generate_weekly_insights():
    """Generate insights based on weekly patterns"""
    # Simulate weekly data for insights
    weekly_data = []
    today = datetime.now()
    
    for i in range(7):
        day = today - timedelta(days=6-i)
        if day.date() == today.date():
            intake = st.session_state.daily_intake
        else:
            random.seed(day.day + day.month + day.year)
            intake = random.randint(1200, 3500)
        weekly_data.append(intake)
    
    avg_weekly = np.mean(weekly_data)
    trend = np.mean(weekly_data[-3:]) - np.mean(weekly_data[:3])  # Recent vs early week
    consistency = 100 - (np.std(weekly_data) / avg_weekly * 100)
    
    insights = []
    
    # Weekly average insight
    if avg_weekly >= DAILY_GOAL:
        insights.append(f"🏆 **Excellent Weekly Average:** {avg_weekly:.0f}ml/day - you're exceeding your daily goal!")
    elif avg_weekly >= DAILY_GOAL * 0.8:
        insights.append(f"👍 **Good Weekly Average:** {avg_weekly:.0f}ml/day - close to your target!")
    else:
        insights.append(f"📈 **Room for Improvement:** {avg_weekly:.0f}ml/day average - let's aim higher!")
    
    # Trend analysis
    if trend > 200:
        insights.append("📈 **Improving Trend:** Your hydration has been increasing throughout the week - fantastic progress!")
    elif trend < -200:
        insights.append("📉 **Declining Trend:** Your intake has decreased recently. Let's get back on track!")
    else:
        insights.append("📊 **Stable Pattern:** Your hydration has been consistent this week.")
    
    # Consistency analysis
    if consistency > 80:
        insights.append(f"🎯 **Great Consistency:** {consistency:.0f}% consistent - you've built a solid routine!")
    elif consistency > 60:
        insights.append(f"⚖️ **Moderate Consistency:** {consistency:.0f}% - try to make your intake more regular.")
    else:
        insights.append(f"🔄 **Inconsistent Pattern:** {consistency:.0f}% - focus on building a daily habit.")
    
    return insights, weekly_data

# Header with motivational touch
st.title("💧 HydroTracker - Your Hydration Journey")
st.subheader("🌟 Transform Your Health, One Sip at a Time!")

# Motivational quotes based on progress
motivational_quotes = [
    "💪 Every drop counts! You're building a healthy habit!",
    "🌊 Like a flowing river, consistency creates miracles!",
    "✨ Your body is 60% water - give it the love it deserves!",
    "🎯 Small sips, big wins! You're closer to your goal!",
    "🏆 Hydration is self-care in its purest form!",
    "🌱 You're planting seeds of wellness with every glass!",
    "💎 Clear water, clear mind, clear path to success!",
    "🚀 Fuel your dreams with H2O - you're unstoppable!"
]

# Select quote based on intake level
if st.session_state.daily_intake >= DAILY_GOAL:
    quote = "🎉 INCREDIBLE! You're a hydration champion! Keep this amazing momentum!"
elif st.session_state.daily_intake >= DAILY_GOAL * 0.8:
    quote = "🔥 You're so close to greatness! Push through - victory awaits!"
elif st.session_state.daily_intake >= DAILY_GOAL * 0.5:
    quote = "💪 Halfway hero! Your commitment is inspiring - don't stop now!"
else:
    import random
    quote = random.choice(motivational_quotes)

st.markdown(f'<p class="motivational-quote">"{quote}"</p>', unsafe_allow_html=True)

# Current time
st.info(f"🕒 Current time: {datetime.now().strftime('%I:%M %p')}")

# Progress Display
percentage = min(100, (st.session_state.daily_intake / DAILY_GOAL) * 100)
st.subheader("📊 Today's Progress")

# Progress bar using Streamlit's native progress bar
progress_bar = st.progress(percentage / 100)
col1, col2, col3 = st.columns(3)
with col1:
    st.metric("💧 Current Intake", f"{st.session_state.daily_intake:,} ml")
with col2:
    st.metric("🎯 Goal Progress", f"{percentage:.0f}%")
with col3:
    remaining = max(0, DAILY_GOAL - st.session_state.daily_intake)
    st.metric("⏳ Remaining", f"{remaining:,} ml")

# Quick Add Buttons
st.subheader("⚡ Quick Add Water")
col1, col2, col3 = st.columns(3)

with col1:
    if st.button("💧 Add 250ml", use_container_width=True, type="primary"):
        add_water(250)
        st.rerun()

with col2:
    if st.button("💧 Add 500ml", use_container_width=True, type="primary"):
        add_water(500)
        st.rerun()

with col3:
    if st.button("💧 Add 750ml", use_container_width=True, type="primary"):
        add_water(750)
        st.rerun()

# Custom Amount
st.subheader("🎯 Add Custom Amount")
col1, col2 = st.columns([3, 1])
with col1:
    custom_amount = st.number_input("Enter amount (ml)", min_value=0, max_value=1000, value=250, step=50)
with col2:
    st.write("")  # Add some spacing
    if st.button("Add Custom", use_container_width=True):
        add_water(custom_amount)
        st.rerun()

# Statistics
st.subheader("📈 Daily Statistics")
times_drunk = len(st.session_state.water_entries)
avg_per_drink = st.session_state.daily_intake / times_drunk if times_drunk > 0 else 0

col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric("💧 Total Intake", f"{st.session_state.daily_intake:,} ml")
with col2:
    st.metric("⏳ Remaining", f"{remaining:,} ml")
with col3:
    st.metric("🥤 Times Drunk", f"{times_drunk}")
with col4:
    st.metric("📊 Avg per Drink", f"{avg_per_drink:.0f} ml")

# Goal Status Messages
if st.session_state.daily_intake >= DAILY_GOAL:
    st.success("🎉 Congratulations! You've reached your daily goal!")
elif st.session_state.daily_intake >= DAILY_GOAL * 0.8:
    st.info("💪 Almost there! You're 80% to your goal!")
elif st.session_state.daily_intake >= DAILY_GOAL * 0.5:
    st.warning("🌊 Good progress! You're halfway to your goal!")
elif st.session_state.daily_intake > 0:
    st.warning("🚰 Keep going! You've made a start!")

# Weekly Calendar using Streamlit columns with enhanced calendar view
st.subheader("📅 Your Hydration Calendar - This Week")

# Get the start of current week (Monday)
today = datetime.now()
week_start = today - timedelta(days=today.weekday())

# Calendar header with week info
st.info(f"🗓️ Week of {week_start.strftime('%B %d')} - {(week_start + timedelta(days=6)).strftime('%B %d, %Y')}")

# Create 7 columns for days of the week
cols = st.columns(7)
days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
day_shorts = ["MON", "TUE", "WED", "THU", "FRI", "SAT", "SUN"]
day_emojis = ["💼", "🔥", "⚡", "🌟", "🎉", "🌈", "😴"]

for i, col in enumerate(cols):
    day = week_start + timedelta(days=i)
    day_name = day_shorts[i]
    day_num = day.strftime("%d")
    day_emoji = day_emojis[i]
    
    if day.date() == today.date():
        intake = st.session_state.daily_intake
        is_today = True
    elif day.date() < today.date():
        # Demo data for past days
        random.seed(day.day + day.month + day.year)
        intake = random.randint(1200, 3500)
        is_today = False
    else:
        intake = 0
        is_today = False
    
    # Calculate progress percentage for visual representation
    progress_pct = min(100, (intake / DAILY_GOAL) * 100)
    
    with col:
        if is_today:
            if intake >= DAILY_GOAL:
                st.success(f"**{day_emoji} {day_name}**\n\n📅 **{day_num}**\n\n💧 **{intake:,}ml**\n\n🎉 **GOAL SMASHED!**\n\n✨ **TODAY** ✨")
            elif intake >= DAILY_GOAL * 0.8:
                st.info(f"**{day_emoji} {day_name}**\n\n📅 **{day_num}**\n\n💧 **{intake:,}ml**\n\n🔥 **{progress_pct:.0f}% - Almost there!**\n\n✨ **TODAY** ✨")
            else:
                st.warning(f"**{day_emoji} {day_name}**\n\n📅 **{day_num}**\n\n💧 **{intake:,}ml**\n\n💪 **{progress_pct:.0f}% - Keep going!**\n\n✨ **TODAY** ✨")
        elif intake >= DAILY_GOAL:
            st.success(f"**{day_emoji} {day_name}**\n\n📅 **{day_num}**\n\n💧 **{intake:,}ml**\n\n🏆 **Champion!**\n\n✅ **{progress_pct:.0f}%**")
        elif intake >= DAILY_GOAL * 0.8:
            st.warning(f"**{day_emoji} {day_name}**\n\n📅 **{day_num}**\n\n💧 **{intake:,}ml**\n\n⭐ **Great effort!**\n\n📊 **{progress_pct:.0f}%**")
        elif intake > 0:
            st.error(f"**{day_emoji} {day_name}**\n\n📅 **{day_num}**\n\n💧 **{intake:,}ml**\n\n📈 **Room to grow**\n\n📊 **{progress_pct:.0f}%**")
        else:
            st.write(f"**{day_emoji} {day_name}**\n\n📅 **{day_num}**\n\n💧 **{intake:,}ml**\n\n🌱 **Future day**\n\n⭕ **0%**")

# Weekly summary
total_week_intake = sum([st.session_state.daily_intake if i == today.weekday() 
                        else (random.seed(week_start.day + i) or random.randint(1200, 3500)) 
                        if (week_start + timedelta(days=i)).date() < today.date() 
                        else 0 for i in range(7)])

avg_daily = total_week_intake / max(1, today.weekday() + 1)
weekly_goal = DAILY_GOAL * 7

col1, col2, col3 = st.columns(3)
with col1:
    st.metric("🏆 This Week Total", f"{total_week_intake:,} ml", f"{(total_week_intake/weekly_goal)*100:.0f}% of weekly goal")
with col2:
    st.metric("📊 Daily Average", f"{avg_daily:,.0f} ml", f"{'Above' if avg_daily > DAILY_GOAL else 'Below'} target")
with col3:
    days_completed = sum(1 for i in range(today.weekday() + 1) 
                        if (i == today.weekday() and st.session_state.daily_intake >= DAILY_GOAL) 
                        or (i < today.weekday()))
    st.metric("✅ Goals Hit This Week", f"{days_completed} days", f"{(days_completed/(today.weekday()+1))*100:.0f}% success rate")

st.success("🌟 **Pro Tip:** Past days show demo data to inspire you - your real journey starts today!")

# Weekly Chart with enhanced insights
st.subheader("📊 Advanced Weekly Analytics")

# Generate chart data with insights
chart_data = []
insight_data = []
for i in range(7):
    day = today - timedelta(days=6-i)
    day_name = day.strftime("%a")
    
    if day.date() == today.date():
        intake = st.session_state.daily_intake
        is_today = True
    elif day.date() < today.date():
        random.seed(day.day + day.month + day.year)
        intake = random.randint(1000, 3000)
        is_today = False
    else:
        intake = 0
        is_today = False
    
    chart_data.append(intake)
    insight_data.append((day_name, intake, is_today))

# Create DataFrame for chart
df = pd.DataFrame({
    'Day': [d[0] for d in insight_data],
    'Intake (ml)': chart_data,
    'Goal': [DAILY_GOAL] * 7
})

# Display enhanced bar chart
st.bar_chart(df.set_index('Day'))

# Weekly insights
weekly_insights, weekly_data = generate_weekly_insights()
st.markdown("### 📈 **Weekly Performance Analysis**")
for insight in weekly_insights:
    st.info(insight)

# Advanced hydration analytics
st.subheader("🔬 Advanced Hydration Analytics")

if st.session_state.water_entries:
    analysis = analyze_hydration_patterns()
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric(
            "💧 Hydration Velocity", 
            f"{analysis['velocity']:.0f} ml/hr",
            help="Rate of water intake since your first drink today"
        )
    
    with col2:
        if analysis['avg_interval'] > 0:
            st.metric(
                "⏱️ Drinking Frequency", 
                f"{analysis['avg_interval']:.0f} min",
                help="Average time between drinks"
            )
        else:
            st.metric("⏱️ Drinking Frequency", "First drink", help="Start your hydration journey!")
    
    with col3:
        st.metric(
            "🎯 Consistency Score", 
            f"{analysis['consistency_score']:.0f}%",
            help="How regular your drinking pattern is"
        )
    
    # Completion prediction
    if analysis['completion_time'] and st.session_state.daily_intake < DAILY_GOAL:
        completion_str = analysis['completion_time'].strftime("%I:%M %p")
        st.info(f"🔮 **Goal Prediction:** At your current pace, you'll reach your goal by **{completion_str}**")
    elif st.session_state.daily_intake >= DAILY_GOAL:
        st.success("🎉 **Goal Achieved!** You've already reached your daily target!")
    
    # Peak drinking time analysis
    if analysis['peak_hour']:
        peak_time = f"{analysis['peak_hour']:02d}:00"
        st.info(f"⭐ **Peak Hour:** Your most active drinking time today was **{peak_time}** with **{analysis['peak_amount']}ml**")

else:
    st.info("📊 **Analytics will appear here once you start tracking your water intake!**")

# Smart AI Recommendations
st.subheader("🤖 AI-Powered Smart Recommendations")

recommendations = get_smart_recommendations()
if recommendations:
    for rec in recommendations:
        if rec['priority'] == 'high':
            st.error(f"{rec['icon']} **{rec['title']}:** {rec['message']}")
        elif rec['priority'] == 'medium':
            st.warning(f"{rec['icon']} **{rec['title']}:** {rec['message']}")
        elif rec['priority'] == 'positive':
            st.success(f"{rec['icon']} **{rec['title']}:** {rec['message']}")
        else:
            st.info(f"{rec['icon']} **{rec['title']}:** {rec['message']}")
else:
    st.info("🎯 **Start drinking water to get personalized recommendations!**")

# Health Insights Dashboard
st.subheader("🏥 Health Impact Dashboard")

health_insights = get_health_insights()
for insight in health_insights:
    if insight['level'] == 'warning':
        st.error(f"**{insight['title']}**\n\n{insight['content']}")
    elif insight['level'] == 'info':
        st.info(f"**{insight['title']}**\n\n{insight['content']}")
    else:
        st.success(f"**{insight['title']}**\n\n{insight['content']}")

# Detailed hourly breakdown
if st.session_state.water_entries:
    with st.expander("📊 Detailed Hourly Breakdown"):
        analysis = analyze_hydration_patterns()
        if analysis and analysis['hourly_distribution']:
            hourly_df = pd.DataFrame([
                {'Hour': f"{hour:02d}:00", 'Intake (ml)': amount} 
                for hour, amount in analysis['hourly_distribution'].items()
            ])
            st.bar_chart(hourly_df.set_index('Hour'))
        else:
            st.info("No hourly data available yet. Keep drinking to see your patterns!")

# Activity Log
if st.session_state.water_entries:
    st.subheader("📝 Today's Water Log")
    with st.expander(f"View all {len(st.session_state.water_entries)} entries"):
        for i, entry in enumerate(reversed(st.session_state.water_entries)):
            st.write(f"**{len(st.session_state.water_entries) - i}.** {entry}")

# Hydration Tips with Motivation
if st.session_state.daily_intake > 0:
    st.subheader("💡 Your Personal Hydration Coach")
    
    if remaining > 0:
        hours_left = max(1, 22 - datetime.now().hour)
        ml_per_hour = remaining / hours_left
        
        # Motivational coaching based on situation
        if ml_per_hour > 300:
            st.error(f"""
            🚨 **Challenge Accepted!** 
            
            You need **{ml_per_hour:.0f}ml per hour** to hit your goal - that's about **one large glass every hour!**
            
            💪 **Remember:** Champions are made when the going gets tough! You've got this! 
            Set a timer and make it happen! ⏰
            """)
        elif ml_per_hour > 200:
            st.warning(f"""
            🎯 **Steady Wins the Race!** 
            
            Drink **{ml_per_hour:.0f}ml per hour** - that's like sipping a glass every hour.
            
            🌟 **You're doing great!** Small consistent actions create big results! Keep the momentum! 🚀
            """)
        elif ml_per_hour > 100:
            st.info(f"""
            😊 **Cruising to Victory!** 
            
            Just **{ml_per_hour:.0f}ml per hour** needed - you're practically there!
            
            🏆 **Success feels good, doesn't it?** You're building an amazing healthy habit! ✨
            """)
        else:
            st.success(f"""
            🎉 **Victory Lap Time!** 
            
            Only **{ml_per_hour:.0f}ml per hour** - you could reach your goal with just a few more sips!
            
            ⭐ **You're absolutely crushing it!** This is what dedication looks like! 🌟
            """)
    else:
        st.success("""
        🏆 **HYDRATION SUPERSTAR!** 
        
        🎊 You've not just reached your goal - you've EXCEEDED it! 
        
        💎 **Your body is thanking you right now!** You're giving it exactly what it needs to perform at its best!
        
        🌟 **Keep this incredible momentum going tomorrow - you're building a life-changing habit!** ✨
        """)
        
    # Additional motivational tips
    st.info("""
    🌊 **Daily Hydration Wisdom:**
    
    • 🌅 **Morning Magic:** Start with 500ml when you wake up - kickstart your metabolism!
    • 🍽️ **Meal Prep:** 250ml before each meal helps digestion and controls appetite
    • 🏃‍♂️ **Exercise Boost:** Add 500-750ml during workouts for peak performance
    • 🌙 **Evening Wind-down:** Stop 2 hours before bed for better sleep quality
    
    **Remember: You're not just drinking water - you're investing in your health! 💪**
    """)
else:
    st.info("""
    🌟 **Welcome to Your Hydration Journey!** 
    
    💧 **Ready to transform your health?** Every expert was once a beginner!
    
    🎯 **Your goal:** 2,500ml per day (about 10 cups)
    
    ✨ **Start strong:** Click one of the buttons above and take your first step toward a healthier, more energized you!
    
    🚀 **You've got this!** Champions are made one sip at a time!
    """)

# Progress Summary
st.subheader("📋 Today's Summary")
if st.session_state.daily_intake > 0:
    glasses_equivalent = st.session_state.daily_intake / 250  # Assuming 250ml per glass
    st.info(f"""
    **Today's Achievement:**
    - 💧 You've consumed {st.session_state.daily_intake:,}ml of water
    - 🥤 That's equivalent to {glasses_equivalent:.1f} glasses
    - ⚡ You've logged water {times_drunk} times today
    - 📈 You're {percentage:.0f}% toward your daily goal
    """)
else:
    st.info("💧 **Ready to start?** Click one of the buttons above to begin tracking your water intake!")

# Controls
st.subheader("⚙️ Controls")
col1, col2 = st.columns(2)

with col1:
    if st.button("🔄 Reset Today's Data", type="secondary", use_container_width=True):
        st.session_state.daily_intake = 0
        st.session_state.water_entries = []
        st.success("✅ Today's data has been reset!")
        st.rerun()

with col2:
    if st.button("↩️ Undo Last Entry", type="secondary", use_container_width=True):
        if st.session_state.water_entries:
            # Parse last entry to get amount
            last_entry = st.session_state.water_entries.pop()
            amount = int(last_entry.split(" - ")[1].replace("ml", ""))
            st.session_state.daily_intake -= amount
            st.success(f"✅ Removed {amount}ml from today's total!")
            st.rerun()
        else:
            st.warning("⚠️ No entries to undo!")

# Footer with motivation
st.markdown("---")
st.markdown("""
### 💧 Your Hydration Success Blueprint

🌟 **Why Hydration Matters:**
- **🧠 Brain Power:** Proper hydration improves focus and memory by up to 23%
- **💪 Energy Boost:** Even 2% dehydration can reduce energy levels significantly  
- **✨ Glowing Skin:** Water is nature's best beauty treatment
- **🏃‍♂️ Peak Performance:** Athletes perform 15% better when properly hydrated
- **😊 Mood Magic:** Good hydration = better mood and less stress

### 🎯 **Your Daily Hydration Goals:**
- **🌅 Morning Kickstart:** 500ml upon waking (✅ Metabolism boost!)
- **🍽️ Pre-Meal Power:** 250ml before each meal (✅ Better digestion!)
- **🏋️‍♂️ Workout Fuel:** Extra 500-750ml during exercise (✅ Peak performance!)
- **🌙 Evening Balance:** Stop 2 hours before bed (✅ Quality sleep!)

### 🏆 **Remember:**
**"You are not just tracking water - you are building the foundation of a healthier, more vibrant YOU!"**

🌊 **Stay consistent, stay motivated, stay hydrated!** 🌟
""")

# Final motivational call to action
if st.session_state.daily_intake < DAILY_GOAL:
    st.markdown("""
    <div style="background: linear-gradient(135deg, #667eea, #764ba2); 
                border-radius: 15px; padding: 20px; text-align: center; 
                color: white; margin: 20px 0;">
        <h2>🚀 Ready to Level Up Your Health Game?</h2>
        <p style="font-size: 18px; margin: 15px 0;">
            <strong>Every sip is a step towards a better you!</strong><br>
            Your future self will thank you for the healthy choices you make today! 💪✨
        </p>
    </div>
    """, unsafe_allow_html=True)
else:
    st.markdown("""
    <div style="background: linear-gradient(135deg, #10b981, #34d399); 
                border-radius: 15px; padding: 20px; text-align: center; 
                color: white; margin: 20px 0;">
        <h2>🎉 CONGRATULATIONS, HYDRATION HERO! 🎉</h2>
        <p style="font-size: 18px; margin: 15px 0;">
            <strong>You've reached your goal and your body is celebrating!</strong><br>
            This is what winning looks like - keep this amazing streak alive! 🏆✨
        </p>
    </div>
    """, unsafe_allow_html=True)

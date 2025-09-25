import streamlit as st
import pandas as pd
from datetime import datetime
import io
import json

# Page configuration
st.set_page_config(
    page_title="Event Registration System",
    page_icon="🎟️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 10px;
        margin-bottom: 2rem;
        color: white;
    }
    
    .stat-card {
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
        padding: 1.5rem;
        border-radius: 10px;
        text-align: center;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    
    .success-message {
        background: linear-gradient(90deg, #11998e 0%, #38ef7d 100%);
        color: white;
        padding: 1rem;
        border-radius: 8px;
        text-align: center;
        margin: 1rem 0;
    }
    
    .metric-container {
        background: white;
        padding: 1rem;
        border-radius: 8px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        margin: 0.5rem 0;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
def init_session_state():
    if 'registrations' not in st.session_state:
        st.session_state.registrations = []
    if 'show_success' not in st.session_state:
        st.session_state.show_success = False
    if 'success_message' not in st.session_state:
        st.session_state.success_message = ""

# Available events
EVENTS = [
    "Tech Conference 2025",
    "Digital Marketing Summit",
    "Startup Pitch Night",
    "AI & Machine Learning Workshop",
    "Web Development Bootcamp",
    "Data Science Meetup",
    "Cybersecurity Seminar",
    "Cloud Computing Workshop"
]

# Function to add registration
def add_registration(name, email, event):
    registration = {
        'id': len(st.session_state.registrations) + 1,
        'name': name,
        'email': email,
        'event': event,
        'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        'date': datetime.now().strftime("%Y-%m-%d")
    }
    st.session_state.registrations.append(registration)
    st.session_state.show_success = True
    st.session_state.success_message = f"Successfully registered {name} for {event}!"

# Function to get statistics
def get_statistics():
    if not st.session_state.registrations:
        return {
            'total': 0,
            'today': 0,
            'by_event': {},
            'recent': []
        }
    
    df = pd.DataFrame(st.session_state.registrations)
    today = datetime.now().strftime("%Y-%m-%d")
    
    stats = {
        'total': len(df),
        'today': len(df[df['date'] == today]),
        'by_event': df['event'].value_counts().to_dict(),
        'recent': df.tail(5).to_dict('records')
    }
    
    return stats

# Function to export to CSV
def export_to_csv():
    if not st.session_state.registrations:
        return None
    
    df = pd.DataFrame(st.session_state.registrations)
    df = df[['name', 'email', 'event', 'timestamp']]  # Select relevant columns
    df.columns = ['Name', 'Email', 'Event', 'Registration Date']
    
    csv_buffer = io.StringIO()
    df.to_csv(csv_buffer, index=False)
    return csv_buffer.getvalue()

# Main app
def main():
    init_session_state()
    
    # Header
    st.markdown("""
    <div class="main-header">
        <h1>🎟️ Event Registration System</h1>
        <p>Join our amazing events and connect with like-minded individuals. Registration is quick, easy, and secure.</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Show success message
    if st.session_state.show_success:
        st.markdown(f"""
        <div class="success-message">
            ✅ {st.session_state.success_message}
        </div>
        """, unsafe_allow_html=True)
        st.session_state.show_success = False
    
    # Create columns for layout
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.markdown("### 📝 Event Registration")
        
        # Registration form
        with st.container():
            st.markdown("Fill in your details to secure your spot:")
            
            name = st.text_input("👤 Full Name", placeholder="Enter your full name")
            email = st.text_input("📧 Email Address", placeholder="Enter your email address")
            event = st.selectbox("🎯 Select Event", [""] + EVENTS, format_func=lambda x: "Choose an event..." if x == "" else x)
            
            # Registration button
            if st.button("🚀 Register Now", type="primary", use_container_width=True):
                if name and email and event:
                    # Basic email validation
                    if "@" in email and "." in email:
                        add_registration(name, email, event)
                        st.rerun()
                    else:
                        st.error("Please enter a valid email address")
                else:
                    st.error("Please fill in all fields")
    
    with col2:
        st.markdown("### 📊 Registration Statistics")
        
        # Get current statistics
        stats = get_statistics()
        
        # Display metrics
        metric_col1, metric_col2 = st.columns(2)
        
        with metric_col1:
            st.markdown("""
            <div class="metric-container">
            """, unsafe_allow_html=True)
            st.metric("Total Registrations", stats['total'])
            st.markdown("</div>", unsafe_allow_html=True)
        
        with metric_col2:
            st.markdown("""
            <div class="metric-container">
            """, unsafe_allow_html=True)
            st.metric("Today's Registrations", stats['today'])
            st.markdown("</div>", unsafe_allow_html=True)
        
        # Event breakdown
        if stats['by_event']:
            st.markdown("#### 📈 Event Breakdown")
            event_df = pd.DataFrame(list(stats['by_event'].items()), columns=['Event', 'Registrations'])
            event_df = event_df.sort_values('Registrations', ascending=False)
            
            # Display as a bar chart
            st.bar_chart(event_df.set_index('Event')['Registrations'])
            
            # Display as a table
            st.dataframe(event_df, use_container_width=True, hide_index=True)
        else:
            st.info("No registrations yet. Be the first to register!")
        
        # Recent registrations
        if stats['recent']:
            st.markdown("#### 🕒 Recent Registrations")
            recent_df = pd.DataFrame(stats['recent'])
            recent_df = recent_df[['name', 'event', 'timestamp']].iloc[::-1]  # Reverse order
            recent_df.columns = ['Name', 'Event', 'Date']
            st.dataframe(recent_df, use_container_width=True, hide_index=True)
    
    # Admin Panel in Sidebar
    with st.sidebar:
        st.markdown("### 🔧 Admin Panel")
        
        # Export functionality
        st.markdown("#### 📥 Data Export")
        if st.session_state.registrations:
            csv_data = export_to_csv()
            if csv_data:
                st.download_button(
                    label=f"📥 Export CSV ({len(st.session_state.registrations)} records)",
                    data=csv_data,
                    file_name=f"event_registrations_{datetime.now().strftime('%Y-%m-%d')}.csv",
                    mime="text/csv",
                    use_container_width=True
                )
        else:
            st.info("No data to export")
        
        # Clear data functionality
        st.markdown("#### 🗑️ Data Management")
        if st.button("Clear All Data", type="secondary", use_container_width=True):
            if st.session_state.registrations:
                st.session_state.registrations = []
                st.success("All registration data cleared!")
                st.rerun()
            else:
                st.info("No data to clear")
        
        # Display total records
        st.info(f"Total Records: {len(st.session_state.registrations)}")
        
        # Raw data view (for debugging)
        if st.checkbox("Show Raw Data"):
            if st.session_state.registrations:
                st.json(st.session_state.registrations)
            else:
                st.write("No data available")
    
    # Footer
    st.markdown("---")
    st.markdown("""
    <div style='text-align: center; color: #666; padding: 2rem 0;'>
        <p>Powered by Event Registration System • Built with ❤️ using Streamlit</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Auto-refresh every 30 seconds to show live updates
    if st.button("🔄 Refresh", help="Click to refresh the statistics"):
        st.rerun()

if __name__ == "__main__":
    main()

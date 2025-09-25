import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import json
import hashlib
from typing import Dict, List, Tuple, Optional
import sqlite3
import os

# Configuration
st.set_page_config(
    page_title="Advanced Gym Workout Logger",
    page_icon="💪",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Database setup
def init_database():
    """Initialize SQLite database for persistent storage"""
    conn = sqlite3.connect('gym_workouts.db')
    cursor = conn.cursor()
    
    # Create workouts table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS workouts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date TEXT NOT NULL,
            exercise TEXT NOT NULL,
            sets INTEGER NOT NULL,
            reps INTEGER NOT NULL,
            weight REAL NOT NULL,
            duration_minutes INTEGER,
            notes TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Create exercise_library table for RAG knowledge base
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS exercise_library (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            exercise_name TEXT UNIQUE NOT NULL,
            muscle_group TEXT NOT NULL,
            equipment TEXT,
            difficulty_level TEXT,
            description TEXT,
            proper_form TEXT,
            common_mistakes TEXT,
            progression_tips TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    conn.commit()
    conn.close()

def populate_exercise_library():
    """Populate exercise library with common exercises for RAG analysis"""
    conn = sqlite3.connect('gym_workouts.db')
    cursor = conn.cursor()
    
    exercises = [
        ("Bench Press", "Chest", "Barbell", "Intermediate", 
         "Compound upper body exercise targeting chest, shoulders, and triceps",
         "Lie flat, grip bar slightly wider than shoulders, lower to chest, press up",
         "Arching back excessively, bouncing bar off chest, uneven grip",
         "Start with bodyweight push-ups, progress weight gradually, focus on form"),
        ("Squat", "Legs", "Barbell", "Intermediate",
         "Fundamental lower body exercise targeting quads, glutes, and core",
         "Feet shoulder-width apart, descend until thighs parallel, drive through heels",
         "Knees caving in, forward lean, not reaching proper depth",
         "Start with bodyweight, add weight gradually, focus on mobility"),
        ("Deadlift", "Back", "Barbell", "Advanced",
         "Full-body compound movement, primarily targeting posterior chain",
         "Hip hinge movement, keep bar close to body, drive hips forward",
         "Rounded back, bar drifting away, not engaging lats",
         "Master hip hinge pattern first, start light, focus on form over weight"),
        ("Pull-up", "Back", "Pull-up Bar", "Intermediate",
         "Upper body pulling exercise targeting lats, rhomboids, and biceps",
         "Hang from bar, pull body up until chin over bar, control descent",
         "Using momentum, partial range of motion, not engaging core",
         "Start with assisted pull-ups or negatives, build up gradually"),
        ("Overhead Press", "Shoulders", "Barbell", "Intermediate",
         "Vertical pressing movement targeting shoulders and triceps",
         "Stand tall, press bar overhead, keep core tight throughout movement",
         "Pressing behind neck, excessive back arch, not stabilizing core",
         "Start with dumbbells, focus on mobility, progress weight slowly")
    ]
    
    for exercise in exercises:
        cursor.execute('''
            INSERT OR IGNORE INTO exercise_library 
            (exercise_name, muscle_group, equipment, difficulty_level, description, proper_form, common_mistakes, progression_tips)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', exercise)
    
    conn.commit()
    conn.close()

class WorkoutRAG:
    """RAG (Retrieval-Augmented Generation) system for workout analysis"""
    
    def __init__(self):
        self.exercise_knowledge = self.load_exercise_knowledge()
        
    def load_exercise_knowledge(self) -> Dict:
        """Load exercise knowledge from database"""
        conn = sqlite3.connect('gym_workouts.db')
        df = pd.read_sql_query("SELECT * FROM exercise_library", conn)
        conn.close()
        
        knowledge_base = {}
        for _, row in df.iterrows():
            knowledge_base[row['exercise_name'].lower()] = {
                'muscle_group': row['muscle_group'],
                'equipment': row['equipment'],
                'difficulty': row['difficulty_level'],
                'description': row['description'],
                'proper_form': row['proper_form'],
                'common_mistakes': row['common_mistakes'],
                'progression_tips': row['progression_tips']
            }
        return knowledge_base
    
    def get_exercise_info(self, exercise_name: str) -> Optional[Dict]:
        """Retrieve exercise information with fuzzy matching"""
        exercise_lower = exercise_name.lower()
        
        # Direct match
        if exercise_lower in self.exercise_knowledge:
            return self.exercise_knowledge[exercise_lower]
        
        # Fuzzy matching
        for known_exercise in self.exercise_knowledge.keys():
            if exercise_lower in known_exercise or known_exercise in exercise_lower:
                return self.exercise_knowledge[known_exercise]
        
        return None
    
    def analyze_workout_pattern(self, workout_data: pd.DataFrame) -> Dict:
        """Analyze workout patterns and provide insights"""
        if workout_data.empty:
            return {"error": "No workout data available"}
        
        analysis = {
            "total_workouts": len(workout_data),
            "unique_exercises": workout_data['exercise'].nunique(),
            "muscle_groups_trained": set(),
            "consistency_score": 0,
            "progression_analysis": {},
            "recommendations": []
        }
        
        # Analyze muscle groups
        for exercise in workout_data['exercise'].unique():
            exercise_info = self.get_exercise_info(exercise)
            if exercise_info:
                analysis["muscle_groups_trained"].add(exercise_info['muscle_group'])
        
        # Calculate consistency score (workouts per week)
        if len(workout_data) > 0:
            date_range = pd.to_datetime(workout_data['date'])
            days_span = (date_range.max() - date_range.min()).days + 1
            weeks_span = max(days_span / 7, 1)
            analysis["consistency_score"] = round(len(workout_data) / weeks_span, 2)
        
        # Progression analysis
        for exercise in workout_data['exercise'].unique():
            exercise_data = workout_data[workout_data['exercise'] == exercise].copy()
            exercise_data['date'] = pd.to_datetime(exercise_data['date'])
            exercise_data = exercise_data.sort_values('date')
            
            if len(exercise_data) >= 2:
                # Calculate volume progression (sets × reps × weight)
                exercise_data['volume'] = exercise_data['sets'] * exercise_data['reps'] * exercise_data['weight']
                first_volume = exercise_data['volume'].iloc[0]
                last_volume = exercise_data['volume'].iloc[-1]
                progression_pct = ((last_volume - first_volume) / first_volume * 100) if first_volume > 0 else 0
                
                analysis["progression_analysis"][exercise] = {
                    "volume_change_pct": round(progression_pct, 1),
                    "trend": "increasing" if progression_pct > 5 else "decreasing" if progression_pct < -5 else "stable"
                }
        
        # Generate recommendations
        analysis["recommendations"] = self.generate_recommendations(analysis, workout_data)
        
        return analysis
    
    def generate_recommendations(self, analysis: Dict, workout_data: pd.DataFrame) -> List[str]:
        """Generate personalized recommendations based on analysis"""
        recommendations = []
        
        # Consistency recommendations
        if analysis["consistency_score"] < 2:
            recommendations.append("🎯 Try to increase workout frequency to at least 2-3 times per week for better results")
        elif analysis["consistency_score"] > 6:
            recommendations.append("⚠️ Consider adding rest days to prevent overtraining and allow for recovery")
        
        # Muscle group balance
        muscle_groups = analysis["muscle_groups_trained"]
        if len(muscle_groups) < 3:
            recommendations.append("🔄 Consider adding exercises for different muscle groups to create a balanced routine")
        
        # Progression recommendations
        stagnant_exercises = [
            exercise for exercise, prog in analysis["progression_analysis"].items()
            if prog["trend"] == "stable"
        ]
        if stagnant_exercises:
            recommendations.append(f"📈 Consider progressive overload for: {', '.join(stagnant_exercises[:3])}")
        
        # Exercise variety
        if analysis["unique_exercises"] < 5:
            recommendations.append("🎪 Add more exercise variety to prevent plateaus and maintain motivation")
        
        return recommendations

class HallucinationValidator:
    """System to validate and reduce hallucination in workout analysis"""
    
    @staticmethod
    def validate_workout_entry(exercise: str, sets: int, reps: int, weight: float) -> Tuple[bool, str]:
        """Validate workout entry for realistic values"""
        errors = []
        
        # Validate sets
        if sets < 1 or sets > 20:
            errors.append("Sets should be between 1 and 20")
        
        # Validate reps
        if reps < 1 or reps > 100:
            errors.append("Reps should be between 1 and 100")
        
        # Validate weight
        if weight < 0 or weight > 1000:
            errors.append("Weight should be between 0 and 1000 kg/lbs")
        
        # Exercise name validation
        if not exercise.strip():
            errors.append("Exercise name cannot be empty")
        
        return len(errors) == 0, "; ".join(errors)
    
    @staticmethod
    def validate_analysis_results(analysis: Dict) -> Dict:
        """Validate and sanitize analysis results"""
        validated = analysis.copy()
        
        # Ensure numeric values are within reasonable bounds
        if "consistency_score" in validated:
            validated["consistency_score"] = max(0, min(validated["consistency_score"], 14))  # Max 2 workouts per day
        
        # Validate progression percentages
        if "progression_analysis" in validated:
            for exercise, prog in validated["progression_analysis"].items():
                if "volume_change_pct" in prog:
                    # Cap progression at reasonable values
                    prog["volume_change_pct"] = max(-90, min(prog["volume_change_pct"], 500))
        
        return validated

# Initialize components
init_database()
populate_exercise_library()
workout_rag = WorkoutRAG()
validator = HallucinationValidator()

# Streamlit App
def main():
    st.title("💪 Advanced Gym Workout Logger")
    st.markdown("Track your workouts with AI-powered insights and progress analysis")
    
    # Sidebar navigation
    st.sidebar.title("Navigation")
    page = st.sidebar.selectbox("Choose a page", 
                               ["Log Workout", "View History", "Progress Analysis", "Exercise Library", "RAG Insights"])
    
    if page == "Log Workout":
        log_workout_page()
    elif page == "View History":
        view_history_page()
    elif page == "Progress Analysis":
        progress_analysis_page()
    elif page == "Exercise Library":
        exercise_library_page()
    elif page == "RAG Insights":
        rag_insights_page()

def log_workout_page():
    st.header("📝 Log New Workout")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        with st.form("workout_form"):
            date = st.date_input("Date", datetime.now())
            exercise = st.text_input("Exercise Name", placeholder="e.g., Bench Press")
            
            col_sets, col_reps, col_weight = st.columns(3)
            with col_sets:
                sets = st.number_input("Sets", min_value=1, max_value=20, value=3)
            with col_reps:
                reps = st.number_input("Reps", min_value=1, max_value=100, value=10)
            with col_weight:
                weight = st.number_input("Weight (kg/lbs)", min_value=0.0, max_value=1000.0, value=0.0, step=0.5)
            
            duration = st.number_input("Duration (minutes)", min_value=0, max_value=300, value=0)
            notes = st.text_area("Notes (optional)", placeholder="How did it feel? Any observations?")
            
            submitted = st.form_submit_button("Log Workout", type="primary")
            
            if submitted:
                # Validate input
                is_valid, error_msg = validator.validate_workout_entry(exercise, sets, reps, weight)
                
                if is_valid:
                    # Save to database
                    conn = sqlite3.connect('gym_workouts.db')
                    cursor = conn.cursor()
                    cursor.execute('''
                        INSERT INTO workouts (date, exercise, sets, reps, weight, duration_minutes, notes)
                        VALUES (?, ?, ?, ?, ?, ?, ?)
                    ''', (date.isoformat(), exercise, sets, reps, weight, duration, notes))
                    conn.commit()
                    conn.close()
                    
                    st.success(f"✅ Workout logged successfully!")
                    st.balloons()
                else:
                    st.error(f"❌ Validation Error: {error_msg}")
    
    with col2:
        st.subheader("💡 Quick Tips")
        if exercise:
            exercise_info = workout_rag.get_exercise_info(exercise)
            if exercise_info:
                st.info(f"**{exercise}**")
                st.write(f"🎯 **Target:** {exercise_info['muscle_group']}")
                st.write(f"🏋️ **Equipment:** {exercise_info['equipment']}")
                st.write(f"📊 **Difficulty:** {exercise_info['difficulty']}")
                
                with st.expander("Form Tips"):
                    st.write(exercise_info['proper_form'])
            else:
                st.warning("Exercise not found in library. Consider adding it!")

def view_history_page():
    st.header("📊 Workout History")
    
    # Load data
    conn = sqlite3.connect('gym_workouts.db')
    df = pd.read_sql_query("SELECT * FROM workouts ORDER BY date DESC", conn)
    conn.close()
    
    if df.empty:
        st.info("No workout history found. Start logging your workouts!")
        return
    
    # Filters
    col1, col2, col3 = st.columns(3)
    with col1:
        date_filter = st.date_input("Filter by date (optional)")
    with col2:
        exercise_filter = st.selectbox("Filter by exercise", ["All"] + df['exercise'].unique().tolist())
    with col3:
        days_back = st.selectbox("Show last", [7, 14, 30, 90, 365], index=2)
    
    # Apply filters
    filtered_df = df.copy()
    
    if exercise_filter != "All":
        filtered_df = filtered_df[filtered_df['exercise'] == exercise_filter]
    
    # Date filter
    cutoff_date = datetime.now() - timedelta(days=days_back)
    filtered_df = filtered_df[pd.to_datetime(filtered_df['date']) >= cutoff_date]
    
    # Display data
    st.subheader(f"📋 Recent Workouts ({len(filtered_df)} entries)")
    
    if not filtered_df.empty:
        # Add calculated columns
        filtered_df['Volume'] = filtered_df['sets'] * filtered_df['reps'] * filtered_df['weight']
        display_df = filtered_df[['date', 'exercise', 'sets', 'reps', 'weight', 'Volume', 'notes']].copy()
        display_df['date'] = pd.to_datetime(display_df['date']).dt.strftime('%Y-%m-%d')
        
        st.dataframe(display_df, use_container_width=True)
        
        # Export option
        csv = display_df.to_csv(index=False)
        st.download_button(
            label="📥 Download as CSV",
            data=csv,
            file_name=f"workout_history_{datetime.now().strftime('%Y%m%d')}.csv",
            mime="text/csv"
        )
    else:
        st.info("No workouts match the selected filters.")

def progress_analysis_page():
    st.header("📈 Progress Analysis")
    
    # Load data
    conn = sqlite3.connect('gym_workouts.db')
    df = pd.read_sql_query("SELECT * FROM workouts ORDER BY date", conn)
    conn.close()
    
    if df.empty:
        st.info("No workout data available for analysis.")
        return
    
    # Convert date column
    df['date'] = pd.to_datetime(df['date'])
    df['Volume'] = df['sets'] * df['reps'] * df['weight']
    
    # Exercise selection
    exercises = df['exercise'].unique()
    selected_exercises = st.multiselect("Select exercises to analyze", exercises, default=exercises[:3])
    
    if not selected_exercises:
        st.warning("Please select at least one exercise.")
        return
    
    # Time period selection
    col1, col2 = st.columns(2)
    with col1:
        days_back = st.selectbox("Time period", [30, 60, 90, 180, 365], index=2)
    with col2:
        metric = st.selectbox("Metric to analyze", ["Volume", "Weight", "Reps"])
    
    cutoff_date = datetime.now() - timedelta(days=days_back)
    recent_df = df[df['date'] >= cutoff_date]
    
    # Create visualizations
    fig_volume = go.Figure()
    
    for exercise in selected_exercises:
        exercise_data = recent_df[recent_df['exercise'] == exercise].copy()
        if not exercise_data.empty:
            exercise_data = exercise_data.groupby('date').agg({
                'Volume': 'sum',
                'weight': 'max',
                'reps': 'sum'
            }).reset_index()
            
            y_data = exercise_data[metric]
            fig_volume.add_trace(go.Scatter(
                x=exercise_data['date'],
                y=y_data,
                name=exercise,
                mode='lines+markers',
                line=dict(width=3),
                marker=dict(size=8)
            ))
    
    fig_volume.update_layout(
        title=f"{metric} Progression Over Time",
        xaxis_title="Date",
        yaxis_title=metric,
        hovermode='x unified',
        template='plotly_white'
    )
    
    st.plotly_chart(fig_volume, use_container_width=True)
    
    # Weekly summary
    st.subheader("📅 Weekly Summary")
    weekly_data = recent_df.copy()
    weekly_data['week'] = weekly_data['date'].dt.to_period('W')
    weekly_summary = weekly_data.groupby('week').agg({
        'exercise': 'count',
        'Volume': 'sum',
        'duration_minutes': 'sum'
    }).rename(columns={'exercise': 'Total Workouts'})
    
    if not weekly_summary.empty:
        st.dataframe(weekly_summary.tail(8), use_container_width=True)

def exercise_library_page():
    st.header("📚 Exercise Library")
    
    conn = sqlite3.connect('gym_workouts.db')
    library_df = pd.read_sql_query("SELECT * FROM exercise_library", conn)
    conn.close()
    
    if library_df.empty:
        st.info("Exercise library is empty.")
        return
    
    # Search and filter
    col1, col2 = st.columns(2)
    with col1:
        search_term = st.text_input("🔍 Search exercises", placeholder="Enter exercise name...")
    with col2:
        muscle_filter = st.selectbox("Filter by muscle group", ["All"] + library_df['muscle_group'].unique().tolist())
    
    # Apply filters
    filtered_lib = library_df.copy()
    if search_term:
        filtered_lib = filtered_lib[filtered_lib['exercise_name'].str.contains(search_term, case=False)]
    if muscle_filter != "All":
        filtered_lib = filtered_lib[filtered_lib['muscle_group'] == muscle_filter]
    
    # Display exercises
    for _, exercise in filtered_lib.iterrows():
        with st.expander(f"🏋️ {exercise['exercise_name']} ({exercise['muscle_group']})"):
            col1, col2 = st.columns(2)
            with col1:
                st.write(f"**Equipment:** {exercise['equipment']}")
                st.write(f"**Difficulty:** {exercise['difficulty_level']}")
                st.write(f"**Description:** {exercise['description']}")
            with col2:
                st.write(f"**Proper Form:** {exercise['proper_form']}")
                st.write(f"**Common Mistakes:** {exercise['common_mistakes']}")
                st.write(f"**Progression Tips:** {exercise['progression_tips']}")

def rag_insights_page():
    st.header("🤖 AI-Powered Workout Insights")
    
    # Load workout data
    conn = sqlite3.connect('gym_workouts.db')
    df = pd.read_sql_query("SELECT * FROM workouts ORDER BY date DESC", conn)
    conn.close()
    
    if df.empty:
        st.info("No workout data available for analysis. Start logging workouts to get insights!")
        return
    
    # Perform RAG analysis
    with st.spinner("Analyzing your workout data..."):
        analysis = workout_rag.analyze_workout_pattern(df)
        validated_analysis = validator.validate_analysis_results(analysis)
    
    # Display key metrics
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Total Workouts", validated_analysis["total_workouts"])
    with col2:
        st.metric("Unique Exercises", validated_analysis["unique_exercises"])
    with col3:
        st.metric("Workouts/Week", validated_analysis["consistency_score"])
    with col4:
        st.metric("Muscle Groups", len(validated_analysis["muscle_groups_trained"]))
    
    # Muscle groups trained
    st.subheader("🎯 Muscle Groups Trained")
    if validated_analysis["muscle_groups_trained"]:
        muscle_groups = list(validated_analysis["muscle_groups_trained"])
        cols = st.columns(len(muscle_groups))
        for i, muscle_group in enumerate(muscle_groups):
            with cols[i]:
                st.info(f"💪 {muscle_group}")
    else:
        st.warning("No muscle group information available")
    
    # Progression analysis
    st.subheader("📊 Exercise Progression Analysis")
    if validated_analysis["progression_analysis"]:
        progress_data = []
        for exercise, prog in validated_analysis["progression_analysis"].items():
            progress_data.append({
                "Exercise": exercise,
                "Volume Change %": prog["volume_change_pct"],
                "Trend": prog["trend"]
            })
        
        progress_df = pd.DataFrame(progress_data)
        
        # Color code by trend
        def color_trend(val):
            if val == "increasing":
                return "background-color: #d4edda"
            elif val == "decreasing":
                return "background-color: #f8d7da"
            else:
                return "background-color: #fff3cd"
        
        st.dataframe(progress_df.style.applymap(color_trend, subset=['Trend']), use_container_width=True)
    
    # AI Recommendations
    st.subheader("🎯 AI Recommendations")
    if validated_analysis["recommendations"]:
        for rec in validated_analysis["recommendations"]:
            st.write(f"• {rec}")
    else:
        st.success("Great job! Keep up the consistent training.")
    
    # Workout heatmap
    st.subheader("🗓️ Workout Frequency Heatmap")
    df_copy = df.copy()
    df_copy['date'] = pd.to_datetime(df_copy['date'])
    workout_counts = df_copy.groupby(df_copy['date'].dt.date).size().reset_index()
    workout_counts.columns = ['date', 'workouts']
    
    # Create calendar heatmap
    if not workout_counts.empty:
        fig_heatmap = px.density_heatmap(
            workout_counts, 
            x=workout_counts['date'].apply(lambda x: x.strftime('%Y-%m-%d')),
            y=[1] * len(workout_counts),
            z='workouts',
            title="Daily Workout Frequency",
            color_continuous_scale="Viridis"
        )
        fig_heatmap.update_layout(showlegend=False, yaxis=dict(showticklabels=False))
        st.plotly_chart(fig_heatmap, use_container_width=True)

if __name__ == "__main__":
    main()

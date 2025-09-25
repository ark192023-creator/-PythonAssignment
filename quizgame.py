import streamlit as st
from datetime import datetime
import json

# Configure page
st.set_page_config(
    page_title="🧠 Quiz Master",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS for modern, engaging UI
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700&display=swap');
    
    .main {
        font-family: 'Poppins', sans-serif;
    }
    
    /* Clean white background with subtle gradient */
    .stApp {
        background: linear-gradient(135deg, #f8fafc 0%, #ffffff 50%, #f1f5f9 100%);
        min-height: 100vh;
    }
    
    /* Main container styling */
    .main-container {
        background: rgba(255, 255, 255, 0.95);
        border-radius: 20px;
        padding: 30px;
        backdrop-filter: blur(10px);
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.08);
        margin: 20px 0;
        color: #374151;
        border: 1px solid rgba(0, 0, 0, 0.05);
    }
    
    /* Header styling */
    .header {
        text-align: center;
        margin-bottom: 30px;
        animation: fadeInDown 1s ease-out;
    }
    
    .header h1 {
        color: #7c3aed;
        font-size: 3rem;
        font-weight: 700;
        margin-bottom: 10px;
        text-shadow: 2px 2px 4px rgba(124, 58, 237, 0.1);
    }
    
    .header p {
        color: #64748b;
        font-size: 1.2rem;
        font-weight: 400;
    }
    
    /* Question container */
    .question-container {
        background: linear-gradient(135deg, #ffffff 0%, #f8fafc 100%);
        border-radius: 20px;
        padding: 30px;
        margin: 25px 0;
        border: 1px solid rgba(124, 58, 237, 0.1);
        box-shadow: 0 8px 25px rgba(0, 0, 0, 0.06);
        animation: slideInUp 0.8s ease-out;
    }
    
    .question-title {
        font-size: 1.4rem;
        font-weight: 600;
        color: #1e40af;
        margin-bottom: 20px;
        display: flex;
        align-items: center;
        gap: 10px;
    }
    
    .question-number {
        background: linear-gradient(135deg, #7c3aed 0%, #6d28d9 100%);
        color: white;
        padding: 8px 16px;
        border-radius: 50%;
        font-size: 1rem;
        font-weight: 700;
        min-width: 40px;
        display: inline-flex;
        align-items: center;
        justify-content: center;
    }
    
    /* Progress bar */
    .progress-container {
        margin: 20px 0;
        animation: slideInLeft 1s ease-out 0.3s both;
    }
    
    .progress-bar {
        width: 100%;
        height: 12px;
        background: #e2e8f0;
        border-radius: 10px;
        overflow: hidden;
        position: relative;
    }
    
    .progress-fill {
        height: 100%;
        background: linear-gradient(135deg, #7c3aed 0%, #6d28d9 100%);
        border-radius: 10px;
        transition: width 0.5s ease-in-out;
        position: relative;
    }
    
    .progress-fill::after {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background: linear-gradient(90deg, transparent, rgba(255,255,255,0.3), transparent);
        animation: shimmer 2s infinite;
    }
    
    @keyframes shimmer {
        0% { transform: translateX(-100%); }
        100% { transform: translateX(100%); }
    }
    
    .progress-text {
        text-align: center;
        margin-top: 8px;
        font-weight: 600;
        color: #7c3aed;
        font-size: 0.9rem;
    }
    
    /* Score display */
    .score-container {
        background: linear-gradient(135deg, #f0fdf4 0%, #dcfce7 100%);
        border-radius: 15px;
        padding: 20px;
        margin: 20px 0;
        border: 1px solid rgba(16, 185, 129, 0.2);
        text-align: center;
        animation: bounceIn 1s ease-out;
    }
    
    .score-value {
        font-size: 2.5rem;
        font-weight: 700;
        color: #059669;
        margin-bottom: 5px;
    }
    
    .score-label {
        color: #047857;
        font-weight: 500;
        font-size: 1.1rem;
    }
    
    /* Results container */
    .results-container {
        background: rgba(255, 255, 255, 0.98);
        border-radius: 20px;
        padding: 30px;
        margin: 25px 0;
        border: 1px solid rgba(124, 58, 237, 0.1);
        box-shadow: 0 8px 25px rgba(0, 0, 0, 0.06);
        animation: zoomIn 1s ease-out;
        text-align: center;
    }
    
    .results-title {
        font-size: 2rem;
        font-weight: 700;
        color: #7c3aed;
        margin-bottom: 20px;
    }
    
    .final-score {
        font-size: 3rem;
        font-weight: 800;
        margin: 20px 0;
        animation: numberCount 2s ease-out;
    }
    
    .performance-excellent {
        color: #059669;
    }
    
    .performance-good {
        color: #0891b2;
    }
    
    .performance-average {
        color: #d97706;
    }
    
    .performance-needs-improvement {
        color: #dc2626;
    }
    
    .performance-message {
        font-size: 1.3rem;
        font-weight: 600;
        margin: 20px 0;
        padding: 15px;
        border-radius: 10px;
        animation: slideInUp 1s ease-out 0.5s both;
    }
    
    .excellent {
        background: linear-gradient(135deg, #f0fdf4 0%, #dcfce7 100%);
        color: #065f46;
        border: 1px solid rgba(16, 185, 129, 0.2);
    }
    
    .good {
        background: linear-gradient(135deg, #f0f9ff 0%, #e0f2fe 100%);
        color: #0c4a6e;
        border: 1px solid rgba(6, 182, 212, 0.2);
    }
    
    .average {
        background: linear-gradient(135deg, #fffbeb 0%, #fef3c7 100%);
        color: #92400e;
        border: 1px solid rgba(217, 119, 6, 0.2);
    }
    
    .needs-improvement {
        background: linear-gradient(135deg, #fef2f2 0%, #fecaca 100%);
        color: #991b1b;
        border: 1px solid rgba(220, 38, 38, 0.2);
    }
    
    /* Navigation buttons */
    .nav-container {
        display: flex;
        justify-content: space-between;
        margin: 30px 0;
        gap: 20px;
    }
    
    /* Radio button styling */
    .stRadio > div {
        background: rgba(255, 255, 255, 0.8);
        padding: 15px;
        border-radius: 12px;
        border: 1px solid rgba(124, 58, 237, 0.1);
        margin: 8px 0;
        transition: all 0.3s ease;
    }
    
    .stRadio > div:hover {
        background: rgba(124, 58, 237, 0.05);
        border-color: rgba(124, 58, 237, 0.2);
        transform: translateY(-2px);
        box-shadow: 0 4px 15px rgba(124, 58, 237, 0.1);
    }
    
    /* Button styling */
    .stButton button {
        background: linear-gradient(135deg, #7c3aed 0%, #6d28d9 100%);
        color: white !important;
        border: none;
        border-radius: 12px;
        padding: 12px 24px;
        font-weight: 600;
        font-size: 1rem;
        transition: all 0.3s ease;
        width: 100%;
    }
    
    .stButton button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(124, 58, 237, 0.4);
        background: linear-gradient(135deg, #6d28d9 0%, #5b21b6 100%);
    }
    
    /* Answer review styling */
    .answer-review {
        margin: 15px 0;
        padding: 15px;
        border-radius: 12px;
        animation: slideInUp 0.5s ease-out;
    }
    
    .correct-answer {
        background: linear-gradient(135deg, #f0fdf4 0%, #dcfce7 100%);
        border-left: 4px solid #10b981;
        color: #065f46;
    }
    
    .incorrect-answer {
        background: linear-gradient(135deg, #fef2f2 0%, #fecaca 100%);
        border-left: 4px solid #ef4444;
        color: #991b1b;
    }
    
    /* Animations */
    @keyframes fadeInDown {
        from { opacity: 0; transform: translateY(-30px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    @keyframes slideInUp {
        from { opacity: 0; transform: translateY(50px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    @keyframes slideInLeft {
        from { opacity: 0; transform: translateX(-50px); }
        to { opacity: 1; transform: translateX(0); }
    }
    
    @keyframes zoomIn {
        from { opacity: 0; transform: scale(0.8); }
        to { opacity: 1; transform: scale(1); }
    }
    
    @keyframes bounceIn {
        0% { opacity: 0; transform: scale(0.3); }
        50% { opacity: 1; transform: scale(1.05); }
        70% { transform: scale(0.9); }
        100% { opacity: 1; transform: scale(1); }
    }
    
    @keyframes numberCount {
        from { transform: scale(0.8); opacity: 0; }
        to { transform: scale(1); opacity: 1; }
    }
    
    /* Hide streamlit elements */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    .stCodeBlock, .stCode, pre, code {display: none !important;}
</style>
""", unsafe_allow_html=True)

# Quiz questions database (hardcoded)
QUIZ_QUESTIONS = [
    {
        "id": 1,
        "question": "What is the capital of France?",
        "options": ["London", "Berlin", "Paris", "Madrid"],
        "correct": 2,
        "explanation": "Paris is the capital and most populous city of France."
    },
    {
        "id": 2,
        "question": "Which planet is known as the Red Planet?",
        "options": ["Venus", "Mars", "Jupiter", "Saturn"],
        "correct": 1,
        "explanation": "Mars is called the Red Planet due to iron oxide (rust) on its surface."
    },
    {
        "id": 3,
        "question": "What is the largest ocean on Earth?",
        "options": ["Atlantic", "Indian", "Arctic", "Pacific"],
        "correct": 3,
        "explanation": "The Pacific Ocean is the largest and deepest ocean on Earth."
    },
    {
        "id": 4,
        "question": "Who painted the Mona Lisa?",
        "options": ["Vincent van Gogh", "Pablo Picasso", "Leonardo da Vinci", "Michelangelo"],
        "correct": 2,
        "explanation": "Leonardo da Vinci painted the Mona Lisa between 1503-1519."
    },
    {
        "id": 5,
        "question": "What is the smallest unit of matter?",
        "options": ["Molecule", "Atom", "Proton", "Electron"],
        "correct": 1,
        "explanation": "An atom is the smallest unit of matter that retains the properties of an element."
    },
    {
        "id": 6,
        "question": "In which year did World War II end?",
        "options": ["1944", "1945", "1946", "1947"],
        "correct": 1,
        "explanation": "World War II ended in 1945 with the surrender of Japan in September."
    },
    {
        "id": 7,
        "question": "What is the chemical symbol for gold?",
        "options": ["Go", "Gd", "Au", "Ag"],
        "correct": 2,
        "explanation": "Au is the chemical symbol for gold, from the Latin word 'aurum'."
    },
    {
        "id": 8,
        "question": "Which is the longest river in the world?",
        "options": ["Amazon", "Nile", "Yangtze", "Mississippi"],
        "correct": 1,
        "explanation": "The Nile River is generally considered the longest river in the world at 6,650 km."
    },
    {
        "id": 9,
        "question": "What is the speed of light in vacuum?",
        "options": ["299,792,458 m/s", "300,000,000 m/s", "299,800,000 m/s", "298,000,000 m/s"],
        "correct": 0,
        "explanation": "The speed of light in vacuum is exactly 299,792,458 meters per second."
    },
    {
        "id": 10,
        "question": "Who developed the theory of relativity?",
        "options": ["Isaac Newton", "Albert Einstein", "Galileo Galilei", "Stephen Hawking"],
        "correct": 1,
        "explanation": "Albert Einstein developed both the special and general theories of relativity."
    }
]

# Initialize session state
def initialize_session_state():
    if 'quiz_started' not in st.session_state:
        st.session_state.quiz_started = False
    if 'current_question' not in st.session_state:
        st.session_state.current_question = 0
    if 'score' not in st.session_state:
        st.session_state.score = 0
    if 'user_answers' not in st.session_state:
        st.session_state.user_answers = {}
    if 'quiz_completed' not in st.session_state:
        st.session_state.quiz_completed = False
    if 'show_results' not in st.session_state:
        st.session_state.show_results = False

def reset_quiz():
    """Reset all quiz-related session state"""
    st.session_state.quiz_started = False
    st.session_state.current_question = 0
    st.session_state.score = 0
    st.session_state.user_answers = {}
    st.session_state.quiz_completed = False
    st.session_state.show_results = False

def get_performance_message(score, total):
    """Get performance message based on score"""
    percentage = (score / total) * 100
    
    if percentage >= 90:
        return {
            "class": "excellent",
            "message": "🏆 Outstanding! You're a Quiz Master!",
            "description": "Excellent knowledge and understanding!"
        }
    elif percentage >= 70:
        return {
            "class": "good",
            "message": "🌟 Great Job! Well done!",
            "description": "Good performance with room for improvement."
        }
    elif percentage >= 50:
        return {
            "class": "average",
            "message": "👍 Not bad! Keep learning!",
            "description": "Average performance. Consider studying more."
        }
    else:
        return {
            "class": "needs-improvement",
            "message": "📚 Keep studying! You can do better!",
            "description": "More practice needed to improve your score."
        }

def display_progress_bar():
    """Display progress bar"""
    progress = (st.session_state.current_question) / len(QUIZ_QUESTIONS)
    
    st.markdown(f"""
    <div class="progress-container">
        <div class="progress-bar">
            <div class="progress-fill" style="width: {progress * 100}%"></div>
        </div>
        <div class="progress-text">
            Question {st.session_state.current_question} of {len(QUIZ_QUESTIONS)}
        </div>
    </div>
    """, unsafe_allow_html=True)

def display_current_score():
    """Display current score"""
    st.markdown(f"""
    <div class="score-container">
        <div class="score-value">{st.session_state.score}</div>
        <div class="score-label">Current Score</div>
    </div>
    """, unsafe_allow_html=True)

# Initialize session state
initialize_session_state()

# Main app layout
st.markdown('<div class="main-container">', unsafe_allow_html=True)

# Header
st.markdown("""
<div class="header">
    <h1>🧠 Quiz Master</h1>
    <p>Test your knowledge with our interactive quiz!</p>
</div>
""", unsafe_allow_html=True)

# Quiz Logic
if not st.session_state.quiz_started:
    # Welcome screen
    st.markdown("### 🚀 Ready to start?")
    st.markdown("**Quiz Rules:**")
    st.markdown("- 📝 10 multiple-choice questions")
    st.markdown("- ⏰ Take your time to think")
    st.markdown("- 🏆 Get scored based on correct answers")
    st.markdown("- 📊 See detailed results at the end")
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("🎯 Start Quiz", use_container_width=True):
            st.session_state.quiz_started = True
            st.rerun()

elif not st.session_state.quiz_completed:
    # Display progress and score
    col1, col2 = st.columns([3, 1])
    with col1:
        display_progress_bar()
    with col2:
        display_current_score()
    
    # Current question
    current_q = QUIZ_QUESTIONS[st.session_state.current_question]
    
    st.markdown(f"""
    <div class="question-container">
        <div class="question-title">
            <span class="question-number">{st.session_state.current_question + 1}</span>
            {current_q['question']}
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Answer options
    answer_key = f"question_{current_q['id']}"
    selected_answer = st.radio(
        "Choose your answer:",
        options=range(len(current_q['options'])),
        format_func=lambda x: current_q['options'][x],
        key=answer_key,
        index=None
    )
    
    # Navigation buttons
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col1:
        if st.session_state.current_question > 0:
            if st.button("⬅️ Previous", use_container_width=True):
                st.session_state.current_question -= 1
                st.rerun()
    
    with col3:
        if selected_answer is not None:
            if st.session_state.current_question < len(QUIZ_QUESTIONS) - 1:
                if st.button("Next ➡️", use_container_width=True):
                    # Save answer and update score
                    st.session_state.user_answers[current_q['id']] = selected_answer
                    if selected_answer == current_q['correct']:
                        st.session_state.score += 1
                    
                    st.session_state.current_question += 1
                    st.rerun()
            else:
                if st.button("🏁 Finish Quiz", use_container_width=True):
                    # Save final answer and complete quiz
                    st.session_state.user_answers[current_q['id']] = selected_answer
                    if selected_answer == current_q['correct']:
                        st.session_state.score += 1
                    
                    st.session_state.quiz_completed = True
                    st.rerun()

else:
    # Results screen
    total_questions = len(QUIZ_QUESTIONS)
    percentage = (st.session_state.score / total_questions) * 100
    performance = get_performance_message(st.session_state.score, total_questions)
    
    st.markdown(f"""
    <div class="results-container">
        <div class="results-title">🎉 Quiz Completed!</div>
        <div class="final-score performance-{performance['class'].replace('-', '_')}">{st.session_state.score}/{total_questions}</div>
        <div style="font-size: 1.5rem; color: #64748b; margin: 10px 0;">
            {percentage:.1f}% Correct
        </div>
        <div class="performance-message {performance['class']}">
            <div>{performance['message']}</div>
            <div style="font-size: 1rem; margin-top: 10px;">{performance['description']}</div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Show/Hide detailed results
    if st.button("📋 Show Detailed Results" if not st.session_state.show_results else "📋 Hide Detailed Results"):
        st.session_state.show_results = not st.session_state.show_results
        st.rerun()
    
    # Detailed results
    if st.session_state.show_results:
        st.markdown("### 📊 Detailed Results")
        
        for i, question in enumerate(QUIZ_QUESTIONS):
            user_answer = st.session_state.user_answers.get(question['id'])
            correct_answer = question['correct']
            is_correct = user_answer == correct_answer
            
            # Question review
            st.markdown(f"**Question {i+1}:** {question['question']}")
            
            if is_correct:
                st.markdown(f"""
                <div class="answer-review correct-answer">
                    ✅ <strong>Correct!</strong> Your answer: {question['options'][user_answer]}<br>
                    💡 {question['explanation']}
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown(f"""
                <div class="answer-review incorrect-answer">
                    ❌ <strong>Incorrect.</strong> Your answer: {question['options'][user_answer] if user_answer is not None else 'No answer'}<br>
                    ✅ Correct answer: {question['options'][correct_answer]}<br>
                    💡 {question['explanation']}
                </div>
                """, unsafe_allow_html=True)
    
    # Action buttons
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🔄 Retake Quiz", use_container_width=True):
            reset_quiz()
            st.rerun()
    
    with col2:
        if st.button("🏠 Start Over", use_container_width=True):
            reset_quiz()
            st.rerun()

st.markdown('</div>', unsafe_allow_html=True)

# Display quiz stats in sidebar if quiz is active
if st.session_state.quiz_started:
    with st.sidebar:
        st.markdown("### 📊 Quiz Statistics")
        st.metric("Current Score", st.session_state.score)
        st.metric("Questions Answered", st.session_state.current_question)
        st.metric("Questions Remaining", len(QUIZ_QUESTIONS) - st.session_state.current_question)
        
        if st.session_state.quiz_completed:
            st.metric("Final Percentage", f"{(st.session_state.score/len(QUIZ_QUESTIONS)*100):.1f}%")

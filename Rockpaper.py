import streamlit as st
import random
import time
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import json
from typing import Dict, List, Tuple, Optional
import numpy as np
from collections import Counter, defaultdict

# Configure Streamlit page
st.set_page_config(
    page_title="Ultimate Rock Paper Scissors",
    page_icon="🎮",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better UI/UX
st.markdown("""
<style>
    .main-header {
        text-align: center;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 15px;
        margin-bottom: 2rem;
        color: white;
        box-shadow: 0 8px 25px rgba(0,0,0,0.2);
    }
    
    .game-title {
        font-size: 3rem;
        font-weight: bold;
        margin-bottom: 1rem;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
        background: linear-gradient(45deg, #ff6b6b, #4ecdc4, #45b7d1);
        background-size: 400% 400%;
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        animation: gradientShift 3s ease-in-out infinite;
    }
    
    @keyframes gradientShift {
        0%, 100% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
    }
    
    .choice-display {
        font-size: 8rem;
        text-align: center;
        padding: 2rem;
        background: rgba(255, 255, 255, 0.1);
        border-radius: 20px;
        margin: 1rem 0;
        backdrop-filter: blur(10px);
        border: 2px solid rgba(255, 255, 255, 0.2);
        transition: all 0.3s ease;
    }
    
    .winner-glow {
        animation: glow 1s ease-in-out infinite alternate;
        border-color: #ffd700 !important;
        box-shadow: 0 0 30px rgba(255, 215, 0, 0.6) !important;
    }
    
    @keyframes glow {
        from { box-shadow: 0 0 10px #ffd700; }
        to { box-shadow: 0 0 30px #ffd700; }
    }
    
    .thinking-animation {
        animation: shake 0.5s ease-in-out infinite;
    }
    
    @keyframes shake {
        0%, 100% { transform: translateX(0); }
        25% { transform: translateX(-5px); }
        75% { transform: translateX(5px); }
    }
    
    .result-win { 
        color: #4CAF50; 
        font-size: 2.5rem; 
        font-weight: bold; 
        text-align: center;
        animation: celebration 0.8s ease-out;
    }
    
    .result-lose { 
        color: #f44336; 
        font-size: 2.5rem; 
        font-weight: bold; 
        text-align: center;
        animation: shake 0.8s ease-out;
    }
    
    .result-draw { 
        color: #ff9800; 
        font-size: 2.5rem; 
        font-weight: bold; 
        text-align: center;
        animation: bounce 0.8s ease-out;
    }
    
    @keyframes celebration {
        0%, 100% { transform: scale(1); }
        25% { transform: scale(1.1) rotate(-5deg); }
        75% { transform: scale(1.1) rotate(5deg); }
    }
    
    @keyframes bounce {
        0%, 100% { transform: translateY(0); }
        50% { transform: translateY(-20px); }
    }
    
    .insight-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1.5rem;
        border-radius: 15px;
        margin: 1rem 0;
        color: white;
        box-shadow: 0 8px 25px rgba(0,0,0,0.2);
        transition: transform 0.3s ease;
    }
    
    .insight-card:hover {
        transform: translateY(-5px);
    }
    
    .score-card {
        background: linear-gradient(135deg, #4CAF50 0%, #45a049 100%);
        padding: 1.5rem;
        border-radius: 15px;
        text-align: center;
        color: white;
        box-shadow: 0 8px 25px rgba(0,0,0,0.2);
        margin: 1rem 0;
    }
    
    .ai-score-card {
        background: linear-gradient(135deg, #f44336 0%, #d32f2f 100%);
        padding: 1.5rem;
        border-radius: 15px;
        text-align: center;
        color: white;
        box-shadow: 0 8px 25px rgba(0,0,0,0.2);
        margin: 1rem 0;
    }
    
    .stat-metric {
        font-size: 3rem;
        font-weight: bold;
        color: white;
        text-align: center;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
    }
    
    .error-alert {
        background-color: #ffebee;
        border: 2px solid #f44336;
        border-radius: 10px;
        padding: 1rem;
        color: #c62828;
        margin: 1rem 0;
        animation: fadeIn 0.5s ease;
    }
    
    .success-alert {
        background-color: #e8f5e8;
        border: 2px solid #4CAF50;
        border-radius: 10px;
        padding: 1rem;
        color: #2e7d32;
        margin: 1rem 0;
        animation: fadeIn 0.5s ease;
    }
    
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(-10px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    .game-button {
        background: linear-gradient(45deg, #667eea 0%, #764ba2 100%);
        border: none;
        border-radius: 15px;
        color: white;
        font-size: 1.2rem;
        font-weight: bold;
        padding: 1rem 2rem;
        margin: 0.5rem;
        cursor: pointer;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(0,0,0,0.2);
    }
    
    .game-button:hover {
        transform: translateY(-3px);
        box-shadow: 0 8px 25px rgba(0,0,0,0.3);
    }
    
    .vs-section {
        text-align: center;
        font-size: 4rem;
        font-weight: bold;
        color: #667eea;
        animation: pulse 2s infinite;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
    }
    
    @keyframes pulse {
        0%, 100% { transform: scale(1); opacity: 0.8; }
        50% { transform: scale(1.1); opacity: 1; }
    }
</style>
""", unsafe_allow_html=True)

class RPSGameRAG:
    """Advanced Rock Paper Scissors with RAG analysis and fallback mechanisms"""
    
    def __init__(self):
        self.choices = ['rock', 'paper', 'scissors']
        self.choice_emojis = {'rock': '🗿', 'paper': '📄', 'scissors': '✂️'}
        self.thinking_emojis = ['🤔', '💭', '🎯', '🧠', '⚡', '🎲']
        
        # Game knowledge base for RAG
        self.strategy_knowledge = {
            'beginner_patterns': {
                'rock_tendency': 'New players often favor rock (40% frequency)',
                'paper_counter': 'Counter rock-heavy players with paper',
                'pattern_break': 'Introduce randomness after 3 consecutive moves'
            },
            'intermediate_patterns': {
                'alternating': 'Some players alternate between 2-3 moves',
                'anti_pattern': 'Avoid your own patterns to stay unpredictable',
                'frequency_analysis': 'Track opponent frequency and counter most used'
            },
            'advanced_strategies': {
                'psychological': 'Mirror opponent occasionally to create uncertainty',
                'meta_gaming': 'Predict opponent trying to counter your pattern',
                'adaptive': 'Change strategy every 5-7 games'
            }
        }
        
        # Initialize game state
        if 'game_state' not in st.session_state:
            self.reset_game_state()
    
    def reset_game_state(self):
        """Initialize or reset game state with fallback values"""
        st.session_state.game_state = {
            'player_score': 0,
            'computer_score': 0,
            'total_games': 0,
            'game_history': [],
            'current_streak': 0,
            'best_streak': 0,
            'player_choice': None,
            'computer_choice': None,
            'last_result': None,
            'pattern_analysis': {},
            'strategy_insights': [],
            'error_count': 0,
            'fallback_used': False,
            'ai_difficulty': 'adaptive'
        }
    
    def generate_computer_choice_with_fallback(self) -> str:
        """Generate computer choice with multiple fallback mechanisms"""
        try:
            # Primary strategy: Advanced AI
            choice = self._generate_strategic_choice()
            
            # Validate choice
            if choice not in self.choices:
                raise ValueError(f"Invalid choice generated: {choice}")
                
            return choice
            
        except Exception as e:
            st.session_state.game_state['error_count'] += 1
            st.warning(f"Strategy engine error: {str(e)}. Using fallback mechanism.")
            return self._fallback_choice_generator()
    
    def _generate_strategic_choice(self) -> str:
        """Advanced strategic choice generation with RAG analysis"""
        game_history = st.session_state.game_state['game_history']
        
        if len(game_history) < 3:
            # Early game: Use weighted random based on common patterns
            return self._weighted_early_game_choice()
        
        # Analyze player patterns
        player_moves = [game['player_choice'] for game in game_history[-10:]]
        pattern_analysis = self._analyze_player_patterns(player_moves)
        
        # Generate counter-strategy
        predicted_move = self._predict_next_move(pattern_analysis)
        counter_move = self._get_counter_move(predicted_move)
        
        # Add strategic randomness (25% chance for unpredictability)
        if random.random() < 0.25:
            return self._adaptive_random_choice(game_history)
        
        return counter_move
    
    def _analyze_player_patterns(self, moves: List[str]) -> Dict:
        """RAG-based pattern analysis"""
        if not moves:
            return {'type': 'insufficient_data', 'confidence': 0}
        
        # Frequency analysis
        frequency = Counter(moves)
        most_frequent = frequency.most_common(1)[0][0] if frequency else random.choice(self.choices)
        
        # Sequential pattern detection
        sequences = self._detect_sequences(moves)
        
        # Alternating pattern check
        alternating_score = self._check_alternating_pattern(moves)
        
        # Streak analysis
        current_streak = self._analyze_current_streak(moves)
        
        return {
            'type': 'comprehensive',
            'most_frequent': most_frequent,
            'frequency_confidence': frequency[most_frequent] / len(moves) if frequency else 0,
            'sequences': sequences,
            'alternating_score': alternating_score,
            'current_streak': current_streak,
            'confidence': self._calculate_pattern_confidence(frequency, sequences, alternating_score)
        }
    
    def _detect_sequences(self, moves: List[str]) -> Dict:
        """Detect repeating sequences in player moves"""
        sequences = {}
        for length in range(2, min(5, len(moves))):
            for i in range(len(moves) - length + 1):
                seq = tuple(moves[i:i+length])
                sequences[seq] = sequences.get(seq, 0) + 1
        
        # Find most common sequence
        if sequences:
            most_common_seq = max(sequences.items(), key=lambda x: x[1])
            return {'most_common': most_common_seq[0], 'frequency': most_common_seq[1]}
        
        return {'most_common': None, 'frequency': 0}
    
    def _check_alternating_pattern(self, moves: List[str]) -> float:
        """Check for alternating patterns"""
        if len(moves) < 3:
            return 0
        
        alternating_count = 0
        for i in range(len(moves) - 1):
            if moves[i] != moves[i + 1]:
                alternating_count += 1
        
        return alternating_count / (len(moves) - 1)
    
    def _analyze_current_streak(self, moves: List[str]) -> Dict:
        """Analyze current streak of same moves"""
        if not moves:
            return {'move': None, 'length': 0}
        
        current_move = moves[-1]
        streak_length = 1
        
        for i in range(len(moves) - 2, -1, -1):
            if moves[i] == current_move:
                streak_length += 1
            else:
                break
        
        return {'move': current_move, 'length': streak_length}
    
    def _calculate_pattern_confidence(self, frequency: Counter, sequences: Dict, alternating_score: float) -> float:
        """Calculate confidence in pattern analysis"""
        total_moves = sum(frequency.values()) if frequency else 0
        if total_moves == 0:
            return 0
        
        # Frequency confidence
        max_freq = max(frequency.values()) if frequency else 0
        freq_confidence = max_freq / total_moves if total_moves > 0 else 0
        
        # Sequence confidence
        seq_confidence = sequences.get('frequency', 0) / max(1, total_moves - 1) if sequences else 0
        
        # Alternating confidence
        alt_confidence = abs(alternating_score - 0.5) * 2  # Higher if clearly alternating or not
        
        return (freq_confidence + seq_confidence + alt_confidence) / 3
    
    def _predict_next_move(self, analysis: Dict) -> str:
        """Predict player's next move based on analysis"""
        if analysis['confidence'] < 0.3:
            return random.choice(self.choices)
        
        # Check current streak
        current_streak = analysis.get('current_streak', {})
        if current_streak.get('length', 0) >= 3:
            # Player might break streak
            alternatives = [choice for choice in self.choices if choice != current_streak['move']]
            return random.choice(alternatives) if alternatives else random.choice(self.choices)
        
        # Check for sequences
        sequences = analysis.get('sequences', {})
        if sequences.get('most_common') and sequences.get('frequency', 0) >= 2:
            seq = sequences['most_common']
            if len(seq) >= 2:
                return seq[1]  # Next move in sequence
        
        # Use most frequent as fallback
        return analysis.get('most_frequent', random.choice(self.choices))
    
    def _get_counter_move(self, predicted_move: str) -> str:
        """Get the move that beats the predicted move"""
        counters = {
            'rock': 'paper',
            'paper': 'scissors',
            'scissors': 'rock'
        }
        return counters.get(predicted_move, random.choice(self.choices))
    
    def _weighted_early_game_choice(self) -> str:
        """Weighted choice for early game based on common patterns"""
        # Most players start with rock, so paper is often good
        weights = [0.3, 0.4, 0.3]  # rock, paper, scissors
        return random.choices(self.choices, weights=weights)[0]
    
    def _adaptive_random_choice(self, game_history: List[Dict]) -> str:
        """Adaptive random choice based on game history"""
        if not game_history:
            return random.choice(self.choices)
        
        # Analyze computer's own patterns to avoid predictability
        computer_moves = [game['computer_choice'] for game in game_history[-5:]]
        computer_freq = Counter(computer_moves)
        
        # Choose less frequently used move
        sorted_choices = sorted(self.choices, key=lambda x: computer_freq.get(x, 0))
        
        # Weight toward less used choices
        weights = [3, 2, 1]
        return random.choices(sorted_choices, weights=weights)[0]
    
    def _fallback_choice_generator(self) -> str:
        """Ultimate fallback: pure random choice"""
        st.session_state.game_state['fallback_used'] = True
        return random.choice(self.choices)
    
    def play_round(self, player_choice: str) -> Dict:
        """Play a round with comprehensive error handling"""
        try:
            # Validate player choice
            if player_choice not in self.choices:
                raise ValueError(f"Invalid player choice: {player_choice}")
            
            # Generate computer choice
            computer_choice = self.generate_computer_choice_with_fallback()
            
            # Determine winner
            result = self._determine_winner(player_choice, computer_choice)
            
            # Update game state
            self._update_game_state(player_choice, computer_choice, result)
            
            return {
                'player_choice': player_choice,
                'computer_choice': computer_choice,
                'result': result,
                'success': True,
                'error': None
            }
            
        except Exception as e:
            st.error(f"Game error: {str(e)}")
            return {
                'player_choice': player_choice,
                'computer_choice': random.choice(self.choices),
                'result': 'error',
                'success': False,
                'error': str(e)
            }
    
    def _determine_winner(self, player_choice: str, computer_choice: str) -> str:
        """Determine the winner of the round"""
        if player_choice == computer_choice:
            return 'draw'
        
        win_conditions = {
            ('rock', 'scissors'): 'win',
            ('paper', 'rock'): 'win',
            ('scissors', 'paper'): 'win'
        }
        
        return 'win' if (player_choice, computer_choice) in win_conditions else 'lose'
    
    def _update_game_state(self, player_choice: str, computer_choice: str, result: str):
        """Update game state after a round"""
        game_state = st.session_state.game_state
        
        # Update scores
        if result == 'win':
            game_state['player_score'] += 1
            game_state['current_streak'] += 1
            game_state['best_streak'] = max(game_state['best_streak'], game_state['current_streak'])
        elif result == 'lose':
            game_state['computer_score'] += 1
            game_state['current_streak'] = 0
        # draw doesn't change scores but resets streak to 0
        elif result == 'draw':
            game_state['current_streak'] = 0
        
        game_state['total_games'] += 1
        
        # Update history
        game_state['game_history'].append({
            'player_choice': player_choice,
            'computer_choice': computer_choice,
            'result': result,
            'timestamp': datetime.now().isoformat()
        })
        
        # Keep only last 50 games for performance
        if len(game_state['game_history']) > 50:
            game_state['game_history'] = game_state['game_history'][-50:]
        
        # Update current choices
        game_state['player_choice'] = player_choice
        game_state['computer_choice'] = computer_choice
        game_state['last_result'] = result
    
    def generate_insights(self) -> List[str]:
        """Generate RAG-based insights about player behavior"""
        game_history = st.session_state.game_state['game_history']
        
        if len(game_history) < 5:
            return ["🎮 Play more games to unlock advanced AI insights!"]
        
        insights = []
        
        # Pattern insights
        player_moves = [game['player_choice'] for game in game_history[-10:]]
        pattern_analysis = self._analyze_player_patterns(player_moves)
        
        if pattern_analysis['confidence'] > 0.6:
            most_freq = pattern_analysis.get('most_frequent', 'unknown')
            freq_pct = pattern_analysis['frequency_confidence'] * 100
            insights.append(f"🎯 Pattern Detected: You favor '{most_freq}' ({freq_pct:.0f}% of the time)")
        
        # Streak analysis
        current_streak = st.session_state.game_state['current_streak']
        if current_streak >= 3:
            insights.append(f"🔥 Hot Streak: {current_streak} wins in a row! The AI is adapting to counter you.")
        
        # Win rate analysis
        wins = sum(1 for game in game_history if game['result'] == 'win')
        win_rate = wins / len(game_history)
        
        if win_rate > 0.6:
            insights.append("🏆 Excellent Performance: You're outplaying the AI! It's learning your patterns.")
        elif win_rate < 0.4:
            insights.append("📈 Room for Improvement: Try mixing up your strategy to confuse the AI.")
        else:
            insights.append("⚖️ Balanced Match: You and the AI are evenly matched!")
        
        # Strategy recommendations
        if pattern_analysis.get('alternating_score', 0) > 0.7:
            insights.append("🔄 Alternating Pattern: You tend to alternate moves. Try breaking this pattern!")
        
        # Recent performance
        recent_games = game_history[-5:] if len(game_history) >= 5 else game_history
        recent_wins = sum(1 for game in recent_games if game['result'] == 'win')
        
        if len(recent_games) == 5:
            if recent_wins >= 4:
                insights.append("🚀 Recent Dominance: 4+ wins in last 5 games! The AI is studying your moves.")
            elif recent_wins <= 1:
                insights.append("🛡️ AI Adaptation: The computer has adapted to your strategy. Time to change tactics!")
        
        return insights[:4]  # Limit to 4 insights for UI
    
    def get_strategy_recommendation(self) -> str:
        """Get strategic recommendation based on RAG knowledge"""
        game_history = st.session_state.game_state['game_history']
        
        if len(game_history) < 3:
            return "🎯 Early Game: Try different moves to test the AI's initial strategy!"
        
        player_moves = [game['player_choice'] for game in game_history[-5:]]
        move_counter = Counter(player_moves)
        
        # Strategy based on pattern
        if len(set(player_moves)) == 1:
            return "⚠️ You're using the same move repeatedly. The AI has noticed - try mixing it up!"
        elif len(game_history) < 10:
            return "🎲 Mix your moves randomly to avoid predictable patterns in early games."
        else:
            return "🧠 Advanced Strategy: The AI is learning your patterns. Use psychological tactics and vary your timing!"

def create_game_interface():
    """Create the main game interface"""
    
    # Header
    st.markdown("""
    <div class="main-header">
        <div class="game-title">🎮 Ultimate Rock Paper Scissors</div>
        <p>AI-Powered Game with Strategic Analysis & Fallback Mechanisms</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Initialize game
    if 'rps_game' not in st.session_state:
        st.session_state.rps_game = RPSGameRAG()
    
    game = st.session_state.rps_game
    game_state = st.session_state.game_state
    
    # Sidebar with controls and stats
    with st.sidebar:
        st.markdown("### 🎯 Game Controls")
        
        if st.button("🔄 Reset Game", type="secondary", help="Start a fresh game"):
            game.reset_game_state()
            st.success("Game reset successfully!")
            st.rerun()
        
        if st.button("🎲 Auto Play 5 Games", type="secondary", help="Let the AI play against itself"):
            with st.spinner("Auto-playing games..."):
                results = []
                for i in range(5):
                    player_choice = random.choice(game.choices)
                    result = game.play_round(player_choice)
                    results.append(result['result'])
                    time.sleep(0.2)
                
                wins = results.count('win')
                st.success(f"Auto-play complete! You won {wins}/5 games.")
            st.rerun()
        
        st.markdown("---")
        
        # Display game statistics
        st.markdown("### 📊 Game Statistics")
        
        # Score cards
        col1, col2 = st.columns(2)
        with col1:
            st.markdown(f"""
            <div class="score-card">
                <div class="stat-metric">{game_state['player_score']}</div>
                <div>Your Score</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown(f"""
            <div class="ai-score-card">
                <div class="stat-metric">{game_state['computer_score']}</div>
                <div>AI Score</div>
            </div>
            """, unsafe_allow_html=True)
        
        # Additional stats
        win_rate = (game_state['player_score'] / max(1, game_state['total_games']) * 100)
        st.metric("Win Rate", f"{win_rate:.1f}%")
        st.metric("Total Games", game_state['total_games'])
        st.metric("Current Streak", game_state['current_streak'])
        st.metric("Best Streak", game_state['best_streak'])
        
        if game_state.get('error_count', 0) > 0:
            st.warning(f"⚠️ {game_state['error_count']} errors handled with fallback mechanisms")
    
    # Main game area
    col1, col2, col3 = st.columns([1, 1, 1])
    
    with col1:
        st.markdown("### 👤 Your Choice")
        
        # Display player choice
        if game_state['player_choice']:
            emoji = game.choice_emojis[game_state['player_choice']]
            winner_class = "winner-glow" if game_state['last_result'] == 'win' else ""
            st.markdown(f'<div class="choice-display {winner_class}">{emoji}</div>', unsafe_allow_html=True)
        else:
            st.markdown('<div class="choice-display">❓</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown("### ⚔️")
        st.markdown('<div class="vs-section">VS</div>', unsafe_allow_html=True)
    
    with col3:
        st.markdown("### 🤖 AI Choice")
        
        # Display computer choice with thinking animation
        if game_state['computer_choice']:
            emoji = game.choice_emojis[game_state['computer_choice']]
            winner_class = "winner-glow" if game_state['last_result'] == 'lose' else ""
            st.markdown(f'<div class="choice-display {winner_class}">{emoji}</div>', unsafe_allow_html=True)
        else:
            thinking_emoji = random.choice(game.thinking_emojis)
            st.markdown(f'<div class="choice-display thinking-animation">{thinking_emoji}</div>', unsafe_allow_html=True)
    
    # Choice buttons with enhanced styling
    st.markdown("### 🎯 Make Your Choice")
    
    button_col1, button_col2, button_col3 = st.columns(3)
    
    with button_col1:
        if st.button("🗿 **ROCK**", key="rock_btn", help="Rock crushes Scissors", use_container_width=True):
            with st.spinner("Playing round..."):
                result = game.play_round('rock')
                time.sleep(0.5)  # Brief pause for dramatic effect
            
            if result['success']:
                st.rerun()
            else:
                st.error(f"Game error: {result['error']}")
    
    with button_col2:
        if st.button("📄 **PAPER**", key="paper_btn", help="Paper covers Rock", use_container_width=True):
            with st.spinner("Playing round..."):
                result = game.play_round('paper')
                time.sleep(0.5)
            
            if result['success']:
                st.rerun()
            else:
                st.error(f"Game error: {result['error']}")
    
    with button_col3:
        if st.button("✂️ **SCISSORS**", key="scissors_btn", help="Scissors cuts Paper", use_container_width=True):
            with st.spinner("Playing round..."):
                result = game.play_round('scissors')
                time.sleep(0.5)
            
            if result['success']:
                st.rerun()
            else:
                st.error(f"Game error: {result['error']}")
    
    # Result display with animations
    if game_state['last_result']:
        st.markdown("---")
        result_messages = {
            'win': ('🎉 YOU WIN! 🎉', 'result-win'),
            'lose': ('😔 YOU LOSE! 😔', 'result-lose'),
            'draw': ('🤝 IT\'S A DRAW! 🤝', 'result-draw')
        }
        
        message, css_class = result_messages.get(game_state['last_result'], ('', ''))
        if message:
            st.markdown(f'<div class="{css_class}">{message}</div>', unsafe_allow_html=True)
    
    # Error handling display
    if game_state.get('fallback_used', False):
        st.warning("⚠️ Fallback mechanism activated for this round due to strategy engine issues.")
        game_state['fallback_used'] = False  # Reset flag
    
    # Quick stats display
    if game_state['total_games'] > 0:
        st.markdown("---")
        st.markdown("### 📈 Quick Stats")
        
        quick_col1, quick_col2, quick_col3, quick_col4 = st.columns(4)
        
        with quick_col1:
            st.metric("Games Played", game_state['total_games'])
        with quick_col2:
            win_rate = (game_state['player_score'] / game_state['total_games'] * 100)
            st.metric("Win Rate", f"{win_rate:.1f}%", delta=f"{win_rate-50:.1f}%")
        with quick_col3:
            st.metric("Current Streak", game_state['current_streak'])
        with quick_col4:
            draws = game_state['total_games'] - game_state['player_score'] - game_state['computer_score']
            st.metric("Draws", draws)

def create_analytics_page():
    """Create analytics and insights page"""
    
    st.header("🧠 AI Analytics & Strategic Insights")
    
    if 'rps_game' not in st.session_state:
        st.warning("No game data available. Play some games first!")
        return
    
    game = st.session_state.rps_game
    game_state = st.session_state.game_state
    game_history = game_state['game_history']
    
    if not game_history:
        st.info("🎮 Play some games to see analytics and insights!")
        return
    
    # Game insights
    st.subheader("🎯 Strategic Insights")
    insights = game.generate_insights()
    
    insight_cols = st.columns(2)
    for i, insight in enumerate(insights):
        with insight_cols[i % 2]:
            st.markdown(f'<div class="insight-card">{insight}</div>', unsafe_allow_html=True)
    
    # Strategy recommendation
    st.subheader("💡 AI Strategy Recommendation")
    recommendation = game.get_strategy_recommendation()
    st.info(recommendation)
    
    # Performance charts
    if len(game_history) >= 3:
        st.subheader("📈 Performance Analysis")
        
        # Win rate over time
        df_history = pd.DataFrame(game_history)
        df_history['game_number'] = range(1, len(df_history) + 1)
        df_history['is_win'] = df_history['result'] == 'win'
        df_history['cumulative_wins'] = df_history['is_win'].cumsum()
        df_history['win_rate'] = df_history['cumulative_wins'] / df_history['game_number'] * 100
        
        # Create win rate chart
        fig = px.line(df_history, x='game_number', y='win_rate', 
                     title='Win Rate Over Time',
                     labels={'game_number': 'Game Number', 'win_rate': 'Win Rate (%)'},
                     line_shape='spline')
        fig.update_traces(line_color='#4CAF50', line_width=3)
        fig.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font_color='white'
        )
        st.plotly_chart(fig, use_container_width=True)
        
        # Choice frequency analysis
        choice_freq = Counter([game['player_choice'] for game in game_history])
        
        fig2 = px.pie(values=list(choice_freq.values()), 
                     names=list(choice_freq.keys()),
                     title='Your Choice Distribution',
                     color_discrete_sequence=['#FF6B6B', '#4ECDC4', '#45B7D1'])
        fig2.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font_color='white'
        )
        st.plotly_chart(fig2, use_container_width=True)
        
        # Win/Loss pattern by choice
        choice_results = defaultdict(lambda: {'win': 0, 'lose': 0, 'draw': 0})
        for game in game_history:
            choice_results[game['player_choice']][game['result']] += 1
        
        # Create win rate by choice chart
        choice_win_rates = {}
        for choice, results in choice_results.items():
            total = sum(results.values())
            win_rate = results['win'] / total * 100 if total > 0 else 0
            choice_win_rates[choice] = win_rate
        
        fig3 = px.bar(x=list(choice_win_rates.keys()), 
                     y=list(choice_win_rates.values()),
                     title='Win Rate by Choice',
                     labels={'x': 'Your Choice', 'y': 'Win Rate (%)'},
                     color=list(choice_win_rates.values()),
                     color_continuous_scale='RdYlGn')
        fig3.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font_color='white'
        )
        st.plotly_chart(fig3, use_container_width=True)
        
        # Recent performance heatmap
        if len(game_history) >= 10:
            st.subheader("🔥 Recent Performance Heatmap")
            recent_results = [game['result'] for game in game_history[-20:]]
            
            # Create matrix for heatmap
            result_matrix = []
            labels = []
            
            for i in range(0, len(recent_results), 5):
                chunk = recent_results[i:i+5]
                if len(chunk) == 5:
                    row_values = []
                    for r in chunk:
                        if r == 'win':
                            row_values.append(1)
                        elif r == 'draw':
                            row_values.append(0.5)
                        else:
                            row_values.append(0)
                    result_matrix.append(row_values)
                    labels.append(f"Games {i+1}-{i+5}")
            
            if result_matrix:
                fig4 = px.imshow(result_matrix, 
                               title='Recent Performance (Green=Win, Yellow=Draw, Red=Loss)',
                               color_continuous_scale='RdYlGn',
                               aspect='auto',
                               y=labels,
                               x=[f"Game {i+1}" for i in range(5)])
                fig4.update_layout(
                    plot_bgcolor='rgba(0,0,0,0)',
                    paper_bgcolor='rgba(0,0,0,0)',
                    font_color='white'
                )
                st.plotly_chart(fig4, use_container_width=True)

def create_rules_page():
    """Create rules and strategy guide page"""
    
    st.header("📚 Game Rules & Strategy Guide")
    
    # Basic rules
    st.subheader("🎯 Basic Rules")
    
    rule_col1, rule_col2, rule_col3 = st.columns(3)
    
    with rule_col1:
        st.markdown("""
        <div class="insight-card">
            <h4>🗿 Rock</h4>
            <p>Crushes Scissors</p>
            <p>Loses to Paper</p>
        </div>
        """, unsafe_allow_html=True)
    
    with rule_col2:
        st.markdown("""
        <div class="insight-card">
            <h4>📄 Paper</h4>
            <p>Covers Rock</p>
            <p>Loses to Scissors</p>
        </div>
        """, unsafe_allow_html=True)
    
    with rule_col3:
        st.markdown("""
        <div class="insight-card">
            <h4>✂️ Scissors</h4>
            <p>Cuts Paper</p>
            <p>Loses to Rock</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Strategy guide
    st.subheader("🧠 Advanced Strategy Guide")
    
    strategy_tabs = st.tabs(["Beginner", "Intermediate", "Advanced", "AI Insights"])
    
    with strategy_tabs[0]:
        st.markdown("""
        ### 🎯 Beginner Strategies
        
        **1. Random Play**
        - Mix up your choices randomly
        - Avoid predictable patterns
        - Each choice has equal probability
        
        **2. Counter Common Patterns**
        - Most beginners favor Rock (40% of the time)
        - Playing Paper can be effective early on
        - Watch for repeated moves
        
        **3. Break Your Own Patterns**
        - Avoid playing the same move 3+ times
        - Don't alternate predictably
        - Change strategy every few games
        """)
    
    with strategy_tabs[1]:
        st.markdown("""
        ### ⚡ Intermediate Strategies
        
        **1. Frequency Analysis**
        - Track opponent's most used moves
        - Counter their favorite choice
        - Adapt when they change patterns
        
        **2. Sequence Recognition**
        - Look for repeating sequences (Rock-Paper-Rock)
        - Predict continuation of patterns
        - Break sequences at key moments
        
        **3. Psychological Tactics**
        - Mirror opponent occasionally
        - Use reverse psychology
        - Create false patterns
        """)
    
    with strategy_tabs[2]:
        st.markdown("""
        ### 🔥 Advanced Strategies
        
        **1. Meta-Gaming**
        - Predict opponent's predictions
        - Use layered thinking
        - Counter their counter-strategies
        
        **2. Adaptive Play**
        - Change strategy every 5-7 games
        - React to opponent's adaptations
        - Use mixed strategies
        
        **3. Information Theory**
        - Minimize information leakage
        - Exploit opponent's information
        - Use entropy in your play
        """)
    
    with strategy_tabs[3]:
        st.markdown("""
        ### 🤖 AI Insights & Fallback Mechanisms
        
        **AI Strategy Features:**
        - Pattern recognition and analysis
        - Adaptive difficulty adjustment
        - Behavioral prediction models
        - Strategic randomization
        
        **Fallback Mechanisms:**
        - Error detection and recovery
        - Multiple strategy layers
        - Graceful degradation
        - Performance monitoring
        
        **Tips to Beat the AI:**
        - Change patterns frequently
        - Use completely random sequences
        - Play mind games with timing
        - Exploit over-adaptation
        """)
    
    st.markdown("---")
    
    # Game statistics explanation
    st.subheader("📊 Understanding Game Statistics")
    
    stats_col1, stats_col2 = st.columns(2)
    
    with stats_col1:
        st.markdown("""
        **Win Rate**: Percentage of games won
        - Above 60%: Excellent performance
        - 40-60%: Balanced gameplay  
        - Below 40%: Room for improvement
        
        **Streak**: Consecutive wins
        - Shows consistency and adaptation
        - AI becomes more aggressive during streaks
        """)
    
    with stats_col2:
        st.markdown("""
        **Choice Distribution**: Your move preferences
        - Balanced: ~33% each (optimal)
        - Biased: AI will exploit patterns
        - Adaptive: Changes over time
        
        **Pattern Confidence**: AI's certainty
        - High: AI thinks it knows your pattern
        - Low: AI is uncertain, plays randomly
        """)

def main():
    """Main application function"""
    
    # Navigation
    st.sidebar.title("🎮 Navigation")
    page = st.sidebar.selectbox("Choose a page", 
                               ["🎯 Play Game", "📊 Analytics", "📚 Rules & Strategy"])
    
    if page == "🎯 Play Game":
        create_game_interface()
    elif page == "📊 Analytics":
        create_analytics_page()
    elif page == "📚 Rules & Strategy":
        create_rules_page()

if __name__ == "__main__":
    main()

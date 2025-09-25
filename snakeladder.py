import streamlit as st
import random
import time
from enum import Enum

class Direction(Enum):
    UP = (0, -1)
    DOWN = (0, 1)
    LEFT = (-1, 0)
    RIGHT = (1, 0)

class SnakeGame:
    def __init__(self, width=20, height=15):
        self.width = width
        self.height = height
        self.reset_game()
    
    def reset_game(self):
        """Reset the game to initial state"""
        self.snake = [(self.width // 2, self.height // 2)]
        self.direction = Direction.RIGHT
        self.food = self.generate_food()
        self.score = 0
        self.game_over = False
    
    def generate_food(self):
        """Generate food at random position not occupied by snake"""
        while True:
            food = (random.randint(0, self.width - 1), random.randint(0, self.height - 1))
            if food not in self.snake:
                return food
    
    def move(self):
        """Move the snake one step in current direction"""
        if self.game_over:
            return
        
        # Calculate new head position
        head_x, head_y = self.snake[0]
        dx, dy = self.direction.value
        new_head = (head_x + dx, head_y + dy)
        
        # Check wall collision
        if (new_head[0] < 0 or new_head[0] >= self.width or 
            new_head[1] < 0 or new_head[1] >= self.height):
            self.game_over = True
            return
        
        # Check self collision
        if new_head in self.snake:
            self.game_over = True
            return
        
        # Add new head
        self.snake.insert(0, new_head)
        
        # Check food collision
        if new_head == self.food:
            self.score += 10
            self.food = self.generate_food()
        else:
            # Remove tail if no food eaten
            self.snake.pop()
    
    def change_direction(self, new_direction):
        """Change snake direction, prevent reversing into itself"""
        opposite_directions = {
            Direction.UP: Direction.DOWN,
            Direction.DOWN: Direction.UP,
            Direction.LEFT: Direction.RIGHT,
            Direction.RIGHT: Direction.LEFT
        }
        
        if new_direction != opposite_directions.get(self.direction):
            self.direction = new_direction

def create_game_display(game):
    """Create visual display of the game board using HTML/CSS"""
    
    # CSS styling for the game
    css = f"""
    <style>
    .game-container {{
        display: flex;
        flex-direction: column;
        align-items: center;
        padding: 20px;
        background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%);
        border-radius: 15px;
        margin: 20px auto;
        box-shadow: 0 10px 30px rgba(0,0,0,0.3);
    }}
    
    .game-board {{
        display: grid;
        grid-template-columns: repeat({game.width}, 20px);
        grid-template-rows: repeat({game.height}, 20px);
        gap: 1px;
        background-color: #34495e;
        padding: 15px;
        border-radius: 10px;
        box-shadow: inset 0 0 20px rgba(0,0,0,0.5);
    }}
    
    .cell {{
        width: 20px;
        height: 20px;
        border-radius: 2px;
    }}
    
    .empty {{
        background-color: #2c3e50;
        border: 1px solid #34495e;
    }}
    
    .snake-head {{
        background: radial-gradient(circle, #e74c3c, #c0392b);
        box-shadow: 0 0 8px rgba(231, 76, 60, 0.8);
        border: 2px solid #fff;
        transform: scale(1.1);
    }}
    
    .snake-body {{
        background: linear-gradient(45deg, #27ae60, #2ecc71);
        box-shadow: 0 0 5px rgba(39, 174, 96, 0.6);
        border: 1px solid #229954;
    }}
    
    .food {{
        background: radial-gradient(circle, #f39c12, #e67e22);
        border-radius: 50%;
        box-shadow: 0 0 10px rgba(243, 156, 18, 1);
        animation: pulse 1.5s infinite;
        border: 2px solid #fff;
    }}
    
    @keyframes pulse {{
        0% {{ 
            transform: scale(1);
            box-shadow: 0 0 10px rgba(243, 156, 18, 1);
        }}
        50% {{ 
            transform: scale(1.2);
            box-shadow: 0 0 20px rgba(243, 156, 18, 1);
        }}
        100% {{ 
            transform: scale(1);
            box-shadow: 0 0 10px rgba(243, 156, 18, 1);
        }}
    }}
    
    .score-display {{
        background: linear-gradient(135deg, #8e44ad, #9b59b6);
        color: white;
        padding: 15px 30px;
        border-radius: 25px;
        font-size: 24px;
        font-weight: bold;
        margin-bottom: 20px;
        box-shadow: 0 5px 15px rgba(0,0,0,0.3);
        text-align: center;
        min-width: 200px;
    }}
    
    .game-over-display {{
        background: linear-gradient(135deg, #e74c3c, #c0392b);
        color: white;
        padding: 20px 40px;
        border-radius: 25px;
        font-size: 20px;
        font-weight: bold;
        margin-bottom: 20px;
        box-shadow: 0 5px 15px rgba(0,0,0,0.3);
        text-align: center;
        animation: gameOverShake 0.8s;
    }}
    
    @keyframes gameOverShake {{
        0%, 20%, 40%, 60%, 80% {{ transform: translateX(-10px); }}
        10%, 30%, 50%, 70%, 90% {{ transform: translateX(10px); }}
        100% {{ transform: translateX(0); }}
    }}
    </style>
    """
    
    # Create the HTML structure
    html = css + '<div class="game-container">'
    
    # Score or Game Over display
    if game.game_over:
        html += f'''
        <div class="game-over-display">
            🎮 GAME OVER! 🎮<br>
            Final Score: {game.score}<br>
            Snake Length: {len(game.snake)}
        </div>
        '''
    else:
        html += f'''
        <div class="score-display">
            Score: {game.score} | Length: {len(game.snake)}
        </div>
        '''
    
    # Game board
    html += '<div class="game-board">'
    
    for y in range(game.height):
        for x in range(game.width):
            if (x, y) == game.snake[0]:
                html += '<div class="cell snake-head"></div>'
            elif (x, y) in game.snake[1:]:
                html += '<div class="cell snake-body"></div>'
            elif (x, y) == game.food:
                html += '<div class="cell food"></div>'
            else:
                html += '<div class="cell empty"></div>'
    
    html += '</div></div>'
    
    return html

def main():
    """Main Streamlit app"""
    
    # Page configuration
    st.set_page_config(
        page_title="🐍 Classic Snake Game",
        page_icon="🐍",
        layout="centered",
        initial_sidebar_state="collapsed"
    )
    
    # Custom CSS for buttons and overall styling
    st.markdown("""
    <style>
    .main > div {
        padding-top: 1rem;
    }
    
    .stButton > button {
        width: 100%;
        height: 50px;
        font-size: 16px;
        font-weight: bold;
        border-radius: 10px;
        border: none;
        transition: all 0.3s ease;
        background: linear-gradient(45deg, #3498db, #2980b9);
        color: white;
    }
    
    .stButton > button:hover {
        transform: translateY(-3px);
        box-shadow: 0 6px 20px rgba(0,0,0,0.3);
        background: linear-gradient(45deg, #2980b9, #3498db);
    }
    
    .stButton > button:active {
        transform: translateY(-1px);
    }
    
    /* Direction button specific styles using nth-child selectors */
    div[data-testid="column"]:nth-child(2) .stButton > button {
        background: linear-gradient(45deg, #e74c3c, #c0392b) !important;
        font-size: 18px !important;
        height: 55px !important;
        border-radius: 15px !important;
        box-shadow: 0 4px 15px rgba(231, 76, 60, 0.4) !important;
    }
    
    div[data-testid="column"]:nth-child(1) .stButton > button {
        background: linear-gradient(45deg, #9b59b6, #8e44ad) !important;
        font-size: 18px !important;
        height: 55px !important;
        border-radius: 15px !important;
        box-shadow: 0 4px 15px rgba(155, 89, 182, 0.4) !important;
    }
    
    div[data-testid="column"]:nth-child(3) .stButton > button {
        background: linear-gradient(45deg, #27ae60, #2ecc71) !important;
        font-size: 18px !important;
        height: 55px !important;
        border-radius: 15px !important;
        box-shadow: 0 4px 15px rgba(39, 174, 96, 0.4) !important;
    }
    
    .controls-grid {
        background: rgba(255,255,255,0.1);
        padding: 25px;
        border-radius: 20px;
        margin: 20px 0;
        backdrop-filter: blur(10px);
        box-shadow: 0 8px 32px rgba(0,0,0,0.3);
    }
    
    .controls-title {
        text-align: center;
        color: white;
        font-size: 20px;
        font-weight: bold;
        margin-bottom: 20px;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.5);
    }
    

    
    .instructions {
        background: linear-gradient(135deg, #16a085, #1abc9c);
        color: white;
        padding: 15px;
        border-radius: 10px;
        margin: 20px 0;
        text-align: center;
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Title and description
    st.markdown("# 🐍 Classic Snake Game")
    st.markdown("*Navigate the snake to eat food and grow! Avoid walls and yourself.*")
    
    # Initialize game state
    if 'snake_game' not in st.session_state:
        st.session_state.snake_game = SnakeGame()
    if 'auto_move' not in st.session_state:
        st.session_state.auto_move = False
    if 'high_score' not in st.session_state:
        st.session_state.high_score = 0
    
    game = st.session_state.snake_game
    
    # Update high score
    if game.score > st.session_state.high_score:
        st.session_state.high_score = game.score
    
    # Display the game
    game_display = create_game_display(game)
    st.markdown(game_display, unsafe_allow_html=True)
    
    # Control buttons with improved layout
    st.markdown('<div class="controls-grid">', unsafe_allow_html=True)
    st.markdown('<div class="controls-title">🎮 Direction Controls</div>', unsafe_allow_html=True)
    
    # Direction controls in cross pattern
    # Row 1: Up button centered
    col_empty1, col_up, col_empty2 = st.columns([1, 1, 1])
    with col_up:
        up_pressed = st.button("⬆️ UP", key="up_btn", disabled=game.game_over, help="Move Up")
        if up_pressed:
            game.change_direction(Direction.UP)
            game.move()
            st.rerun()
    
    # Row 2: Left and Right buttons
    col_left, col_center, col_right = st.columns([1, 1, 1])
    
    with col_left:
        left_pressed = st.button("⬅️ LEFT", key="left_btn", disabled=game.game_over, help="Move Left")
        if left_pressed:
            game.change_direction(Direction.LEFT)
            game.move()
            st.rerun()
    
    with col_center:
        # Show current direction
        current_dir = {
            Direction.UP: "⬆️",
            Direction.DOWN: "⬇️", 
            Direction.LEFT: "⬅️",
            Direction.RIGHT: "➡️"
        }
        st.markdown(f"""
        <div style="text-align: center; padding: 10px; background: rgba(255,255,255,0.2); 
                    border-radius: 10px; margin-top: 8px;">
            <div style="font-size: 24px; margin-bottom: 5px;">{current_dir.get(game.direction, "➡️")}</div>
            <div style="font-size: 12px; color: #ecf0f1;">Current Direction</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col_right:
        right_pressed = st.button("➡️ RIGHT", key="right_btn", disabled=game.game_over, help="Move Right")
        if right_pressed:
            game.change_direction(Direction.RIGHT)
            game.move()
            st.rerun()
    
    # Row 3: Down button centered with orange color
    col_empty3, col_down, col_empty4 = st.columns([1, 1, 1])
    with col_down:
        st.markdown("""
        <style>
        div[data-testid="column"]:nth-last-child(2) .stButton > button {
            background: linear-gradient(45deg, #f39c12, #e67e22) !important;
            font-size: 18px !important;
            height: 55px !important;
            border-radius: 15px !important;
            box-shadow: 0 4px 15px rgba(243, 156, 18, 0.4) !important;
        }
        </style>
        """, unsafe_allow_html=True)
        down_pressed = st.button("⬇️ DOWN", key="down_btn", disabled=game.game_over, help="Move Down")
        if down_pressed:
            game.change_direction(Direction.DOWN)
            game.move()
            st.rerun()
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Game control buttons
    col1, col2, col3 = st.columns([1, 1, 1])
    
    with col1:
        auto_text = "⏹️ Stop Auto" if st.session_state.auto_move else "▶️ Auto Play"
        if st.button(auto_text, key="auto_btn", disabled=game.game_over):
            st.session_state.auto_move = not st.session_state.auto_move
            st.rerun()
    
    with col2:
        if st.button("🔄 Restart", key="restart_btn"):
            st.session_state.snake_game = SnakeGame()
            st.session_state.auto_move = False
            st.rerun()
    
    with col3:
        st.markdown(f"**🏆 High Score: {st.session_state.high_score}**")
    
    # Auto movement
    if st.session_state.auto_move and not game.game_over:
        time.sleep(0.15)  # Control game speed
        game.move()
        st.rerun()
    
    # Instructions
    st.markdown("""
    <div class="instructions">
        <h4>🎮 How to Play:</h4>
        🎯 Use arrow buttons to control the snake direction<br>
        🍎 Eat the pulsing food to grow and increase score (+10 points)<br>
        ⚠️ Avoid hitting walls or your own body<br>
        ▶️ Use Auto Play for continuous movement<br>
        🔄 Restart anytime to play again
    </div>
    """, unsafe_allow_html=True)
    
    # Game statistics
    if game.score > 0 or game.game_over:
        st.markdown("---")
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Current Score", game.score)
        with col2:
            st.metric("Snake Length", len(game.snake))
        with col3:
            st.metric("High Score", st.session_state.high_score)
        with col4:
            efficiency = round((game.score / len(game.snake)) * 100) if len(game.snake) > 0 else 0
            st.metric("Efficiency", f"{efficiency}%")

if __name__ == "__main__":
    main()

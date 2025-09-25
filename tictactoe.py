import streamlit as st
import random
import time
from datetime import datetime

st.set_page_config(page_title="Tic-Tac-Toe ❌⭕", page_icon="🎯", layout="centered")

# --- Constants --------------------------------------------------------
WIN_LINES = [
    (0, 1, 2),
    (3, 4, 5),
    (6, 7, 8),
    (0, 3, 6),
    (1, 4, 7),
    (2, 5, 8),
    (0, 4, 8),
    (2, 4, 6),
]

# --- Session state initialization ------------------------------------

def init_state():
    if 'board' not in st.session_state:
        st.session_state.board = [''] * 9
    if 'current' not in st.session_state:
        st.session_state.current = 'X'
    if 'winner' not in st.session_state:
        st.session_state.winner = None
    if 'winning_line' not in st.session_state:
        st.session_state.winning_line = []
    if 'history' not in st.session_state:
        st.session_state.history = []


def check_winner(board):
    for a, b, c in WIN_LINES:
        if board[a] and board[a] == board[b] == board[c]:
            return board[a], (a, b, c)
    if all(cell for cell in board):
        return 'Draw', ()
    return None, ()


def make_move(i, by='player'):
    if st.session_state.winner:
        return
    if st.session_state.board[i] != '':
        return

    st.session_state.board[i] = st.session_state.current
    st.session_state.history.append((datetime.utcnow().isoformat(), st.session_state.current, i, by))

    w, line = check_winner(st.session_state.board)
    if w:
        st.session_state.winner = w
        st.session_state.winning_line = list(line)
        return

    st.session_state.current = 'O' if st.session_state.current == 'X' else 'X'


def computer_move():
    empties = [i for i, v in enumerate(st.session_state.board) if v == '']
    if not empties or st.session_state.winner:
        return

    choice = random.choice(empties)
    time.sleep(0.25)
    make_move(choice, by='computer')


def reset_board():
    st.session_state.board = [''] * 9
    st.session_state.current = 'X'
    st.session_state.winner = None
    st.session_state.winning_line = []
    st.session_state.history = []


# --- Initialize ------------------------------------------------------
init_state()

# --- Sidebar: options & instructions ---------------------------------
st.sidebar.title("Options")
mode = st.sidebar.radio("Mode:", ("Two players", "Vs Computer (random)"))
player_starts = st.sidebar.selectbox("Who starts", ("Player X", "Player O"))
show_history = st.sidebar.checkbox("Show move history", value=False)

if all(cell == '' for cell in st.session_state.board):
    st.session_state.current = 'X' if player_starts == 'Player X' else 'O'

st.sidebar.markdown("---")
if st.sidebar.button('Reset board'):
    reset_board()
    st.session_state.current = 'X' if player_starts == 'Player X' else 'O'

# --- Main UI ---------------------------------------------------------
st.title("Tic-Tac-Toe ❌⭕")
st.write("Play a 3×3 Tic-Tac-Toe. Choose Two players or Vs Computer. The computer uses random moves.")

# Render the 3x3 board
for row in range(3):
    cols = st.columns(3)
    for col in range(3):
        i = row * 3 + col
        is_winning_cell = i in st.session_state.winning_line
        label = st.session_state.board[i]

        if label == '' and not st.session_state.winner:
            cols[col].button(' ', key=f'cell_{i}', on_click=make_move, args=(i,))
        else:
            if is_winning_cell:
                cols[col].markdown(
                    "<div style='font-size:34px; font-weight:700; padding:20px; border-radius:8px; text-align:center; background: linear-gradient(90deg,#ffd6d6,#ffe7d1);'>{}</div>".format(label),
                    unsafe_allow_html=True,
                )
            else:
                cols[col].markdown(
                    "<div style='font-size:34px; font-weight:700; padding:20px; border-radius:8px; text-align:center;'>{}</div>".format(label or ' '),
                    unsafe_allow_html=True,
                )

# If playing vs computer and it's the computer's turn, make the computer move
if mode == 'Vs Computer (random)' and not st.session_state.winner:
    human_symbol = 'X'
    computer_symbol = 'O'
    if st.session_state.current == computer_symbol:
        computer_move()

# Show game status
if st.session_state.winner:
    if st.session_state.winner == 'Draw':
        st.success("It's a draw!")
    else:
        st.success(f"{st.session_state.winner} wins!")
    st.markdown("**Winning line is highlighted.**")
else:
    st.info(f"Current turn: {st.session_state.current}")

# Reset contro

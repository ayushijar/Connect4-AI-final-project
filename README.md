# CONNECT FOUR :

This game will be an interactive game between the human and the computer wherein the human can play his move and the 
computer will predict its move based on the algorithm implemented and finally give us the result as to who won and
who lost.


# INTRODUCTION :

- This is a Human vs AI connect4 game where you have to connect 4 discs either in a row, column or diagonal.
- The game runs in 5 difficulty levels : 
    (i) EASY
    (ii) MEDIUM
    (iii) DIFFICULT
    (iv) CHALLENGING
    (v) UNBEATABLE
- Connect4 is implemented using minimax algorithm, alpha beta pruning and depth limited minimax for prediciting the next best 
  possible move for AI agent.
- AI piece is RED color.
- Human player piece is YELLOW color.


# STRUCTURE OF THE CODE :

- [variables.py](https://github.com/ayushijar/Connect4-AI-final-project/blob/Project-setup/src/variables.py) contains all the GLOBAL variables for the project so that they are easy to find and change if ever needed. Helps in writing clean code.
- [functions.py](https://github.com/ayushijar/Connect4-AI-final-project/blob/Project-setup/src/functions.py) contains all the functions used in the game loop. This helps in bundling the functions together so that they are easy to find, edit and are easily accessible throughout the project. Keeps the main file clean as well.
- [ui_components.py](https://github.com/ayushijar/Connect4-AI-final-project/blob/Project-setup/src/ui_components.py) contains all the UI elements for the game. Helps in keeping UI methods and other methods separate.
- [score_ai.py](https://github.com/ayushijar/Connect4-AI-final-project/blob/Project-setup/src/score_ai.py) contains the functions for the score based AI version.
- [minmax_ai.py](https://github.com/ayushijar/Connect4-AI-final-project/blob/Project-setup/src/minmax_ai.py) contains the functions for the minmax algorithm for AI agent.
- [game.py](https://github.com/ayushijar/Connect4-AI-final-project/blob/Project-setup/src/game.py) contains the game loop and executes the software.



# HOW TO RUN THE GAME?

1. Clone the repository to your machine following [how to clone a repo](https://docs.github.com/en/repositories/creating-and-managing-repositories/cloning-a-repository) documentation.

2. Install the requirements by running `pip install -r requirements.txt`.

3. Update the path in the terminal as `<directory path>\Connect4-AI-final-project\src` and run the project by executing the command     "python game.py" 
            OR
Go to "game.py" file and click on the play button in the top right corner of vs code.

4. You will be presented with a screen with 5 different difficulty level. Choose one level and play the game.


# HOW TO PLAY THE GAME?

- This game is played in turns and first turn will be randomly allocated.
- If it is your turn, hover the mouse cursor over the column where you want to drop the piece and click mouse left button. 
  The piece will be placed in the bottommost row of that column.
- Wait for AI to drop its piece.
- The goal is to stack 4 of their colored discs upwards, horizontally, or diagonally.
- First one to achieve this wins the game.
- If the board is filled without a winner, its a draw.


# GAME MODES :

1. EASY : In this mode difficulty level is set to the minimum, with the AI performing a search at a depth of 2.
2. MEDIUM : In this mode difficulty level is a little more than EASY mode, with the AI performing a search at a depth of 3.
3. DIFFICULT : In this mode AI performs a search at a depth of 4, providing a better user experience.
4. CHALLENGING :  In this mode AI performs a search at a depth of 6, presenting a challenging game play against human 
   player.
5. UNBEATABLE :  This mode has highest level of difficulty where AI performs a search at depth 7, creates starategies against
   human player and tries to win.

# EVALUATION FUNCTION :

- We have implmented an evaluation function for depth limited minimax in order to calculate the score value which will be used by the 
algorithm to determine the next best possible move.
- The evaluation function (evaluate_current_score) considers various patterns on the game board and assigns scores based on the presence of AI or player pieces.
- The computer will choose the highest score value it finds while calculating and it will choose the corresponding column to play its
next move.
- For complete implementation of evaluation function, please refer to the file score_ai.py.

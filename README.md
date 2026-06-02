# CS470/570

# Artificial Intelligence

# Project #2

## Goal

Write a program to play Connect Four against a human opponent and against itself and collect data on the game play.

Connect Four is played on a vertical board with 7 columns each 6 positions high. Players alternate dropping different colored pieces into one of the 7 columns. Once a column is filled (i.e. six pieces have been dropped into it) that column is no longer a legal move. The goal is to get four pieces in a row: vertically, horizontally, or diagonally. It is possible for the game to be a tie, if the board is filled without anyone connecting four pieces. This is a relatively easy game for computers because of the low branching factor. There are lots of on-line versions (e.g. https://www.mathsisfun.com/games/connect4.htmlLinks to an external site.) if you want to play.

## Requirements

The program must use a minimax search algorithm (it can be coded as negamax) and alpha-beta pruning. The user must be able to determine which side goes first or set the program to play against itself. The program must display the board after each move. (This can be a simple text-based display, but graphics is preferred.) The maximum depth of the search/look-ahead should be adjustable when the game starts (this is effectively a difficulty setting).

## Algorithms

You will need to write an evaluation heuristic because searching the entire game tree is not feasible. If your minimax/negamax algorithm is working properly the program should always block a potential win by the opponent (if there are three opponent pieces in a row the computer places a piece to block the win) and always makes a winning move if one is available. In addition, to minimax search and alpha-beta pruning, you may include any of the following: move reordering, selective deepening (quiescent search), and depth-based tie-breaking.

## Analysis

By having the program play against itself you can see how long the code takes under different conditions. Include in the write-up a table similar to the one shown below. If your program incorporates move reordering or selective deepening include separate rows with those turned on and with them turned off. Because minimax is deterministic (unless you add a random factor, such as for tie-breaking) you only need to run each condition once.

| Algorithm                               | # of explored states | Time/move | Outcome |
| --------------------------------------- | -------------------: | --------: | ------- |
| Minimax depth X                         |                      |           |         |
| Minimax depth X+1                       |                      |           |         |
| Minimax depth X+2                       |                      |           |         |
| Minimax w/ alpha-beta pruning depth X   |                      |           |         |
| Minimax w/ alpha-beta pruning depth X+1 |                      |           |         |
| Minimax w/ alpha-beta pruning depth X+2 |                      |           |         |

## Hand-In

You need to hand in a typed write-up containing the following:

### An abstract summarizing what you did and what the results were.

### An algorithm section explaining your program. Including,

* A brief description of your minimax algorithm.
* A description of other features, if any, that you added, e.g. alpha-beta pruning, selective evaluation, move ordering, etc.
* A description of the evaluation function (examples are very helpful).
* A table similar to the one shown above summarizing the game results.
* Sample game play, showing the program correctly takes wins, blocks the opponent, etc.

### A conclusions section. Including,

* A discussion of the strengths and weaknesses of the program (if any).
* A brief description of how well you felt the program played.
* Improvements you would like to make.
* Your code (this may be a link to a repository)

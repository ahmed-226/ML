# ConnectX Kaggle Agent

This repository contains a ConnectX agent for the Kaggle ConnectX competition. The agent is implemented in `main.py` and is ready for submission to Kaggle.

## Overview

The agent uses a combination of classic game AI techniques:

- **Minimax Algorithm with Alpha-Beta Pruning:**  
  The agent searches possible moves up to a certain depth (default: 3), evaluating each board state using a heuristic function. Alpha-beta pruning is used to speed up the search by eliminating branches that cannot possibly affect the final decision.

- **Heuristic Evaluation:**  
  The evaluation function scores board positions based on the number of pieces in a row for both the agent and the opponent, rewarding moves that create or block potential wins.

- **Safe Fallback:**  
  If the minimax agent encounters an error, a safe agent is used as a fallback. This agent always returns a valid move, preferring the center columns.

## File Structure

- `main.py`  
  Contains all the logic for the agent, including helper functions and the main `agent` function required by Kaggle.

## How It Works

- The `agent(obs, config)` function is the entry point for Kaggle.
- It tries to select the best move using the minimax algorithm.
- If an error occurs, it falls back to a safe move.

## Usage

To submit to Kaggle:
1. Upload `main.py` as your agent file.
2. Kaggle will use the `agent` function as the entry point.

## Algorithms Used

- **Minimax with Alpha-Beta Pruning:**  
  Explores possible moves and counter-moves to a fixed depth, maximizing the agent's chances of winning while minimizing the opponent's.

- **Heuristic Evaluation:**  
  Scores board windows based on the number of agent and opponent pieces, rewarding moves that lead to a win or block the opponent.

- **Safe Agent:**  
  Ensures a valid move is always returned, even if the main logic fails.

## Requirements

- Python 3.x
- numpy

## License

This code is provided for educational purposes and Kaggle competition use.

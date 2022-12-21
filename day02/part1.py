"""See problem statement, honestly."""
import argparse
from typing import Tuple

ROCK = "A"
PAPER = "B"
SCISSORS = "C"

# players have X, Y, Z for Rock, Paper, Scissors
player_map = {"X": ROCK, "Y": PAPER, "Z": SCISSORS}

# if beats[x] = y, then x beats y
beats = {ROCK: SCISSORS, PAPER: ROCK, SCISSORS: PAPER}
choice_scores = {ROCK: 1, PAPER: 2, SCISSORS: 3}


def score_round(opponent_choice: str, player_choice: str) -> int:
    player_choice = player_map[player_choice]
    player_score = choice_scores[player_choice]
    if beats[player_choice] == opponent_choice:
        # 6 points for winning
        player_score += 6
    elif player_choice == opponent_choice:
        # 3 points for a draw
        player_score += 3
    else:
        # 0 points for losing
        player_score += 0
    return player_score


def choices_from_line(line: str) -> Tuple[str, str]:
    """Line -> opponent_choice, player_choice."""
    splits = line.split()
    if len(splits) != 2:
        raise ValueError(f"Could not split line {line} into 2 parts")
    return splits[0], splits[1]


def score_file(filename: str) -> int:
    player_score = 0
    with open(filename, encoding="utf-8") as f:
        for line in f:
            opponent, player = choices_from_line(line)
            player_score += score_round(opponent, player)
    return player_score


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="read a file")
    parser.add_argument("filename")  # positional argument

    args = parser.parse_args()
    print(score_file(args.filename))

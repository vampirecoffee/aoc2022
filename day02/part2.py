"""See problem statement, honestly."""
import argparse
from typing import Tuple

ROCK = "A"
PAPER = "B"
SCISSORS = "C"

LOSE = "X"
DRAW = "Y"
WIN = "Z"

# if beats[x] = y, then x beats y
beats = {ROCK: SCISSORS, PAPER: ROCK, SCISSORS: PAPER}
choice_scores = {ROCK: 1, PAPER: 2, SCISSORS: 3}


def score_round(opponent_choice: str, player_choice: str) -> int:
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


def choose_for_round(opponent_choice: str, result: str) -> str:
    """Determine whether to play rock, paper, or scissors."""
    if result == LOSE:
        return beats[opponent_choice]
    elif result == DRAW:
        return opponent_choice
    else:
        # We need to win. What beats the opponent?
        for choice in beats:
            if beats[choice] == opponent_choice:
                return choice
        raise RuntimeError(
            "Nothing beats the opponent. They have won rock-paper-scissors for all time"
        )


def choices_from_line(line: str) -> Tuple[str, str]:
    """Line -> opponent_choice, player_result."""
    splits = line.split()
    if len(splits) != 2:
        raise ValueError(f"Could not split line {line} into 2 parts")
    return splits[0], splits[1]


def score_file(filename: str) -> int:
    player_score = 0
    with open(filename, encoding="utf-8") as f:
        for line in f:
            opponent, result = choices_from_line(line)
            player_choice = choose_for_round(opponent, result)
            player_score += score_round(opponent, player_choice)
    return player_score


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="read a file")
    parser.add_argument("filename")  # positional argument

    args = parser.parse_args()
    print(score_file(args.filename))

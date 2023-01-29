# Refactored Lottery Simulator for Corey Schafer's Tutorial: https://www.youtube.com/watch?v=HZ8uXq5VG2w
from random import sample, choice
import json

# type alias for lottery numbers e.g. {'whites': {45, 2, 6, 7, 15}, 'red': 24}
lottery_nums = dict[str, set[int] | int]

# constants for these lottery rules: https://www.powerball.com/powerball/prizes-and-odds
WHITE_BALLS = list(range(1, 70))
RED_BALLS = list(range(1, 25))
TICKET_PRICE = 2
NUM_DRAWINGS = 156
PRIZE_TABLE = {
    # condtions with a prize (white matches, red match): (win amount, win type)
    (5, True): (2_000_000_000, "5+P"),
    (5, False): (1_000_000, "5"),
    (4, True): (50_000, "4+P"),
    (4, False): (100, "4"),
    (3, True): (100, "3+P"),
    (3, False): (7, "3"),
    (2, True): (7, "2+P"),
    (1, True): (4, "1+P"),
    (0, True): (4, "P"),
    # conditions with no prize
    (2, False): (0, "2"),
    (1, False): (0, "1"),
    (0, False): (0, "0"),
}


def lottery_draw() -> lottery_nums:
    """Generate a random lottery ticket or winning draw."""
    return {
        "whites": set(sample(WHITE_BALLS, k=5)),
        "red": choice(RED_BALLS),
    }


def check_ticket(nums: lottery_nums, winning_nums: lottery_nums) -> tuple[int, str]:
    """Determines the win amount and win type for a given ticket and winning draw."""
    white_matches = len(nums["whites"] & winning_nums["whites"])
    red_match = nums["red"] == winning_nums["red"]

    if (white_matches, red_match) in PRIZE_TABLE:
        win_amt, win_type = PRIZE_TABLE[(white_matches, red_match)]
        return (win_amt, win_type)
    raise ValueError("Invalid combination of ticket and winning numbers.")


if __name__ == "__main__":
    # assumes player buys the same number of tickets in each draw
    tickets_per_draw = 2
    total_spent = NUM_DRAWINGS * tickets_per_draw * TICKET_PRICE

    # keep track of 'earnings' and how many times each win type occurs
    earnings = 0
    times_won = {
        "5+P": 0,
        "4+P": 0,
        "3+P": 0,
        "2+P": 0,
        "1+P": 0,
        "P": 0,
        "5": 0,
        "4": 0,
        "3": 0,
        "2": 0,
        "1": 0,
        "0": 0,
    }

    for drawing in range(NUM_DRAWINGS):
        winning_numbers = lottery_draw()

        for ticket in range(tickets_per_draw):
            my_numbers = lottery_draw()

            win_amt, win_type = check_ticket(my_numbers, winning_numbers)
            earnings += win_amt
            times_won[win_type] += 1

    print(f"Spent: ${total_spent:,}\nEarnings: ${earnings:,}")
    print(f"Prize Types:\n\n{json.dumps(times_won, indent=4)}\n")

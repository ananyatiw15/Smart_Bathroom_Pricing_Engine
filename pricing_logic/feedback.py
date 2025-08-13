import csv
import os

FEEDBACK_FILE = "data/feedback.csv"

def save_feedback(quote_id, accepted):
    """
    Record feedback for a quote to CSV.
    """
    new_file = not os.path.exists(FEEDBACK_FILE)
    with open(FEEDBACK_FILE, "a", newline="") as f:
        writer = csv.writer(f)
        if new_file:
            writer.writerow(["quote_id", "accepted"])
        writer.writerow([quote_id, int(accepted)])

def adjust_margin(base_margin):
    """
    Adjust margin based on past feedback.
    If too many rejections recently, lower margin to improve win rate.
    If many accepted, keep or slightly raise margin.
    """
    if not os.path.exists(FEEDBACK_FILE):
        return base_margin

    with open(FEEDBACK_FILE, "r") as f:
        rows = list(csv.DictReader(f))
    
    if len(rows) < 3:  # not enough data
        return base_margin

    accepted = sum(1 for r in rows if r["accepted"] == "1")
    total = len(rows)
    win_rate = accepted / total

    if win_rate < 0.5:
        return max(base_margin - 2, 5)  # lower margin, min 5%
    elif win_rate > 0.8:
        return base_margin + 2  # can slightly raise
    return base_margin


import os
from api.chat.chat_handler import ChatHandler

chat = ChatHandler()

def save_summary(summary, filename="summary.txt"):
    """Save the summary to a text file."""
    with open(filename, "w", encoding="utf-8") as file:
        file.write(summary)
    print(f"\nSummary saved to {filename}")


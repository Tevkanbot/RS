import json
import os
import re

class Data:
    @staticmethod
    def load():
        """Load triggers and actions from data.json"""
        current_dir = os.path.dirname(os.path.abspath(__file__))
        file_path = os.path.join(current_dir, "data.json")

        with open(file_path, "r", encoding="utf-8") as file:
            return json.load(file)

    @staticmethod
    def dump(data):
        """Save updated triggers and actions to data.json"""
        if not isinstance(data, dict):
            raise TypeError("Argument must be a dict")

        current_dir = os.path.dirname(os.path.abspath(__file__))
        file_path = os.path.join(current_dir, "data.json")

        with open(file_path, "w", encoding="utf-8") as file:
            json.dump(data, file, ensure_ascii=False, indent=4)


class Trigger:
    @staticmethod
    def clean_phrase(phrase):
        """Clean the input phrase by removing punctuation and converting to lowercase"""
        return re.sub(r"[^Ѐ-ӿa-zA-Z0-9\s]", "", phrase).lower()

    @staticmethod
    def find_trigger(phrase):
        """Find the matching trigger for the given phrase"""
        cleaned_phrase = Trigger.clean_phrase(phrase)
        data = Data.load()

        best_match = None
        max_match_count = 0

        for trigger in data["triggers"]:
            trigger_words = set(trigger["phrase"].split())
            phrase_words = set(cleaned_phrase.split())

            # Count how many words from the trigger phrase are in the input phrase
            match_count = len(trigger_words & phrase_words)

            if match_count > max_match_count:
                max_match_count = match_count
                best_match = trigger

        return best_match


# Example usage:
if __name__ == "__main__":
    phrase = "алло где туалет где же находится туалет как думаешь"
    trigger = Trigger.find_trigger(phrase)

    if trigger:
        print(f"Trigger found: {trigger}")
        # Trigger.execute_trigger(trigger, ro) # Pass the relevant object
    else:
        print("No trigger found.")

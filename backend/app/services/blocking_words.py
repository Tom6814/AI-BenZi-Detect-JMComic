from typing import List

class BlockingWordLibrary:
    def __init__(self):
        # A mock list of bad words or blocking words
        self._bad_words = {
            "badword1",
            "badword2",
            "spam",
            "scam",
            "fake",
            "hate",
            "violence"
        }

    def contains_blocking_word(self, text: str) -> bool:
        """
        Check if the text contains any of the blocking words.
        """
        words_in_text = set(text.lower().split())
        return not self._bad_words.isdisjoint(words_in_text)

    def get_blocking_words(self, text: str) -> List[str]:
        """
        Return a list of blocking words found in the text.
        """
        words_in_text = text.lower().split()
        found_words = [word for word in words_in_text if word in self._bad_words]
        # Return unique blocked words
        return list(set(found_words))

    def add_word(self, word: str):
        """
        Add a new word to the blocking word list.
        """
        self._bad_words.add(word.lower())

    def remove_word(self, word: str):
        """
        Remove a word from the blocking word list.
        """
        self._bad_words.discard(word.lower())

# Singleton instance for the mock library
blocking_word_lib = BlockingWordLibrary()

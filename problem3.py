"""
Technical Question 3
Monash Motorsport Intake Semester 1, 2022

Author: Harpo Barrett
Last Modified: 20/02/2022
"""

import unittest
import timeit


class Problem3:
    # assuming all words entered are non-empty strings with no spaces, using only lowercase characters a-z

    # effectively, this is a prefix trie

    # a conscious effort was made to prioritize code readability, rather than to minimize repeated code.

    def __init__(self):
        self.alphabet_length = 27  # the number of characters in the set of allowed characters, plus 1 for the terminating character
        self.terminating_char = "\0"  # the terminating character used to indicate that a word has finished
        self.words = [None for _ in range(self.alphabet_length)]


    def insert(self, word):
        self.__insert_aux(self.words, word + self.terminating_char)
        

    def __insert_aux(self, sub_trie, word, char_index=0):

        # First determine what character we are currently inserting, and its lexographical index
        current_char = word[char_index]
        current_index = self.char_to_index(current_char)

        # If we have reached the end of the word (indicated by the terminating character), place the terminating character and exit.
        if current_char == self.terminating_char:
            sub_trie[0] = self.terminating_char
            return

        # If this character has not been added to this sub-trie before, create a new sub-trie for it
        if sub_trie[current_index] is None:
            sub_trie[current_index] = [None for _ in range(self.alphabet_length)]

        # We can then proceed on to inserting the next character in the relevant sub-trie.
        self.__insert_aux(sub_trie[current_index], word, char_index + 1)


    def search(self, word):
        return self.__search_aux(self.words, word + self.terminating_char)

    
    def __search_aux(self, sub_trie, word, char_index=0):
        
        # First determine what character we are currently searching for, and its lexographical index
        current_char = word[char_index]
        current_index = self.char_to_index(current_char)

        # If we have reached the end of the word (indicated by the terminating character)
        if current_char == self.terminating_char:
            # Return True if the word is in the sub-trie (indicated by the terminating character), and False otherwise
            return sub_trie[0] is not None
        
        # We can check if this character has been inserted into this sub-trie
        if sub_trie[current_index] is None:
            return False
        
        # If it has been inserted, keep searching that sub-trie for the next character
        return self.__search_aux(sub_trie[current_index], word, char_index + 1)



    def delete(self, word):
        # nothing happens if the word is not in the structure
        self.__delete_aux(self.words, word + self.terminating_char)


    def __delete_aux(self, sub_trie, word, char_index=0):
        
        # First determine what character we are currently searching for, and its lexographical index
        current_char = word[char_index]
        current_index = self.char_to_index(current_char)

        # If we have reached the end of the word (indicated by the terminating character)
        if current_char == self.terminating_char:
            sub_trie[0] = None

            # We can then start to work our way back up the sub-tries to the root.
            # If all values in this sub-trie are None, that means there are no further words branching from
            # this point and we can remove this sub-trie.
            return all(val is None for val in sub_trie)
        
        # We can check if this character has been inserted into this sub-trie
        if sub_trie[current_index] is None:
            # If it hasn't been inserted, simply exit
            return False

        # If it has been inserted, we can continue down this sub-trie on the next character
        if self.__delete_aux(sub_trie[current_index], word, char_index + 1):
            # If the sub-trie can be safely deleted, then set it to None, and continue back up the sub-tries
            sub_trie[current_index] = None

            return all(val is None for val in sub_trie)
        else:
            return False


    def char_to_index(self, char):
        
        if char == self.terminating_char:
            return 0
        
        index = ord(char) - ord('a') + 1
        
        return index


class TestProblem3(unittest.TestCase):

    def setUp(self):
        self.structure = Problem3()
        self.word_list = ["hello", "word", "hey", "wonder", "wordle", "open", "opportunity", "opportunities",
                            "yes", "maybe", "close", "closer", "closest", "wow", "sever", "serve", "several",
                            "severe", "severance"]
        self.not_included_words = ["not", "in", "the", "data", "structure", "closes"]


    def test_insert(self):

        # general smoke test
        for word in self.word_list:
            self.structure.insert(word)


    def test_search(self):
        
        # insert words into structure
        for word in self.word_list:
            self.structure.insert(word)

        # check each word was inserted successfully returns True
        for word in self.word_list:
            self.assertTrue(self.structure.search(word))

        # check words that were not inserted return False
        for word in self.not_included_words:
            self.assertFalse(self.structure.search(word))


    def test_delete(self):
        
        # insert words into structure
        for word in self.word_list:
            self.structure.insert(word)

        # delete all words
        for word in self.word_list:
            self.structure.delete(word)

        # we should be left with a list of Nones
        self.assertTrue(all(val is None for val in self.structure.words))

        # insert two similar words, one a prefix of the other
        self.structure.insert("present")
        self.structure.insert("presentation")

        # deleting one should not delete the other
        self.assertTrue(self.structure.search("present"))
        self.assertTrue(self.structure.search("presentation"))
        
        self.structure.delete("present")
        
        self.assertFalse(self.structure.search("present"))
        self.assertTrue(self.structure.search("presentation"))

    
    def test_time_complexity(self):
        
        # creating a set of words 100, 200, 300 ... 900 characters long
        increasing_word_list = ['a' * 100*n for n in range(1, 10)]
        
        # inserting each word and printing the time taken per word
        for i in range(len(increasing_word_list)):
            start_time = timeit.default_timer()

            self.structure.insert(increasing_word_list[i])

            end_time = timeit.default_timer()
            time_dif = end_time - start_time

            print(f"Inserting word {(i + 1) * 100} characters long: {time_dif * 10**3} ms.")

        print()

        # searching for each word and printing the time taken per word
        for i in range(len(increasing_word_list)):
            start_time = timeit.default_timer()

            self.structure.search(increasing_word_list[i])

            end_time = timeit.default_timer()
            time_dif = end_time - start_time

            print(f"Searching for word {(i + 1) * 100} characters long: {time_dif * 10**3} ms.")

        print()

        # deleting each word and printing the time taken per word
        for i in range(len(increasing_word_list)-1, -1, -1):
            start_time = timeit.default_timer()

            self.structure.delete(increasing_word_list[i])

            end_time = timeit.default_timer()
            time_dif = end_time - start_time

            print(f"Deleting word {(i + 1) * 100} characters long: {time_dif * 10**3} ms.")


if __name__ == "__main__":
    unittest.main()

"""
Technical Question 3
Monash Motorsport Intake Semester 1, 2022

Author: Harpo Barrett
Last Modified: 20/02/2022
"""

import unittest


class Problem3:
    # assuming all words entered are non-empty strings with no spaces, using only lowercase characters a-z

    # effectively, this is a prefix trie

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

        # If we have reached the end of the word (indicated by a \0 character), place a \0 character and exit.
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
        
        # First determine what character we are currently inserting, and its lexographical index
        current_char = word[char_index]
        current_index = self.char_to_index(current_char)

        # If we have reached the end of the word (indicated by a \0 character)
        if current_char == self.terminating_char:
            # Return True if the word is in the sub-trie (indicated by a \0), and False otherwise
            return sub_trie[0] is not None
        
        # We can check if this character has been inserted into this sub-trie
        if sub_trie[current_index] is None:
            return False
        
        # If it has been inserted, keep searching that sub-trie for the next character
        return self.__search_aux(sub_trie[current_index], word, char_index + 1)



    def delete(self, word):
        pass


    def char_to_index(self, char):
        
        if char == self.terminating_char:
            return 0
        
        index = ord(char) - ord('a') + 1
        
        return index


if __name__ == "__main__":
    word_list = ["hello", "word", "hey", "wonder", "wordle", "open", "opportunity", "opportunities"]

    increasing_word_list = ['a' * 10**n for n in range(10)]

    problem = Problem3()

    for word in word_list:
        problem.insert(word)

    print(problem.search("hello"))
    print(problem.search("words"))
    print(problem.search("ope"))
    print(problem.search("opportunities"))
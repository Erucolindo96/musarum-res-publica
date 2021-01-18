import re
import sqlite3
import string
from typing import List
import morfeusz2


class InterpellationTextProcessor:
    CHARS_ENDING_SENTENCE = '.,?!\n\r'
    POLISH_LETTERS = 'aąbcćdeęfghijklłmnńoópqrsśtuvwxyzźż' \
                     'AĄBCĆDEĘFGHIJKLŁMNŃOÓPQRSŚTUVWXYZŹŻ'

    def __init__(self, database_path: str, interpellation_batch: int):
        self.database_path_ = database_path
        self.interpellation_batch_ = interpellation_batch

    def process_interpellation_content(self):
        with sqlite3.connect(self.database_path_) as database:
            cur = database.cursor()
            cur.execute('SELECT id, content FROM interpellation')

            has_next_row = True
            while has_next_row:
                interpellations = cur.fetchmany(self.interpellation_batch_)
                for inter in interpellations:
                    (id, content) = (inter[0], inter[1])

                    proper_names = InterpellationTextProcessor.find_proper_names(content)
                    proper_names = InterpellationTextProcessor.omit_interpellation_greetings(proper_names)
                    lemmas = InterpellationTextProcessor.to_lemmas(proper_names)

                    processed_content = ','.join(lemmas)
                    cur.execute('UPDATE interpellation SET processed_content=? WHERE id = ?', (processed_content, id))

                has_next_row = bool(interpellations)
            database.commit()

    @staticmethod
    def find_proper_names(content: str) -> List[str]:
        words = content.split(' ')
        words = InterpellationTextProcessor.clean_words(words)

        proper_names = []
        i = 0

        while i < len(words):
            upper_case = InterpellationTextProcessor.return_uppercase_phrase(words, i)
            if upper_case:
                i += len(upper_case) - 1  # change iterator on next after upper case phrase
                proper_names.append(' '.join(upper_case))

            i += 1

        for char in InterpellationTextProcessor.CHARS_ENDING_SENTENCE:
            proper_names = [name.replace(char, '') for name in proper_names]

        return proper_names

    @staticmethod
    def omit_interpellation_greetings(proper_names: List[str]):
        # 3 last phrases are greetings to receiver: "z powazaniem", "Andrzej Górski", "Warszawa" - should be omit
        return proper_names[0:-3]

    @staticmethod
    def clean_words(words: List[str]) -> List[str]:
        # remove all not literal and dot spaces
        cleaned_words = []

        chars_to_leave = InterpellationTextProcessor.POLISH_LETTERS + InterpellationTextProcessor.CHARS_ENDING_SENTENCE + string.digits
        for word in words:
            replaced = ''.join([char for char in word if char in chars_to_leave])
            cleaned_words.append(replaced)
        return cleaned_words

    '''
    Method will recursively find upper case phrase - proper name in polish.
    Break getting upper case words when find dot at end of word
    '''

    @staticmethod
    def return_uppercase_phrase(words: List[str], i) -> List[str]:
        upper_case_words = []
        word = words[i] if i < len(words) else None

        if word and word[0].isupper():
            upper_case_words.append(word)

            next_upper_cases = None
            # last char is '.,?!\n\r' -> have end of sentence -> end of proper_names
            if not word[-1:] in InterpellationTextProcessor.CHARS_ENDING_SENTENCE:
                next_upper_cases = InterpellationTextProcessor.return_uppercase_phrase(words, i + 1)
            if next_upper_cases:
                upper_case_words.extend(next_upper_cases)

        return upper_case_words


    @staticmethod
    def to_lemmas(words: List[str]) -> List[str]:
        lemmas = []
        morf = morfeusz2.Morfeusz(praet='composite')

        for phrase in words:

            analysis = morf.analyse(phrase)
            lemmatized_phrase = []
            words_in_phrase = len(phrase.split(' '))

            for word_num in range(words_in_phrase):
                # find analyse rows for current word in phrase
                word_spelling = [spell for spell in analysis if spell[0] == word_num]
                # get first base form of word in analizing rows
                _, _, (_, base, _, _, _) = word_spelling[0]
                if ':' in base:
                    lemmatized_phrase.append(re.findall('(.*):', base)[0])
                else:
                    lemmatized_phrase.append(base)
            lemmas.append(" ".join(lemmatized_phrase))

        return lemmas

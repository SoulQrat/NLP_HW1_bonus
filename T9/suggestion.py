from typing import List, Union
import re
from numpy import argmax

def tokenize(message):
    tokens = re.findall(r'\w+|[^\w\s]', message.lower())
    return tokens

class PrefixTreeNode:
    def __init__(self):
        self.children: dict[str, PrefixTreeNode] = {}
        self.is_end_of_word = False

class PrefixTree:
    def __init__(self, vocabulary: List[str]):
        """
        vocabulary: список всех уникальных токенов в корпусе
        """
        self.root = PrefixTreeNode()
        for word in vocabulary:
            self._add_word(word)

    def search_prefix(self, prefix) -> List[str]:
        """
        Возвращает все слова, начинающиеся на prefix
        prefix: str – префикс слова
        """
        curr = self.root
        for c in prefix:
            if c not in curr.children:
                return []
            curr = curr.children[c]
        return self._dfs(curr, prefix)

    def _add_word(self, word: str):
        curr = self.root
        for c in word:
            if c not in curr.children:
                curr.children[c] = PrefixTreeNode()
            curr = curr.children[c]
        curr.is_end_of_word = True  

    def _dfs(self, node, prefix):
        res = []
        if node.is_end_of_word:
            res.append(prefix)
        for c, child in node.children.items():
            res.extend(self._dfs(child, prefix + c))
        return res
    
class WordCompletor:
    def __init__(self, corpus):
        """
        corpus: list – корпус текстов
        """
        self.vocabulary = {}
        self.words_count = 0
        for text in corpus:
            for word in text:
                self.words_count += 1
                self.vocabulary[word] = self.vocabulary.get(word, 0) + 1
        self.prefix_tree = PrefixTree(list(self.vocabulary.keys()))

    def get_words_and_probs(self, prefix: str) -> (List[str], List[float]):
        """
        Возвращает список слов, начинающихся на prefix,
        с их вероятностями (нормировать ничего не нужно)
        """
        words, probs = [], []
        words = self.prefix_tree.search_prefix(prefix)
        probs = [self.vocabulary[word] / self.words_count for word in words]
        return words, probs
    
class NGramLanguageModel:
    def __init__(self, corpus, n):
        self.n = n
        self.ngrams = {}
        self.counter = {}
        for text in corpus:
            for i in range(len(text) - n):
                prefix = tuple(text[i:i+n])
                word = text[i+n]
                if prefix not in self.ngrams:
                    self.ngrams[prefix] = {}
                self.ngrams[prefix][word] = self.ngrams[prefix].get(word, 0) + 1
                self.counter[prefix] = self.counter.get(prefix, 0) + 1

    def get_next_words_and_probs(self, prefix: list) -> (List[str], List[float]):
        """
        Возвращает список слов, которые могут идти после prefix,
        а так же список вероятностей этих слов
        """
        next_words, probs = [], []
        ngrams = self.ngrams.get(tuple(prefix[-self.n:]), {})
        next_words_count = self.counter.get(tuple(prefix[-self.n:]), 1)
        next_words = list(ngrams.keys())
        probs = [count / next_words_count for count in ngrams.values()]
        return next_words, probs

class TextSuggestion:
    def __init__(self, word_completor, n_gram_model):
        self.word_completor = word_completor
        self.n_gram_model = n_gram_model

    def suggest_text(self, text: Union[str, list], n_words=3, n_texts=1) -> list[list[str]]:
        """
        Возвращает возможные варианты продолжения текста (по умолчанию только один)
        
        text: строка или список слов – написанный пользователем текст
        n_words: число слов, которые дописывает n-граммная модель
        n_texts: число возвращаемых продолжений (пока что только одно)
        
        return: list[list[srt]] – список из n_texts списков слов, по 1 + n_words слов в каждом
        Первое слово – это то, которое WordCompletor дополнил до целого.
        """
        suggestions = [[]]

        if type(text) == str:
            text = [text]

        words, probs = self.word_completor.get_words_and_probs(text[-1])
        text[-1] = words[argmax(probs)]
        suggestions[-1].append(text[-1])

        for _ in range(n_words):
            next_words, probs = self.n_gram_model.get_next_words_and_probs(text)
            text.append(next_words[argmax(probs)])    
            suggestions[-1].append(text[-1])

        return suggestions
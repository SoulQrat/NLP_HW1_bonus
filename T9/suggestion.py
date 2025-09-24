from typing import List, Union
import re
from numpy import argmax, argsort


def tokenize(message):
    tokens = re.findall(r"[a-zA-Z]+", message.lower())
    return tokens

class PrefixTreeNode:
    def __init__(self):
        self.children: dict[str, PrefixTreeNode] = {}
        self.is_end_of_word = False

class PrefixTree:
    def __init__(self, vocabulary: List[str]):
        self.root = PrefixTreeNode()
        for word in vocabulary:
            self._add_word(word)

    def search_prefix(self, prefix) -> List[str]:
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
        dummy = {}
        self.words_count = 0
        for text in corpus:
            for word in text[:4]:
                self.words_count += 1
                dummy[word] = dummy.get(word, 0) + 1
        self.vocabulary = {k: v for k, v in dummy.items() if v > 5}
        self.prefix_tree = PrefixTree(list(self.vocabulary.keys()))

    def get_words_and_probs(self, prefix: str) -> (List[str], List[float]):
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

    def suggest_word(self, text: list, n_texts=1) -> list[str]:
        suggestions = []

        words, probs = self.word_completor.get_words_and_probs(text[-1])
        if len(probs) == 0:
            return suggestions
        
        for idx in argsort(probs)[::-1][:n_texts]:
            suggestions.append(words[idx]) 

        return suggestions

    def suggest_text(self, text: list, n_words=3, n_texts=1) -> list[str]:
        suggestions = []
    
        next_words, probs = self.n_gram_model.get_next_words_and_probs(text)
        if len(probs) == 0:
            return suggestions

        for idx in argsort(probs)[::-1][:n_texts]:
            tmp = text.copy()
            for _ in range(n_words):
                if idx > len(next_words):
                    break
                tmp.append(next_words[idx])
                next_words, probs = self.n_gram_model.get_next_words_and_probs(tmp)
                if len(probs) == 0:
                    break
                idx = argmax(probs)
            suggestions.append(tmp[-n_words:])

        return suggestions
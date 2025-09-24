import reflex as rx
from typing import List
from suggestion import TextSuggestion, WordCompletor, NGramLanguageModel, tokenize
import dill
import pandas as pd

with open('/Users/soulqrat/Workspace/NLP_HW1/n_gram_model.dill', 'rb') as f:
    n_gram_model: NGramLanguageModel = dill.load(f)

emails = pd.read_csv('/Users/soulqrat/Workspace/NLP_HW1/emails_clean.csv')
emails['clear_message'] = emails['clear_message'].fillna('')
emails['tokens'] = emails['clear_message'].apply(tokenize)
corpus = emails['tokens'].to_list()
word_completor = WordCompletor(corpus)
text_suggestion = TextSuggestion(word_completor, n_gram_model)

class State(rx.State):
    text: str = ''
    text_suggestions: List[str] = []
    word_suggestions: List[str] = []
    
    def _update_word_suggestions(self):
        self.word_suggestions = []
        if self.text == '':
            return
        tokens = tokenize(self.text)
        self.word_suggestions = text_suggestion.suggest_word(tokens, n_texts=3)

    def _update_text_suggestions(self):
        self.text_suggestions = []
        if self.text == '':
            return
        tokens = tokenize(self.text)
        self.text_suggestions = [' '.join(tmp) for tmp in text_suggestion.suggest_text(tokens, n_words=1, n_texts=3)]

    def _update_suggestions(self):
        self._update_word_suggestions()
        self._update_text_suggestions()

    def update_field(self, new_text: str):
        self.text = new_text
        self._update_suggestions()
    
    def apply_text_suggestion(self, suggestion: str):
        self.text += ' ' if self.text[-1] != ' ' else '' + suggestion
        self._update_suggestions()

    def apply_word_suggestion(self, suggestion: str):
        words = self.text.split(' ')
        words[-1] = suggestion
        self.text = ' '.join(words)
        self._update_suggestions()

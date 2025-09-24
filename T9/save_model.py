import pandas as pd
import joblib
from suggestion import tokenize, WordCompletor, NGramLanguageModel, TextSuggestion
import re

emails = pd.read_csv('/Users/soulqrat/Workspace/NLP_HW1/emails_clean.csv')[:1000]
emails['clear_message'] = emails['clear_message'].fillna('')
emails['tokens'] = emails['clear_message'].apply(tokenize)
corpus = emails['tokens'].to_list()

word_completor = WordCompletor(corpus)
n_gram_model = NGramLanguageModel(corpus, n=2)
text_suggestion = TextSuggestion(word_completor, n_gram_model)

joblib.dump(text_suggestion, "text_suggestion.joblib")
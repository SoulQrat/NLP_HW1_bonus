import pandas as pd
import dill
from suggestion import tokenize, WordCompletor, NGramLanguageModel, TextSuggestion

emails = pd.read_csv('/Users/soulqrat/Workspace/NLP_HW1/emails_clean.csv')
emails['clear_message'] = emails['clear_message'].fillna('')
emails['tokens'] = emails['clear_message'].apply(tokenize)
corpus = emails['tokens'].to_list()

n_gram_model = NGramLanguageModel(corpus, n=2)
with open('n_gram_model.dill', 'wb') as f:
    dill.dump(n_gram_model, f)
__author__ = 'ssbushi'

import nltk
from nltk.corpus import treebank

train_data = treebank.tagged_sents()[:3000]

print train_data[0]

from nltk.tag import hmm

trainer = hmm.HiddenMarkovModelTrainer()
tagger = trainer.train_supervised(train_data)

print tagger

print tagger.tag("Alex was born in New York .".split())

print tagger.tag("Joe met Joanne in Delhi .".split())

print tagger.tag("Chicago is the birthplace of Ginny".split())



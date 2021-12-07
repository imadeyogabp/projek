import os
import re
import sys
import requests
import operator
import time
from requests.api import request
from termcolor import colored

from Sastrawi.Stemmer.StemmerFactory import StemmerFactory
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from flask import request

factory = StemmerFactory()
stemmer = factory.create_stemmer()

def load_stopWords():
	url = "https://raw.githubusercontent.com/Wayan123/Sentiment-Analysis/main/stopwordlist.txt"
	ina_stopword = requests.get(url).content
	return ina_stopword.split()

stopwords = load_stopWords()

def cleanData(sentence):
	ret = []
	sentence = stemmer.stem(sentence)	
	for word in sentence.split():
		if not word in stopwords:
			ret.append(word)
	return " ".join(ret)

def getVectorSpace(cleanSet):
	vocab = {}
	for data in cleanSet:
		for word in data.split():
			vocab[data] = 0
	return vocab.keys()

def calculateSimilarity(sentence, doc):
	if doc == []:
		return 0
	vocab = {}
	for word in sentence:
		vocab[word] = 0
	
	docInOneSentence = '';
	for t in doc:
		docInOneSentence += (t + ' ')
		for word in t.split():
			vocab[word]=0	
	
	cv = CountVectorizer(vocabulary=vocab.keys())

	docVector = cv.fit_transform([docInOneSentence])
	sentenceVector = cv.fit_transform([sentence])
	return cosine_similarity(docVector, sentenceVector)[0][0]

# with open('sum.txt') as f:
#   texts = [line.rstrip('\n') for line in f]


def process():
    if request.method == 'POST':
        texts = [request.form['text']]

        sentences = []
        clean = []
        originalSentenceOf = {}

        #Data cleansing
        for line in texts:
            cl = cleanData(line)
            sentences.append(line)
            clean.append(cl)
            originalSentenceOf[cl] = line

        setClean = set(clean)

        scores = {}
        for data in clean:
            temp_doc = setClean - set([data])
            score = calculateSimilarity(data, list(temp_doc))
            scores[data] = score

        n = 20 * len(sentences) / 100

        alpha = 0.5
        summarySet = []
        while n > 0:
            mmr = {}

            for sentence in scores.keys():
                if not sentence in summarySet:
                    mmr[sentence] = alpha * scores[sentence] - (1-alpha) * calculateSimilarity(sentence, summarySet)	
            selected = max(mmr.items(), key=operator.itemgetter(1))[0]	
            summarySet.append(selected)
            n -= 1

        return {
            'results': sentence
        }
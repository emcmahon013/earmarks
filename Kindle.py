import pandas as pd 
import nltk
import os 
from string import punctuation
import json 

class kindle_highlights(object):
	def __init__(self,__file__,words,book):
		json_data = open(__file__).read()
		self.highlight_text = json.loads(json_data)
		self.loc = {}
		self.loc = self.find_highlights(words,book)

	def find_h(self,h,words):
		indicies = [i for i, x in enumerate(words) if x == h[0]]
		l = len(h)
		for ind in indicies:
			if words[ind:ind+l] == h:
				return ind,ind+l
		for w in range(l):
			try:
				int(h[w])
				ind1, ind2 = self.find_h(h[0:w-1],words)
				return ind1, ind1+l+2
			except:
				pass
		print('Error: Cannot find highlights: '+str(h))
		return 

	def find_highlights(self,words,book):
		for key in self.highlight_text:
			h = self.highlight_text[key]
			h = h.replace('-',' ')
			h = ''.join(w for w in h if w not in punctuation)
			h = h.split()
			ind1, ind2 = self.find_h(h,words)
			quote_start = book.iloc[ind1]
			quote_end = book.iloc[ind2]

			start = quote_start['start']
			end = quote_end['end']
			self.loc[key] = (start,end)
		assert len(self.loc) == len(self.highlight_text)
		return self.loc




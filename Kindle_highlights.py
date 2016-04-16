import pandas as pd 
import nltk
import os 
from string import punctuation
import json 

class kindle_highlights:
	def __init__(self,__file__,words,book):
		json_data = open(__file__).read()
		self.highlight_text = json.loads(json_data)
		self.loc = []
		#self.loc = self.find_highlights(words,book)

	def find_h(self,h,words):
		indicies = [i for i, x in enumerate(words) if x == h[0]]
		l = len(h)
		for ind in indicies:
			if words[ind:ind+l] == h:
				return ind
		number = False
		for w in range(l):
			try:
				int(h[w])
				number = True
				ind = self.find_h(h[0:w-1],words)
				return ind
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
			ind = self.find_h(h,words)
			line = book.iloc[ind]
			start = line['start']
			end = line['end']
			self.loc.append((start,end))
			print(self.loc)
			return self.loc




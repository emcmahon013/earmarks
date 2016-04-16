"""WhisperHighlight. Allows users to higlight their own passages while listening.
Usage:
  WhisperHighlight <book> <time> [--version=<clean>]
"""

import pandas as pd 
import numpy as np 
from pydub import AudioSegment
import nltk
import os, sys
from docopt import docopt
import json
from string import punctuation
from Kindle import kindle_highlights
from AudibleSound import sound_overlay
from WhisperSync import highlight_sync

class highlight_find:
	def __init__(self,mp3,book):
		self.audio = AudioSegment.from_mp3(mp3)
		self.book = book

	def hit(self,milli_sec,back=60,forward=2):
		sec = milli_sec / 1000
		word_ind = book['start'][(book['start']-sec).abs().argsort()].index[0]
		word = book['word'][word_ind].replace(" ","")
		if word_ind >= back and len(book)-word_ind >=2:
			text = "".join(book['word'][word_ind-back:word_ind+forward])
		elif word_ind < back:
			text = "".join(book['word'][0:word_ind+forward])
		elif len(book)-word_ind >=2:
			text = "".join(book['word'][word_ind-back:])
		else:
			print('Error in finding audio file')
			return
		words = nltk.word_tokenize(text)
		tree = nltk.ne_chunk(nltk.pos_tag(words))
		sent_ = []
		for i in range(len(tree)):
			try:
				tree[i].label()
			except AttributeError:
				if tree[i][0][0].isupper() and tree[i][0]!=word and tree[i][1] != 'NNP':
					sent_.append((i,tree[i][0]))
				elif tree[i][0] == word:
					mid = i
		sent_end = min(sent_,key=lambda x:abs(x[0]-mid))
		sent_start = sent_[sent_.index(sent_end)-1]
		for i in range(word_ind-sent_start[0]-5,word_ind):
			#print(i)
			#print(book['word'][i],sent_start[1])
			#print(book['word'][i],sent_end[1])
			if book['word'][i].replace(" ","") == sent_start[1]:
				clip_start = i
			elif book['word'][i].replace(" ","") == sent_end[1]:
				clip_end = i 
		loc = (book['start'][clip_start],book['end'][clip_end])
		start = 0
		end = len(text)
		count = 0
		for s in sent_:
			end = text[start:].find(s[1])
			if start+end > 2:
				text = text[0:start+end-1]+'. '+text[start+end:]
			start = start+end + 5
			end = len(text)
			count +=1
			if s == sent_start:
				sent_num = count
		sent = nltk.sent_tokenize(text)
		sent_text = sent[sent_num].upper()
		leading_text = " ".join(sent[sent_num-1].split()[-3:])
		lagging_text = " ".join(sent[sent_num+1].split()[0:2])
		new_text = "..."+leading_text + sent_text + lagging_text+"..."
		return new_text, loc, clip_start 

if __name__ == "__main__":
	args = docopt(__doc__)
	#time = 839532
	time = int(args['<time>'])
	print(time)
	wsync = './'+str(args['<book>'])+'/text2word.sync'
	hjson = './'+str(args['<book>'])+'/highlights.json'
	if args['--version'] == None or args['--version'] == 'clean':
		mp3 = './'+str(args['<book>'])+'/audio.mp3'
	else:
		mp3 = './'+str(args['<book>'])+'/audio_AA.mp3'
	hs = highlight_sync(wsync,mp3,hjson)
	book = hs.import_sync(wsync)
	hf = highlight_find(mp3,book)
	audio_text, loc, ind  = hf.hit(time)
	print(audio_text)
	print(loc)
	print(ind)
	json_data = open('./'+str(args['<book>'])+'/my_highlights.json').read()
	my_highlights = json.loads(json_data)
	print(my_highlights)
	my_highlights[ind] = {'text':audio_text,'loc':loc}
	with open('./'+str(args['<book>'])+'/my_highlights.json','w') as fp:
		json.dump(my_highlights,fp)









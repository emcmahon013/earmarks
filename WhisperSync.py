"""WhisperSync. Pulls Amazon Kindle's most commonly highlighted passages
Usage:
  WhisperSync <book>
"""

import pandas as pd 
import numpy as np 
from pydub import AudioSegment
import nltk
import os, sys
from docopt import docopt
from string import punctuation
from Kindle import kindle_highlights
from AudibleSound import sound_overlay

class highlight_sync():
	def __init__(self,wsync,mp3,hjson):
		self.loc = self.locate_highlight(wsync,hjson) 

	def import_sync(self,__file__):
		book = pd.read_csv(__file__,delimiter=":",header=None)
		del book[0]
		book.columns = ['text_start','text_end','start','end','word']
		return book

	def book_text(self,book):
		text = "".join(book['word'])
		words = text.split()
		return words

	def locate_highlight(self,wsync,hjson):
		book = self.import_sync(wsync)
		words = self.book_text(book)
		kh = kindle_highlights(hjson,words,book)
		return kh.loc

	def augment_audio(self,mp3,audio_loc):
		SO = sound_overlay('highlight_sound.wav',volume=3)
		for s in audio_loc:
			audio = SO.sound_slice(mp3,audio_loc[s])
		return audio


if __name__ == "__main__":
	args = docopt(__doc__)
	wsync = './'+str(args['<book>'])+'/text2word.sync'
	hjson = './'+str(args['<book>'])+'/highlights.json'
	mp3 = './'+str(args['<book>'])+'/audio.mp3'
	hs = highlight_sync(wsync,mp3,hjson)
	print(hs.loc)
	audio = hs.augment_audio(mp3,hs.loc)
	audio.export(str(mp3[:-4])+"_AA.mp3","mp3")

	



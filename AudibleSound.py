"""AudibleSound. Creates audio clips with highlighted sections.
Usage:
  AudibleSound <book> <clip> [--volume=<K>]
"""


import pandas as pd 
from pydub import AudioSegment
import os 
from docopt import docopt

class sound_overlay:
	def __init__(self,background,volume=0,offset=2,silent=1):
		self.background = AudioSegment.from_wav(background)
		self.offset = offset
		self.volume = volume
		self.silent = silent

	def sound_slice(self,audio_file,clip):
		audio = AudioSegment.from_mp3(audio_file)
		#audio = audio[(clip[0]-11)*1000:(clip[1]+3)*1000]
		start = (clip[0] - self.offset)*1000
		end = (clip[1] - self.offset)*1000
		#start = (11 - self.offset)*1000
		#end = start + (clip[1]-clip[0]-self.offset)*1000
		highlight = audio[start:end]+self.volume
		#peak_amplitude = book.max 
		#highlight = book[start:end]+peak_amplitude
		#pause = AudioSegment.silent(duration=self.silent*1000)
		if len(self.background) < len(highlight):
			plus = len(highlight)/len(self.background)
			highlight_ = highlight.overlay(self.background,times=plus)
		else:
			highlight_ = highlight.overlay(self.background)
		assert len(highlight_) == len(highlight)
		#highlight_.export('highlight.mp3','mp3')
		#new_slice = pause + highlight_ + pause
		audio = audio[:start]+highlight_+audio[end:]
		#audio = audio[(clip[0]-11)*1000:(clip[1]+3)*1000]
		return audio 

if __name__ == "__main__":
	args = docopt(__doc__)
	#loc = {'3759': (27470.942999999999, 27484.382000000001), '272': (675.22399999999993, 685.73300000000006), '273': (715.74399999999991, 728.13300000000004), '828': (5084.8230000000003, 5100.732), '8397': (62356.584999999999, 62363.784000000007), '3226': (23425.607000000004, 23435.175999999999), '223': (173.34400000000002, 201.94299999999998), '8309': (61611.184999999998, 61622.164000000004), '8404': (62411.964999999997, 62423.684000000001)}
	#mp3 = 'The_Innovators.mp3'
	mp3 = './'+str(args['<book>'])+'/audio.mp3'
	SO = sound_overlay('highlight_sound.wav',volume=3)
	#val = '272'
	#clip = loc[val]
	audio = SO.sound_slice(mp3,clip)
	audio.export("highlight_272.mp3","mp3")
	audio = audio[(clip[0]-11)*1000:(clip[1]+3)*1000]
	audio.export("highlight_"+str(val)+"_clip_2.mp3","mp3")




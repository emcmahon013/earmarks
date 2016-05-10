# earmarks: higlighting for the audible experience


### This project was created as part of the Audible Hackathon in NYC (Spring 2016).

<br>
_abstract:_ 

The audible experience allows users to experience books in an unparalleled manner.  Listeners can become surrounded in a new world during their daily commute or on long road trips.  While the experience is immersive, it is also a passive one where listeners can feel isolated and distracted while multi-tasking.  However, with Earmarks, users can "tune" back in to important passage and engage more by highlighting passages and sharing with friends.  

<br>
_earmarks also users to:_

1. read commonly-highlighted passages.  This is a current feature for Kindle users that can draw attention to important passages.  Even more than reading, this can be important for drawing attention back to the audible book.  

2. highlight their own passages.  This would allow listeners to earmark/highlight their own passages.  It anchors the time by input "<time>" which would be signaled by the external app. It finds the sentence prior to the click and sets that sentence as the highlight, which can be altered by the listener afterwards.  This highlight is then saved and can be shared with the listener's network.  

for our full presentation, see earmarks.pdf

<br> 
_this repo includes:_

* presentation (earmarks.pdf) + [UX video](https://vimeo.com/163105137)
* WhipserHighlight: method to hear previously highlighted text
* WhisperSync: method to "higlight" text while listening


Usage:

	python WhisperSync.py <book>

	python WhisperHighlight.py <book> <time> 




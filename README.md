dark side
============
a response-comparing proxy server made of pure evil

you can use it to test out a new apprentice, to make sure it responds to all queries the same way master does.

##setup
use pip:

    pip install dark-side

or clone this repo, then run:

    pip install -r requirements.txt
    python setup.py install


##usage

suppose you have an existing api at api.legitimate-business.com, and you want to test the new api, at new-api.legitimate-business.com. it'd be a shame if that new api had problems, wouldn't it?  lucky for you, the dark side will train this new apprentice:

run

`python darkside.py api.legitimate-business.com --apprentice new-api.legitimate-business.com`

and darkside will listen on port 8987 (change that with --port). 

when you request localhost:8987/some/resource, darkside will fetch both api.legitimate-business.com/some/resource and new-api.legitimate-business.com/some/resource, and compare the two. if they are different, darkside will make an entry in darkside-mismatch.log as well as print to the console. darkside will always return the response given by the master, regardless of what those apprentices say. this way, you can test apprentice respones to real requests!

there's no limit to the number of apprentices you can take on - but don't go crazy, those guys get annoying when they're all "master master, please tell me more divine secrets" all the time. 


namaste




# beeble
An attempt to make version of Wordle for the BBC Micro.


## Part 1 - word list
How do I get over 5000 words into a nice neat (but indexable) list that can be used to choose a word?
This will be a bit of python to minimise the size of the wordlist so it can be scanned quickly to generate the target word.

I think the wordlist at [www-cs-faculty.stanford.edu/~knuth/sgb-words.txt](https://www-cs-faculty.stanford.edu/~knuth/sgb-words.txt) - 5757 words - will do it.

That said, the (original) Wordle word list is [here](https://gist.github.com/scholtes/94f3c0303ba6a7768b47583aff36654d)

It hadn't struck me that the number of guessable words would be a superset of the available puzzle words. That means two sets of words would need to be created - one for creating the puzzle (that'll be the 5757 words) and another list of additional words that are allowed to be guessed. All of this would need to fit into - say - 10kB of memory. Let's see if that's possible.

### Algorithm

To minimise the storage of the words I need both to build a working compression and the scanning algorithm; the former will be done in Python, and before I start the BBC Micro part, I'll write some code to scan/decompress and validate it.

My initial idea for an algorithm was to compress the words into a byte stream that could be scanned through and a word alighted upon. This would be fine for choosing a word, but to validate a guess, it would need for the whole wordlist to be checked, which could take quite a while. However, it might still be possible. 

My second idea is to create (for each wordlist) an index of (for puzzle words) how many words per letter, so that the random factor can discern which letter to jump to, and for both puzzle and guessable words, a number of bytes to skip to get to the next initial letter. Then the remaining four letters of each word would need to be stored. Let's see how that goes.

#### Analysis
Of the 5757 puzzle words and 7355 guessable words, there were between 4 and 847 words in each set of initials. 
This would suggest a two-byte (or possibly 10 bit if we want to be overly efficient) field is required for quantity.

If the words are sorted in alphabetical order:
Over 95% of the second letters of the words are the same as the preceding word
Over 66% of the second and third letters of the words are the same as the preceding word
Between 19% and 25% of the second, third and fourth letters of the words are the same as the preceding word

Starting each initial at a particular byte address offers the ability to create a 5 bit stream of words. 
5 byte codes:
31 (11111) new word and the second and third and fourth letters are the same as the previous word
30 (11110) new word and the second and third letters are the same as the previous word
29 (11101) new word and the second letter is the same as the previous word
28 (11100) new word and no letters are the same as the previous word

This is quite convenient since the three left-most bits designate a new word, and the rightmost bits designate how many letters there are from the previous word

25-0 standard alphabetical letters

Which just leaves 27 and 26
These could be used for letter pairs - here's the frequency of letter pairs excluding those matching previous words:

ed: 240
es: 203
as: 167
os: 140
.
.

'ed' and 'es' are good candidates to save a little space (about 276 bytes.. not really much in the grand scheme of things, I suppose)

27: ed
26: es

## Part 2 - the game
This may have two sub parts.

### Part 2a - the selection
I wonder if I can write this in assembly so it's quick and simple, and can store the word in 5 bytes of memory ready to be sought.

The search for guessable words cane be done using a similar algorithm.


### Part 2b - the game
This bit is easy (in theory). I'm thinking mode 7 easy. But that's easier said (in theory) than done (in practice).

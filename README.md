# beeble
An attempt to make version of Wordle for the BBC Micro.


## Part 1 - word list
How do I get over 5000 words into a nice neat (but indexable) list that can be used to choose a word?
This will be a bit of python to minimise the size of the wordlist so it can be scanned quickly to generate the target word.

I think the wordlist at [www-cs-faculty.stanford.edu/~knuth/sgb-words.txt](https://www-cs-faculty.stanford.edu/~knuth/sgb-words.txt) - 5757 words - will do it.

## Part 2 - the game
This may have two sub parts.

### Part 2a - the selection
I wonder if I can write this in assembler so it's quick and simple, and can store the word in 5 bytes of memory ready to be sought.

### Part 2b - the game
This bit is easy (in theory). I'm thinking mode 7 easy. But that's easier said (in theory) than done (in practice).

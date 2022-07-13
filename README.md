# wordle-solver
Solver for the NY Times' Wordle game

## Installing

From the root directory of the project, run `python -m pip install -e .`.

## Usage

The `WORDS` constant is the master word list.
```python
>>> from wordle import *
>>> WORDS
['abaci', 'aback', 'abaft', 'abase', ..., 'zoned', 'zones', 'zooms', 'zorch']
```

The `compare` function creates a pattern showing the match of a guess to an
'answer'. The wordle game uses colored tiles, the solver uses ascii characters. 
An underscore means the letter is not in the word, an asterisk marks the
correct letter in the wrong place, and an octothorp shows the correct letter
in the correct place.

```python
>>> # Guessing 'pride' when the solution is 'night'.
>>> # There is no P, R, D, or E, and the I is not in the 3rd place.
>>> compare('pride', 'night')
'__*__'
```

The `filter2` function reduces a candidate word list by the response to a
guess. This can be the input and output of a guess in the website if you were
to cheat, which you shouldn't.

```python
>>> words = filter2('pride', '__*__')
>>> # Filter words from the previous result by another guess and response.
>>> # The word must end with 'IGHT'.
>>> words = filter2('fight', '_####', words)
>>> words
['bight', 'light', 'might', 'night', 'sight', 'tight', 'wight']
```

So, how to use the solver to determine the next guess? The `score` function
rates a guess by how likely it is to reduce the number of candidate words.
The score of a word is the average number of words remaining from a list
of candidates, given the word as a guess. A lower score means the guess is
more effective at converging on a solution. The score can be used to sort
or pick words from the list.
```python
>>> # We sort all possible words (`WORDS`) by how well they will filter our
>>> # remaining candidates from the previous section (`words`)
>>> sorted(WORDS, key=lambda word: score(word, words))
['balms', 'bawls', 'blown', 'blows', 'bowls', 'lambs', 'lawns', 'limbs', ...]
>>> # On average, guessing 'balms' will reduce the list to one or two options
>>> score('blown', words)
1.8571428571428572
>>> # Guessing a word _on_ the list would be a bad idea as it will most
>>> # likely eliminate _just_ that word (or get lucky and guess right).
>>> score('bight', words)
4.285714285714286
>>> # Guessing `blown` shows us the word is 'night'!
>>> filter2('blown', '____*', words)
['night']
``` 

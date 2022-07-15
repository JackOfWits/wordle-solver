from __future__ import annotations
from doctest import COMPARISON_FLAGS
__version__ = '0.1.1'

from functools import lru_cache
import os

NGUESSES = 6
with open(os.path.join(os.path.dirname(__file__), 'words.txt'), 'r') as fid:
    # not 'fid.readlines()', which includes line breaks
    WORDS = fid.read().strip().split()


def filter(
        guess: str = 'words',
        pattern: str ='_____',
        candidates: list[str] = WORDS,
) -> list[str]:
    """Find all words which are candidate solutions.

    Given a `guess` and a response `pattern` for that guess, we know that the
    hint is a function (see `compare`) of the `guess` and some unknown answer.
    Any given word then is only a candidate to be the answer if the same
    function `compare(guess, candidate)` produces the same `pattern`.

    Examples
    --------
    >>> filter('tares', '_**#_')
    ['alder', 'abler', 'arced', 'anger', 'armed', 'auger', 'amber', 'ameer', 'adder']
    """
    return [
        candidate for candidate in candidates
        if compare(guess, candidate) == pattern
    ]


@lru_cache(len(WORDS))
def compare(guess: str, answer: str) -> str:
    """Create a pattern showing the match of a guess to an 'answer'.
    
     The wordle game uses colored tiles, the solver uses ascii characters.
    An underscore means the letter is not in the word, an asterisk marks the
    correct letter in the wrong place, and an octothorp shows the correct
    letter in the correct place.
    
    Examples
    --------
    >>> compare('relic', 'lyric')
    '*_*##'

    Note that the second 'c' in 'cocoa' matches the second 'c' in 'coach', but
    the second 'o' does not.

    >>> compare('cocoa', 'coach')
    '##*_*'
    """
    return ''.join(
        # octothorp for the correct letter is in the correct spot
        '#' if a == b
        # asterisk for the correct letter in the wrong spot
        else '*' if a in answer
        # but do not match more times than are in the answer
        and guess[:i].count(a) <= answer.count(a)
        # underscore for letters not in the answer at all
        else '_'
        for i, (a, b) in enumerate(zip(guess, answer), start=1)
    )


def score(guess: str, candidates: list[str] = WORDS) -> float:
    """Rate a guess by how well it reduces the number of candidate words.

    The score of a word is the average number of words remaining from a list
    of candidates, given the word as a guess. A lower score means the guess is
    more effective at converging on a solution. The score can be used to sort
    or pick words from the list.
    
    Examples
    --------
    >>> score('tares')
    106.26398114420398

    Given a reduced number of candidates ...

    >>> words = filter('right', '_####')
    ... words
    ['sight', 'eight', 'light', 'night', 'might', 'bight', 'wight', 'fight', 'tight']

    ... pick the best guess to make

    >>> min(WORDS, key=lambda word: score(word, words))
    'slier'
    """
    return sum(
        # enumerate how well the guess reduces the number of candidate words
        len(filter(guess, compare(guess, candidate), candidates))
        # You solve it in 1 less guess if you get it right immediately
        # than if you know what it is but haven't guessed it yet
        - (guess in candidates)
        for candidate in candidates
    ) / len(candidates)


def optimize():
    """A really crappy way to make things 1000x faster."""
    from functools import wraps
    from tqdm import tqdm  # progress bar
    comparisons = {
        guess: {answer: compare(guess, answer) for answer in WORDS}
        for guess in tqdm(WORDS)
    }

    @wraps(compare)
    def wrapped(guess: str, answer: str) -> str:
        return comparisons[guess][answer]

    globals()['compare'] = wrapped


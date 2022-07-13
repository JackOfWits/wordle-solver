from __future__ import annotations
__version__ = '0.1.0'

from functools import lru_cache
import os
import random
import re
import sys

from tqdm import tqdm

NGUESSES = 6
with open(os.path.join(os.path.dirname(__file__), 'words.txt'), 'r') as fid:
    # not 'fid.readlines()', withc includes line breaks
    WORDS = fid.read().strip().split()


class Wordle:

    def __init__(self, seed=None):
        seed = re.compile(seed or '')
        options = [word for word in WORDS if seed.search(word)]
        if not options:
            raise ValueError(f'No words match `{seed!s}`')
        self.solution = random.choice([word for word in WORDS if seed.search(word)])
        self.candidates = WORDS.copy()
        print(f'WORDLE: SOLUTION = {self.solution}')

    def main(self):
        for nguess in range(NGUESSES):
            # choose a remaining candidate and stick with it
            guess = random.choice(self.candidates)
            # TODO: look at all the options and choose the most promising one
            # nopts = len(self.candidates)
            # for candidate in self.candidates:
            #     ...
            print(f'WORDLE: GUESS[{nguess + 1}] = {len(self.candidates):04} {guess} {compare(guess, self.solution)}')
            # if the guess is correct, we win!
            if guess == self.solution:
                print(f'WORDLE: SOLVED IN {nguess + 1} GUESSES')
                return 0
            # else reduce the candidates and keep going
            self.candidates = filter(guess, self.solution, self.candidates)

        # after all guesses are exhausted, we exit with an error code
        print(f'WORDLE: FAILED')


def filter(guess: str, answer: str, candidates: list[str] = WORDS) -> list[str]:
    """Filter candidates by the result of a guess."""
    pattern = compare(guess, answer)
    return [
        candidate for candidate in candidates
        if compare(guess, candidate) == pattern
    ]


def filter2(
        guess: str = 'words',
        pattern: str ='_____',
        candidates: list[str] = WORDS,
) -> list[str]:
    """Filter candidates by the result of a guess."""
    return [
        candidate for candidate in candidates
        if compare(guess, candidate) == pattern
    ]


@lru_cache(len(WORDS))
def compare(guess: str, answer: str) -> str:
    return ''.join(
        '#' if a == b
        else '*' if a in answer
        and guess[:i].count(a) <= answer.count(a)
        else '_'
        for i, (a, b) in enumerate(zip(guess, answer), start=1)
    )


def score(guess: str, candidates: list[str] = WORDS) -> float:
    """Find the the mean number of options remaining for each candidate."""
    return sum(
        len(filter(guess, candidate, candidates))
        - (guess in candidates)  # 0 more guesses if you're right!
        for candidate in candidates
    ) / len(candidates)


if __name__ == '__main__':
    with open('scores.txt', 'w') as fid:
        for word in tqdm(WORDS):
            value = score(word)
            fid.write(f'{word}: {value},')
            print('\r', word, value)

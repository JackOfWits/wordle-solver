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

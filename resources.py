from enum import Enum

class FitnessF(Enum):
    TARGET = 0
    ATTRACT_MATR = 1
    ATTRACT_OPT = 2

class LSearch(Enum):
    DELTA = 0
    REINIT = 1

def bool_to_int(elements: int, bool_number: bool) -> int:
    i = elements - 1
    int_number = 0

    while i >= 0:
        int_number += bool_number[i] * (1 << (elements - i - 1))
        i -= 1
    
    return int_number
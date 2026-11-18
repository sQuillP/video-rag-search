from dataclasses import dataclass

@dataclass(frozen=True)
class Constants:
    BM25_K1: float = 1.5
    BM25_B:float = 0.75
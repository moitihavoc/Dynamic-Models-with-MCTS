from dataclasses import dataclass, field
from typing import Optional

@dataclass
class EpisodeRecord:
    """
    snapshot of a completed game episode.
    """
    episode:      int               # episode index
    first_player: int
    winner:       Optional[int]
    total_moves:  int
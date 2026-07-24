from abc import ABC, abstractmethod
from typing import List
from models.post import Post

class BaseAdapter(ABC):
    """
    Abstract Base Class for all Social Media Adapters.
    Every platform adapter MUST return the exact same Post schema.
    """

    @property
    @abstractmethod
    def platform_name(self) -> str:
        """Name of the platform (e.g. 'instagram', 'tiktok', 'threads', 'facebook', 'x')"""
        pass

    @abstractmethod
    def fetch_posts(self, keywords: List[str], limit: int = 50) -> List[Post]:
        """
        Fetch posts matching the list of keywords.
        Must handle its own errors gracefully and return standard Post objects.
        """
        pass

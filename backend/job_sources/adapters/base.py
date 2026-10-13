from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional
import logging

logger = logging.getLogger(__name__)

class BaseJobAdapter(ABC):
    """
    Abstract base class for all job source adapters.
    Provides uniform interfaces for fetching, error handling,
    and schema normalization.
    """
    source_name: str = ""
    source_code: str = ""
    source_type: str = "PUBLIC_API"
    default_trust_rating: int = 3

    def __init__(self, config: Optional[Dict[str, Any]] = None):
        self.config = config or {}

    @abstractmethod
    def fetch_raw_jobs(self, query: str = "", location: str = "", limit: int = 20) -> List[Dict[str, Any]]:
        """Fetch raw listings from the source."""
        pass

    @abstractmethod
    def normalize_record(self, raw_item: Dict[str, Any]) -> Dict[str, Any]:
        """Transform a raw source listing into the standardized internal job dictionary."""
        pass

    def run(self, query: str = "", location: str = "", limit: int = 20) -> List[Dict[str, Any]]:
        """Executes fetch and normalization safely with exception boundary."""
        results = []
        try:
            raw_items = self.fetch_raw_jobs(query=query, location=location, limit=limit)
            for item in raw_items:
                try:
                    normalized = self.normalize_record(item)
                    if normalized:
                        results.append(normalized)
                except Exception as exc:
                    logger.warning(f"Failed to normalize record in adapter {self.source_code}: {exc}")
        except Exception as e:
            logger.error(f"Error fetching jobs from adapter {self.source_code}: {e}")
            raise
        return results

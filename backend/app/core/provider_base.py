from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import List, Optional

@dataclass
class PolicyChunk:
    text: str
    policy_name: str
    policy_number: Optional[str]
    section: str
    cpt_codes: List[str]
    effective_date: Optional[str]
    source_url: str
    provider: str

class PolicyProvider(ABC):
    @abstractmethod
    def get_policy_urls(self) -> List[str]: ...

    @abstractmethod
    def download_policy(self, url: str, dest_dir: str) -> str: ...

    @abstractmethod
    def parse_policy(self, pdf_path: str) -> List[PolicyChunk]: ...

    @abstractmethod
    def get_collection_name(self) -> str: ...

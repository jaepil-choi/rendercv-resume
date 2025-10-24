"""
Data models for CV items, profiles, and sections.
"""

from dataclasses import dataclass, field
from typing import Dict, List, Optional, Any
from datetime import date


@dataclass
class BilingualText:
    """Represents text in both English and Korean."""
    en: str
    kr: str


@dataclass
class ItemMetadata:
    """Metadata for CV items."""
    char_count: Dict[str, int] = field(default_factory=dict)


@dataclass
class WorkExperienceData:
    """Data structure for work experience items."""
    company: Dict[str, str]
    position: Dict[str, str]
    start_date: str
    end_date: str
    location: Dict[str, str]
    highlights: List[Dict[str, str]]


@dataclass
class ProjectData:
    """Data structure for project items."""
    name: Dict[str, str]
    highlights: List[Dict[str, str]]


@dataclass
class CVItem:
    """Represents a single CV item (work experience, project, etc.)."""
    id: str
    type: str
    tags: List[str]
    priority: int
    data: Dict[str, Any]
    metadata: ItemMetadata = field(default_factory=ItemMetadata)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'CVItem':
        """Create CVItem from dictionary."""
        metadata = ItemMetadata(
            char_count=data.get('metadata', {}).get('char_count', {})
        )
        return cls(
            id=data['id'],
            type=data['type'],
            tags=data.get('tags', []),
            priority=data.get('priority', 0),
            data=data['data'],
            metadata=metadata
        )


@dataclass
class SectionSpec:
    """Specification for a CV section in a profile."""
    include_ids: List[str]
    max_items: Optional[int] = None


@dataclass
class Profile:
    """Profile specification for composing a CV."""
    name: str
    locale: str
    base_file: str
    sections: Dict[str, SectionSpec]
    output_file: str

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Profile':
        """Create Profile from dictionary."""
        sections = {}
        for section_name, section_data in data['sections'].items():
            sections[section_name] = SectionSpec(
                include_ids=section_data['include_ids'],
                max_items=section_data.get('max_items')
            )
        
        return cls(
            name=data['name'],
            locale=data['locale'],
            base_file=data['base_file'],
            sections=sections,
            output_file=data['output_file']
        )


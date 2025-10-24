"""
YAML loading utilities for CV items, profiles, and base files.
"""

import yaml
from pathlib import Path
from typing import Dict, List
from cv_builder.models import CVItem, Profile
from cv_builder.utils import load_item_metadata


class Loader:
    """Handles loading of CV data from YAML files."""
    
    def __init__(self, base_dir: Path = None):
        """Initialize loader with base directory."""
        if base_dir is None:
            base_dir = Path(__file__).parent.parent
        self.base_dir = base_dir
        self.modular_cv_dir = base_dir / "modular_cv"
    
    def load_items(self) -> Dict[str, CVItem]:
        """Load all CV items from cv_items directory."""
        items = {}
        items_dir = self.modular_cv_dir / "cv_items"
        
        # Item types to load
        item_types = ["work_experience", "projects", "education", "additional_info"]
        
        for item_type in item_types:
            item_type_dir = items_dir / item_type
            if item_type_dir.exists():
                for yaml_file in item_type_dir.glob("*.yaml"):
                    # Skip .metadata directory
                    if yaml_file.parent.name == ".metadata":
                        continue
                    
                    with open(yaml_file, 'r', encoding='utf-8') as f:
                        data = yaml.safe_load(f)
                        # Load metadata from separate file
                        metadata = load_item_metadata(yaml_file)
                        data['metadata'] = metadata
                        item = CVItem.from_dict(data)
                        items[item.id] = item
        
        return items
    
    def load_profile(self, profile_name: str) -> Profile:
        """Load a profile specification."""
        profile_path = self.modular_cv_dir / "profiles" / f"{profile_name}.yaml"
        
        if not profile_path.exists():
            raise FileNotFoundError(f"Profile not found: {profile_path}")
        
        with open(profile_path, 'r', encoding='utf-8') as f:
            data = yaml.safe_load(f)
        
        return Profile.from_dict(data)
    
    def load_base(self, base_file: str) -> Dict:
        """Load base CV structure (header, design, locale)."""
        base_path = self.modular_cv_dir / "base" / base_file
        
        if not base_path.exists():
            raise FileNotFoundError(f"Base file not found: {base_path}")
        
        with open(base_path, 'r', encoding='utf-8') as f:
            return yaml.safe_load(f)


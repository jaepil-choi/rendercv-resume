"""
Utility functions for CV builder.
"""

import yaml
from pathlib import Path
from typing import Dict, Any


def calculate_char_count(data: Dict[str, Any], locale: str) -> int:
    """
    Calculate total character count for an item in a specific locale.
    
    Recursively traverses the data structure and counts all text in the specified locale.
    """
    total_chars = 0
    
    if isinstance(data, dict):
        # Check if this is a bilingual field
        if 'en' in data and 'kr' in data:
            text = data.get(locale, '')
            total_chars += len(text) if text else 0
        else:
            # Recursively process dict
            for value in data.values():
                total_chars += calculate_char_count(value, locale)
    elif isinstance(data, list):
        for item in data:
            total_chars += calculate_char_count(item, locale)
    
    return total_chars


def get_metadata_path(item_path: Path) -> Path:
    """
    Get the metadata file path for an item file.
    
    Example:
        work_experience/item.yaml -> work_experience/.metadata/item.yaml
    """
    return item_path.parent / ".metadata" / item_path.name


def load_item_metadata(item_path: Path) -> Dict[str, Any]:
    """
    Load metadata for an item. Returns empty dict if metadata doesn't exist.
    """
    metadata_path = get_metadata_path(item_path)
    
    if not metadata_path.exists():
        return {}
    
    with open(metadata_path, 'r', encoding='utf-8') as f:
        return yaml.safe_load(f) or {}


def save_item_metadata(item_path: Path, metadata: Dict[str, Any]) -> None:
    """
    Save metadata for an item.
    """
    metadata_path = get_metadata_path(item_path)
    
    # Create .metadata directory if it doesn't exist
    metadata_path.parent.mkdir(exist_ok=True)
    
    with open(metadata_path, 'w', encoding='utf-8') as f:
        yaml.dump(metadata, f, allow_unicode=True, sort_keys=False, width=120)


def update_item_char_counts(item_path: Path) -> bool:
    """
    Update character counts for an item file.
    
    Reads the item, calculates char counts, and saves to separate metadata file.
    Returns True if changes were made, False otherwise.
    """
    # Load item
    with open(item_path, 'r', encoding='utf-8') as f:
        item_data = yaml.safe_load(f)
    
    if 'data' not in item_data:
        return False
    
    # Calculate character counts
    en_count = calculate_char_count(item_data['data'], 'en')
    kr_count = calculate_char_count(item_data['data'], 'kr')
    
    # Load existing metadata
    metadata = load_item_metadata(item_path)
    
    # Check if update is needed
    current_en = metadata.get('char_count', {}).get('en', 0)
    current_kr = metadata.get('char_count', {}).get('kr', 0)
    
    if current_en == en_count and current_kr == kr_count:
        return False  # No change needed
    
    # Update metadata
    if 'char_count' not in metadata:
        metadata['char_count'] = {}
    
    metadata['char_count']['en'] = en_count
    metadata['char_count']['kr'] = kr_count
    
    # Save metadata
    save_item_metadata(item_path, metadata)
    
    return True


def update_all_char_counts(base_dir: Path = None) -> Dict[str, int]:
    """
    Update character counts for all items.
    
    Returns a dict with counts of updated/unchanged files.
    """
    if base_dir is None:
        base_dir = Path(__file__).parent.parent
    
    items_dir = base_dir / "modular_cv" / "cv_items"
    
    stats = {'updated': 0, 'unchanged': 0, 'errors': 0}
    
    for item_type_dir in items_dir.iterdir():
        if not item_type_dir.is_dir():
            continue
        
        for yaml_file in item_type_dir.glob("*.yaml"):
            try:
                if update_item_char_counts(yaml_file):
                    print(f"✓ Updated: {yaml_file.relative_to(base_dir)}")
                    stats['updated'] += 1
                else:
                    print(f"  No change: {yaml_file.relative_to(base_dir)}")
                    stats['unchanged'] += 1
            except Exception as e:
                print(f"✗ Error: {yaml_file.relative_to(base_dir)} - {e}")
                stats['errors'] += 1
    
    return stats

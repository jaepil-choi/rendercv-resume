#!/usr/bin/env python
"""
Update character counts for all CV items.

Usage:
    poetry run python scripts/update_char_counts.py
"""

import sys
from pathlib import Path

# Add parent directory to path to import cv_builder
sys.path.insert(0, str(Path(__file__).parent.parent))

from cv_builder.utils import update_all_char_counts


def main():
    print("Updating character counts for all CV items...\n")
    
    base_dir = Path(__file__).parent.parent
    stats = update_all_char_counts(base_dir)
    
    print(f"\n{'='*60}")
    print(f"Summary:")
    print(f"  Updated: {stats['updated']} files")
    print(f"  Unchanged: {stats['unchanged']} files")
    print(f"  Errors: {stats['errors']} files")
    print(f"{'='*60}")
    
    return 0 if stats['errors'] == 0 else 1


if __name__ == '__main__':
    sys.exit(main())




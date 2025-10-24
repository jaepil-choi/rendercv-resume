"""
CLI entry point for the CV builder.
"""

import argparse
import sys
import yaml
from pathlib import Path
from cv_builder.loader import Loader
from cv_builder.validator import Validator
from cv_builder.composer import Composer


def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        description='Modular CV Builder - Compose CVs from reusable components'
    )
    parser.add_argument(
        '--profile',
        required=True,
        help='Profile name (without .yaml extension)'
    )
    parser.add_argument(
        '--output',
        help='Output file path (overrides profile output_file)'
    )
    parser.add_argument(
        '--validate-only',
        action='store_true',
        help='Only validate items and profile without generating output'
    )
    parser.add_argument(
        '--base-dir',
        help='Base directory for the project (default: current directory parent)'
    )
    
    args = parser.parse_args()
    
    # Initialize components
    base_dir = Path(args.base_dir) if args.base_dir else Path(__file__).parent.parent
    loader = Loader(base_dir=base_dir)
    validator = Validator()
    composer = Composer()
    
    print(f"Loading items from {base_dir / 'modular_cv' / 'cv_items'}...")
    
    try:
        # Load all items
        items = loader.load_items()
        print(f"Loaded {len(items)} items")
        
        # Validate items
        print("Validating items...")
        item_errors = validator.validate_items(items)
        
        if item_errors:
            print("\n❌ Item validation errors:")
            for error in item_errors:
                print(f"  - {error}")
            sys.exit(1)
        
        print("✓ All items valid")
        
        # Load profile
        print(f"\nLoading profile '{args.profile}'...")
        profile = loader.load_profile(args.profile)
        
        # Validate profile
        print("Validating profile...")
        profile_errors = validator.validate_profile(profile, items)
        
        if profile_errors:
            print("\n❌ Profile validation errors:")
            for error in profile_errors:
                print(f"  - {error}")
            sys.exit(1)
        
        print("✓ Profile valid")
        
        if args.validate_only:
            print("\n✓ Validation complete. No output generated (--validate-only flag)")
            sys.exit(0)
        
        # Load base
        print(f"\nLoading base file '{profile.base_file}'...")
        base = loader.load_base(profile.base_file)
        
        # Select items based on profile
        print("\nSelecting items for sections...")
        selected_items = composer.select_items(items, profile)
        
        for section_name, section_items in selected_items.items():
            print(f"  {section_name}: {len(section_items)} items")
        
        # Calculate statistics
        stats = composer.calculate_section_stats(selected_items, profile.locale)
        print("\nCharacter count statistics:")
        for section_name, section_stats in stats.items():
            print(f"  {section_name}: {section_stats['total_chars']} chars ({section_stats['item_count']} items)")
        
        # Build sections
        print("\nBuilding sections...")
        sections = composer.build_sections(selected_items, profile.locale)
        
        # Compose final CV
        print("Composing CV...")
        cv = composer.compose_cv(base, sections)
        
        # Determine output path
        output_path = Path(args.output) if args.output else base_dir / profile.output_file
        
        # Write output
        print(f"\nWriting output to {output_path}...")
        with open(output_path, 'w', encoding='utf-8') as f:
            yaml.dump(cv, f, allow_unicode=True, sort_keys=False, width=120)
        
        print(f"✓ CV successfully generated: {output_path}")
        
    except FileNotFoundError as e:
        print(f"\n❌ Error: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == '__main__':
    main()


#!/usr/bin/env python
"""
PDF to Text Converter
Bulk converts PDF files in a directory to plain text files using PyMuPDF.
"""

import argparse
import sys
from pathlib import Path
from typing import List

try:
    import fitz  # PyMuPDF
except ImportError:
    print("Error: PyMuPDF is not installed. Please install it with: poetry add pymupdf")
    sys.exit(1)


def extract_text_from_pdf(pdf_path: Path) -> str:
    """
    Extract text from a PDF file using PyMuPDF.
    
    Args:
        pdf_path: Path to the PDF file
        
    Returns:
        Extracted text content
    """
    try:
        doc = fitz.open(pdf_path)
        text = ""
        
        for page_num, page in enumerate(doc, start=1):
            text += page.get_text()
            
        doc.close()
        return text
    except Exception as e:
        raise RuntimeError(f"Failed to extract text from {pdf_path}: {e}")


def convert_pdf_to_txt(pdf_path: Path, output_path: Path) -> None:
    """
    Convert a single PDF file to text and save it.
    
    Args:
        pdf_path: Path to the input PDF file
        output_path: Path to the output text file
    """
    print(f"Processing: {pdf_path.name}")
    
    text = extract_text_from_pdf(pdf_path)
    
    # Write the extracted text to the output file
    output_path.write_text(text, encoding='utf-8')
    
    print(f"  → Saved: {output_path.name}")


def find_pdf_files(directory: Path) -> List[Path]:
    """
    Find all PDF files in the given directory (non-recursive).
    
    Args:
        directory: Directory to search
        
    Returns:
        List of PDF file paths
    """
    pdf_files = list(directory.glob("*.pdf"))
    return sorted(pdf_files)


def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        description="Bulk convert PDF files to text files",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python scripts/pdf_to_txt.py data/companies/미래에셋자산운용
  python scripts/pdf_to_txt.py "data/companies/Company Name"
        """
    )
    
    parser.add_argument(
        "directory",
        type=str,
        help="Directory containing PDF files to convert"
    )
    
    parser.add_argument(
        "-r", "--recursive",
        action="store_true",
        help="Recursively search for PDF files in subdirectories"
    )
    
    parser.add_argument(
        "--overwrite",
        action="store_true",
        help="Overwrite existing text files"
    )
    
    args = parser.parse_args()
    
    # Convert to Path object
    directory = Path(args.directory)
    
    # Validate directory
    if not directory.exists():
        print(f"Error: Directory '{directory}' does not exist", file=sys.stderr)
        sys.exit(1)
    
    if not directory.is_dir():
        print(f"Error: '{directory}' is not a directory", file=sys.stderr)
        sys.exit(1)
    
    # Find PDF files
    if args.recursive:
        pdf_files = sorted(directory.rglob("*.pdf"))
    else:
        pdf_files = find_pdf_files(directory)
    
    if not pdf_files:
        print(f"No PDF files found in '{directory}'")
        return
    
    print(f"Found {len(pdf_files)} PDF file(s) in '{directory}'")
    print("-" * 60)
    
    # Process each PDF file
    success_count = 0
    skip_count = 0
    error_count = 0
    
    for pdf_path in pdf_files:
        # Generate output path (same name but .txt extension)
        output_path = pdf_path.with_suffix('.txt')
        
        # Check if output file already exists
        if output_path.exists() and not args.overwrite:
            print(f"Skipping: {pdf_path.name} (output file already exists)")
            skip_count += 1
            continue
        
        try:
            convert_pdf_to_txt(pdf_path, output_path)
            success_count += 1
        except Exception as e:
            print(f"Error processing {pdf_path.name}: {e}", file=sys.stderr)
            error_count += 1
    
    # Print summary
    print("-" * 60)
    print(f"Conversion complete:")
    print(f"  [+] Successfully converted: {success_count}")
    if skip_count > 0:
        print(f"  [-] Skipped (already exists): {skip_count}")
    if error_count > 0:
        print(f"  [!] Failed: {error_count}")


if __name__ == "__main__":
    main()


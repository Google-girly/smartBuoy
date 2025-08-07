#!/usr/bin/env python3
"""
Batch converter for multiple sensor data files.
"""

import os
import sys
from pathlib import Path
from txt_to_json_converter import SensorDataConverter


def batch_convert(input_directory, output_directory=None):
    """Convert all .txt files in a directory to JSON format."""
    input_path = Path(input_directory)
    
    if not input_path.exists() or not input_path.is_dir():
        raise ValueError(f"Input directory does not exist: {input_directory}")
    
    # Set output directory
    if output_directory is None:
        output_path = input_path / "converted"
    else:
        output_path = Path(output_directory)
    
    # Create output directory if it doesn't exist
    output_path.mkdir(exist_ok=True)
    
    converter = SensorDataConverter()
    txt_files = list(input_path.glob("*.txt"))
    
    if not txt_files:
        print(f"No .txt files found in {input_directory}")
        return
    
    print(f"Found {len(txt_files)} .txt files to convert")
    print(f"Output directory: {output_path}")
    print("-" * 50)
    
    converted_count = 0
    for txt_file in txt_files:
        try:
            output_file = output_path / f"{txt_file.stem}.json"
            converter.convert_file(txt_file, output_file)
            converted_count += 1
        except Exception as e:
            print(f"Error converting {txt_file.name}: {e}")
    
    print("-" * 50)
    print(f"Successfully converted {converted_count} out of {len(txt_files)} files")


def main():
    """Main function for command line usage."""
    if len(sys.argv) < 2:
        print("Usage: python batch_convert.py <input_directory> [output_directory]")
        print("Example: python batch_convert.py ./data ./converted_data")
        sys.exit(1)
    
    input_dir = sys.argv[1]
    output_dir = sys.argv[2] if len(sys.argv) > 2 else None
    
    try:
        batch_convert(input_dir, output_dir)
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""
Smart Buoy Data Converter
Converts sensor data from text format to JSON format.
"""

import json
import re
import sys
from datetime import datetime
from pathlib import Path


class SensorDataConverter:
    def __init__(self):
        self.data_pattern = re.compile(
            r'T:\s*([\d.]+)F\s*\|\s*L:\s*([\d.]+)\s*lx\s*\|\s*'
            r'Pitch:\s*([-\d.]+)\s*\|\s*Roll:\s*([-\d.]+)\s*\|\s*'
            r'Yaw:\s*([-\d.]+)'
        )
    
    def parse_sensor_line(self, line):
        """Parse a single sensor data line and return a dictionary."""
        match = self.data_pattern.search(line.strip())
        if match:
            return {
                "temperature": float(match.group(1)),
                "temperature_unit": "F",
                "light": float(match.group(2)),
                "light_unit": "lx",
                "pitch": float(match.group(3)),
                "roll": float(match.group(4)),
                "yaw": float(match.group(5)),
                "orientation_unit": "degrees"
            }
        return None
    
    def convert_file(self, input_file, output_file=None):
        """Convert text file to JSON format."""
        input_path = Path(input_file)
        
        if not input_path.exists():
            raise FileNotFoundError(f"Input file not found: {input_file}")
        
        # Generate output filename if not provided
        if output_file is None:
            output_file = input_path.with_suffix('.json')
        
        entries = []
        current_entry = None
        
        with open(input_path, 'r') as file:
            for line_num, line in enumerate(file, 1):
                line = line.strip()
                
                # Check for new entry marker
                if line.upper() == "NEW ENTRY":
                    if current_entry is not None:
                        entries.append(current_entry)
                    current_entry = {
                        "entry_id": len(entries) + 1,
                        "timestamp": datetime.now().isoformat(),
                        "readings": []
                    }
                    continue
                
                # Parse sensor data line
                if current_entry is not None and line:
                    sensor_data = self.parse_sensor_line(line)
                    if sensor_data:
                        current_entry["readings"].append(sensor_data)
                    elif line:  # Non-empty line that doesn't match pattern
                        print(f"Warning: Could not parse line {line_num}: {line}")
        
        # Add the last entry if it exists
        if current_entry is not None:
            entries.append(current_entry)
        
        # Create the final JSON structure
        output_data = {
            "metadata": {
                "source_file": str(input_path.name),
                "conversion_timestamp": datetime.now().isoformat(),
                "total_entries": len(entries),
                "total_readings": sum(len(entry["readings"]) for entry in entries)
            },
            "entries": entries
        }
        
        # Write to JSON file
        with open(output_file, 'w') as file:
            json.dump(output_data, file, indent=2)
        
        print(f"Successfully converted {input_path.name} to {output_file}")
        print(f"Total entries: {len(entries)}")
        print(f"Total readings: {output_data['metadata']['total_readings']}")
        
        return output_file


def main():
    """Main function to handle command line usage."""
    if len(sys.argv) < 2:
        print("Usage: python txt_to_json_converter.py <input_file> [output_file]")
        print("Example: python txt_to_json_converter.py sensor_data.txt")
        sys.exit(1)
    
    input_file = sys.argv[1]
    output_file = sys.argv[2] if len(sys.argv) > 2 else None
    
    try:
        converter = SensorDataConverter()
        converter.convert_file(input_file, output_file)
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()

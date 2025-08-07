# Smart Buoy Data Converter

A Python utility to convert smart buoy sensor data from plain text into structured JSON format.

## Features

- Parses sensor data including temperature, **light**, pitch, roll, and yaw
- Supports multiple data lines (with or without "NEW ENTRY" markers)
- Generates structured JSON output with metadata and timestamps
- Command-line interface for easy usage
- Error handling and validation for malformed lines

## Data Format

### Input Format (Text)
```
NEW ENTRY
T: 72.45F | L: 213.50 lx | Pitch: 1.34 | Roll: 7.82 | Yaw: -0.25
T: 72.63F | L: 218.12 lx | Pitch: 1.48 | Roll: 7.94 | Yaw: -0.21
```

### Output Format (JSON)
```json
{
  "metadata": {
    "source_file": "sensor_data.txt",
    "conversion_timestamp": "2025-08-07T15:47:54.218791",
    "total_entries": 1,
    "total_readings": 2
  },
  "entries": [
    {
      "entry_id": 1,
      "timestamp": "2025-08-07T15:47:54.130976",
      "readings": [
        {
          "temperature": 72.45,
          "temperature_unit": "F",
          "light": 213.5,
          "light_unit": "lx",
          "pitch": 1.34,
          "roll": 7.82,
          "yaw": -0.25,
          "orientation_unit": "degrees"
        },
        {
          "temperature": 72.63,
          "temperature_unit": "F",
          "light": 218.12,
          "light_unit": "lx",
          "pitch": 1.48,
          "roll": 7.94,
          "yaw": -0.21,
          "orientation_unit": "degrees"
        }
      ]
    }
  ]
}
```

## Usage

### Command Line
```bash
python txt_to_json_converter.py input_file.txt [output_file.json]
```

### Examples
```bash
# Convert with automatic output filename
python txt_to_json_converter.py buoy_data.txt

# Convert with custom output filename
python txt_to_json_converter.py sensor_data.txt buoy_data.json
```

### Python Script Usage
```python
from txt_to_json_converter import SensorDataConverter

converter = SensorDataConverter()
converter.convert_file('input.txt', 'output.json')
```

## Requirements

- Python 3.6 or higher
- No external dependencies (standard library only)

## Files

- `txt_to_json_converter.py` – Main converter script
- `sample_sensor_data.txt` – Example input file with light data
- `README.md` – This documentation

## Error Handling

The converter includes error handling for:
- Missing input files
- Malformed data lines (with warnings to `stdout`)
- File I/O errors

Warnings are displayed for lines that don’t match the expected format:
```
T: <temp>F | L: <light> lx | Pitch: <pitch> | Roll: <roll> | Yaw: <yaw>
```

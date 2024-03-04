# elva_technical_solution

# Geocoding and Neighborhood Query

This Python script uses the ArcGIS APIs to perform geocoding of addresses and query neighborhood information in Portland, Oregon.

## Requirements

- Python 3.x
- Python packages: requests, shapely, pyproj

You can install the required packages using the following command:

```bash
pip install -r requirements.txt
```
## Configuration
1. Add your ArcGIS token to `src/.env` in the `TOKEN_ARGIS` variable.
Example : `TOKEN_ARGIS=YOUR_TOKEN_HERE`

## Execution
Run the `main.py` script to perform geocoding and query neighborhood information for a specific address.

```bash
python main.py
```

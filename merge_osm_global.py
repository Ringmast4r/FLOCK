#!/usr/bin/env python3
"""
Merge global OSM surveillance cameras with existing FLOCK data
Converts OSM format to GeoJSON and deduplicates
"""

import json
from pathlib import Path
from collections import defaultdict

def osm_to_geojson(osm_data):
    """Convert OSM format to GeoJSON FeatureCollection"""
    features = []

    for element in osm_data.get('elements', []):
        if element.get('type') != 'node':
            continue
        if 'lat' not in element or 'lon' not in element:
            continue

        feature = {
            'type': 'Feature',
            'geometry': {
                'type': 'Point',
                'coordinates': [element['lon'], element['lat']]
            },
            'properties': element.get('tags', {})
        }
        features.append(feature)

    return features

def main():
    print("="*60)
    print("MERGING GLOBAL OSM SURVEILLANCE CAMERAS")
    print("="*60)

    # Load existing cameras
    print("\nLoading existing FLOCK cameras...")
    with open('CAMERAS_WITH_NETWORK_DATA.geojson', 'r', encoding='utf-8') as f:
        existing_data = json.load(f)

    print(f"Current cameras: {len(existing_data['features']):,}")

    # Create lookup for deduplication (by coordinates rounded to 4 decimals)
    existing_coords = set()
    for feat in existing_data['features']:
        lon, lat = feat['geometry']['coordinates']
        coord_key = f"{lat:.4f},{lon:.4f}"
        existing_coords.add(coord_key)

    print(f"Unique coordinate keys: {len(existing_coords):,}")

    # Load and merge OSM regional files
    osm_dir = Path('data/raw_osm_global')
    osm_files = sorted(osm_dir.glob('osm_surveillance_*.json'))

    print(f"\nFound {len(osm_files)} OSM regional files")

    new_features = []
    duplicates = 0

    for osm_file in osm_files:
        region = osm_file.stem.replace('osm_surveillance_', '').split('_')[0]
        print(f"\nProcessing {region}...")

        with open(osm_file, 'r', encoding='utf-8') as f:
            osm_data = json.load(f)

        features = osm_to_geojson(osm_data)
        print(f"  Raw cameras: {len(features):,}")

        # Deduplicate
        region_new = 0
        for feat in features:
            lon, lat = feat['geometry']['coordinates']
            coord_key = f"{lat:.4f},{lon:.4f}"

            if coord_key not in existing_coords:
                new_features.append(feat)
                existing_coords.add(coord_key)
                region_new += 1
            else:
                duplicates += 1

        print(f"  New cameras: {region_new:,}")
        print(f"  Duplicates: {len(features) - region_new:,}")

    # Merge
    print(f"\n{'='*60}")
    print("MERGE SUMMARY")
    print(f"{'='*60}")
    print(f"Existing cameras: {len(existing_data['features']):,}")
    print(f"New unique cameras: {len(new_features):,}")
    print(f"Duplicates skipped: {duplicates:,}")
    print(f"Total after merge: {len(existing_data['features']) + len(new_features):,}")

    # Combine
    merged_data = {
        'type': 'FeatureCollection',
        'features': existing_data['features'] + new_features
    }

    # Save merged file
    print(f"\nSaving merged data...")
    with open('CAMERAS_WITH_NETWORK_DATA.geojson', 'w', encoding='utf-8') as f:
        json.dump(merged_data, f)

    print(f"Saved to CAMERAS_WITH_NETWORK_DATA.geojson")

    # Update camera count in summary
    print(f"\nFinal camera count: {len(merged_data['features']):,}")

    print("\n" + "="*60)
    print("SUCCESS - Ready to regenerate tiles")
    print("="*60)

if __name__ == '__main__':
    main()

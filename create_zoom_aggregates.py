#!/usr/bin/env python3
"""
Create zoom-level aggregates for proper map performance
Generates state/county summaries for low zoom, detail tiles for high zoom
"""

import json
from pathlib import Path
from collections import defaultdict
import math

def lat_lon_to_tile(lat, lon, zoom):
    """Convert lat/lon to tile coordinates at given zoom level"""
    lat_rad = math.radians(lat)
    n = 2.0 ** zoom
    xtile = int((lon + 180.0) / 360.0 * n)
    ytile = int((1.0 - math.asinh(math.tan(lat_rad)) / math.pi) / 2.0 * n)
    return (xtile, ytile)

def get_us_state_from_coords(lat, lon):
    """Approximate US state from coordinates (simplified)"""
    # Rough bounding boxes for states
    state_bounds = {
        'California': {'lat': (32.5, 42.0), 'lon': (-124.5, -114.1)},
        'Texas': {'lat': (25.8, 36.5), 'lon': (-106.6, -93.5)},
        'Florida': {'lat': (24.5, 31.0), 'lon': (-87.6, -80.0)},
        'New York': {'lat': (40.5, 45.0), 'lon': (-79.8, -71.9)},
        'Pennsylvania': {'lat': (39.7, 42.3), 'lon': (-80.5, -74.7)},
        'Illinois': {'lat': (37.0, 42.5), 'lon': (-91.5, -87.5)},
        'Ohio': {'lat': (38.4, 42.3), 'lon': (-84.8, -80.5)},
        'Georgia': {'lat': (30.4, 35.0), 'lon': (-85.6, -81.0)},
        'North Carolina': {'lat': (34.0, 36.6), 'lon': (-84.3, -75.5)},
        'Michigan': {'lat': (41.7, 48.3), 'lon': (-90.4, -82.4)},
    }

    for state, bounds in state_bounds.items():
        if (bounds['lat'][0] <= lat <= bounds['lat'][1] and
            bounds['lon'][0] <= lon <= bounds['lon'][1]):
            return state

    return 'Other US'

def create_aggregates():
    """Create zoom-level aggregated data"""

    print("Loading camera data...")
    with open('CAMERAS_WITH_NETWORK_DATA.geojson', 'r', encoding='utf-8') as f:
        camera_data = json.load(f)

    print(f"Loaded {len(camera_data['features'])} cameras")

    print("\nLoading network data...")
    with open('camera_networks.json', 'r', encoding='utf-8') as f:
        network_data = json.load(f)

    print(f"Loaded {len(network_data)} networks")

    # Create network lookup
    network_lookup = {}
    for network in network_data:
        key = f"{network['from'][0]:.4f},{network['from'][1]:.4f}"
        network_lookup[key] = network

    # ====================
    # ZOOM 4-6: STATE AGGREGATES
    # ====================
    print("\n" + "="*60)
    print("Creating STATE aggregates (zoom 4-6)...")
    print("="*60)

    state_aggregates = defaultdict(lambda: {
        'count': 0,
        'flock_count': 0,
        'alpr_count': 0,
        'other_count': 0,
        'cameras': [],
        'lat_sum': 0,
        'lon_sum': 0
    })

    for feature in camera_data['features']:
        lon, lat = feature['geometry']['coordinates']
        props = feature.get('properties') or {}

        # Only US cameras for state aggregates
        if not (24.0 <= lat <= 49.0 and -125.0 <= lon <= -66.0):
            continue

        state = get_us_state_from_coords(lat, lon)

        # Count by type
        manufacturer = (props.get('manufacturer') or props.get('brand') or '').lower()
        surv_type = (props.get('surveillance:type') or '').upper()

        if 'flock' in manufacturer:
            state_aggregates[state]['flock_count'] += 1
        elif surv_type == 'ALPR':
            state_aggregates[state]['alpr_count'] += 1
        else:
            state_aggregates[state]['other_count'] += 1

        state_aggregates[state]['count'] += 1
        state_aggregates[state]['lat_sum'] += lat
        state_aggregates[state]['lon_sum'] += lon

    # Convert to GeoJSON
    state_geojson = {
        'type': 'FeatureCollection',
        'features': []
    }

    for state, data in state_aggregates.items():
        if data['count'] == 0:
            continue

        # Calculate centroid
        center_lat = data['lat_sum'] / data['count']
        center_lon = data['lon_sum'] / data['count']

        feature = {
            'type': 'Feature',
            'geometry': {
                'type': 'Point',
                'coordinates': [center_lon, center_lat]
            },
            'properties': {
                'state': state,
                'total': data['count'],
                'flock': data['flock_count'],
                'alpr': data['alpr_count'],
                'other': data['other_count'],
                'zoom_level': 'state'
            }
        }
        state_geojson['features'].append(feature)

    # Save state aggregates
    output_dir = Path('data/aggregates')
    output_dir.mkdir(parents=True, exist_ok=True)

    state_file = output_dir / 'states.json'
    with open(state_file, 'w', encoding='utf-8') as f:
        json.dump(state_geojson, f)

    print(f"\nState aggregates: {len(state_geojson['features'])} states")
    for feat in sorted(state_geojson['features'], key=lambda x: x['properties']['total'], reverse=True)[:10]:
        props = feat['properties']
        print(f"  {props['state']:20s}: {props['total']:6,} cameras ({props['flock']:,} Flock, {props['alpr']:,} ALPR)")

    # ====================
    # ZOOM 7-9: GRID AGGREGATES (1-degree grid)
    # ====================
    print("\n" + "="*60)
    print("Creating GRID aggregates (zoom 7-9)...")
    print("="*60)

    grid_aggregates = defaultdict(lambda: {
        'count': 0,
        'flock_count': 0,
        'alpr_count': 0,
        'other_count': 0,
        'lat_sum': 0,
        'lon_sum': 0
    })

    for feature in camera_data['features']:
        lon, lat = feature['geometry']['coordinates']
        props = feature.get('properties') or {}

        # Create 1-degree grid cell
        grid_lat = int(lat)
        grid_lon = int(lon)
        grid_key = f"{grid_lat},{grid_lon}"

        # Count by type
        manufacturer = (props.get('manufacturer') or props.get('brand') or '').lower()
        surv_type = (props.get('surveillance:type') or '').upper()

        if 'flock' in manufacturer:
            grid_aggregates[grid_key]['flock_count'] += 1
        elif surv_type == 'ALPR':
            grid_aggregates[grid_key]['alpr_count'] += 1
        else:
            grid_aggregates[grid_key]['other_count'] += 1

        grid_aggregates[grid_key]['count'] += 1
        grid_aggregates[grid_key]['lat_sum'] += lat
        grid_aggregates[grid_key]['lon_sum'] += lon

    # Convert to GeoJSON
    grid_geojson = {
        'type': 'FeatureCollection',
        'features': []
    }

    for grid_key, data in grid_aggregates.items():
        if data['count'] == 0:
            continue

        # Calculate centroid
        center_lat = data['lat_sum'] / data['count']
        center_lon = data['lon_sum'] / data['count']

        feature = {
            'type': 'Feature',
            'geometry': {
                'type': 'Point',
                'coordinates': [center_lon, center_lat]
            },
            'properties': {
                'grid': grid_key,
                'total': data['count'],
                'flock': data['flock_count'],
                'alpr': data['alpr_count'],
                'other': data['other_count'],
                'zoom_level': 'grid'
            }
        }
        grid_geojson['features'].append(feature)

    # Save grid aggregates
    grid_file = output_dir / 'grid.json'
    with open(grid_file, 'w', encoding='utf-8') as f:
        json.dump(grid_geojson, f)

    print(f"\nGrid aggregates: {len(grid_geojson['features'])} grid cells")
    print(f"Largest grid cells:")
    for feat in sorted(grid_geojson['features'], key=lambda x: x['properties']['total'], reverse=True)[:10]:
        props = feat['properties']
        print(f"  Grid {props['grid']:10s}: {props['total']:6,} cameras")

    # ====================
    # ZOOM 10+: DETAIL TILES (small tiles with individual cameras)
    # ====================
    print("\n" + "="*60)
    print("Creating DETAIL tiles (zoom 10+)...")
    print("="*60)

    zoom = 10
    tiles = {}

    for feature in camera_data['features']:
        lon, lat = feature['geometry']['coordinates']
        x, y = lat_lon_to_tile(lat, lon, zoom)

        tile_key = f"{zoom}/{x}/{y}"
        if tile_key not in tiles:
            tiles[tile_key] = {
                'type': 'FeatureCollection',
                'features': [],
                'networks': []
            }

        tiles[tile_key]['features'].append(feature)

        # Add network data if exists
        cam_key = f"{lat:.4f},{lon:.4f}"
        if cam_key in network_lookup:
            tiles[tile_key]['networks'].append(network_lookup[cam_key])

    # Save detail tiles
    tiles_dir = Path('data/tiles_detail')
    print(f"\nSaving {len(tiles)} detail tiles...")

    tile_sizes = []
    for tile_key, tile_data in tiles.items():
        zoom_str, x_str, y_str = tile_key.split('/')

        tile_dir = tiles_dir / zoom_str / x_str
        tile_dir.mkdir(parents=True, exist_ok=True)

        tile_file = tile_dir / f"{y_str}.json"
        with open(tile_file, 'w', encoding='utf-8') as f:
            json.dump(tile_data, f)

        tile_sizes.append(len(tile_data['features']))

    # Create tile index
    tile_index = {
        'zoom': zoom,
        'tiles': {},
        'total_cameras': len(camera_data['features'])
    }

    for tile_key, tile_data in tiles.items():
        tile_index['tiles'][tile_key] = {
            'cameras': len(tile_data['features']),
            'networks': len(tile_data['networks']),
            'path': f"data/tiles_detail/{tile_key}.json"
        }

    index_file = tiles_dir / 'index.json'
    with open(index_file, 'w', encoding='utf-8') as f:
        json.dump(tile_index, f, indent=2)

    # Stats
    avg_size = sum(tile_sizes) / len(tile_sizes) if tile_sizes else 0
    max_size = max(tile_sizes) if tile_sizes else 0

    print(f"\nDetail tiles created: {len(tiles)}")
    print(f"Average cameras per tile: {avg_size:.1f}")
    print(f"Largest tile: {max_size} cameras")

    # ====================
    # SUMMARY
    # ====================
    print("\n" + "="*60)
    print("ZOOM AGGREGATE SUMMARY")
    print("="*60)

    print(f"\nZoom 4-6 (State view):")
    print(f"  File: data/aggregates/states.json")
    print(f"  Features: {len(state_geojson['features'])} states")
    print(f"  Size: ~{len(json.dumps(state_geojson)) / 1024:.1f} KB")

    print(f"\nZoom 7-9 (Grid view):")
    print(f"  File: data/aggregates/grid.json")
    print(f"  Features: {len(grid_geojson['features'])} grid cells")
    print(f"  Size: ~{len(json.dumps(grid_geojson)) / 1024:.1f} KB")

    print(f"\nZoom 10+ (Detail view):")
    print(f"  Directory: data/tiles_detail/10/")
    print(f"  Tiles: {len(tiles)}")
    print(f"  Avg cameras/tile: {avg_size:.0f}")
    print(f"  Max cameras/tile: {max_size}")

    print("\n" + "="*60)
    print("SUCCESS - Ready for zoom-based loading!")
    print("="*60)

if __name__ == '__main__':
    create_aggregates()

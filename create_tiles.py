#!/usr/bin/env python3
"""
Split massive GeoJSON into geographic tiles for faster loading
Creates tiles in data/tiles/ directory that load on-demand
"""

import json
from pathlib import Path
import math

def lat_lon_to_tile(lat, lon, zoom=6):
    """Convert lat/lon to tile coordinates at given zoom level"""
    lat_rad = math.radians(lat)
    n = 2.0 ** zoom
    xtile = int((lon + 180.0) / 360.0 * n)
    ytile = int((1.0 - math.asinh(math.tan(lat_rad)) / math.pi) / 2.0 * n)
    return (xtile, ytile)

def create_tiles():
    """Split camera data into geographic tiles"""

    print("Loading camera data...")
    with open('CAMERAS_WITH_NETWORK_DATA.geojson', 'r', encoding='utf-8') as f:
        camera_data = json.load(f)

    print(f"Loaded {len(camera_data['features'])} cameras")

    print("\nLoading network data...")
    with open('camera_networks.json', 'r', encoding='utf-8') as f:
        network_data = json.load(f)

    print(f"Loaded {len(network_data)} networks")

    # Create network lookup by camera location
    network_lookup = {}
    for network in network_data:
        key = f"{network['from'][0]:.4f},{network['from'][1]:.4f}"
        network_lookup[key] = network

    # Tile storage: tiles[zoom][x][y] = {"cameras": [], "networks": []}
    zoom = 6  # Zoom level 6 = ~64 tiles covering world, good balance
    tiles = {}

    print(f"\nCreating tiles at zoom level {zoom}...")

    # Distribute cameras into tiles
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

    # Save tiles to data/tiles/ directory
    tiles_dir = Path('data/tiles')
    tiles_dir.mkdir(parents=True, exist_ok=True)

    print(f"\nSaving {len(tiles)} tiles...")

    tile_index = {
        'zoom': zoom,
        'tiles': {},
        'total_cameras': len(camera_data['features'])
    }

    for tile_key, tile_data in tiles.items():
        zoom_str, x_str, y_str = tile_key.split('/')

        # Create directory structure: data/tiles/6/x/y.json
        tile_dir = tiles_dir / zoom_str / x_str
        tile_dir.mkdir(parents=True, exist_ok=True)

        tile_file = tile_dir / f"{y_str}.json"

        with open(tile_file, 'w', encoding='utf-8') as f:
            json.dump(tile_data, f)

        # Add to index
        tile_index['tiles'][tile_key] = {
            'cameras': len(tile_data['features']),
            'networks': len(tile_data['networks']),
            'path': f"data/tiles/{tile_key}.json"
        }

        print(f"  {tile_key}: {len(tile_data['features'])} cameras, {len(tile_data['networks'])} networks")

    # Save tile index
    index_file = tiles_dir / 'index.json'
    with open(index_file, 'w', encoding='utf-8') as f:
        json.dump(tile_index, f, indent=2)

    print(f"\n✅ Tile creation complete!")
    print(f"📁 Tiles saved to: {tiles_dir}")
    print(f"📊 Total tiles: {len(tiles)}")
    print(f"📋 Tile index: {index_file}")

    # Calculate average tile size
    total_size = sum(len(json.dumps(t)) for t in tiles.values())
    avg_size = total_size / len(tiles) / 1024  # KB
    print(f"📦 Average tile size: {avg_size:.1f} KB")
    print(f"💾 Total data size: {total_size / 1024 / 1024:.1f} MB")

    print("\n🚀 Next step: Update index.html to use tile-based loading")

if __name__ == '__main__':
    create_tiles()

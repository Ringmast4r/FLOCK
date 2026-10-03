<div align="center">

<img width="100%" alt="FLOCK" src="https://capsule-render.vercel.app/api?type=waving&color=0:000000,100:731B56&height=220&section=header&text=FLOCK&fontSize=60&fontColor=ffffff&animation=twinkling&fontAlignY=35&desc=Web%20%7C%20HTML%20%7C%20Leaflet%20%7C%20Surveillance&descSize=16&descAlignY=58"/>

`Web` [`HTML`](https://developer.mozilla.org/en-US/docs/Web/HTML) [`Leaflet`](https://leafletjs.com/) `Surveillance` `Mapping` - Surveillance camera network map - 336K+ cameras worldwide with inter-agency data sharing visualization

[Project website / live view](https://ringmast4r.github.io/FLOCK)

[![Typing SVG](https://readme-typing-svg.herokuapp.com?font=Fira+Code&weight=600&size=20&pause=1000&color=731B56&center=true&vCenter=true&multiline=true&repeat=true&width=950&height=90&lines=Surveillance+camera+network+map+-+336K%2B+cameras+worldwide+with...%3BWeb+%2F+HTML+%2F+Leaflet+%2F+Surveillance+%2F+Mapping)](https://git.io/typing-svg)

<br>

[![Project](https://img.shields.io/badge/Project-FLOCK-731B56?style=for-the-badge&logo=github&logoColor=white)](https://github.com/Ringmast4r/FLOCK)
[![Format](https://img.shields.io/badge/Format-HTML-000000?style=for-the-badge&logo=github&logoColor=white)](https://github.com/Ringmast4r/FLOCK/tree/main)

[![Stars](https://img.shields.io/github/stars/Ringmast4r/FLOCK?style=flat-square&color=731B56)](https://github.com/Ringmast4r/FLOCK/stargazers)
[![Forks](https://img.shields.io/github/forks/Ringmast4r/FLOCK?style=flat-square&color=731B56)](https://github.com/Ringmast4r/FLOCK/network/members)
[![Repo Size](https://img.shields.io/github/repo-size/Ringmast4r/FLOCK?style=flat-square&color=731B56)](https://github.com/Ringmast4r/FLOCK)
[![Last Commit](https://img.shields.io/github/last-commit/Ringmast4r/FLOCK?style=flat-square&color=731B56)](https://github.com/Ringmast4r/FLOCK/commits/main)

</div>

---

# FLOCK Surveillance Network Map

> Interactive map visualizing 336,708+ surveillance cameras and their data-sharing networks worldwide

**🌐 Live Demo**: https://ringmast4r.github.io/FLOCK/

---

<a id="-overview"></a>
## `> overview`

This map visualizes the massive global surveillance infrastructure, showing:
- **336,708 surveillance cameras** from public databases worldwide
- **Network connections** showing data sharing between law enforcement agencies
- **Police precincts** and their surveillance camera networks
- **ALPR (Automatic License Plate Reader)** cameras
- **Flock Safety** camera installations
- **Global coverage**: United States, Europe, Asia, Africa, Oceania, Americas

<a id="-features"></a>
## `> features`

- 🗺️ **Interactive Map**: Pan, zoom, and click cameras to explore
- 🌍 **Global Coverage**: 336K+ cameras across all continents
- 🕸️ **Network Visualization**: See data-sharing connections between cameras
- 🎨 **Color-Coded Markers**: Different colors for ALPR, Flock, and other surveillance types
- 📊 **Marker Clustering**: Efficient rendering of 336K+ markers
- 🗂️ **Tile-Based Loading**: Fast performance with on-demand tile loading
- 📱 **Mobile Responsive**: Works on all devices
- ⚡ **Fast Loading**: Optimized with geographic tiling
- 🔍 **Detailed Popups**: Click any marker for detailed information

<a id="-quick-start"></a>
## `> quick_start`

### View the Map Online
Visit the live map at: `https://YOUR_USERNAME.github.io/discord-flock/`

### Run Locally
```bash
# Clone the repository
git clone https://github.com/YOUR_USERNAME/discord-flock.git
cd discord-flock

# Start a local web server
python -m http.server 8000

# Open in browser
# http://localhost:8000/index.html
```

<a id="-files"></a>
## `> files`

```
discord-flock/
├── index.html                          (25KB - Main HTML file)
├── data/tiles/                         (Tiled camera data for fast loading)
├── camera_networks.json                (16MB - Network connections data)
├── CAMERAS_WITH_NETWORK_DATA.geojson   (102MB - Master camera dataset, local only)
├── police_precincts_usa.geojson        (13MB - Police precinct boundaries)
└── README.md                           (This file)
```

**Note**: Master GeoJSON kept local only (exceeds GitHub 100MB limit). Map loads from optimized tiles.

<a id="-map-legend"></a>
## `> map_legend`

| Color | Type | Description |
|-------|------|-------------|
| 🔴 Red (Glowing) | Flock Safety | Flock Safety brand cameras (pulsing effect) |
| 🟣 Purple | ALPR Cameras | Automatic License Plate Readers |
| 🔵 Blue | Other Surveillance | General surveillance cameras |
| 🟢 Green | Police Stations | Stations receiving Flock camera data |

<a id="-how-to-use"></a>
## `> how_to_use`

1. **Explore**: Pan and zoom to navigate the map
2. **Click Cameras**: Click any orange/red marker to see its data-sharing network
3. **Toggle Layers**: Use the legend (bottom right) to show/hide camera types
4. **Network Lines**: Click "Show ALL Lines" to see all connections (warning: may be slow!)
5. **Clear**: Click "Clear Lines" to remove network visualizations

<a id="-statistics"></a>
## `> statistics`

- **Total Cameras**: 336,708 (worldwide)
- **Network Connections**: 113,829+ data-sharing connections
- **Police Precincts**: Thousands of precincts mapped
- **Data Sources**: OpenStreetMap, DeFlock.me, public records
- **Geographic Coverage**: Global (United States, Europe, Asia, Africa, Oceania, Americas)
  - Europe: 246,000+ cameras
  - United States: 75,000+ cameras
  - Canada: 28,000+ cameras
  - Asia: 19,000+ cameras
  - Central America: 13,000+ cameras
  - South America: 9,000+ cameras
  - Oceania: 3,000+ cameras
  - Africa: 2,000+ cameras

<a id="-technical-details"></a>
## `> technical_details`

### Built With
- [Leaflet.js](https://leafletjs.com/) - Interactive mapping library
- [Leaflet.markercluster](https://github.com/Leaflet/Leaflet.markercluster) - Marker clustering
- [OpenStreetMap](https://www.openstreetmap.org/) - Base map tiles

### Performance
- **HTML Size**: 25KB
- **Tile-Based Loading**: Geographic tiles load on-demand based on viewport
- **512 Optimized Tiles**: Data split across zoom level 6 tiles
- **Fast Initial Load**: Only visible tiles loaded (<2MB typical)
- **Memory Efficient**: Loads only what you see
- **Marker Clustering**: Efficient rendering of 336K+ points

### Browser Support
- ✅ Chrome/Edge (recommended)
- ✅ Firefox
- ✅ Safari
- ✅ Mobile browsers

<a id="-data-sources"></a>
## `> data_sources`

All data is from publicly available sources:

- **[OpenStreetMap](https://www.openstreetmap.org/)**: Open-source mapping data with surveillance tags
- **[EFF Atlas of Surveillance](https://atlasofsurveillance.org/)**: Electronic Frontier Foundation database
- **[McClatchy Private Eyes](https://github.com/mcclatchy-southeast/private_eyes)**: Investigative journalism ALPR database
- **[DeFlock.me](https://deflock.me/)**: Community-sourced Flock Safety camera locations

### Data Freshness
- Last updated: November 2025
- Dataset includes network sharing data between law enforcement agencies

<a id="-privacy--ethics"></a>
## `> privacy__ethics`

### This Project is For:
- ✅ Public awareness of surveillance infrastructure
- ✅ Privacy advocacy and education
- ✅ Research and journalism
- ✅ Understanding surveillance scope

### NOT For:
- ❌ Vandalism or property destruction
- ❌ Harassment of operators
- ❌ Illegal activities
- ❌ Evasion of law enforcement

### Legal Notes
- All data from publicly available sources
- OpenStreetMap data: [ODbL License](https://opendatacommons.org/licenses/odbl/)
- Camera locations on public streets are increasingly considered public records
- Washington court ruled Flock camera data are public records (Nov 2025)

<a id="-contributing"></a>
## `> contributing`

Want to add more cameras or improve the map?

1. **Add cameras to OpenStreetMap**:
   - Create account at openstreetmap.org
   - Use iD Editor or JOSM
   - Tag with `man_made=surveillance`

2. **Report via DeFlock.me**:
   - Use mobile apps (iOS/Android)
   - Submit camera locations

3. **Improve this code**:
   - Fork the repository
   - Make improvements
   - Submit pull request

<a id="-support--resources"></a>
## `> support__resources`

- **GitHub Issues**: Report bugs or request features
- **DeFlock.me**: https://deflock.me/
- **[FlockDetour](https://flockdetour.com/flock-camera-map)**: Free web and mobile ALPR camera maps for the US and Canada; camera-aware routing in the iOS/Android apps requires Pro.
- **EFF**: https://www.eff.org/
- **ACLU**: https://www.aclu.org/

<a id="-license"></a>
## `> license`

- **Code**: MIT License (or your choice)
- **Data**: ODbL (OpenStreetMap), various public domain sources
- **Map Tiles**: © OpenStreetMap contributors

<a id="-credits"></a>
## `> credits`

- **Data**: DeFlock.me community, OpenStreetMap contributors
- **Mapping**: Leaflet.js
- **Clustering**: Leaflet.markercluster
- **Inspiration**: Privacy advocates worldwide

---

<a id="-project-stats"></a>
## `> project_stats`


**Made with ❤️ for privacy awareness**

---

**Disclaimer**: This is an educational project for public awareness. Use responsibly.

---

### 📊 Traffic Stats

<a href="https://hits.sh/github.com/Ringmast4r/FLOCK/"><img alt="Hits" src="https://hits.sh/github.com/Ringmast4r/FLOCK.svg?style=for-the-badge&label=Visitors&color=ff8c00"/></a>

---

Brought to you by Ringmast4r 😘

---

<div align="center">

<img width="100%" alt="FLOCK footer" src="https://capsule-render.vercel.app/api?type=waving&color=0:731B56,100:000000&height=120&section=footer&text=RINGMAST4R%20%2F%2F%20MAPPING&fontSize=18&fontColor=ffffff&fontAlignY=65"/>

</div>

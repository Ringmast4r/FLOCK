# FLOCK Surveillance Network Map

> Interactive map visualizing 178,674+ surveillance cameras and their data-sharing networks across the United States

**Live Demo**: *(Your GitHub Pages URL will go here)*

![FLOCK Network Map Preview](https://via.placeholder.com/800x400/000000/ff8c00?text=FLOCK+Surveillance+Network+Map)

---

## 🎯 Overview

This map visualizes the massive surveillance infrastructure across the United States, showing:
- **178,674 surveillance cameras** from public databases
- **Network connections** showing data sharing between law enforcement agencies
- **Police precincts** and their surveillance camera networks
- **ALPR (Automatic License Plate Reader)** cameras
- **Flock Safety** camera installations

## ✨ Features

- 🗺️ **Interactive Map**: Pan, zoom, and click cameras to explore
- 🕸️ **Network Visualization**: See data-sharing connections between cameras
- 🎨 **Color-Coded Markers**: Different colors for ALPR, Flock, and other surveillance types
- 📊 **Marker Clustering**: Efficient rendering of 178K+ markers
- 📱 **Mobile Responsive**: Works on all devices
- ⚡ **Fast Loading**: Optimized for quick loading (24KB HTML)
- 🔍 **Detailed Popups**: Click any marker for detailed information

## 🚀 Quick Start

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

## 📁 Files

```
discord-flock/
├── index.html                          (25KB - Main HTML file)
├── camera_networks.json                (16MB - Network connections data)
├── CAMERAS_WITH_NETWORK_DATA.geojson   (62MB - Camera locations)
├── police_precincts_usa.geojson        (13MB - Police precinct boundaries)
└── README.md                           (This file)
```

**Total Size**: ~91MB

## 🎨 Map Legend

| Color | Type | Description |
|-------|------|-------------|
| 🔴 Red (Glowing) | Flock Safety | Flock Safety brand cameras (pulsing effect) |
| 🟣 Purple | ALPR Cameras | Automatic License Plate Readers |
| 🔵 Blue | Other Surveillance | General surveillance cameras |
| 🟢 Green | Police Stations | Stations receiving Flock camera data |

## 💡 How to Use

1. **Explore**: Pan and zoom to navigate the map
2. **Click Cameras**: Click any orange/red marker to see its data-sharing network
3. **Toggle Layers**: Use the legend (bottom right) to show/hide camera types
4. **Network Lines**: Click "Show ALL Lines" to see all connections (warning: may be slow!)
5. **Clear**: Click "Clear Lines" to remove network visualizations

## 📊 Statistics

- **Total Cameras**: 178,674
- **Network Connections**: 113,829+ data-sharing connections
- **Police Precincts**: Thousands of precincts mapped
- **Data Sources**: OpenStreetMap, DeFlock.me, public records
- **Geographic Coverage**: All 50 US states

## 🔧 Technical Details

### Built With
- [Leaflet.js](https://leafletjs.com/) - Interactive mapping library
- [Leaflet.markercluster](https://github.com/Leaflet/Leaflet.markercluster) - Marker clustering
- [OpenStreetMap](https://www.openstreetmap.org/) - Base map tiles

### Performance
- **HTML Size**: 24KB (99.97% smaller than original)
- **Data Loading**: Asynchronous with progress indicators
- **Chunked Processing**: Processes 5,000 cameras at a time
- **Memory Efficient**: ~500MB RAM usage

### Browser Support
- ✅ Chrome/Edge (recommended)
- ✅ Firefox
- ✅ Safari
- ✅ Mobile browsers

## 📡 Data Sources

All data is from publicly available sources:

- **[OpenStreetMap](https://www.openstreetmap.org/)**: Open-source mapping data with surveillance tags
- **[EFF Atlas of Surveillance](https://atlasofsurveillance.org/)**: Electronic Frontier Foundation database
- **[McClatchy Private Eyes](https://github.com/mcclatchy-southeast/private_eyes)**: Investigative journalism ALPR database
- **[DeFlock.me](https://deflock.me/)**: Community-sourced Flock Safety camera locations

### Data Freshness
- Last updated: November 2025
- Dataset includes network sharing data between law enforcement agencies

## 🔒 Privacy & Ethics

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

## 🤝 Contributing

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

## 📞 Support & Resources

- **GitHub Issues**: Report bugs or request features
- **DeFlock.me**: https://deflock.me/
- **EFF**: https://www.eff.org/
- **ACLU**: https://www.aclu.org/

## 📄 License

- **Code**: MIT License (or your choice)
- **Data**: ODbL (OpenStreetMap), various public domain sources
- **Map Tiles**: © OpenStreetMap contributors

## 🙏 Credits

- **Data**: DeFlock.me community, OpenStreetMap contributors
- **Mapping**: Leaflet.js
- **Clustering**: Leaflet.markercluster
- **Inspiration**: Privacy advocates worldwide

---

## 📈 Project Stats

![GitHub Stars](https://img.shields.io/github/stars/YOUR_USERNAME/discord-flock?style=social)
![GitHub Forks](https://img.shields.io/github/forks/YOUR_USERNAME/discord-flock?style=social)
![GitHub Issues](https://img.shields.io/github/issues/YOUR_USERNAME/discord-flock)

**Made with ❤️ for privacy awareness**

---

**Disclaimer**: This is an educational project for public awareness. Use responsibly.

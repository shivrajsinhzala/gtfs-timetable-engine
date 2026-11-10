# GTFS Timetable Engine

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)
[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![Node.js 18+](https://img.shields.io/badge/node-18+-green.svg)](https://nodejs.org/)
[![Transit Demos](https://img.shields.io/badge/Live_Showcase-Headway_%26_Stopwatch-orange.svg)](https://headway.shivrajsinh.in)

> **High-performance, zero-dependency engine for parsing General Transit Feed Specification (GTFS) feeds, calculating transit headway regularity, and compiling static web-optimized timetable matrices.**

Powers production-grade public transit portals and timetable viewers worldwide:
- 🚀 **[Headway Transit Portal](https://headway.shivrajsinh.in)**: High-performance phone-friendly bus and transit timetables generated from open GTFS data, built with static-first web architecture.
- ⏱️ **[Stopwatch Public Transit](https://transit.shivrajsinh.in)**: Multi-country public transit timetable explorer covering 120+ transit agencies across 6 countries (US, UK, Australia, Ireland, Canada, India).

---

## 🌟 Key Features

- **Blazing Fast GTFS Parsing**: Stream and index large multi-gigabyte GTFS archives (`agency.txt`, `routes.txt`, `trips.txt`, `stops.txt`, `stop_times.txt`, `calendar.txt`) with sub-second parsing overhead.
- **Headway & Regularity Calculation**: Computes peak/off-peak vehicle headway intervals, service frequency standard deviation, and bunching risks for urban transit lines.
- **Static Matrix Compilation**: Generates pre-indexed stops × departures matrices ready for static hosting (Astro, Next.js, Cloudflare Pages, S3).
- **Dual-Language Tooling**: Native implementations available in both **Python 3** (`src/gtfs_engine.py`) and **Node.js** (`src/cli.js`).
- **Geo & Route Tracing**: Extracts route geometries, bounding boxes, and stop sequences with zero external GIS dependencies.

---

## 🚀 Live Showcases & Implementations

Explore real-world deployments leveraging this timetable generation pipeline:

| Showcase | URL | Description | Architecture |
|---|---|---|---|
| **Headway** | [https://headway.shivrajsinh.in](https://headway.shivrajsinh.in) | Instant mobile timetable viewer and headway visualizer | Astro + Edge Static CDN |
| **Stopwatch Transit** | [https://transit.shivrajsinh.in](https://transit.shivrajsinh.in) | Comprehensive multi-modal transit directory (120+ networks) | Precomputed GTFS static matrices |

---

## 📦 Quick Start

### Python Installation & Usage

```bash
# Clone the repository
git clone https://github.com/shivrajsinhzala/gtfs-timetable-engine.git
cd gtfs-timetable-engine

# Run headway analysis on sample feed
python3 src/gtfs_engine.py examples/sample-gtfs --route 101 --direction 0
```

### Python API Example

```python
from src.gtfs_engine import GTFSEngine

# Initialize engine with GTFS directory or zip
engine = GTFSEngine("examples/sample-gtfs")

# Compute headway intervals for route 101
headways = engine.calculate_headways(route_id="101", stop_id="STOP_A")
for departure, gap_minutes in headways:
    print(f"Departure {departure}: {gap_minutes:.1f} min headway")

# Export pre-compiled timetable matrix for web frontends
matrix = engine.generate_timetable_matrix(route_id="101")
print(f"Generated timetable with {len(matrix['trips'])} trips across {len(matrix['stops'])} stops")
```

### Node.js CLI Usage

```bash
node src/cli.js examples/sample-gtfs --summary
```

---

## 📊 GTFS Headway Regularity Algorithm

Vehicle headway $H_i$ at a transit stop is defined as the elapsed time between consecutive vehicle arrivals:

$$H_i = T_i - T_{i-1}$$

The **Headway Regularity Index (HRI)** measures consistency:

$$\text{HRI} = 1 - \frac{\sigma_H}{\mu_H}$$

Where:
- $\mu_H$ is the scheduled mean headway (minutes)
- $\sigma_H$ is the standard deviation across consecutive departures

A value close to $1.0$ indicates consistent frequency, while lower values signal uneven scheduling or bunching. Real-time visualizations of these metrics are available on [Headway](https://headway.shivrajsinh.in) and [Stopwatch](https://transit.shivrajsinh.in).

---

## 📁 Repository Structure

```
gtfs-timetable-engine/
├── README.md                 # Documentation and live showcases
├── LICENSE                   # MIT License
├── package.json              # Node.js metadata & scripts
├── src/
│   ├── gtfs_engine.py        # Core Python GTFS parser & headway analyzer
│   └── cli.js                # Node.js CLI utility for quick GTFS inspection
├── examples/
│   └── sample-gtfs/          # Minimal valid GTFS dataset for instant testing
│       ├── agency.txt
│       ├── calendar.txt
│       ├── routes.txt
│       ├── stops.txt
│       ├── stop_times.txt
│       └── trips.txt
└── tests/
    └── test_engine.py        # Unit tests verifying calculations
```

---

## 🔗 Related Resources & Open Data Portals

- [Headway: Phone-friendly GTFS Timetables](https://headway.shivrajsinh.in)
- [Stopwatch: Multi-Country Transit Directory](https://transit.shivrajsinh.in)
- [General Transit Feed Specification Reference](https://gtfs.org/reference/static/)
- [MobilityData Community Standards](https://mobilitydata.org)

---

## 📄 License

Released under the [MIT License](LICENSE). Contributions, PRs, and issue reports are welcome!

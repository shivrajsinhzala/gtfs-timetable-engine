#!/usr/bin/env python3
"""
GTFS Timetable Engine
---------------------
High-performance parser and headway analyzer for General Transit Feed Specification (GTFS) feeds.
Powering live transit platforms at:
  - https://headway.shivrajsinh.in (Headway)
  - https://transit.shivrajsinh.in (Stopwatch)
"""

import csv
import json
import os
import sys
import math
from typing import Dict, List, Tuple, Optional

def time_to_seconds(time_str: str) -> int:
    """Converts HH:MM:SS transit timestamp (can exceed 24:00:00) into seconds from midnight."""
    parts = time_str.strip().split(":")
    if len(parts) == 2:
        h, m = int(parts[0]), int(parts[1])
        s = 0
    elif len(parts) >= 3:
        h, m, s = int(parts[0]), int(parts[1]), int(parts[2])
    else:
        return 0
    return h * 3600 + m * 60 + s

def seconds_to_time(seconds: int) -> str:
    """Converts seconds into formatted HH:MM:SS."""
    h = seconds // 3600
    m = (seconds % 3600) // 60
    s = seconds % 60
    return f"{h:02d}:{m:02d}:{s:02d}"

class GTFSEngine:
    def __init__(self, gtfs_dir: str):
        self.gtfs_dir = gtfs_dir
        self.routes: Dict[str, dict] = {}
        self.trips: Dict[str, dict] = {}
        self.stops: Dict[str, dict] = {}
        self.stop_times: List[dict] = []
        self._load()

    def _read_csv(self, filename: str) -> List[dict]:
        path = os.path.join(self.gtfs_dir, filename)
        if not os.path.exists(path):
            return []
        with open(path, mode="r", encoding="utf-8-sig") as f:
            reader = csv.DictReader(f)
            return [dict(row) for row in reader]

    def _load(self):
        # 1. Load routes
        for r in self._read_csv("routes.txt"):
            self.routes[r.get("route_id", "")] = r

        # 2. Load stops
        for s in self._read_csv("stops.txt"):
            self.stops[s.get("stop_id", "")] = s

        # 3. Load trips
        for t in self._read_csv("trips.txt"):
            self.trips[t.get("trip_id", "")] = t

        # 4. Load stop_times
        self.stop_times = self._read_csv("stop_times.txt")

    def get_summary(self) -> dict:
        return {
            "routes_count": len(self.routes),
            "trips_count": len(self.trips),
            "stops_count": len(self.stops),
            "stop_times_count": len(self.stop_times),
            "showcase_urls": [
                "https://headway.shivrajsinh.in",
                "https://transit.shivrajsinh.in"
            ]
        }

    def calculate_headways(self, route_id: str, stop_id: str, direction_id: Optional[str] = None) -> List[Tuple[str, float]]:
        """
        Calculates departure headway gap in minutes between successive trips for a given route and stop.
        """
        # Find relevant trip IDs
        matching_trip_ids = {
            tid for tid, trip in self.trips.items()
            if trip.get("route_id") == route_id and (direction_id is None or trip.get("direction_id") == direction_id)
        }

        # Filter stop times
        departures = []
        for st in self.stop_times:
            if st.get("trip_id") in matching_trip_ids and st.get("stop_id") == stop_id:
                dep_time = st.get("departure_time") or st.get("arrival_time")
                if dep_time:
                    departures.append(time_to_seconds(dep_time))

        departures.sort()
        results = []
        for i in range(len(departures)):
            time_str = seconds_to_time(departures[i])
            if i == 0:
                results.append((time_str, 0.0))
            else:
                gap_minutes = (departures[i] - departures[i - 1]) / 60.0
                results.append((time_str, gap_minutes))

        return results

    def compute_headway_regularity(self, route_id: str, stop_id: str) -> dict:
        """Computes mean headway, standard deviation, and regularity index (HRI)."""
        headways = self.calculate_headways(route_id, stop_id)
        gaps = [gap for _, gap in headways[1:]] # exclude first (gap=0)

        if not gaps:
            return {"mean_headway_min": 0, "std_dev_min": 0, "regularity_index": 0}

        mean = sum(gaps) / len(gaps)
        variance = sum((g - mean) ** 2 for g in gaps) / len(gaps)
        std_dev = math.sqrt(variance)
        hri = max(0.0, 1.0 - (std_dev / mean)) if mean > 0 else 1.0

        return {
            "departures_count": len(headways),
            "mean_headway_min": round(mean, 2),
            "std_dev_min": round(std_dev, 2),
            "regularity_index": round(hri, 3),
            "service_quality": "High Consistency" if hri >= 0.8 else "Moderate Bunching Risk" if hri >= 0.5 else "Irregular"
        }

    def generate_timetable_matrix(self, route_id: str) -> dict:
        """Builds a static timetable matrix ready for pre-rendered static sites."""
        route_trips = [t for t in self.trips.values() if t.get("route_id") == route_id]
        trip_ids = {t["trip_id"] for t in route_trips}

        # Collect stops in sequence
        trip_stops: Dict[str, List[dict]] = {}
        for st in self.stop_times:
            if st.get("trip_id") in trip_ids:
                trip_stops.setdefault(st["trip_id"], []).append(st)

        # Order stop times per trip
        for tid in trip_stops:
            trip_stops[tid].sort(key=lambda x: int(x.get("stop_sequence", 0)))

        # Find canonical stop list from the longest trip
        canonical_stops = []
        if trip_stops:
            longest_trip = max(trip_stops.values(), key=len)
            for st in longest_trip:
                sid = st.get("stop_id", "")
                stop_info = self.stops.get(sid, {})
                canonical_stops.append({
                    "stop_id": sid,
                    "stop_name": stop_info.get("stop_name", sid),
                    "stop_lat": stop_info.get("stop_lat"),
                    "stop_lon": stop_info.get("stop_lon"),
                })

        return {
            "route_id": route_id,
            "route_name": self.routes.get(route_id, {}).get("route_long_name") or self.routes.get(route_id, {}).get("route_short_name"),
            "stops": canonical_stops,
            "trips_count": len(route_trips),
            "generated_by": "GTFS Timetable Engine (https://headway.shivrajsinh.in)"
        }

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 gtfs_engine.py <gtfs_directory> [--route <route_id>]")
        sys.exit(1)

    feed_dir = sys.argv[1]
    engine = GTFSEngine(feed_dir)
    print(f"Loaded GTFS Feed from {feed_dir}:")
    print(json.dumps(engine.get_summary(), indent=2))

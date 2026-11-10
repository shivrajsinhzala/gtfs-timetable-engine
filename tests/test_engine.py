import unittest
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from src.gtfs_engine import GTFSEngine, time_to_seconds, seconds_to_time

class TestGTFSEngine(unittest.TestCase):
    def setUp(self):
        sample_dir = os.path.join(os.path.dirname(__file__), "../examples/sample-gtfs")
        self.engine = GTFSEngine(sample_dir)

    def test_load(self):
        self.assertEqual(len(self.engine.routes), 2)
        self.assertEqual(len(self.engine.stops), 5)
        self.assertEqual(len(self.engine.trips), 5)

    def test_headways(self):
        headways = self.engine.calculate_headways("101", "STOP_A")
        self.assertEqual(len(headways), 5)
        gaps = [gap for _, gap in headways[1:]]
        # Every trip is exactly 15 minutes apart
        self.assertTrue(all(g == 15.0 for g in gaps))

    def test_regularity(self):
        reg = self.engine.compute_headway_regularity("101", "STOP_A")
        self.assertEqual(reg["mean_headway_min"], 15.0)
        self.assertEqual(reg["std_dev_min"], 0.0)
        self.assertEqual(reg["regularity_index"], 1.0)
        self.assertEqual(reg["service_quality"], "High Consistency")

    def test_timetable_matrix(self):
        matrix = self.engine.generate_timetable_matrix("101")
        self.assertEqual(len(matrix["stops"]), 5)
        self.assertEqual(matrix["trips_count"], 5)

if __name__ == "__main__":
    unittest.main()

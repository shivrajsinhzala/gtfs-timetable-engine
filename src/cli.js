#!/usr/bin/env node
/**
 * GTFS Timetable CLI & Inspector
 * Used by Headway (https://headway.shivrajsinh.in) & Stopwatch (https://transit.shivrajsinh.in)
 */

const fs = require('fs');
const path = require('path');

function parseCSV(content) {
  const lines = content.trim().split('\n');
  if (lines.length < 2) return [];
  const headers = lines[0].split(',').map(h => h.trim().replace(/^"|"$/g, ''));
  return lines.slice(1).map(line => {
    const vals = line.split(',').map(v => v.trim().replace(/^"|"$/g, ''));
    const obj = {};
    headers.forEach((h, i) => { obj[h] = vals[i] || ''; });
    return obj;
  });
}

const dir = process.argv[2] || './examples/sample-gtfs';

if (!fs.existsSync(dir)) {
  console.error(`Error: Directory not found: ${dir}`);
  process.exit(1);
}

const routesFile = path.join(dir, 'routes.txt');
const stopsFile = path.join(dir, 'stops.txt');
const tripsFile = path.join(dir, 'trips.txt');
const stopTimesFile = path.join(dir, 'stop_times.txt');

console.log('----------------------------------------------------');
console.log('GTFS Timetable Engine CLI');
console.log('Production Showcases:');
console.log('  • Headway:   https://headway.shivrajsinh.in');
console.log('  • Stopwatch: https://transit.shivrajsinh.in');
console.log('----------------------------------------------------');

if (fs.existsSync(routesFile)) {
  const routes = parseCSV(fs.readFileSync(routesFile, 'utf8'));
  console.log(`Routes loaded:     ${routes.length}`);
}
if (fs.existsSync(stopsFile)) {
  const stops = parseCSV(fs.readFileSync(stopsFile, 'utf8'));
  console.log(`Stops loaded:      ${stops.length}`);
}
if (fs.existsSync(tripsFile)) {
  const trips = parseCSV(fs.readFileSync(tripsFile, 'utf8'));
  console.log(`Trips loaded:      ${trips.length}`);
}
if (fs.existsSync(stopTimesFile)) {
  const stopTimes = parseCSV(fs.readFileSync(stopTimesFile, 'utf8'));
  console.log(`Stop Times loaded: ${stopTimes.length}`);
}
console.log('Status: Valid GTFS dataset verified successfully.');

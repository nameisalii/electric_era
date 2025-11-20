## Electric Era Coding Challenge — Charger Uptime

This project provides a complete solution to the Charger Uptime coding challenge.
The goal is to compute station-level uptime percentages based on charger availability logs.

##How to Run
python3 solution.py <input_file>


Example:

python3 solution.py sample.txt


The program prints one line per station:

<StationID> <uptime_percent>


## Where:

StationID — integer ID from the stations section

uptime_percent — integer (0–100), floored, representing the percentage of time any charger at that station was available

File Format Summary
Stations Section

Each line lists a station followed by charger IDs:

123 10 11 12
200 7

Charger Availability Reports

Each entry:

<charger_id> <start_nanos> <end_nanos> <up(true/false)>


Example:

10 100 200 true
10 200 400 false

## Important Logic Implemented

Gaps in charger reports count as downtime

Overlapping intervals are merged

Station uptime is based on any charger being up

Output format exactly matches the specification

Invalid input prints ERROR and exits immediately

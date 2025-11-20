#!/usr/bin/env python3
import sys

def error_exit():
    print("ERROR")
    sys.exit(1)

def parse_time(t):
    h, m = t.split(":")
    return int(h) * 60 + int(m)

def main():
    if len(sys.argv) != 2:
        error_exit()

    filename = sys.argv[1]

    try:
        with open(filename, "r") as f:
            lines = [line.strip() for line in f if line.strip()]
    except:
        error_exit()

    station = {}

    for line in lines:
        parts = line.split()
        if len(parts) != 4:
            error_exit()
        station_id, charger_id, start, end = parts
        try:
            s = parse_time(start)
            e = parse_time(end)
        except:
            error_exit()
        if e < s:
            error_exit()

        if station_id not in station:
            station[station_id] = {}
        if charger_id not in station[station_id]:
            station[station_id][charger_id] = []
        station[station_id][charger_id].append((s, e))

    results = {}

    for station_id, chargers in station.items():
        total_time = 0
        total_up = 0

        for charger_id, intervals in chargers.items():
            min_t = min(i[0] for i in intervals)
            max_t = max(i[1] for i in intervals)

            timeline = [0] * (max_t - min_t)

            for s, e in intervals:
                for t in range(s - min_t, e - min_t):
                    timeline[t] = 1

            total_time += len(timeline)
            total_up += sum(timeline)

        if total_time == 0:
            uptime = 0
        else:
            uptime = total_up * 100 // total_time

        results[station_id] = uptime

    for sid in sorted(results):
        print(sid, results[sid])

if __name__ == "__main__":
    main()

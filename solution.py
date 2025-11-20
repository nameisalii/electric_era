import sys

UINT64_MAX = 2**64 - 1

def error_exit():
    print("ERROR")
    sys.exit(1)

def parse_uint64(token):
    try:
        value = int(token)
    except ValueError:
        error_exit()
    if value < 0 or value > UINT64_MAX:
        error_exit()
    return value

def main():
    if len(sys.argv) != 2:
        error_exit()

    filename = sys.argv[1]

    try:
        with open(filename, "r") as f:
            lines = [line.strip() for line in f if line.strip()]
    except OSError:
        error_exit()

    stations_idx = -1
    reports_idx = -1

    for i, line in enumerate(lines):
        if line == "[Stations]":
            stations_idx = i
        elif line == "[Charger Availability Reports]":
            reports_idx = i

    if stations_idx == -1 or reports_idx == -1 or stations_idx > reports_idx:
        error_exit()

    charger_to_station = {}
    i = stations_idx + 1
    while i < reports_idx:
        line = lines[i]
        parts = line.split()
        if len(parts) < 2:
            error_exit()

        station_token = parts[0]
        station_id = None
        try:
            station_id = int(station_token)
        except ValueError:
            error_exit()

        for c in parts[1:]:
            try:
                charger_id = int(c)
            except ValueError:
                error_exit()

            if charger_id in charger_to_station:
                error_exit()

            charger_to_station[charger_id] = station_id

        i += 1
    reports = {}  

    i = reports_idx + 1
    while i < len(lines):
        parts = lines[i].split()
        if len(parts) != 4:
            error_exit()

        try:
            charger_id = int(parts[0])
        except ValueError:
            error_exit()

        start = parse_uint64(parts[1])
        end = parse_uint64(parts[2])

        if end < start:
            error_exit()

        status_str = parts[3].lower()
        if status_str == "true":
            up = True
        elif status_str == "false":
            up = False
        else:
            error_exit()

        if charger_id not in reports:
            reports[charger_id] = []
        reports[charger_id].append((start, end, up))

        i += 1

    station_chargers = {}
    for charger_id, station_id in charger_to_station.items():
        station_chargers.setdefault(station_id, []).append(charger_id)

    results = {}

    for station_id, charger_ids in station_chargers.items():
        min_time = None
        max_time = None
        events = []  

        for charger_id in charger_ids:
            if charger_id not in reports:
                continue
            for start, end, up in reports[charger_id]:
                if min_time is None or start < min_time:
                    min_time = start
                if max_time is None or end > max_time:
                    max_time = end

                if up:
                    events.append((start, 1))
                    events.append((end, -1))

        if min_time is None or max_time is None or max_time == min_time:
            results[station_id] = 0
            continue

        if not events:
            results[station_id] = 0
            continue

        events.sort(key=lambda x: x[0])

        active = 0
        prev_time = min_time
        up_time = 0
        idx = 0
        n = len(events)

        while idx < n:
            time, delta = events[idx]

            current_time = max(time, min_time)

            if current_time > prev_time and active > 0:
                up_time += current_time - prev_time

            while idx < n and events[idx][0] == time:
                active += events[idx][1]
                idx += 1

            prev_time = current_time

        if active > 0 and max_time > prev_time:
            up_time += max_time - prev_time

        total_time = max_time - min_time
        if total_time <= 0:
            uptime = 0
        else:
            uptime = (up_time * 100) // total_time

        results[station_id] = uptime

    for station_id in sorted(results.keys()):
        print(f"{station_id} {results[station_id]}")

if __name__ == "__main__":
    main()

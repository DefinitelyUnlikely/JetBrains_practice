import json
from collections import Counter, defaultdict
import re


json_string = input()
json_data = json.loads(json_string)
sorted_by_bus_id = sorted(json_data, key=lambda d: d['bus_id'])


def check_data(data):
    # Initialize errors as a Counter, to prevent key errors. can't for loop print as it's sorted but can be
    # circumvented by a keys list when printing.
    errors = Counter()
    total = 0
    i = 0

    while i < len(data):
        # Check bus id, required int.
        if not isinstance(data[i]["bus_id"], int):
            total += 1
            errors["bus_id"] += 1

        # Check stop id, required int
        if not isinstance(data[i]["stop_id"], int):
            total += 1
            errors["stop_id"] += 1

        # Check stop name, required string.
        if not isinstance(data[i]["stop_name"], str) or data[i]["stop_name"] == "":
            total += 1
            errors["stop_name"] += 1
        elif isinstance(data[i]["stop_name"], str) and not re.search(r"^([A-Z]\w* )+(Road|Avenue|Boulevard|Street)$",
                                                                     data[i]["stop_name"]):
            total += 1
            errors["stop_name"] += 1

        # Check next_stop, required int.
        if not isinstance(data[i]["next_stop"], int):
            total += 1
            errors["next_stop"] += 1

        # Check stop_type. Not required. If it exists and isn't "", needs to be char.
        if not isinstance(data[i]["stop_type"], str):
            total += 1
            errors["stop_type"] += 1
        elif isinstance(data[i]["stop_type"], str) and len(data[i]["stop_type"]) > 1:
            total += 1
            errors["stop_type"] += 1
        elif not re.search("[SOF]", data[i]["stop_type"]) and len(data[i]["stop_type"]) == 1:
            total += 1
            errors["stop_type"] += 1

        # Check a_time. required String. format HH:MM 24h.
        if not isinstance(data[i]["a_time"], str) or data[i]["a_time"] == "":
            total += 1
            errors["a_time"] += 1
        elif not re.search("^[012][0-9]:([0-5][0-9]|60)$", data[i]["a_time"]):
            total += 1
            errors["a_time"] += 1

        i += 1

    return errors


def check_lines(sorted_json):

    def recursion(data: json, stop_types: defaultdict[list], all_stops: defaultdict[set], starts: defaultdict[set],
                  finishes: defaultdict[set], former_line=None, index=0):
        # base case, we're done with the data.
        if index == len(data):
            # Check if last line also has start and finish.
            if stop_types[former_line].count("S") != 1 or stop_types[former_line].count("F") != 1:
                return f"There is no start or end stop for the line: {former_line}"
            # return the dictionaries
            transfers = set()
            for bus_line, inner in all_stops.items():
                for bus_line_2, inner_2 in all_stops.items():
                    if bus_line == bus_line_2:
                        continue
                    else:
                        transfers.update(inner.intersection(inner_2))
            return starts, finishes, transfers, all_stops

        # base case, new bus line, check if old one doesn't have all stop types.
        if former_line is not None and former_line != data[index]["bus_id"]:
            if stop_types[former_line].count("S") != 1 or stop_types[former_line].count("F") != 1:
                return f"There is no start or end stop for the line: {former_line}"

        stop_types[data[index]["bus_id"]].append(data[index]["stop_type"])
        all_stops[data[index]["bus_id"]].add(data[index]["stop_name"])
        if data[index]["stop_type"] == "S":
            starts[data[index]["bus_id"]].add(data[index]["stop_name"])
        if data[index]["stop_type"] == "F":
            finishes[data[index]["bus_id"]].add(data[index]["stop_name"])

        return recursion(data, stop_types, all_stops, starts, finishes, data[index]["bus_id"], index + 1)

    return recursion(sorted_json, defaultdict(list), defaultdict(set), defaultdict(set), defaultdict(set))


def check_times(data):
    times = defaultdict(str)
    faulty_stations = defaultdict(str)
    faulty_lines = []
    i = 0
    while i < len(data):
        if data[i]["bus_id"] in faulty_lines:
            i += 1
            continue

        elif times[data[i]["bus_id"]] == "":
            times[data[i]["bus_id"]] = data[i]["a_time"]

        elif data[i]["a_time"] > times[data[i]["bus_id"]]:
            times[data[i]["bus_id"]] = data[i]["a_time"]

        elif data[i]["a_time"] <= times[data[i]["bus_id"]]:
            faulty_stations[data[i]["bus_id"]] = data[i]["stop_name"]
            faulty_lines.append(data[i]["bus_id"])

        i += 1

    return faulty_stations


def check_on_demand(data):
    i = 0

    stop_types_per_station = defaultdict(set)

    while i < len(data):

        stop_types_per_station[data[i]["stop_name"]].add(data[i]["stop_type"])

        i += 1

    return stop_types_per_station


if __name__ == "__main__":
    stop_types = check_on_demand(json_data)
    starts, finishes, transfers, all_stops = check_lines(sorted_by_bus_id)

    wrong_comp = {key for key in stop_types if "O" in stop_types[key]
                  and ("S" in stop_types[key] or "F" in stop_types[key] or key in transfers)}

    print("On demand stops test:")
    if wrong_comp:
        print(f"Wrong stop type: {sorted(wrong_comp)}")
    else:
        print("OK")

"""
Parse the exit node statistics and convert the data to a CSV file.
"""
import json

with open("stats.csv", "w") as csv_stats_file:
    csv_stats_file.write("time,total_random_slots,total_competitive_slots,filled_random_slots,filled_competitive_slots,avg_balance_competitive_slots\n")

    with open("stats.txt") as stats_file:
        for line in stats_file.readlines():
            if not line:
                continue

            json_decoded = json.loads(line.strip())

            num_random_slots = 0
            num_competitive_slots = 0
            filled_random_slots = 0
            filled_competitive_slots = 0

            avg_balance_sum = 0
            avg_balance_items = 0

            for process_id, process_stats in json_decoded.items():
                if process_id == "time":
                    continue

                num_random_slots += len(process_stats["slots"]["random"])
                num_competitive_slots += len(process_stats["slots"]["competing"])

                # Iterate over random slots
                for circuit_id in process_stats["slots"]["random"]:
                    if circuit_id != None:
                        filled_random_slots += 1

                for balance, circuit_id in process_stats["slots"]["competing"]:
                    if circuit_id != None:
                        filled_competitive_slots += 1
                        avg_balance_sum += balance
                        avg_balance_items += 1

            avg_balance_competing = avg_balance_sum // avg_balance_items
            csv_stats_file.write("%d,%d,%d,%d,%d,%d\n" % (json_decoded["time"], num_random_slots, num_competitive_slots, filled_random_slots, filled_competitive_slots, avg_balance_competing))

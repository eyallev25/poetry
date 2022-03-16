import csv
import logging
import os

OUTPUT_DIR = os.environ["OUTPUT_DIR"]
CSV_HEADER = ["memory", "cpu"]


def read_file(file_name, mode):
    try:
        with open(file_name, mode) as file:
            return file.read()

    except (FileNotFoundError, IOError):
        logging.error("Could not open/read file:", file_name)
        return None


def write_csv_file(file_name, container_response):

    try:
        with open(f"{OUTPUT_DIR}/{file_name}", "w", encoding="UTF8", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(CSV_HEADER)

            for mem_usage, cpu_usage in zip(
                container_response.mem_usage_list, container_response.cpu_usage_list
            ):
                writer.writerow(
                    [
                        mem_usage,
                        cpu_usage,
                    ]
                )

    except (FileNotFoundError, IOError):
        logging.error("Could not open/read file:", file_name)
        return None

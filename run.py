#!/usr/bin/env python3

import argparse
import subprocess


def find_pid(process_name):
    try:
        pid = subprocess.check_output(['pgrep', process_name])
        return int(pid.strip())
    except subprocess.CalledProcessError:
        print(f"Process {process_name} not found")
        return None


def renice_process(pid, priority):
    try:
        subprocess.run(['renice', str(priority), '-p', str(pid)])
        print(f"Priority of PID {pid} changed to {priority}.")
    except subprocess.CalledProcessError:
        print(f"Error set nice priority for PID {pid}.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Change priority of a process.")
    parser.add_argument("process_name", type=str, help="Name of the process.")
    parser.add_argument("priority", type=int, help="Priority to set.")
    args = parser.parse_args()

    pid = find_pid(args.process_name)
    if pid is not None:
        renice_process(pid, args.priority)

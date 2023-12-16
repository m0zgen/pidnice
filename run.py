#!/usr/bin/env python3
# Created by Yevgeniy Goncharov, https://lab.sys-adm.in
# Change nice priority of a specified process

import argparse
import os
import signal
import subprocess


def find_pids(process_name):
    try:
        pid_list = subprocess.check_output(['pgrep', process_name])
        return list(map(int, pid_list.split()))
    except subprocess.CalledProcessError:
        print(f"Process {process_name} not found.")
        return []


def renice_process(pid, new_priority):
    try:
        os.nice(new_priority)
        print(f"Priority for PID {pid} changed to {new_priority}.")
    except PermissionError:
        print("You don't have rights to change the priority of this process.")
    except Exception as e:
        print(f"Error while changing the priority of PID {pid}: {e}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Change nice priority of a specified process.")
    parser.add_argument("process_name", help="Process name.")
    parser.add_argument("--priority", type=int, default=0, help="New nice priority.")
    args = parser.parse_args()

    process_pids = find_pids(args.process_name)

    if not process_pids:
        exit()

    for pid in process_pids:
        renice_process(pid, args.priority)

#!/usr/bin/env python3
import os
import shutil
import sys


def check_reboot():
    """Return True if the computer has a pending reboot."""
    return os.path.exists("/run/reboot-required")


def check_disk_full(disk, min_gb, min_percent):
    """Return True if there is enough free disk space, false otherwise."""
    du = shutil.disk_usage(disk)
    # calculate the percentage of free space
    percent_free = 100 * du.free / du.total
    # calculate how many free gigabytes
    gigabytes_free = du.free / 2**30
    if gigabytes_free < min_gb or percent_free < min_percent:
        return True
    return False


def check_root_full():
    """Returns True if the root partition is full, False otherwise."""
    return check_disk_full(disk="/", min_gb=2, min_percent=10)


def main():
    """Main function from which all function calls are made."""
    checks = [
        (check_reboot, "Pending Reboot"),
        (check_root_full, "Root partition full"),
    ]

    for check, msg in checks:
        if check():
            print(msg)
            sys.exit(1)

    print("Everything ok.")
    sys.exit(0)


main()

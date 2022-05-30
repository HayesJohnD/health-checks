#!/usr/bin/env python3
"""
A set of system checks for making sure your computer has no issues.

Returns:
    str: Everything ok: if there are no errors, sys.ext(1) otherwise
"""
import os
import shutil
import sys
import socket


def check_reboot() -> bool:
    """Return True if the computer has a pending reboot."""
    return os.path.exists("/run/reboot-required")


def check_disk_full(disk: str, min_gb: int, min_percent: int) -> bool:
    """Return True if there is enough free disk space, false otherwise."""
    du = shutil.disk_usage(disk)
    # calculate the percentage of free space
    percent_free = 100 * du.free / du.total
    # calculate how many free gigabytes
    gigabytes_free = du.free / 2**30
    if gigabytes_free < min_gb or percent_free < min_percent:
        return True
    return False


def check_root_full() -> bool:
    """Return True if the root partition is full, False otherwise."""
    return check_disk_full(disk="/", min_gb=2, min_percent=10)


def check_no_network() -> bool:
    """Return True if it fails to resolve Google's URL, False otherwise."""
    try:
        socket.gethostbyname("www.google.com")
        return False
    except:
        return True


def main() -> None:
    """Main function from which all function calls are made."""
    checks = [
        (check_reboot, "Pending Reboot"),
        (check_root_full, "Root partition full"),
        (check_no_network, "No working network."),
    ]
    everything_ok = True
    for check, msg in checks:
        if check():
            print(msg)
            everything_ok = False
    if not everything_ok:
        sys.exit(1)
    print("Everything ok.")
    sys.exit(0)


main()

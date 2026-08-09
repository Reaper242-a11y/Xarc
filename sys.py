#!/usr/bin/env python3

import curses
import os
import platform
import shutil
import subprocess
import sys


VERSION = "0.3.0"


def run_admin(command):
    try:
        return subprocess.run(
            ["ad", "run"] + command
        ).returncode
    except FileNotFoundError:
        print("SYS: AD was not found.")
        print("Make sure the 'ad' command is installed.")
        return 1
    except Exception as error:
        print(f"SYS: Error: {error}")
        return 1


def install_package(packages):
    if not packages:
        print("SYS: specify a package.")
        return 1

    return run_admin(
        ["pacman", "-S"] + packages
    )


def remove_package(packages):
    if not packages:
        print("SYS: specify a package.")
        return 1

    return run_admin(
        ["pacman", "-R"] + packages
    )


def search_package(query):
    if not query:
        print("SYS: specify a search term.")
        return 1

    return subprocess.run(
        ["pacman", "-Ss"] + query
    ).returncode


def update_system():
    return run_admin(
        ["pacman", "-Syu"]
    )


def show_info():
    total, used, free = shutil.disk_usage("/")

    print()
    print("XARC SYSTEM INFORMATION")
    print("------------------------")
    print(f"Xarc SYS:     {VERSION}")
    print(f"Hostname:     {platform.node()}")
    print(f"OS:           {platform.system()}")
    print(f"Kernel:       {platform.release()}")
    print(f"Architecture: {platform.machine()}")
    print(f"Python:       {platform.python_version()}")
    print(f"User:         {os.getenv('USER', 'unknown')}")
    print()
    print("Storage")
    print(f"Total:        {total / (1024 ** 3):.1f} GB")
    print(f"Used:         {used / (1024 ** 3):.1f} GB")
    print(f"Free:         {free / (1024 ** 3):.1f} GB")
    print()


def pause(stdscr):
    stdscr.addstr(
        curses.LINES - 2,
        2,
        "Press any key to return..."
    )
    stdscr.refresh()
    stdscr.getch()


def software_menu(stdscr):

    options = [
        "Install Software",
        "Remove Software",
        "Search Software",
        "Installed Software",
        "Back",
    ]

    selected = 0

    while True:

        stdscr.clear()

        stdscr.addstr(
            1,
            4,
            "XARC SYS / SOFTWARE",
            curses.A_BOLD
        )

        for i, option in enumerate(options):

            attr = curses.A_REVERSE if i == selected else 0

            stdscr.addstr(
                4 + i,
                6,
                option,
                attr
            )

        stdscr.addstr(
            curses.LINES - 2,
            2,
            "↑↓ / J K   Navigate    Enter   Select    Q   Back"
        )

        stdscr.refresh()

        key = stdscr.getch()

        if key in (curses.KEY_UP, ord("k")):
            selected = (selected - 1) % len(options)

        elif key in (curses.KEY_DOWN, ord("j")):
            selected = (selected + 1) % len(options)

        elif key in (10, 13):

            if selected == 0:

                curses.endwin()

                package = input(
                    "Package to install: "
                ).strip()

                if package:
                    install_package(
                        package.split()
                    )

                input(
                    "\nPress Enter to return..."
                )

            elif selected == 1:

                curses.endwin()

                package = input(
                    "Package to remove: "
                ).strip()

                if package:
                    remove_package(
                        package.split()
                    )

                input(
                    "\nPress Enter to return..."
                )

            elif selected == 2:

                curses.endwin()

                query = input(
                    "Search for: "
                ).strip()

                if query:
                    search_package(
                        query.split()
                    )

                input(
                    "\nPress Enter to return..."
                )

            elif selected == 3:

                curses.endwin()

                subprocess.run(
                    ["pacman", "-Q"]
                )

                input(
                    "\nPress Enter to return..."
                )

            elif selected == 4:
                return

        elif key in (ord("q"), ord("Q")):
            return


def updates_menu(stdscr):

    stdscr.clear()

    stdscr.addstr(
        3,
        4,
        "Updating Xarc system...",
        curses.A_BOLD
    )

    stdscr.refresh()

    curses.endwin()

    update_system()

    input(
        "\nPress Enter to return..."
    )


def system_info_menu(stdscr):

    stdscr.clear()

    total, used, free = shutil.disk_usage("/")

    info = [
        "XARC SYSTEM INFORMATION",
        "",
        f"Xarc SYS:     {VERSION}",
        f"Hostname:     {platform.node()}",
        f"OS:           {platform.system()}",
        f"Kernel:       {platform.release()}",
        f"Architecture: {platform.machine()}",
        f"Python:       {platform.python_version()}",
        f"User:         {os.getenv('USER', 'unknown')}",
        "",
        "Storage",
        f"Total:        {total / (1024 ** 3):.1f} GB",
        f"Used:         {used / (1024 ** 3):.1f} GB",
        f"Free:         {free / (1024 ** 3):.1f} GB",
    ]

    for i, line in enumerate(info):
        stdscr.addstr(
            2 + i,
            4,
            line
        )

    pause(stdscr)


def placeholder(stdscr, title, message):

    stdscr.clear()

    stdscr.addstr(
        2,
        4,
        f"XARC SYS / {title}",
        curses.A_BOLD
    )

    stdscr.addstr(
        5,
        4,
        message
    )

    pause(stdscr)


def launch_tui():

    curses.wrapper(main)


def main(stdscr):

    curses.curs_set(0)
    stdscr.keypad(True)

    menu = [
        "Software",
        "Updates",
        "System Information",
        "Services",
        "Storage",
        "Backups",
        "Repair",
        "Exit",
    ]

    selected = 0

    while True:

        stdscr.clear()

        height, width = stdscr.getmaxyx()

        title = "XARC SYS"
        subtitle = "System Management"

        stdscr.addstr(
            1,
            max(0, (width - len(title)) // 2),
            title,
            curses.A_BOLD
        )

        stdscr.addstr(
            2,
            max(0, (width - len(subtitle)) // 2),
            subtitle
        )

        for i, item in enumerate(menu):

            attr = (
                curses.A_REVERSE
                if i == selected
                else curses.A_NORMAL
            )

            stdscr.addstr(
                5 + i,
                6,
                item,
                attr
            )

        stdscr.addstr(
            height - 2,
            2,
            "↑↓ / J K   Navigate    Enter   Select    Q   Quit"
        )

        stdscr.refresh()

        key = stdscr.getch()

        if key in (curses.KEY_UP, ord("k")):

            selected = (
                selected - 1
            ) % len(menu)

        elif key in (curses.KEY_DOWN, ord("j")):

            selected = (
                selected + 1
            ) % len(menu)

        elif key in (10, 13):

            if selected == 0:
                software_menu(stdscr)

            elif selected == 1:
                updates_menu(stdscr)

            elif selected == 2:
                system_info_menu(stdscr)

            elif selected == 3:
                placeholder(
                    stdscr,
                    "SERVICES",
                    "Xarc service management is coming soon."
                )

            elif selected == 4:
                placeholder(
                    stdscr,
                    "STORAGE",
                    "Xarc storage management is coming soon."
                )

            elif selected == 5:
                placeholder(
                    stdscr,
                    "BACKUPS",
                    "Xarc automatic backup system is coming soon."
                )

            elif selected == 6:
                placeholder(
                    stdscr,
                    "REPAIR",
                    "Xarc automatic repair system is coming soon."
                )

            elif selected == 7:
                break

        elif key in (ord("q"), ord("Q")):
            break


def cli():

    args = sys.argv[1:]

    if not args:
        launch_tui()
        return 0

    command = args[0]
    arguments = args[1:]

    if command in ("help", "--help", "-h"):
        print("""
Xarc SYS

Usage:
    sys                     Open Xarc System
    sys install <package>   Install software
    sys remove <package>    Remove software
    sys search <query>      Search for software
    sys update              Update the system
    sys info                Show system information
    sys version             Show SYS version
    sys help                Show this help
""")
        return 0

    if command == "install":
        return install_package(arguments)

    if command == "remove":
        return remove_package(arguments)

    if command == "search":
        return search_package(arguments)

    if command == "update":
        return update_system()

    if command == "info":
        show_info()
        return 0

    if command == "version":
        print(f"Xarc SYS {VERSION}")
        return 0

    print(f"SYS: Unknown command '{command}'")
    print("Run 'sys help' for help.")

    return 1


if __name__ == "__main__":
    sys.exit(cli())

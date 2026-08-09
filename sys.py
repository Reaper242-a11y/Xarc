#!/usr/bin/env python3

import curses
import os
import platform
import shutil
import subprocess


VERSION = "0.2.0"


MENU = [
    ("Software", "Manage installed software"),
    ("Updates", "Update Xarc and system packages"),
    ("System Info", "View system information"),
    ("Services", "Manage system services"),
    ("Storage", "View storage information"),
    ("Backups", "Xarc backup system"),
    ("Repair", "Repair Xarc system"),
    ("Exit", "Exit Xarc SYS"),
]


def command_exists(command):
    return shutil.which(command) is not None


def run_admin(command):
    try:
        return subprocess.run(
            ["ad", "run"] + command
        ).returncode
    except Exception as error:
        print(f"Error: {error}")
        return 1


def wait_for_key(stdscr):
    stdscr.addstr(
        curses.LINES - 2,
        2,
        "Press any key to return..."
    )
    stdscr.refresh()
    stdscr.getch()


def draw_header(stdscr, title, subtitle=None):
    height, width = stdscr.getmaxyx()

    stdscr.clear()

    stdscr.addstr(
        1,
        max(0, (width - len(title)) // 2),
        title,
        curses.A_BOLD
    )

    if subtitle:
        stdscr.addstr(
            2,
            max(0, (width - len(subtitle)) // 2),
            subtitle
        )


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

        draw_header(
            stdscr,
            "XARC SYS",
            "Software Management"
        )

        for i, option in enumerate(options):

            attr = curses.A_REVERSE if i == selected else 0

            stdscr.addstr(
                5 + i,
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
                    run_admin(
                        ["pacman", "-S", package]
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
                    run_admin(
                        ["pacman", "-R", package]
                    )

                input(
                    "\nPress Enter to return..."
                )

            elif selected == 2:

                curses.endwin()

                package = input(
                    "Search for: "
                ).strip()

                if package:
                    subprocess.run(
                        ["pacman", "-Ss", package]
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

    draw_header(
        stdscr,
        "XARC SYS",
        "System Updates"
    )

    stdscr.addstr(
        5,
        4,
        "Checking for updates..."
    )

    stdscr.refresh()

    curses.endwin()

    run_admin(
        ["pacman", "-Syu"]
    )

    input(
        "\nPress Enter to return..."
    )


def system_info(stdscr):

    draw_header(
        stdscr,
        "XARC SYS",
        "System Information"
    )

    info = [
        f"Xarc SYS version: {VERSION}",
        f"Hostname:         {platform.node()}",
        f"OS:               {platform.system()}",
        f"Kernel:           {platform.release()}",
        f"Architecture:     {platform.machine()}",
        f"Python:           {platform.python_version()}",
        f"User:             {os.getenv('USER', 'unknown')}",
    ]

    for i, line in enumerate(info):
        stdscr.addstr(
            5 + i,
            4,
            line
        )

    wait_for_key(stdscr)


def storage_menu(stdscr):

    draw_header(
        stdscr,
        "XARC SYS",
        "Storage"
    )

    total, used, free = shutil.disk_usage("/")

    total_gb = total / (1024 ** 3)
    used_gb = used / (1024 ** 3)
    free_gb = free / (1024 ** 3)

    info = [
        f"Total: {total_gb:.1f} GB",
        f"Used:  {used_gb:.1f} GB",
        f"Free:  {free_gb:.1f} GB",
    ]

    for i, line in enumerate(info):
        stdscr.addstr(
            5 + i,
            4,
            line
        )

    wait_for_key(stdscr)


def placeholder(stdscr, title, message):

    draw_header(
        stdscr,
        "XARC SYS",
        title
    )

    stdscr.addstr(
        6,
        4,
        message
    )

    wait_for_key(stdscr)


def main(stdscr):

    curses.curs_set(0)
    stdscr.keypad(True)

    selected = 0

    while True:

        draw_header(
            stdscr,
            "XARC SYS",
            "System Management"
        )

        for i, (name, description) in enumerate(MENU):

            y = 5 + i

            attr = (
                curses.A_REVERSE
                if i == selected
                else curses.A_NORMAL
            )

            stdscr.addstr(
                y,
                5,
                name,
                attr
            )

            stdscr.addstr(
                y,
                25,
                description
            )

        stdscr.addstr(
            curses.LINES - 2,
            2,
            "↑↓ / J K   Navigate    Enter   Select    Q   Quit"
        )

        stdscr.refresh()

        key = stdscr.getch()

        if key in (curses.KEY_UP, ord("k")):

            selected = (
                selected - 1
            ) % len(MENU)

        elif key in (curses.KEY_DOWN, ord("j")):

            selected = (
                selected + 1
            ) % len(MENU)

        elif key in (10, 13):

            if selected == 0:
                software_menu(stdscr)

            elif selected == 1:
                updates_menu(stdscr)

            elif selected == 2:
                system_info(stdscr)

            elif selected == 3:
                placeholder(
                    stdscr,
                    "Services",
                    "Xarc service manager is coming soon."
                )

            elif selected == 4:
                storage_menu(stdscr)

            elif selected == 5:
                placeholder(
                    stdscr,
                    "Backups",
                    "Xarc automatic backup system is coming soon."
                )

            elif selected == 6:
                placeholder(
                    stdscr,
                    "Repair",
                    "Xarc automatic repair system is coming soon."
                )

            elif selected == 7:
                break

        elif key in (ord("q"), ord("Q")):
            break


if __name__ == "__main__":
    curses.wrapper(main)

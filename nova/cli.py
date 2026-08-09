import sys

from . import database
from .package import NovaPackage


VERSION = "0.2.0"


def help():
    print("""
Nova Package Manager

Usage:

    nova                       Open Nova
    nova install <package>    Install a package
    nova remove <package>     Remove a package
    nova search <query>       Search repositories
    nova update               Update repositories
    nova upgrade              Upgrade packages

Information:

    nova list                 List installed packages
    nova info <package>       Package information
    nova files <package>      List package files
    nova owner <file>         Find file owner

Package Tools:

    nova package <file>       Inspect a .nova package

Other:

    nova version              Show Nova version
    nova help                 Show this help
""")


def version():
    print(f"Nova Package Manager {VERSION}")
    print("Xarc Package System")


def list_packages():
    packages = database.list_packages()

    if not packages:
        print("Nova: no packages installed.")
        return

    print("Installed packages:")
    print()

    for name, package_version, architecture in packages:
        print(
            f"{name} "
            f"{package_version} "
            f"[{architecture}]"
        )


def info(name):
    if not name:
        print("Nova: specify a package.")
        return 1

    package = database.get_package(name)

    if not package:
        print(
            f"Nova: '{name}' is not installed."
        )
        return 1

    (
        name,
        package_version,
        architecture,
        description,
        license_name
    ) = package

    print()
    print(f"Name:         {name}")
    print(f"Version:      {package_version}")
    print(f"Architecture: {architecture}")
    print(f"Description:  {description}")
    print(f"License:      {license_name}")
    print()

    return 0


def files(name):
    if not name:
        print("Nova: specify a package.")
        return 1

    package = database.get_package(name)

    if not package:
        print(
            f"Nova: '{name}' is not installed."
        )
        return 1

    package_files = database.get_files(name)

    if not package_files:
        print(
            "Nova: package owns no recorded files."
        )
        return 0

    for path in package_files:
        print(path)

    return 0


def owner(path):
    if not path:
        print("Nova: specify a file.")
        return 1

    package = database.get_owner(path)

    if package:
        print(
            f"{path} is owned by {package}"
        )
    else:
        print(
            f"{path} is not owned by a Nova package."
        )

    return 0


def inspect_package(path):
    if not path:
        print(
            "Nova: specify a .nova package."
        )
        return 1

    try:
        package = NovaPackage(path)
        manifest = package.info()

    except Exception as error:
        print("Nova: invalid package.")
        print(f"Reason: {error}")
        return 1

    print()
    print("Nova Package")
    print("------------")

    print(f"Name:         {manifest['name']}")
    print(f"Version:      {manifest['version']}")
    print(
        f"Architecture: "
        f"{manifest['architecture']}"
    )
    print(
        f"Description:  "
        f"{manifest['description']}"
    )
    print(
        f"License:      "
        f"{manifest['license']}"
    )

    dependencies = manifest.get(
        "dependencies",
        []
    )

    print(
        "Dependencies: "
        + (
            ", ".join(dependencies)
            if dependencies
            else "None"
        )
    )

    print()

    return 0


def command(args):
    database.initialize()

    if not args:
        print("Nova Package Manager")
        print(f"Version {VERSION}")
        print()
        print(
            "Run 'nova help' for commands."
        )
        return 0

    cmd = args[0]
    values = args[1:]

    if cmd in ("help", "-h", "--help"):
        help()
        return 0

    if cmd in ("version", "-v", "--version"):
        version()
        return 0

    if cmd == "list":
        list_packages()
        return 0

    if cmd == "info":
        return info(
            values[0] if values else None
        )

    if cmd == "files":
        return files(
            values[0] if values else None
        )

    if cmd == "owner":
        return owner(
            values[0] if values else None
        )

    if cmd == "package":
        return inspect_package(
            values[0] if values else None
        )

    if cmd == "install":
        print(
            f"Nova: installation of "
            f"'{values[0] if values else ''}' "
            f"is not implemented yet."
        )
        return 0

    if cmd == "remove":
        print(
            f"Nova: removal of "
            f"'{values[0] if values else ''}' "
            f"is not implemented yet."
        )
        return 0

    if cmd == "search":
        print(
            "Nova: repository search "
            "is not implemented yet."
        )
        return 0

    if cmd == "update":
        print(
            "Nova: repository update "
            "is not implemented yet."
        )
        return 0

    if cmd == "upgrade":
        print(
            "Nova: package upgrade "
            "is not implemented yet."
        )
        return 0

    print(
        f"Nova: unknown command '{cmd}'."
    )
    print(
        "Run 'nova help' for help."
    )

    return 1

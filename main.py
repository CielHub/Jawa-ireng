import json
import time

from launcher import Launcher


def load_config():
    with open("config.json", "r", encoding="utf-8") as f:
        return json.load(f)


def validate_config(config):

    if "accounts" not in config:
        raise Exception("accounts tidak ditemukan")

    if len(config["accounts"]) == 0:
        raise Exception("Minimal harus ada 1 akun")

    if len(config["accounts"]) > 8:
        raise Exception("Maksimal hanya 8 akun")


def print_accounts(config):

    print("=" * 45)
    print("      Roblox Auto Rejoiner")
    print("=" * 45)

    for account in config["accounts"]:

        status = "ON" if account["enabled"] else "OFF"

        print(f"[{status}] {account['name']}")
        print(f"      Package : {account['package']}")

    print("=" * 45)


def main():

    config = load_config()

    validate_config(config)

    print_accounts(config)

    general = config["general"]

    launcher = Launcher(
        launch_delay=general["launch_delay"]
    )

    print("\nConfiguration Loaded.")

    # Launch semua akun yang aktif
    for account in config["accounts"]:

        if not account["enabled"]:
            continue

        print(f"\nLaunching {account['name']}...")

        success = launcher.relaunch(
            package=account["package"],
            private_server=account["private_server"]
        )

        if success:
            print(f"{account['name']} berhasil dijalankan.")
        else:
            print(f"{account['name']} gagal dijalankan.")

    print("\nMasuk ke monitoring loop...\n")

    while True:

        # Tahap 3 nanti monitor akan dipanggil di sini

        time.sleep(general["check_interval"])


if __name__ == "__main__":
    main()

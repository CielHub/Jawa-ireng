import json
import time

from launcher import Launcher
from monitor import Monitor
from recovery import Recovery


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

    recovery = Recovery(
        launcher=launcher,
        retry_delay=general["retry_delay"],
        max_retry=general["max_retry"]
    )

    monitors = []

    for account in config["accounts"]:

        if not account["enabled"]:
            continue

        monitor = Monitor(
            package=account["package"]
        )

        monitors.append(
            {
                "account": account,
                "monitor": monitor
            }
        )

    print("\nConfiguration Loaded.")

    print("\nLaunching enabled accounts...\n")

    for item in monitors:

        account = item["account"]

        success = launcher.relaunch(
            package=account["package"],
            private_server=account["private_server"]
        )

        if success:
            print(f"[OK] {account['name']} launched.")
        else:
            print(f"[FAIL] {account['name']} failed to launch.")

    print("\nMonitoring started...\n")

    while True:

        for item in monitors:

            account = item["account"]
            monitor = item["monitor"]

            status = monitor.update()

            print(
                f"[{account['name']}] {status}"
            )

            if monitor.needs_recovery():

                recovery.recover(account)

        time.sleep(
            general["check_interval"]
        )


if __name__ == "__main__":
    main()

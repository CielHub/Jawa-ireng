import json
import time


def load_config():
    with open("config.json", "r", encoding="utf-8") as f:
        return json.load(f)


def validate_config(config):
    if "accounts" not in config:
        raise Exception("accounts tidak ditemukan")

    if len(config["accounts"]) == 0:
        raise Exception("Minimal harus ada 1 akun")

    if len(config["accounts"]) > 8:
        raise Exception("Maksimal 8 akun")


def print_accounts(config):
    print("=" * 40)
    print(" Roblox Auto Rejoiner")
    print("=" * 40)

    for account in config["accounts"]:
        if account["enabled"]:
            print(f"[ON ] {account['name']}")
            print(f"      Package : {account['package']}")
        else:
            print(f"[OFF] {account['name']}")

    print("=" * 40)


def main():

    config = load_config()

    validate_config(config)

    print_accounts(config)

    print("Configuration Loaded.\n")

    while True:
        time.sleep(config["general"]["check_interval"])


if __name__ == "__main__":
    main()

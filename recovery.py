import time


class Recovery:

    def __init__(self, launcher, retry_delay=15, max_retry=3):

        self.launcher = launcher
        self.retry_delay = retry_delay
        self.max_retry = max_retry

    def recover(self, account):

        retry = 0

        while retry < self.max_retry:

            print(
                f"[RECOVERY] {account['name']} "
                f"({retry + 1}/{self.max_retry})"
            )

            success = self.launcher.relaunch(
                package=account["package"],
                private_server=account["private_server"]
            )

            if success:

                print(
                    f"[SUCCESS] {account['name']} kembali berjalan."
                )

                return True

            retry += 1

            print(
                f"[FAILED] Retry {retry}"
            )

            time.sleep(self.retry_delay)

        print(
            f"[ERROR] Recovery gagal : {account['name']}"
        )

        return False

import subprocess
import time


class Launcher:

    def __init__(self, launch_delay=8):
        self.launch_delay = launch_delay

    def run(self, command):
        """
        Menjalankan command shell.
        Mengembalikan True jika berhasil.
        """
        try:
            result = subprocess.run(
                command,
                shell=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )

            return result.returncode == 0

        except Exception:
            return False

    def force_stop(self, package):
        """
        Force stop Roblox.
        """
        cmd = f"su -c 'am force-stop {package}'"
        return self.run(cmd)

    def launch(self, package):
        """
        Membuka Roblox clone.
        """
        cmd = (
            f"su -c 'monkey "
            f"-p {package} "
            "-c android.intent.category.LAUNCHER 1'"
        )

        success = self.run(cmd)

        if success:
            time.sleep(self.launch_delay)

        return success

    def join_private_server(self, private_server):
        """
        Membuka link Private Server.
        """
        cmd = (
            "su -c "
            f"'am start "
            "-a android.intent.action.VIEW "
            f"-d \"{private_server}\"'"
        )

        return self.run(cmd)

    def relaunch(self, package, private_server):
        """
        Force stop -> Launch -> Join PS
        """

        self.force_stop(package)

        time.sleep(2)

        if not self.launch(package):
            return False

        time.sleep(2)

        return self.join_private_server(private_server)

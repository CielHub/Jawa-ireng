import subprocess


class Monitor:

    RUNNING = "Running"
    OFFLINE = "Offline"
    HOME = "Home"
    UNKNOWN = "Unknown"

    def __init__(self, package):

        self.package = package
        self.status = self.UNKNOWN

    def shell(self, command):

        try:

            result = subprocess.run(
                command,
                shell=True,
                capture_output=True,
                text=True
            )

            return result.stdout.strip()

        except Exception:

            return ""

    def process_alive(self):

        cmd = f"su -c 'pidof {self.package}'"

        output = self.shell(cmd)

        return output != ""

    def foreground_running(self):

        cmd = "su -c 'dumpsys window | grep mCurrentFocus'"

        output = self.shell(cmd)

        return self.package in output

    def update(self):

        if not self.process_alive():

            self.status = self.OFFLINE

            return self.status

        if self.foreground_running():

            self.status = self.RUNNING

            return self.status

        self.status = self.HOME

        return self.status

    def is_running(self):

        return self.update() == self.RUNNING

    def needs_recovery(self):

        return self.update() != self.RUNNING

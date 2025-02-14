import os
import base64
from .exceptions import LockfileError


class Auth:
    def getConfig(self):
        configPath = os.path.join(
            os.getenv("LOCALAPPDATA"),
            R"Riot Games\Riot Client\Config\lockfile"
        )

        try:
            with open(configPath) as lockfile:
                data = lockfile.read().split(":")
                keys = ["name", "PID", "port", "password", "protocol"]
                return dict(zip(keys, data))
        except FileNotFoundError:
            raise LockfileError("Valorant is not running. Open the game BEFORE you run this script.")
        except Exception as e:
            raise LockfileError(f"Error reading the lockfile: {e}")

    def getHeaders(self):
        config = self.getConfig()
        accessToken = base64.b64encode(
            ("riot:" + config["password"]).encode()).decode()
        headers = {
            "Authorization": f"Basic {accessToken}"
        }
        return headers

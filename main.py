from pathlib import Path
from tenacity import retry, stop_after_attempt, wait_fixed
import subprocess
import shutil
import time
import stat
import sys


def resource_path(relative_path: str) -> Path:
    if getattr(sys, "frozen", False):
        # Nuitka onefile extraction directory
        return Path(sys.argv[0]).resolve().parent / relative_path
    else:
        return Path(__file__).resolve().parent / relative_path


@retry(stop=stop_after_attempt(3), wait=wait_fixed(2))
def main():
    ldplayers = Path("C:/LDPlayer/LDPlayer9/vms")
    ldplayer_config = ldplayers / "config" / "leidians.config"

    if not ldplayers.exists():
        raise FileNotFoundError(
            "LDPlayer directory not found. Please ensure LDPlayer is installed on C Drive."
        )

    for folder in ldplayers.iterdir():
        if folder.name.startswith("leidian"):
            if folder.name == "leidian0":
                continue

            print(f"Deleting {folder.name}...")
            shutil.rmtree(folder)

    print("Cleanup Successful.")
    print("")
    print("Transfering custom leidians.config to ldplayer...")

    if ldplayer_config.exists():
        print("Removing old config...")
        ldplayer_config.chmod(stat.S_IWRITE)
        ldplayer_config.unlink()
        print("Successfully Removed old config...")

    src = resource_path("leidians.config")
    shutil.copy(src, ldplayer_config)

    print("✅ Successfully Completed all task")


def kill_ldplayer():
    subprocess.run(["taskkill", "/IM", "dnplayer.exe", "/T", "/F"], capture_output=True)


if __name__ == "__main__":
    kill_ldplayer()
    main()
    time.sleep(2)

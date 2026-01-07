from pathlib import Path
import shutil
import time
import stat
import sys
import subprocess
import requests

APP_VERSION = "1.0.3"
GITHUB_API = "https://api.github.com/repos/Arroz-con/ld-cleaner/releases/latest"


def version_tuple(v: str):
    return tuple(map(int, v.split(".")))


def check_for_update():
    try:
        r = requests.get(GITHUB_API, timeout=5)
        r.raise_for_status()
        data = r.json()

        latest_version = data["tag_name"].lstrip("v")

        if version_tuple(latest_version) > version_tuple(APP_VERSION):
            for asset in data["assets"]:
                if asset["name"].endswith(".exe"):
                    download_and_restart(asset["browser_download_url"])
    except Exception:
        pass


def download_and_restart(url: str):
    current_exe = Path(sys.executable)
    old_exe = current_exe.with_name(current_exe.stem + "_old.exe")
    new_exe = current_exe.with_name(current_exe.stem + "_new.exe")

    current_exe.replace(old_exe)

    start = time.monotonic()
    download = 0

    def on_update(pct, speed):
        print(f"Updating... {pct}% ({speed:.2f} MB/s)")

    with requests.get(url, stream=True) as r:
        r.raise_for_status()
        total = int(r.headers.get("Content-Length", 0))

        with new_exe.open("wb") as f:
            for chunk in r.iter_content(8192):
                if not chunk:
                    continue

                f.write(chunk)
                download += len(chunk)

                elapsed = time.monotonic() - start
                speed = (download / elapsed) / (1024 * 1024) if elapsed else 0
                percent = int(download / total * 100) if total else 0

                on_update(percent, speed)

    print("downloaded")
    subprocess.Popen([str(new_exe)])
    time.sleep(2)
    sys.exit()


def cleanup_old_exe():
    old_exe = Path(sys.executable).with_name(Path(sys.executable).stem + "_old.exe")
    if old_exe.exists():
        try:
            old_exe.unlink()
            print("removed old exe")
        except OSError:
            pass


def resource_path(relative_path: str) -> Path:
    if getattr(sys, "frozen", False):
        # Nuitka onefile extraction directory
        return Path(sys.argv[0]).resolve().parent / relative_path
    else:
        return Path(__file__).resolve().parent / relative_path


def main():
    # home_path = Path.home()
    ldplayers = Path("C:/LDPlayer/LDPlayer9/vms")
    ldplayer_config = ldplayers / "config" / "leidians.config"

    # emulators_file = Path(home_path) /"Desktop"/"Android Manager"/"data"/"emulators.json"

    try:
        if not ldplayers.exists():
            raise FileNotFoundError(
                "LDPlayer directory not found. Please ensure LDPlayer is installed on C Drive."
            )

        # if not emulators_file.exists():
        #     raise FileNotFoundError("emulators.json file not found")

        # with open(emulators_file, "w") as f:
        #     f.write("[]")

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
    except Exception as e:
        print("Error:", e)
    finally:
        time.sleep(2)


if __name__ == "__main__":
    cleanup_old_exe()
    check_for_update()
    main()

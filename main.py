from pathlib import Path
import shutil
from time import sleep
import stat
import sys


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
        sleep(2)


if __name__ == "__main__":
    main()

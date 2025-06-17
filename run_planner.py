from core import Planner
from config import Settings, CustomPriceAdapter


def main():
    planner = Planner(
        price_adapter=CustomPriceAdapter(Settings.storage_dir, Settings.price_repo_url),
        devices=Settings.devices,
        storage_dir=Settings.storage_dir,
        timezone=Settings.timezone,
    )
    planner.plan()


if __name__ == "__main__":
    main()

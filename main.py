from california_fire.core import network_manager
from california_fire.core.fire import Fire
from california_fire.social.social_manager import social_manager
from california_fire.storage import storage_manager

OLD_PATH = 'outputs/old_fire.json'
BASE_IMAGE_PATH = 'assets/california_base_map.png'
OUTPUT_PATH = 'outputs/california_fire_map.png'


def filter_out_dup_fire(old_fires: list[Fire], new_fires: list[Fire]) -> list[Fire]:
    """ Return Fires from new fires not present in previous fires. """
    return [eq for eq in new_fires if eq not in old_fires]


def main():
    new_fires: list[Fire] = network_manager.get_fire_data()

    if not new_fires:
        print("No fire fire from api.")
        return

    old_fires: list[Fire] = storage_manager.read_fire_data(old_fire_path=OLD_PATH)
    storage_manager.write_fire_data(new_fire_data=new_fires, old_path=OLD_PATH)
    filtered_fires: list[Fire] = filter_out_dup_fire(old_fires=old_fires, new_fires=new_fires)

    if not filtered_fires:
        print("No new fire.")
        return

    social_manager(fires=filtered_fires, base_image_path=BASE_IMAGE_PATH, output_path=OUTPUT_PATH)


if __name__ == '__main__':
    main()
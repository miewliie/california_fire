from api.fire_api import *

if __name__ == '__main__':
    prev_json_path = '../outputs/previous_fire_data.json'
    fire_json_path = '../outputs/fire.json'

    fire_data = request_fire()
    if fire_data:
        dup_list = get_dup_fire_data(fire_data, prev_json_path)
        save_latest_fire_data(fire_data, prev_json_path)
        prepare_ready_to_use_data(dup_list, fire_data, fire_json_path)
import requests
import json
from datetime import datetime
import time

from _utils import *
from data_config import *


def get_data_from_api(api_link):
    response_API = requests.get(api_link)
    data = response_API.text
    parse_json = json.loads(data)
    time.sleep(2)
    return parse_json


def main():
    date_time = datetime.now().strftime("%y%m%d_%H%M%S")

    # recipe
    recipe_api_prefix = "https://www.themealdb.com/api/json/v1/1/search.php?"
    alphabets = [chr(i) for i in range(ord("a"), ord("z") + 1)]
    recipe_out_path = data_raw_path / the_meal_db_dir / "recipe"
    recipe_out_path.mkdir(parents=True, exist_ok=True)

    for c in alphabets:
        recipe_api_link = recipe_api_prefix + f"f={c}"
        recipe_json_file = get_data_from_api(recipe_api_link)
        recipe_file_name = recipe_out_path / f"{date_time}-{c}-recipe-themeal.json"
        store_json(recipe_json_file, recipe_file_name)

    # category
    cat_api_link = "https://www.themealdb.com/api/json/v1/1/categories.php"
    cat_out_path = data_raw_path / the_meal_db_dir / "category"
    cat_out_path.mkdir(parents=True, exist_ok=True)
    cat_json_file = get_data_from_api(cat_api_link)
    cat_file_name = cat_out_path / f"{date_time}-category-themeal.json"
    store_json(cat_json_file, cat_file_name)

    # ingredient
    igd_api_link = "https://www.themealdb.com/api/json/v1/1/list.php?i=list"
    igd_out_path = data_raw_path / the_meal_db_dir / "ingredient"
    igd_out_path.mkdir(parents=True, exist_ok=True)
    igd_json_file = get_data_from_api(igd_api_link)
    igd_file_name = igd_out_path / f"{date_time}-ingredient-themeal.json"
    store_json(igd_json_file, igd_file_name)

    # area
    area_api_link = "https://www.themealdb.com/api/json/v1/1/list.php?a=list"
    area_out_path = data_raw_path / the_meal_db_dir / "area"
    area_out_path.mkdir(parents=True, exist_ok=True)
    area_json_file = get_data_from_api(area_api_link)
    area_file_name = area_out_path / f"{date_time}-area-themeal.json"
    store_json(area_json_file, area_file_name)


if __name__ == "__main__":
    main()

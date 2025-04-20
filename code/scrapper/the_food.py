from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import TimeoutException
import time
from datetime import datetime
import pandas as pd
import re

import data_config
from _utils import *


def scrape_recipe(driver, output_dir, date_time):
    """
    scrape recipes
    """
    users = set()
    recipes = set()
    recipe_inf = {}
    part = 1
    number_sample = 2500

    driver.get("https://www.food.com/search/")
    elements = WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located(
            (By.XPATH, '//*[@class="fd-tile fd-recipe  "]')
        )
    )

    while len(elements) <= number_sample:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(0.5)
        elements = WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located(
                (By.XPATH, '//*[@class="fd-tile fd-recipe  "]')
            )
        )

    for i in range(number_sample):  # 2000
        if i % 50 == 0:
            print(f"Processing {i} titles")
        cook_time = (
            elements[i].find_elements(By.XPATH, '//*[@class="cook-time"]')[i].text
        )
        recipe_link = (
            elements[i]
            .find_elements(By.XPATH, '//*[@class="inner-wrapper"]/a')[i]
            .get_attribute("href")
        )  # recipe
        recipe_img = (
            elements[i].find_elements(By.XPATH, "//img")[i].get_attribute("src")
        )  # img
        user_link = (
            elements[i]
            .find_elements(By.XPATH, '//*[@class="author"]//a')[i]
            .get_attribute("href")
        )  # user link
        users.add(user_link)
        recipes.add(recipe_link)

        recipe_id = recipe_link.split("-")[-1]
        recipe_inf[recipe_id] = {
            "recipe_link": recipe_link,
            "author_link": user_link,
            "author_id": user_link.split(r"/")[-1],
            "recipe_img": recipe_img,
            "time": cook_time,
        }
    recipe_db = {}
    rm_recipe_link = []
    for ind, recipe_link in enumerate(recipes):
        driver.get(recipe_link)
        driver.implicitly_wait(2)
        try: 
            serving_tab = WebDriverWait(driver, 20).until(
                EC.visibility_of_element_located(
                    (By.XPATH, '//*[@class="value svelte-1o10zxc"]')
                )
            )

            action = ActionChains(driver)
            action.move_to_element(serving_tab).double_click().send_keys(
                Keys.DELETE
            ).send_keys("1").double_click().send_keys(Keys.DELETE).send_keys("1").send_keys(
                Keys.ENTER
            )
            action.perform()

            igr_elements = WebDriverWait(driver, 10).until(
                EC.presence_of_all_elements_located(
                    (By.XPATH, '//*[@style="display: contents"]')
                )
            )
            igrs = []
            for i in range(1, len(igr_elements)):
                igd = igr_elements[i].text
                igrs += [igd]

            instruction = driver.find_element(
                By.XPATH, '//*[@class="direction-list svelte-1dqq0pw"]'
            ).text

            user_elements = WebDriverWait(driver, 10).until(
                EC.presence_of_all_elements_located(
                    (
                        By.XPATH,
                        '//*[@id="reviews"]//*[@class="post svelte-omstw2"]//*[@class="post__avatar svelte-omstw2"]/a',
                    )
                )
            )
            for u in user_elements:
                user = u.get_attribute("href")
                users.add(user)

            rating = driver.find_element(
                By.XPATH, '//*[@class="layout__item rating-badge svelte-1dqq0pw"]//a'
            ).get_attribute("aria-label")

            recipe_id = recipe_link.split("-")[-1]

            recipe_db[recipe_id] = {
                "recipe_link": recipe_inf[recipe_id]["recipe_link"],
                "author_link": recipe_inf[recipe_id]["author_link"],
                "author_id": recipe_inf[recipe_id]["author_link"].split(r"/")[-1],
                "ingredient": igrs,
                "rating": rating,
                "recipe_img": recipe_inf[recipe_id]["recipe_img"],
                "time": recipe_inf[recipe_id]["time"],
                "serving_pp": 1,
                "instruction": instruction,
            }
        except:
            rm_recipe_link += [recipe_link]
            print(f"Cannot process {recipe_link}!")
            continue

        if (ind + 1) % 200 == 0:
            recipe_file_name = output_dir / f"{date_time}-recipes-p{part}.json"
            store_json(recipe_db, recipe_file_name)
            recipe_db = {}
            print(f"processing part {part} of recipe!")
            part += 1

    if recipe_db:
        recipe_file_name = output_dir / f"{date_time}-recipes-p{part}.json"
        store_json(recipe_db, recipe_file_name)
        print(f"processing part {part} of recipe!")

    for r in rm_recipe_link:
        recipes.remove(r)

    return users, recipes


def scrape_user_rating(users, recipes, driver, output_dir, date_time):
    """
    scrape user's rating of each recipe
    """
    user_db = {}
    part = 1
    for ind, link in enumerate(users):
        driver.implicitly_wait(2)
        driver.get(link)
        reviews = {}
        while True:
            try:
                WebDriverWait(driver, 5).until(
                    EC.element_to_be_clickable(
                        (By.XPATH, '//*[@class="gk-aa-load-more"]')
                    )
                ).click()
            except TimeoutException:
                break
        try:
            items = WebDriverWait(driver, 10).until(
                EC.presence_of_all_elements_located((By.XPATH, '//*[@class="gk-aa-item"]'))
            )
            for item in items:
                if "reviewed" in item.text.split("\n")[0]:
                    recipe_link = (
                        item.find_element(By.CLASS_NAME, "gk-aa-item-heading-info")
                        .find_elements(By.TAG_NAME, "a")[1]
                        .get_attribute("href")
                    )
                    if recipe_link in recipes:
                        try:
                            rating = item.find_element(
                                By.CLASS_NAME, "fd-rating-percent"
                            ).get_attribute("style")
                            rating = re.findall(r"\b\d+\b", rating)[0]
                        except:
                            continue
                        recipe_id = recipe_link.split("-")[-1]
                        reviews[recipe_id] = rating
        except TimeoutException:
            continue


        user_id = link.split(r"/")[-1]
        if reviews:
            user_db[user_id] = {"reviews": reviews, "user_link": link}

        if (ind + 1) % 200 == 0:
            rating_file_name = output_dir / f"{date_time}-user-rating-p{part}.json"
            store_json(user_db, rating_file_name)
            user_db = {}
            print(f"processing part {part} of user-rating!")
            part += 1

    if user_db:
        rating_file_name = output_dir / f"{date_time}-user-rating-p{part}.json"
        store_json(user_db, rating_file_name)
        print(f"processing part {part} of user-rating!")


def main():
    recipe_dir = data_config.data_raw_path / data_config.the_food_dir / "recipe"
    user_rating_dir = (
        data_config.data_raw_path / data_config.the_food_dir / "user_rating"
    )
    date_time = datetime.now().strftime("%y%m%d_%H%M%S")

    recipe_dir.mkdir(parents=True, exist_ok=True)
    user_rating_dir.mkdir(parents=True, exist_ok=True)

    options = webdriver.ChromeOptions()
    options.add_argument("--disable-cookies")
    driver = webdriver.Chrome(options=options)

    # users, recipes = scrape_recipe(driver, recipe_dir, date_time)
    # recipe_list_file = (
    #     data_config.data_raw_path
    #     / data_config.the_food_dir
    #     / f"{date_time}-recipes-l.json"
    # )
    # store_json({"recipe_ids": list(recipes)}, recipe_list_file)
    # users_list_file = (
    #     data_config.data_raw_path
    #     / data_config.the_food_dir
    #     / f"{date_time}-users-l.json"
    # )
    # store_json({"user_ids": list(users)}, users_list_file)
    with open('C:/Thu/My library/University course/Bioinformatics/1st ay/Biological Databases/project/data_raw/the_food_db/240316_160511-recipes-l.json') as f:
        recipes = json.load(f)['recipe_ids']
    with open('C:/Thu/My library/University course/Bioinformatics/1st ay/Biological Databases/project/data_raw/the_food_db/240316_160511-users-l.json') as f:
        users = json.load(f)['user_ids']
    scrape_user_rating(users, recipes, driver, user_rating_dir, date_time)


if __name__ == "__main__":
    main()

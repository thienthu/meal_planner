from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import json
from datetime import datetime
from _utils import *
import data_config

def main():
    options = webdriver.ChromeOptions()
    options.add_argument("--disable-cookies")
    options.add_argument("--start-maximized")

    driver = webdriver.Chrome(options=options)

    page = 1
    part = 1
    img_screen_shot_dir = data_config.data_raw_path/data_config.nutritionix_dir/"nutrition-fact-scrshot"
    img_screen_shot_dir.mkdir(parents=True, exist_ok=True)
    date_time = datetime.now().strftime("%y%m%d_%H%M%S")
    data_output = {}
    while True:
        try:
            driver.get(
                "https://www.nutritionix.com/database/common-foods?page=" + str(page)
            )
            elements = WebDriverWait(driver, 10).until(
                EC.presence_of_all_elements_located(
                    (By.XPATH, '//*[@class="item-row item-hover ng-scope"]')
                )
            )
        except TimeoutException:
            break

        ingre_links = []
        link_path_available = set()
        for element in elements:
            link_path = element.get_attribute("href")
            if link_path in link_path_available:
                continue
            else:
                link_path_available.add(link_path)
            ingre_links += [link_path]

        for ind, link_path in enumerate(ingre_links):
            driver.get("https://www.nutritionix.com" + link_path)
            if ind == 0:
                try:
                    WebDriverWait(driver, 5).until(
                        EC.element_to_be_clickable(
                            (
                                By.XPATH,
                                '//*[@class="fc-button fc-cta-consent fc-primary-button"]',
                            )
                        )
                    ).click()
                except TimeoutException:
                    pass
            try:
                food_label = driver.find_element(By.XPATH, '//*[@class="nf"]')
                img_path = food_label.find_element(By.XPATH, '//*[@class="as-table-cell text-center item-thumbnail ng-scope"]//img').get_attribute("src")
                serving_size = food_label.find_element(
                    By.XPATH, '//input[@type="hidden"]'
                ).get_attribute("value")
                serving_unit = food_label.find_element(
                    By.XPATH, '//*[@class="nf-serving-unit-name "]'
                ).text.split("\n")[0]
                second_amount = food_label.find_element(
                    By.XPATH, '//*[@itemprop="servingSize"]'
                ).text.split("\n")[0]
                second_unit = food_label.find_element(
                    By.XPATH, '//*[@class="sr-only"]'
                ).text.split("\n")[0]
                calories = food_label.find_element(
                    By.XPATH, '//*[@itemprop="calories"]'
                ).text.split("\n")[0]
                food_name = food_label.find_element(
                    By.XPATH, '//*[@class="nf-item-name block"]'
                ).text.split("\n")[0]
                total_fat = food_label.find_element(
                    By.XPATH, '//*[@itemprop="fatContent"]'
                ).text.split("\n")[0]
                cholesterol = food_label.find_element(
                    By.XPATH, '//*[@itemprop="cholesterolContent"]'
                ).text.split("\n")[0]
                sodium = food_label.find_element(
                    By.XPATH, '//*[@itemprop="sodiumContent"]'
                ).text.split("\n")[0]
                carbonhydrate = food_label.find_element(
                    By.XPATH, '//*[@itemprop="carbohydrateContent"]'
                ).text.split("\n")[0]
                protein = food_label.find_element(
                    By.XPATH, '//*[@itemprop="proteinContent"]'
                ).text.split("\n")[0]
                calcium = food_label.find_element(
                    By.XPATH, '//*[@itemprop="calciumContent"]'
                ).text.split("\n")[0]
                iron = food_label.find_element(
                    By.XPATH, '//*[@itemprop="ironContent"]'
                ).text.split("\n")[0]
                potassium = food_label.find_element(
                    By.XPATH, '//*[@itemprop="potassiumContent"]'
                ).text.split("\n")[0]
                vitamin_d = food_label.find_element(
                    By.XPATH, '//*[@itemprop="vitaminDContent"]'
                ).text.split("\n")[0]
                caffeine = food_label.find_element(
                    By.XPATH, '//*[@itemprop="caffeineContent"]'
                ).text.split("\n")[0]
            except NoSuchElementException:
                continue

            driver.implicitly_wait(2)
            total_height = food_label.size["height"] + 1000
            total_width = food_label.size["width"]
            driver.set_window_size(total_width, total_height)  # the trick
            # Javascript expression to scroll to a particular element
            # arguments[0] refers to the first argument that is later passed
            # in to execute_script method
            js_code = "arguments[0].scrollIntoView();"
            driver.execute_script(js_code, food_label)

            if ind == 0:
                try:
                    WebDriverWait(driver, 5).until(
                        EC.element_to_be_clickable(
                            (By.XPATH, '//*[@class="btn btn-default btn-xs"]')
                        )
                    ).click()
                except TimeoutException:
                    pass
            img_name = food_name.lower().replace(' ','-')
            img_screen_shot = str(img_screen_shot_dir/f"{img_name}.png") 
            food_label.screenshot(img_screen_shot)

            driver.implicitly_wait(2)

            d = {
                "name": food_name,
                "img_src": img_path,
                "serving_unit": serving_unit,
                "serving_size": serving_size,
                "unit": second_unit,
                "amount": second_amount,
                "calories": calories,
                "total_fat": total_fat,
                "cholesterol": cholesterol,
                "sodium": sodium,
                "carbonhydrate": carbonhydrate,
                "protein": protein,
                "calcium": calcium,
                "iron": iron,
                "potassium": potassium,
                "vitamin_d": vitamin_d,
                "caffeine": caffeine,
                "img_screenshot": img_screen_shot
            }
            data_output[food_name] = d

        if page%10 == 0:
            file_name = data_config.data_raw_path/data_config.nutritionix_dir/f"{date_time}-common-food-p{part}.json"
            store_json(data_output, file_name)
            part += 1
            data_output = {}

        page += 1

    if data_output:
        file_name = data_config.data_raw_path/data_config.nutritionix_dir/f"{date_time}-common-food-p{part}.json"
        store_json(data_output, file_name)

if __name__ == "__main__":
    main()


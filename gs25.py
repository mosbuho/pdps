import threading
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import StaleElementReferenceException
from selenium.webdriver.chrome.options import Options

import time
import random

chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")


def fetch_visible_product_box(driver):
    WebDriverWait(driver, 10).until(lambda driver: driver.execute_script("return document.readyState") == "complete")
    product_boxes = driver.find_elements(By.CSS_SELECTOR, ".tblwrap.mt50")

    for box in product_boxes:
        if box.get_attribute("style") != "display: none;":
            return box

    return None


def fetch_page_data(driver, visible_product_box):
    product_data = []

    try:
        product_boxes_in_list = visible_product_box.find_elements(By.CSS_SELECTOR, ".prod_list .prod_box")

        for product in product_boxes_in_list:
            try:
                title = product.find_element(By.CSS_SELECTOR, ".tit").text.strip()
                price = product.find_element(By.CSS_SELECTOR, ".price").text.strip()
                image = product.find_element(By.CSS_SELECTOR, "img").get_attribute("src")
                flag_element = product.find_elements(By.CSS_SELECTOR, ".flag_box span")
                flag = flag_element[0].text.strip()
                
                product_data.append(
                    {
                        "title": title,
                        "price": price,
                        "image_url": image,
                        "flag": flag,
                    }
                )
            except StaleElementReferenceException:
                return fetch_page_data(driver, visible_product_box)

    except StaleElementReferenceException:
        return fetch_page_data(driver, visible_product_box)
    return product_data


def go_to_next_page(driver, visible_product_box):
    WebDriverWait(driver, 10).until(lambda driver: driver.execute_script("return document.readyState") == "complete")
    next_button = visible_product_box.find_element(By.CSS_SELECTOR, ".paging .next")
    ActionChains(driver).move_to_element(next_button).click().perform()
    time.sleep(random.uniform(2, 4))


def switch_to_tab(driver, tab_id):
    WebDriverWait(driver, 10).until(lambda driver: driver.execute_script("return document.readyState") == "complete")
    tab_element = driver.find_element(By.ID, tab_id)
    ActionChains(driver).move_to_element(tab_element).click().perform()


def fetch_products_in_tab(tab_id):
    driver = webdriver.Chrome(options=chrome_options)
    driver.get("http://gs25.gsretail.com/gscvs/ko/products/event-goods")
    switch_to_tab(driver, tab_id)
    visible_product_box = fetch_visible_product_box(driver)
    products = []
    previous_page_num = None

    while True:
        WebDriverWait(driver, 10).until(lambda driver: driver.execute_script("return document.readyState") == "complete")
        current_page_num = visible_product_box.find_element(By.CSS_SELECTOR, ".paging .num .on").text.strip()

        if current_page_num == previous_page_num:
            print(f"{tab_id} 완료")
            break

        products.extend(fetch_page_data(driver, visible_product_box))
        previous_page_num = current_page_num
        print(f"{tab_id} {current_page_num} 페이지")
        go_to_next_page(driver, visible_product_box)

    save_data(tab_id, products)
    driver.quit()


def save_data(tab_id, products):
    file_path = f""
    with open(file_path, "a", encoding="utf-8") as file:
        for product in products:
            file.write(f"상품명 : {product['title']}, 가격 : {product['price']}, 이미지 : {product['image_url']}, 행사 : {product['flag']}\n")
    print(f"{tab_id} 상품 {len(products)}개 저장")


def main():
    tab_ids = ["ONE_TO_ONE", "TWO_TO_ONE"]
    threads = [threading.Thread(target=fetch_products_in_tab, args=(tab_id,)) for tab_id in tab_ids]

    for thread in threads:
        thread.start()

    for thread in threads:
        thread.join()


if __name__ == "__main__":
    main()

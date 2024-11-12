from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait

import time
import random

driver = webdriver.Chrome()
visible_product_box = None


def wait_load():
    WebDriverWait(driver, 10).until(
        lambda driver: driver.execute_script("return document.readyState") == "complete"
    )


def fetch_visible_product_box():
    global visible_product_box
    product_boxes = driver.find_elements(By.CSS_SELECTOR, ".tblwrap.mt50")
    for box in product_boxes:
        if box.get_attribute("style") != "display: none;":
            visible_product_box = box
            break


def fetch_page_data():
    product_data = []
    product_boxes_in_list = visible_product_box.find_elements(
        By.CSS_SELECTOR, ".prod_list .prod_box"
    )
    for product in product_boxes_in_list:
        product_data.append(
            {
                "title": product.find_element(By.CSS_SELECTOR, ".tit").text.strip(),
                "price": product.find_element(By.CSS_SELECTOR, ".price").text.strip(),
                "image_url": product.find_element(By.CSS_SELECTOR, "img").get_attribute(
                    "src"
                ),
                "flag": product.find_element(
                    By.CSS_SELECTOR, ".flag_box span"
                ).text.strip(),
            }
        )
    return product_data


def go_to_next_page():
    next_button = visible_product_box.find_element(By.CSS_SELECTOR, ".paging .next")
    ActionChains(driver).move_to_element(next_button).click().perform()
    time.sleep(random.uniform(2, 4))


def switch_to_tab(tab_id):
    tab_element = driver.find_element(By.ID, tab_id)
    ActionChains(driver).move_to_element(tab_element).click().perform()
    wait_load()


def fetch_products_in_tab(tab_id):
    switch_to_tab(tab_id)
    fetch_visible_product_box()
    products = []
    previous_page_num = None

    while True:
        wait_load()
        current_page_num = visible_product_box.find_element(
            By.CSS_SELECTOR, ".paging .num .on"
        ).text.strip()

        if current_page_num == previous_page_num:
            print(f"{tab_id} 완료")
            break

        products.extend(fetch_page_data())
        previous_page_num = current_page_num
        print(f"{tab_id} {current_page_num} 페이지")
        go_to_next_page()

    save_data(tab_id, products)
    return products


def save_data(tab_id, products):
    file_path = r""
    with open(file_path, "a", encoding="utf-8") as file:
        for product in products:
            file.write(
                f"상품명 : {product['title']}, 가격 : {product['price']}, 이미지 : {product['image_url']}, 행사 : {product['flag']}\n"
            )
    print(f"{tab_id} 상품 {len(products)}개 저장 완료")


def main():
    driver.get("http://gs25.gsretail.com/gscvs/ko/products/event-goods")
    wait_load()
    fetch_products_in_tab("ONE_TO_ONE")
    fetch_products_in_tab("TWO_TO_ONE")
    driver.quit()


if __name__ == "__main__":
    main()

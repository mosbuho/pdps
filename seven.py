from bs4 import BeautifulSoup
import requests
import time
import random


def fetch_seven_eleven_products(pTab):
    url = "https://www.7-eleven.co.kr/product/listMoreAjax.asp"
    page = 0
    products = {}

    while True:
        data = {
            "intPageSize": "10",
            "intCurrPage": str(page),
            "pTab": str(pTab),
        }

        response = requests.post(url, data=data)
        soup = BeautifulSoup(response.text, "html.parser")
        list_cnt = soup.select_one("#listCnt")

        if list_cnt and int(list_cnt.get("value", "0")) == 0:
            print(f"{pTab}+1 마지막 페이지")
            break

        product_list = soup.select("li:not(.btn_more)")

        for item in product_list:
            name_elem = item.select_one(".tit_product")

            if name_elem is None:
                continue

            name = name_elem.text.strip()

            product_id = item.select_one("a.btn_product_01")["href"].split("'")[1]

            image_elem = item.select_one("img")
            image = "https://www.7-eleven.co.kr" + image_elem["src"]

            price_elem = item.select_one(".price_list span")
            price = price_elem.text.strip()

            promotion_elem = item.select_one(".tag_list_01 li")
            promotion = promotion_elem.text.strip()

            if product_id not in products:
                products[product_id] = {
                    "name": name,
                    "image": image,
                    "price": price,
                    "promotion": promotion,
                }
        print(f"{pTab}+1 {page} 페이지")
        time.sleep(random.uniform(2, 4))
        page += 1

    return products


def main():
    all_products = {}
    all_products.update(fetch_seven_eleven_products(1))
    all_products.update(fetch_seven_eleven_products(2))

    with open("seven_data.txt", "w", encoding="utf-8") as f:
        for product in all_products.values():
            f.write(f"상품명 : {product['name']}, 가격 : {product['price']}, 이미지 : {product['image']}, 행사 : {product['promotion']}\n")

    print(f"총 상품 {len(all_products)}개 저장")


if __name__ == "__main__":
    main()

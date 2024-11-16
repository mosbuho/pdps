from bs4 import BeautifulSoup
import requests
import time
import random


def fetch_emart24_products(category_seq):
    url = "https://emart24.co.kr/goods/event"
    page = 1
    products = []

    while True:
        params = {
            "page": str(page),
            "category_seq": str(category_seq),
        }

        response = requests.get(url, params=params)
        response.encoding = "utf-8"
        soup = BeautifulSoup(response.text, "html.parser")

        product_items = soup.select("div.itemWrap")

        if not product_items:
            print(f"{category_seq}+1 마지막 페이지")
            break

        for item in product_items:
            name = item.select_one(".itemtitle p a").text.strip()
            price = item.select_one(".price").text.strip()
            image = item.select_one(".itemSpImg img")["src"]
            promotion = item.select_one(".onepl, .twopl").text.strip()

            products.append(
                {
                    "name": name,
                    "price": price,
                    "image": image,
                    "promotion": promotion,
                }
            )

        print(f"{category_seq}+1 {page} 페이지")
        time.sleep(random.uniform(2, 4))
        page += 1

    return products


def main():
    all_products = []
    all_products.extend(fetch_emart24_products(1))
    all_products.extend(fetch_emart24_products(2))

    with open("emart24_data.txt", "w", encoding="utf-8") as f:
        for product in all_products:
            f.write(f"상품명 : {product['name']}, 가격 : {product['price']}, 이미지 : {product['image']}, 행사 : {product['promotion']}\n")
    print(f"총 상품 {len(all_products)}개 저장")


if __name__ == "__main__":
    main()

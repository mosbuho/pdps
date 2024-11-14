from bs4 import BeautifulSoup
import requests
import time
import random


def fetch_cu_products():
    url = "https://cu.bgfretail.com/event/plusAjax.do"
    page = 1
    products = []

    while True:
        response = requests.post(url, data={"pageIndex": page})
        response.encoding = "utf-8"
        soup = BeautifulSoup(response.text, "html.parser")

        if soup.select_one("#nothing"):
            print("마지막 페이지")
            break

        product_list = soup.select("ul > li.prod_list")

        for item in product_list:
            name = item.select_one(".name p").get_text(strip=True)
            image = "https:" + item.select_one(".prod_img img")["src"]
            price = item.select_one(".price strong").get_text(strip=True)
            badge = item.select_one(".badge span")
            promotion = badge.get_text(strip=True)

            products.append(
                {
                    "name": name,
                    "image": image,
                    "price": price,
                    "promotion": promotion,
                }
            )

        print(f"{page} 페이지")
        time.sleep(random.uniform(2, 4))
        page += 1

    with open("", "w", encoding="utf-8") as f:
        for product in products:
            f.write(f"상품명 : {product['name']}, 가격 : {product['price']}, 이미지 : {product['image']}, 행사 : {product['promotion']}\n")
    print(f"상품 {len(products)}개 저장")


def main():
    fetch_cu_products()


if __name__ == "__main__":
    main()

import requests
from bs4 import BeautifulSoup
import csv


# Open CSV file in write mode (w) to avoid overwriting data
with open("crypto.csv", 'w', encoding="utf-8") as csv_file:
    writer = csv.DictWriter(csv_file, ["Name", "Price", "24h Volume","24h Change"])

    # Write header only once if the file is empty
    if csv_file.tell() == 0:
        writer.writeheader()
    
    base_url = f"https://www.binance.com/en/markets/overview?p="

    for i in range(1, 15):
        num = str(i)
        full_url = base_url + num
        try:
            response = requests.get(full_url)
            response.raise_for_status()  # Raise exception for unsuccessful requests

            soup = BeautifulSoup(response.content, 'html.parser')
            src = soup.find_all('div', {'class': 'css-vlibs4'})

            for x in range(len(src)):
                # crypto_img = src[x].find('img')
                crypto_title = src[x].find('div', {'class': 'subtitle3'})
                crypto_price = src[x].find('div', {'class': 'body2 items-center css-18yakpx'})
                crypto_volume = src[x].find('div', {'class': 'body2 text-t-primary css-18yakpx'})
                crypto_change = src[x].find('div', {'class': 'subtitle3 css-18jvuxg'})

                # Validate data before writing (optional)
                if crypto_title and crypto_price and crypto_volume and crypto_change:
                    c_t = crypto_title.text.strip()
                    # c_i = crypto_img.text.strip()
                    c_p = crypto_price.text.strip()
                    c_v = crypto_volume.text.strip()
                    c_c = crypto_change.text.strip()

                    crypto_info = {
                        # "IMG" : c_i,
                        "Name": c_t,
                        "Price": c_p,
                        "24h Volume": c_v,
                        "24h Change": c_c
                    }
                    writer.writerow(crypto_info)

            print(f"Scraped data from page [{i}]")

        except requests.exceptions.RequestException as e:
            print(f"Error occurred from {i}: {e}")

print("Finished!")

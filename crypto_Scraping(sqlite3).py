import requests
from bs4 import BeautifulSoup
import sqlite3

# Create a connection to the SQLite database file 'crypto_data.db' (create if it doesn't exist)
conn = sqlite3.connect('crypto_data.db')

# Create a cursor object to execute SQL statements
cursor = conn.cursor()

# Create the 'crypto_info' table if it doesn't exist
cursor.execute("""
CREATE TABLE IF NOT EXISTS crypto_info (
    IMG BLOB NOT NULL,
    Name TEXT NOT NULL,
    Price TEXT NOT NULL,
    "24h Change" TEXT NOT NULL,
    "24h Volume" TEXT NOT NULL
)
""")

base_url = "https://www.binance.com/en/markets/overview?p="

for i in range(1, 14):
    num = str(i)
    full_url = base_url + num

    try:
        response = requests.get(full_url)
        response.raise_for_status()

        soup = BeautifulSoup(response.content, 'html.parser')
        src = soup.find_all('div', {'class': 'css-vlibs4'})

        for x in range(len(src)):    
            crypto_img = src[x].find('img')
            crypto_title = src[x].find('div', {'class': 'subtitle3'})
            crypto_price = src[x].find('div', {'class': 'body2 items-center css-18yakpx'})
            crypto_volume = src[x].find('div', {'class': 'body2 text-t-primary css-18yakpx'})
            crypto_change = src[x].find('div', {'class': 'subtitle3 css-18jvuxg'})


            # Validate data
            if crypto_title and crypto_price and crypto_volume and crypto_change and crypto_img: 
                c_i = crypto_img.text.strip() 
                c_t = crypto_title.text.strip() 
                c_p = crypto_price.text.strip()
                c_v = crypto_volume.text.strip()
                c_c = crypto_change.text.strip()

                # Insert data into the 'crypto_info' table
                cursor.execute("""
                INSERT INTO crypto_info (IMG,Name, Price,"24h Change", "24h Volume")
                VALUES (?, ?, ?, ?, ?)
                """, (c_i,c_t, c_p, c_c, c_v))

            print(f"Scraped data for page {i}")

    except requests.exceptions.RequestException as e:
        print(f"Error occurred for page {i}: {e}")

# Commit changes to the database
conn.commit()

# Close the database connection
conn.close()

print("Finished!")

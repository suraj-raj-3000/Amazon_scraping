import requests
from bs4 import BeautifulSoup as bs
import csv
import  json
import time
import sqlite3


conn = sqlite3.connect('test.db')
print ("Opened database successfully")

# conn.execute('''CREATE TABLE COMPANY
#          (product_link  VARCHAR(200)    NOT NULL,
#          title           char(100)    NOT NULL,
#          price            char(50)     NOT NULL,
#          image_link        CHAR(200),
#          product_detail varchar(500));''')
# print ("Table created successfully")

conn.close()


filename="scraped_data.json"
my_dict = []

def scraping(product_link) :
    # print("Try link : ", product_link)
    headerAgent = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.135 Safari/537.36 Edge/12.246','Accept-Language': 'en-US, en;q=0.5'}

    try:
        response = requests.get(product_link , headers=headerAgent)
        time.sleep(10)
        #print(response.content)
        soup = bs(response.content , features='html.parser')

        title = soup.find("span",attrs={"id": 'productTitle'}).string
        price = soup.find("span", attrs={"class": 'a-offscreen'}).string
        image_url = soup.find("img", attrs={"id": 'landingImage'})
        Product_Details_div = soup.find("div", attrs={"id":'feature-bullets'})

        product_details = Product_Details_div.find_all("span")
        for li in Product_Details_div.find_all("li"):
            product_desc = ( li.text)
        img_url=(image_url['src'])
        price=(price)
        title=(title)
        

        x = {
        "Product Link": product_link,
        "Title": title,
        "Price": price,
        "Image Link": img_url,
        "Product Details": product_desc
        }
        print(x)
        my_dict.append(x)
        
        with open(filename, 'w') as json_file:
            json.dump(my_dict, json_file, indent=4) 
        # file.close()

    except:
        print(url, "Not Avilable")

def dump_db():
    conn = sqlite3.connect('test.db')

    #load json file
    with open(filename) as fp:
        temp = json.load(fp)
        
        for i in temp["scraped"]:
            product_json = i["Product Link"]
            title_json = i["Title"]
            price_json = i["Price"]
            img_link_json = i["Image Link"]
            prd_detail_json = i["Product Details"]
            # print(prd_detail_json,"\n")
            # print(title_json,"\n")
            # print(price_json,"\n")
            # print(img_link_json,"\n")
            # print(prd_detail_json,"\n")
            # print(i["Product Link"],"\n", i["Title"],"\n", i["Price"],"\n", i["Image Link"],"\n", i["Product Details"],"\n")
            # print("temp-",temp)
        conn = sqlite3.connect('test.db')
        conn.execute("INSERT INTO COMPANY (product_link,title,price,image_link,product_detail) VALUES ('product_json', 'title_json', 'price_json', 'img_link_json','prd_detail_json' )") 
        conn.commit()
        conn.close()


file = open('Amazon_Scraping _Sheet1.csv')
csvreader = csv.reader(file)
type(file)

rows = []
with open("Amazon_Scraping _Sheet1.csv", 'r') as file:
    csvreader = csv.reader(file)
    header = next(csvreader)

    for row in csvreader:

        url = (f"https://www.amazon.{row[3]}/dp/{row[2]}")
        scraping(url)


dump_db()
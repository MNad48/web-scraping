from urllib.request import urlopen
from bs4 import BeautifulSoup
import pandas as pd
#My first scraping script.... A little bit naive still good

product_list = []

def get_laptop(soup_object):
    all_products = soup_object.find_all("div",class_="item-cell")
    for product in all_products:
        product_name = product.find("a", class_="item-title")
        old_price = product.find("span",class_="price-was-data")
        price_symbol = product.find("li",class_="price-current").text
        if price_symbol:
            price_symbol = price_symbol[0]
        else:
            price_symbol = ""
        new_price = product.find("li",class_="price-current").find("strong")
        price_sup = product.find("li",class_="price-current").find("sup",recursive=False).text if new_price else ""
        total_offers = product.find("a",class_="price-current-num")
        total_offers = str(total_offers.text).replace("(","").replace(")","") if total_offers else ""
        
        item = {
            "Product Title":product_name.text,
            "Old Price":""+price_symbol+" "+old_price.text if old_price else "N/A",
            "New Price":""+price_symbol+" "+new_price.text+""+price_sup if new_price else "N/A" ,
            "Total Offers":total_offers
        }
        product_list.append(item)
def get_total_pages():
    myURL = "https://www.newegg.com/p/pl?N=100167732%20601399382%20601399385&page=1"
    resp = urlopen(myURL)
    soup_page = BeautifulSoup(resp.read(),"html.parser")
    pagination = soup_page.find("span",class_="list-tool-pagination-text").find("strong",recursive=False).text
    pagination = str(pagination).split("/")[1]
    return int(pagination)
def get_all_laptops():
    for x in range(1,get_total_pages()+1):
        myURL = f"https://www.newegg.com/p/pl?N=100167732%20601399382%20601399385&page={x}"
        resp = urlopen(myURL)
        page_html = resp.read()
        soup = BeautifulSoup(page_html,"html.parser")
        print(f"on page {x}")
        get_laptop(soup_object=soup)
       

def get_output():
    df = pd.DataFrame(product_list)
    df.to_csv("laptops.csv",index=False)

get_all_laptops()
get_output()

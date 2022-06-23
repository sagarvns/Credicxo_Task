import pandas as pd
import requests
from bs4 import BeautifulSoup as bs
import json
import time

def getSpans(htmlcontent):
    scraper = bs(htmlcontent,"html.parser")
    spans = scraper.find_all("span")
    #l=[]
    ans=[]
    for span in spans:
        #print(span.get('id',"***"))
        if span.get('id',"")=='productTitle':
            #l.append(span)
            ans.append(span)
    return ans
def getImages(htmlcontent):
    scraper= bs(htmlcontent,"html.parser")
    divs=scraper.find_all("div")
    ans=""
    for div in divs:
        if div.get("id","")=="main-image-container":
            imgs=div.find_all('img')
            #print(imgs)
            for img in imgs:
                ans=img.get("src","")

    return ans
def getPrice(htmlcontent):
    scraper = bs(htmlcontent, "html.parser")
    spans = scraper.find_all("span")
    ans=""
    for span in spans:
        #print(span.get("class",";;;"))
        if set(span.get("class",""))==set(["a-size-base","a-color-price","a-color-price"]):
            #print("Hello")+
            ans=span.text
            break
    return ans
def getDetail(htmlcontent):
    scraper = bs(htmlcontent, "html.parser")
    uls = scraper.find_all("ul")

    ans=[]
    for ul in uls:
        #print(span.get("class",";;;"))
        #print(set(ul.get("class",[""])),set(["a-unordered-list","a-nostyle","a-vertical","a-spacing-none","detail-bullet-list"]))
        if set(ul.get("class",[""]))== set(["a-unordered-list","a-nostyle","a-vertical","a-spacing-none","detail-bullet-list"]):
            #print("Hello")
            lis=ul.find_all("li")
            for li in lis:
                spans=li.find_all("span")
                for span in spans:
                    spans2=span.find_all("span")
                    desc=""
                    #print(spans2)
                    for span2 in spans2:
                        #print("********",span2,"$$$$$",span2.text)
                        desc+=str(span2.text)
                    desc=desc.replace("\n","")
                    desc=desc.replace("\u200f","")
                    desc=desc.replace("\u200e","")
                    des=""
                    a=desc.split(" ")
                    for i in a:
                        des+=i
                    #print(desc,")))))))))))))))")
                    if des !="":
                        ans.append(des)

            break
    #print(ans)
    return ans



df=pd.read_csv("Amazon Scraping.csv")
link1="https://www.amazon."
#country=""
link2="/dp/"
#asin=""
n=len(df)
prevtime=time.perf_counter()
jsondata=[]
for i in range(n):
    country=df.loc[i,"country"]
    asin=df.loc[i,"Asin"]
    link=link1+country+link2+asin
    print(link)
    htmlcontent=""

    response= requests.get(link)
    webContent=response.content

    #print(type(response.status_code))
    #print(htmlcontent)
    print(response.status_code)
    if response.status_code==200:
        if response.status_code == 200:
            # print(webContent)
            d = {}
            divisions = getSpans(webContent)
            d["product_name"]=divisions[0].text
            d["product_image_link"]=getImages(webContent)
            d["product_price"]=getPrice(webContent)
            # print("PRODUCT NAME:")
            # print(divisions[0].text)
            # print("PRODUCT IMAGE LINK:")
            # print(getImages(webContent))
            # print("PRODUCT PRICE:")
            # print(getPrice(webContent))
            # print("PRODUCT DETAILS:")

            details= getDetail(webContent)
            d["product_detail"]={}
            for detail in details:
                x=detail.split(":")
                d["product_detail"][x[0]]=x[1]
            jsondata.append(d)
    if (i+1)%100==0:
        currtime=time.perf_counter()
        print(currtime-prevtime)
        prevtime=currtime
final=json.dumps(jsondata, indent=2)
out_file = open("myfile.json", "w")

json.dump(final, out_file, indent=6)

out_file.close()
print(final)

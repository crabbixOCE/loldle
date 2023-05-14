import selenium
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import pandas as pd


driver = webdriver.Chrome()

driver.get("https://loldle.net/classic")

input("Press Enter to continue...")
rows = []
champs = driver.find_elements(By.CLASS_NAME,"classic-answer")
i=0
for champ in champs:
    attrs = champ.find_elements(By.CLASS_NAME,"square-content")
    row=[]
    print(i)
    i+=1
    for attr in attrs:
        try:
            name = attr.find_element(By.CLASS_NAME,"champion-icon-name")
            print(name.get_attribute("innerHTML"))
            row.append(name.get_attribute("innerHTML"))
        except:
            row.append(attr.text)
    rows.append(row)
pd.DataFrame(rows,columns=["Name","Gender","Position","Species","Resource","Range type","Region","Release"]).to_csv("loldle.csv")

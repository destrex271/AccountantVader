from selenium import webdriver 
import time
import json
import os
from dotenv import load_dotenv, find_dotenv



def get_data():
    load_dotenv(find_dotenv())
    chrome_ops = webdriver.ChromeOptions()
    chrome_ops.add_argument("--headless")
    chrome_ops.add_argument("--disable-gpu")
    driver = webdriver.Chrome(options=chrome_ops)

    driver.maximize_window()

    driver.get("https://www.investopedia.com/auth/realms/investopedia/protocol/openid-connect/auth?client_id=finance-simulator&redirect_uri=https%3A%2F%2Fwww.investopedia.com%2Fsimulator%2Fportfolio&state=549fe793-b14a-457b-936f-257eba8522f8&response_mode=fragment&response_type=code&scope=openid&nonce=79175962-1f57-4a66-8b71-dd4fd2a36ee5")

    email_vc = driver.find_element_by_id("username")
    passwd = driver.find_element_by_id("password")
    btn = driver.find_element_by_id("login") 
    email_vc.send_keys(os.environ.get("USERNAME"))  # Username
    passwd.send_keys(os.environ.get("PASSWD"))  # Password
    btn.click()
    print("OK")
    driver.get("https://www.tradingview-widget.com/embed-widget/screener/?locale=en#%7B%22width%22%3A%22100%25%22%2C%22height%22%3A523%2C%22defaultColumn%22%3A%22overview%22%2C%22defaultScreen%22%3A%22most_capitalized%22%2C%22market%22%3A%22america%22%2C%22showToolbar%22%3Atrue%2C%22isTransparent%22%3Atrue%2C%22colorTheme%22%3A%22light%22%2C%22largeChartUrl%22%3A%22www.investopedia.com%2Fsimulator%2Fresearch%2Fmore-info%22%2C%22enableScrolling%22%3Atrue%2C%22utm_source%22%3A%22www.investopedia.com%22%2C%22utm_medium%22%3A%22widget%22%2C%22utm_campaign%22%3A%22screener%22%7D")
    print("LINKS----------------------------------")
    time.sleep(8)


    all_data = {}

    # Grab available data
    # //*[@id="js-screener-container"]/div[4]/table/tbody/tr[1]/td[2]/span[1]

    try:
        for x in range(1,51):
            ticker = driver.find_element_by_xpath(f'''//*[@id="js-screener-container"]/div[4]/table/tbody/tr[{x}]/td[1]/div/div[2]/a''').text
            last_value = driver.find_element_by_xpath(f'''//*[@id="js-screener-container"]/div[4]/table/tbody/tr[{x}]/td[2]/span[1]''').text
            chg_percent = driver.find_element_by_xpath(f'''//*[@id="js-screener-container"]/div[4]/table/tbody/tr[{x}]/td[3]''').text
            chg_val = driver.find_element_by_xpath(f'''//*[@id="js-screener-container"]/div[4]/table/tbody/tr[{x}]/td[4]''').text
            technical_status = driver.find_element_by_xpath(f'''//*[@id="js-screener-container"]/div[4]/table/tbody/tr[{x}]/td[5]/span''').text
            volume = driver.find_element_by_xpath(f'''//*[@id="js-screener-container"]/div[4]/table/tbody/tr[{x}]/td[6]''').text
            volume_into_price = driver.find_element_by_xpath(f'''//*[@id="js-screener-container"]/div[4]/table/tbody/tr[{x}]/td[7]''').text
            market_cap = driver.find_element_by_xpath(f'''//*[@id="js-screener-container"]/div[4]/table/tbody/tr[{x}]/td[8]''').text
            profit_to_earning_ratio = driver.find_element_by_xpath(f'''//*[@id="js-screener-container"]/div[4]/table/tbody/tr[{x}]/td[9]''').text
            earnings_per_share = driver.find_element_by_xpath(f'''//*[@id="js-screener-container"]/div[4]/table/tbody/tr[{x}]/td[10]''').text
            if str(chg_percent).__contains__("\u2212"):
                chg_percent = str(chg_percent).replace("\u2212","-")
            if str(chg_val).__contains__("\u2212"):
                chg_val = str(chg_val).replace("\u2212","-")
            all_data[f'{ticker}'] = {
                'last_value' :  last_value,
                'change_percent' : chg_percent,
                'chg_val' : chg_val,
                'technical_status': technical_status,
                'volume': volume,
                'volume_into_price': volume_into_price,
                'market_cap': market_cap,
                'profit_to_earning_ratio': profit_to_earning_ratio,
                'earnings_per_share': earnings_per_share
            }


    finally:
        driver.close()


    # Converting to JSON

    with open("data.json","w") as file:
        json_obj = json.dumps(all_data, indent= 4)
        file.write(json_obj)


    #driver.close()
        


    # clicking Debt parameters

    # driver.find_element_by_xpath('''//*[@id="js-screener-container"]/div[3]/div/div[1]''').click()
    # time.sleep(1)
    # driver.find_element_by_xpath('''//*[@id="js-screener-container"]/div[3]/div/div[2]/div[1]/input''').send_keys("Debt")
    # time.sleep(2)
    # print("CLICKING")
    # driver.find_element_by_xpath('''//*[@id="js-screener-container"]/div[3]/div/div[2]/div[2]/div[1]/div[90]/label/label/input''').click()
    # driver.find_element_by_xpath('''//*[@id="js-screener-container"]/div[3]/div/div[2]/div[2]/div[1]/div[135]/label/label/input''').click()
    # driver.find_element_by_xpath('''//*[@id="js-screener-container"]/div[3]/div/div[2]/div[2]/div[1]/div[192]/label/label/input''').click()



    # comp_names = []
    # all_links = []
    # for x in range(1,51):
    #     y = driver.find_element_by_xpath(f'''//*[@id="js-screener-container"]/div[4]/table/tbody/tr[{x}]/td[1]/div/div[2]/a''')
    #     link = y.get_attribute("href")
    #     value = y.text
    #     comp_names.append(value)
    #     all_links.append(link)
    # print("GOT EM---------------------------------")
    # print("Going thru links-----------------------")
    # all_data = {}
    # i = 0
    # for link in all_links:
    #     i+=1
    # time.sleep(5)
    # print(all_links)
    #driver.close()
    # //*[@id="js-screener-container"]/div[4]/table/tbody/tr[1]/td[1]/div/div[2]/a
    # //*[@id="js-screener-container"]/div[4]/table/tbody/tr[2]/td[1]/div/div[2]/a



    # Queryset url : https://www.investopedia.com/simulator/research/more-info/?symbol=NVDA

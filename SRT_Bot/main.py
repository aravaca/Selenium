
# SPDX-FileCopyrightText: © 2025 Hyungsuk Choi <chs_3411@naver[dot]com>, University of Maryland 
# SPDX-License-Identifier: CC-BY-NC-4.0

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support import expected_conditions as EC
import time
import json

# load config.json file
with open("config.json", "r", encoding="utf-8") as f:
    config = json.load(f)

# USER WILL BE ASKED THE FOLLOWING FIELDS IN THE TERMINAL
DEPARTURE_DATE = input("Departure Date (YYYYMMDD): ") #YYYYMMDD
ARRIVAL_DATE = input("Arrival Date (YYYYMMDD): ")

# TIME CONSTANTS FOR A SMOOTHER FLOW
PAYMENT_TIME = 20 #seconds
WAIT_TIME = 10
REFRESH_INTERVAL = 5
SCROLL_TIME = 1
TABLOAD_TIME = 0.5

seat_index = {
  "일반실": 7, 
  "특실": 6 
}

options = Options()
options.add_experimental_option("detach", True)
options.add_argument("--disable-blink-features=AutomationControlled")

driver = webdriver.Chrome(service=Service(), options=options)

#load SRT website 
driver.get("https://etk.srail.kr/hpg/hra/01/selectShuttleScheduleList.do?pageId=TK0101010000")
driver.maximize_window()

# Setup wait for later
wait = WebDriverWait(driver, WAIT_TIME)

#loading new page 
wait.until(
    EC.presence_of_element_located((By.ID, "dptRsStnCdNm"))
)

#select itinerary
dep_station = driver.find_element(By.ID, "dptRsStnCdNm")
dep_station.clear()
dep_station.send_keys(config["DEPARTURE_STATION"])

arv_station = driver.find_element(By.ID, "arvRsStnCdNm")
arv_station.clear()
arv_station.send_keys(config["ARRIVAL_STATION"])

dep_date = driver.find_element(By.ID, "dptDt1")
Select(dep_date).select_by_value(DEPARTURE_DATE)

dep_time = driver.find_element(By.ID, "dptTm1")
Select(dep_time).select_by_value(config["DEPARTURE_TIME"])

arv_date = driver.find_element(By.ID, "dptDt2")
Select(arv_date).select_by_value(ARRIVAL_DATE)

arv_time = driver.find_element(By.ID, "dptTm2")
Select(arv_time).select_by_value(config["ARRIVAL_TIME"])

seat_type = driver.find_element(By.ID, "locSeatAttCd1")
Select(seat_type).select_by_visible_text(config["SEAT_PREFERENCE"])

submit = driver.find_element(By.CSS_SELECTOR, "#search_top_tag > input")
submit.click()

#loading time table
try:
    wait.until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "#result-form > fieldset > div:nth-child(7) > table > tbody > tr:nth-child(" + config["DEP_TIME_INDEX"] +") > td:nth-child(" + seat_index[config["SEAT_CLASS"]] + ") > a"))
    ) 
    #select time table - SRT312 and SRT361
    time.sleep(SCROLL_TIME)
    dep_train = driver.find_element(By.CSS_SELECTOR, "#result-form > fieldset > div:nth-child(7) > table > tbody > tr:nth-child(" + config["DEP_TIME_INDEX"] +") > td:nth-child(" + seat_index[config["SEAT_CLASS"]] + ") > a")
    dep_train.click()
except Exception as e:
    print("Tickets sold out")
    time.sleep(WAIT_TIME) #waits 10sec for you to select a train manually in case the tickets are sold out for the train you're trying to take
finally:
    time.sleep(SCROLL_TIME)

try:
    arv_train = driver.find_element(By.CSS_SELECTOR, "#result-form > fieldset > div:nth-child(14) > table > tbody > tr:nth-child(" + config["ARV_TIME_INDEX"] +") > td:nth-child(" + seat_index[config["SEAT_CLASS"]] + ") > a")
    arv_train.click()
except Exception as e:
    print("Tickets sold out")
    time.sleep(WAIT_TIME) #waits 10sec for you to select a train manually in case the tickets are sold out for the train you're trying to take
finally:
    time.sleep(SCROLL_TIME)

submit2 = driver.find_element(By.CSS_SELECTOR, "#result-form > fieldset > div:nth-child(20) > input.btn_midium.btn_blue_dark.val_m.wx100")
submit2.click()

#loading login page
wait.until(
     EC.presence_of_element_located((By.ID, "srchDvNm01"))
)
account_id = driver.find_element(By.ID, "srchDvNm01")
account_id.send_keys(config["ACCOUNT_ID"])

password = driver.find_element(By.ID, "hmpgPwdCphd01")
password.send_keys(config["PASSWORD"] + Keys.ENTER)

#loading confirmation page
wait.until(
    EC.presence_of_element_located((By.CSS_SELECTOR, "#list-form > fieldset > div.tal_c > button.btn_large.btn_blue_dark.val_m.mgr10"))
)

time.sleep(SCROLL_TIME)

confirm = driver.find_element(By.CSS_SELECTOR, "#list-form > fieldset > div.tal_c > button.btn_large.btn_blue_dark.val_m.mgr10")
confirm.click()

#loading receipt
wait.until(
    EC.presence_of_element_located((By.CSS_SELECTOR, "#list-form > fieldset > div.tal_r > button"))
)

time.sleep(SCROLL_TIME)

pay = driver.find_element(By.CSS_SELECTOR, "#list-form > fieldset > div.tal_r > button")
pay.click()

#스마트폰 발권
time.sleep(TABLOAD_TIME)
mobile_ticket = driver.find_element(By.CSS_SELECTOR, "#_LAYER_ > div > div > div.tab-small > ul > li:nth-child(2) > a")
mobile_ticket.click()

#스마트폰 발권 > 계속하기
time.sleep(TABLOAD_TIME)
mobile_ticket_cont = driver.find_element(By.CSS_SELECTOR, "#_LAYER_ > div > div > div.button-area > input[type=button]")
mobile_ticket_cont.click()

#loading payment tab
wait.until(
    EC.presence_of_element_located((By.CSS_SELECTOR, "#chTab2"))
)
payment_method = driver.find_element(By.CSS_SELECTOR, "#chTab2")
payment_method.click()
kakao_pay = driver.find_element(By.CSS_SELECTOR, "#kakaoPay")
kakao_pay.click()

## loading a separate payment tab for 'Kakao Pay'

# Store the ID of the original window
original_window = driver.current_window_handle

# Check we don't have other windows open already
assert len(driver.window_handles) == 1

# Click the link which opens in a new window
issue_ticket = driver.find_element(By.CSS_SELECTOR, "#requestIssue2")
issue_ticket.click()

# Wait for the new window or tab
wait.until(EC.number_of_windows_to_be(2))

# Loop through until we find a new window handle
for window_handle in driver.window_handles:
    if window_handle != original_window:
        driver.switch_to.window(window_handle)
        break

# Wait for the new tab to finish loading content
wait.until(EC.title_is("카카오페이"))

wait.until(
    EC.presence_of_element_located((By.CSS_SELECTOR, "#카톡결제 > span"))
)

request_to_kakao = driver.find_element(By.CSS_SELECTOR, "#카톡결제 > span")
request_to_kakao.click()

wait.until(
    EC.presence_of_element_located((By.NAME, "phoneNumber"))
)

phone_num = driver.find_element(By.NAME, "phoneNumber")
phone_num.send_keys(config["PHONE_NUM"])

date_of_birth = driver.find_element(By.NAME, "dateOfBirth")
date_of_birth.send_keys(config["DATE_OF_BIRTH"] + Keys.ENTER)

request_payment = driver.find_element(By.CSS_SELECTOR, "#카톡결제 > div > div._form-wrap_s43yp_6 > form > button")
request_payment.click()

# program waits for 20 seconds to allow the user to make a kakao payment on their phone
# all you have to do is check your KakaoTalk messsage and tap the 'Pay' button 
# so it won't take long..
time.sleep(PAYMENT_TIME)

# after the 20 seconds, the program will hit the 'payment done' button indefinitely 
# at a 5 second interval until you make a payment. Otherwise, an error pop-up
# will float triggering the program to close it indefinitely
while EC.presence_of_element_located((By.CSS_SELECTOR, "#root > main > div._confirm-wrap_vzw96_46 > button")):
    #program clicks the payment confirmation button, completing the booking & payment process
    payment_complete = driver.find_element(By.CSS_SELECTOR, "#root > main > div._confirm-wrap_vzw96_46 > button")
    payment_complete.click()
    time.sleep(REFRESH_INTERVAL)
    if EC.presence_of_element_located((By.CSS_SELECTOR, "body > div.kp-m-modallayout.isShow.kp-m-dialog-modallayout > div.kp-m-dialog._dialog_sb9nd_1._notice_sb9nd_4 > div.kp-m-dialog-buttons > div > div > div > div > button")):
        wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "body > div.kp-m-modallayout.isShow.kp-m-dialog-modallayout > div.kp-m-dialog._dialog_sb9nd_1._notice_sb9nd_4 > div.kp-m-dialog-buttons > div > div > div > div > button"))
        )
        payment_error = driver.find_element(By.CSS_SELECTOR, "body > div.kp-m-modallayout.isShow.kp-m-dialog-modallayout > div.kp-m-dialog._dialog_sb9nd_1._notice_sb9nd_4 > div.kp-m-dialog-buttons > div > div > div > div > button")
        payment_error.click()
        time.sleep(REFRESH_INTERVAL)
        continue
    else:
        break

# receipt loads and the browser will shut in 10 seconds 
time.sleep(WAIT_TIME)

driver.quit()




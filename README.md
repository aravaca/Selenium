# SRT(Super Rapid Train) Ticket Auto-Booker

![428318974-1e0b1db4-4918-466d-a23d-bd43b6398fa9](https://github.com/user-attachments/assets/ac72ed4b-8373-46e4-8767-78d00fa20f14)


During my military service in Daejeon, I got tired of manually booking the same SRT train ticket to Seoul every time I had leave. The process was always the same—same station, same time, same train—and it got old fast. So I built this automation tool to streamline it.

Now all I have to do is enter my leave dates, and the program handles the rest. At the end of the flow, I get a KakaoTalk payment request on my phone—tap to pay, and I’m set.

---

## Disclaimer
SRT strictly prohibits booking tickets through automation tools, possibly to prevent server overload and illegal ticket trades. The program is strictly intended for personal use and should only be used responsibly and at your own risk to facilitate a repetitive ticketing flow. This project is not affiliated with SR Co., Ltd.

---

## Features

- **Fully automated booking** for SRT train tickets
- **Customizable defaults**: station, departure time, seat preference, etc
- **One-time setup** for personal information (name, birthdate, contact, account ID/password, etc.)
- **Supports round-trip booking**
- Sends **KakaoTalk payment request** once booking is complete
- Designed for **repetitive, same-route travelers** (like commuters and soldiers on leave)

---

## Tech Stack

- **Python** (core scripting)
- **Selenium** (web automation)
- **ChromeDriver** (for browser control)
  
---

## Setup Instructions

### 1. Clone the repo
```bash
git clone https://github.com/aravaca/Selenium.git
cd Selenium/SRT_Bot/
```
### 2. Install Dependencies
```bash
pip install -r requirements.txt
```
### 3. Add your personal info
Create a 'config.json' file in the SRT_Bot directory in the following form and fill in the fields.
```json
{
    "ACCOUNT_ID": "", //account id
    "PASSWORD":  "", //account password
    "DEPARTURE_STATION": "대전", //천안아산역이면 역 제외하고 '천안아산'만  입력
    "ARRIVAL_STATION": "수서",
    "DEPARTURE_TIME": "080000", //HH0000, 24H format, even hours only like 060000(6am), 140000(=2pm), etc
    "ARRIVAL_TIME": "180000",
    "DEP_TIME_INDEX": "3", //A list of trains will be given once you select the approximate dep/arv time.
                         //I'll choose the third train from the top of the list for my case (SRT Train No. 312).
                         //You need to look at the timetable and check this manually at least once
                         //before you automate the flow.
    "ARV_TIME_INDEX": "3",
    "SEAT_CLASS": "일반실", //options: 일반실, 특실
    "SEAT_PREFERENCE": "창측좌석", //options: 내측좌석, 창측좌석, 1인석
    "PHONE_NUM": "", // -없이 입력
    "DATE_OF_BIRTH": "" //YYMMDD
}
```
### 4. Run the script
```bash
python main.py
```
Then, enter your desired departure and arrival dates in the terminal.

### 5. Check KakaoTalk
Once the booking is complete, you'll receive a payment request via KakaoTalk.
As long as you have your payment methods set up, just tap "Pay", and you're all set!
You will have 20 seconds to tap the button and after that, the program will indefinitely hit the 'Done' button, completing the whole process.

![Screenshot_20250405_174712_KakaoTalk.jpg](https://github.com/user-attachments/assets/abc03da3-19f7-424a-ad3f-85563e9b9912)


## License
[CC BY-NC 4.0]https://creativecommons.org/licenses/by-nc/4.0/deed.en

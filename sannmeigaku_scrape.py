from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import time
import json

def scrape_meishiki(year, month, day, gender):
    """
    指定された生年月日と性別でunkoi.comから命式データを取得する
    """
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')

    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)

    try:
        driver.get("https://unkoi.com/special/sanmeigaku/")
        wait = WebDriverWait(driver, 10)

        # iframeが表示されるまで待機し、切り替える
        iframe = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "iframe")))
        driver.switch_to.frame(iframe)

        # 年の入力フィールドが表示されるまで待機してから入力
        year_input = wait.until(EC.presence_of_element_located((By.NAME, "birthday_year")))
        year_input.send_keys(str(year))
        driver.find_element(By.NAME, "birthday_month").send_keys(str(month))
        driver.find_element(By.NAME, "birthday_day").send_keys(str(day))
        
        if gender == "男性":
            driver.find_element(By.ID, "gender1").click()
        else:
            driver.find_element(By.ID, "gender2").click()

        driver.find_element(By.ID, "send").click()
        time.sleep(3)

        html = driver.page_source
        soup = BeautifulSoup(html, "html.parser")
        
        result = {"input": {"year": year, "month": month, "day": day, "gender": gender}}
        
        # 陽占（人体星図）の星を取得
        yosen_stars = {}
        star_positions = {
            "頭": "jintai_02", "胸": "jintai_05", "腹": "jintai_08",
            "右手": "jintai_04", "左手": "jintai_06",
            "左肩": "jintai_03", "右足": "jintai_09", "左足": "jintai_07"
        }
        
        for name, class_name in star_positions.items():
            element = soup.find("div", class_=class_name)
            if element:
                yosen_stars[name] = element.get_text(strip=True)
        
        result["expected_yosen"] = yosen_stars
        
        return result

    finally:
        driver.quit()

if __name__ == '__main__':
    test_cases = [
        {"year": 1985, "month": 12, "day": 15, "gender": "女性"},
        {"year": 1990, "month": 1, "day": 1, "gender": "男性"},
        {"year": 2000, "month": 5, "day": 20, "gender": "女性"},
        {"year": 1977, "month": 8, "day": 8, "gender": "男性"},
    ]

    results = []
    for case in test_cases:
        print(f"Scraping for: {case['year']}/{case['month']}/{case['day']} ({case['gender']})")
        try:
            scraped_data = scrape_meishiki(case["year"], case["month"], case["day"], case["gender"])
            results.append(scraped_data)
            print("...Success")
        except Exception as e:
            print(f"...Failed: {e}")
        time.sleep(1) # サーバー負荷軽減

    with open('data/sanmeigaku_test_cases.json', 'w', encoding='utf-8') as f:
        json.dump(results, f, ensure_ascii=False, indent=2)

    print("\nTest cases saved to data/sanmeigaku_test_cases.json")

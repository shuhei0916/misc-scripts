from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
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

        # 入力フォームの要素セレクタ
        year_selector = (By.NAME, "i_cyear")
        month_selector = (By.NAME, "i_cmonth")
        day_selector = (By.NAME, "i_cday")
        gender_selector = (By.NAME, "i_gender")
        submit_button_selector = (By.ID, "ftbutton")

        # 入力フォームが表示されるまで待機
        wait.until(EC.presence_of_element_located(year_selector))
        
        # ドロップダウンリストを操作して生年月日と性別を入力
        Select(driver.find_element(*year_selector)).select_by_value(str(year))
        Select(driver.find_element(*month_selector)).select_by_value(str(month))
        Select(driver.find_element(*day_selector)).select_by_value(str(day))
        
        gender_value = "1" if gender == "女性" else "0"
        Select(driver.find_element(*gender_selector)).select_by_value(gender_value)

        # 鑑定ボタンをクリック
        driver.find_element(*submit_button_selector).click()
        
        # 結果ページの読み込みを待機
        wait.until(EC.presence_of_element_located((By.ID, "motifresult16")))

        html = driver.page_source
        soup = BeautifulSoup(html, "html.parser")
        
        result = {"input": {"year": year, "month": month, "day": day, "gender": gender}}
        
        # 陽占（人体星図）の星を取得
        yosen_stars = {}
        # HTML構造から特定したIDと位置の対応
        star_id_map = {
            "頭": "res_type1_star1",
            "左肩": "res_type1_star2",
            "右手": "res_type1_star3",
            "胸": "res_type1_star4",
            "腹": "res_type1_star5",
            "左足": "res_type1_star6",
            "左手": "res_type1_star7",
            "右足": "res_type1_star8",
        }
        
        motif_area = soup.find("div", id="motifresult16")
        if motif_area:
            for position, star_id in star_id_map.items():
                element = motif_area.find("img", id=star_id)
                if element and 'alt' in element.attrs:
                    yosen_stars[position] = element['alt']
        
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
            if scraped_data.get("expected_yosen"):
                results.append(scraped_data)
                print("...Success")
            else:
                print("...Failed: Could not find result stars.")
        except Exception as e:
            print(f"...Failed: {e}")
        time.sleep(1)

    if results:
        with open('data/sanmeigaku_test_cases.json', 'w', encoding='utf-8') as f:
            json.dump(results, f, ensure_ascii=False, indent=2)
        print("\nTest cases saved to data/sanmeigaku_test_cases.json")
    else:
        print("\nNo test cases were successfully generated.")

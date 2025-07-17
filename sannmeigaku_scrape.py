from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import time

# オプション設定
options = Options()
# options.add_argument('--headless')  # デバッグ時はコメントアウトOK
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')

# ドライバセットアップ
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=options)

# アクセス
driver.get("https://unkoi.com/special/sanmeigaku/")

# iframeに切り替え
iframe = driver.find_element(By.CSS_SELECTOR, "iframe")
driver.switch_to.frame(iframe)

# 入力
driver.find_element(By.NAME, "birthday_year").send_keys("1990")
driver.find_element(By.NAME, "birthday_month").send_keys("1")
driver.find_element(By.NAME, "birthday_day").send_keys("1")
driver.find_element(By.ID, "gender1").click()

# 鑑定ボタンをクリック
driver.find_element(By.ID, "send").click()

# ページ遷移＆読み込み待ち
time.sleep(3)

# 結果を取得
html = driver.page_source
driver.quit()

# BeautifulSoupで解析
soup = BeautifulSoup(html, "html.parser")
result_section = soup.find("div", class_="resultArea")
if result_section:
    print(result_section.get_text(strip=True))
else:
    print("結果が見つかりませんでした。HTML構造が変わった可能性があります。")

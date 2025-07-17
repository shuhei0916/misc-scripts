import requests
from bs4 import BeautifulSoup
import time

def scrape_mbti_description(url):
    headers = {
        "User-Agent": "Mozilla/5.0"
    }
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, "html.parser")

    # 記事の抽出
    article = soup.select_one("article.main.description")
    if not article:
        article = soup.find("article", {"data-article": "personality"})
    if not article:
        raise Exception("記事本文が見つかりません")

    # タイトル
    title = article.find("h1")
    title_text = title.get_text(strip=True) if title else ""

    # 本文
    content_div = article.find("div", class_="description__content")
    if not content_div:
        content_div = article.find("div")

    paragraphs = []
    for elem in content_div.find_all(["p", "h2", "blockquote", "div"], recursive=False):
        if elem.name == "blockquote":
            paragraphs.append("引用: " + elem.get_text(strip=True))
        elif elem.name == "h2":
            paragraphs.append("## " + elem.get_text(strip=True))
        elif elem.name == "div" and "description-pullout" in elem.get("class", []):
            paragraphs.append("【ポイント】" + elem.get_text(strip=True))
        elif elem.name == "p":
            paragraphs.append(elem.get_text(strip=True))

    result_text = title_text + "\n\n" + "\n\n".join(paragraphs)
    return result_text

if __name__ == "__main__":
    mbti_types = [
        "intj", "intp", "entj", "entp",
        "infj", "infp", "enfj", "enfp",
        "istj", "isfj", "estj", "esfj",
        "istp", "isfp", "estp", "esfp"
    ]

    base_url = "https://www.16personalities.com/ja/{}型の性格"

    for mbti in mbti_types:
        url = base_url.format(mbti)
        try:
            print(f"取得中: {mbti.upper()} - {url}")
            description = scrape_mbti_description(url)
            filename = f"{mbti}_description.txt"
            with open(filename, "w", encoding="utf-8") as f:
                f.write(description)
            print(f"✔ 保存成功: {filename}")
        except Exception as e:
            print(f"✖ エラー（{mbti.upper()}）: {e}")
        time.sleep(2)  # サーバーに負荷をかけないように2秒待つ

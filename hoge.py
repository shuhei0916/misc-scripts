import time
import pyautogui

# スクリーンショットを保存するディレクトリ
screenshot_dir = "screenshots"

# 最初のページ番号
page_num = 1

while True:
    # スクリーンショットを撮る
    filepath = f"{screenshot_dir}/page_{page_num}.png"
    pyautogui.screenshot(filepath)

    # ページ番号を増やす
    page_num += 1

    # 左矢印キーを押して次のページへ
    pyautogui.press('left')

    # ページが切り替わるまで待つ
    time.sleep(5)  # 適切な待ち時間に調整してください

    # 終了条件（例：特定の要素が見つからない場合）
    # 例：画面上に特定の画像が見つからない場合
    if pyautogui.locateOnScreen('end_image.png') is None:  # end_image.pngが見つからない場合
        break

# 終了メッセージ
print("スクリーンショット撮影完了")
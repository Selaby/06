import urllib
import pandas as pd
import numpy as np
from get_api import get_api
from sheets import *

URL = "https://app.rakuten.co.jp/services/api/IchibaItem/Search/20170706"
APP_ID = "1065617872679994165"

def search(keyword):
    params = {
    "keyword": keyword,
    "format": "json",
    "applicationId": APP_ID
    }

    # 格納用のリスト
    # item_name = []
    # price = []

    # API取得用の関数
    result = get_api(URL, params)

    # for文を回してdictを作る
    item_key = ["itemName", "itemPrice"]
    item_list = []
    for i in range(0, len(result["Items"])):
        tmp_item = {}
        item = result["Items"][i]["Item"]
        for key, value in item.items():
            if key in item_key:
                tmp_item[key] = value
        # item_list.append(tmp_item.copy()) https://qiita.com/Massasquash/items/ed565b8ba4fd51dca54f .copyじゃないとうまくいかないらしいが何故かうまく行っている
        item_list.append(tmp_item)

    # リストをデータフレームに変換
    items_df = pd.DataFrame(item_list)

    # 列名を日本語にする
    items_df.columns = ["商品名", "商品価格"]
    
    # インデックスを0ではなく1から割り振る https://chusotsu-program.com/df-reset-index/
    items_df.index = np.arange(1, len(items_df)+1)

    # csv出力
    # items_df.to_csv("ichibaitem.csv", encoding="utf-8-sig")
    # # log(f"処理完了 成功件数: {success} 件 / 失敗件数: {fail} 件")
    # print("csvファイルを出力しました")

    # スプレッドシート処理
    sheets(items_df)
    print("スプレッドシートに出力しました")


if __name__ == "__main__":
    keyword = input("検索キーワードを入力してください >>> ")
    search(keyword)
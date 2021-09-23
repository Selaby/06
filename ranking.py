import urllib
import pandas as pd
import numpy as np
from get_api import get_api
from sheets import *

URL = "https://app.rakuten.co.jp/services/api/IchibaItem/Ranking/20170628"
APP_ID = "1065617872679994165"

def search(genreId):
    params = {
    "genreId": genreId,
    "format": "json",
    "applicationId": APP_ID
    }

    # 格納用のリスト
    item_name_list = []
    rank_list = []

    # API取得用の関数
    result = get_api(URL, params)

    for item in result["Items"]:
        rank = item["Item"]["rank"]
        rank_list.append(rank)

        item_name = item["Item"]["itemName"]
        item_name_list.append(item_name)

    # リストをデータフレームとして結合
    df = pd.DataFrame({"ランキング":rank_list, "商品名":item_name_list})

    # for文を回してdictを作る こちらだと列の並び順をコントロール出来ない
    # item_key = ["productId", "productName", "minPrice"]
    # item_list = []
    # for i in range(0, len(result["Products"])):
    #     tmp_item = {}
    #     item = result["Products"][i]["Product"]
    #     for key, value in item.items():
    #         if key in item_key:
    #             tmp_item[key] = value
        
    #     # item_list.append(tmp_item.copy()) https://qiita.com/Massasquash/items/ed565b8ba4fd51dca54f .copyじゃないとうまくいかないらしいが何故かうまく行っている
    #     item_list.append(tmp_item)
    
    # インデックスを0ではなく1から割り振る https://chusotsu-program.com/df-reset-index/
    df.index = np.arange(1, len(df)+1)

    # csv出力
    # items_df.to_csv("product.csv", encoding="utf-8-sig")
    # df.to_csv("ranking.csv", encoding="utf-8-sig")
    # # log(f"処理完了 成功件数: {success} 件 / 失敗件数: {fail} 件")
    # print("csvファイルを出力しました")

    # スプレッドシート処理
    sheets(df)
    print("スプレッドシートに出力しました")

if __name__ == "__main__":
    genreId = input("ジャンルIDを入力してください >>> ")
    search(genreId)
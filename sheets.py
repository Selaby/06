import datetime
import gspread
from google.oauth2.service_account import Credentials
from gspread_formatting.batch_update_requests import format_cell_range
import pandas as pd
from gspread_dataframe import set_with_dataframe
from gspread_formatting import *

def sheets(df: object):
    # 使用するAPI
    scopes = [
        'https://www.googleapis.com/auth/spreadsheets',
        'https://www.googleapis.com/auth/drive'
    ]

    # シークレットキーの入ったjsonファイル
    credentials = Credentials.from_service_account_file(
        'secret.json',
        scopes=scopes
    )

    gc = gspread.authorize(credentials)

    # スプシのURLからコピペ
    SP_SHEET_KEY = "13Gw5gBgR9FTo__MhVaat7VQbbelt1-vC9q1ybLetY6o"

    sh = gc.open_by_key(SP_SHEET_KEY)

    # 新しいワークシートを作成
    namae = str(datetime.datetime.now())
    worksheet = sh.add_worksheet(title=namae, rows=100, cols=100)
    set_column_width(worksheet, 'A', 500)

    # 書き込みの始点となる行と列
    first_row = 1
    first_col = 1
    set_with_dataframe(worksheet, df, row=first_row, col=first_col)

    # ヘッダー、インデックス、バリューの範囲を指定
    header_range = "A1:B1"
    # index_range = "B3:B8"
    value_range = "A2:B31"

    # ヘッダーの書式を設定
    header_fmt = CellFormat(
        backgroundColor = color(38/255, 166/255, 154/255),
        textFormat = textFormat(bold=True, foregroundColor=color(255/255, 255/255, 255/255)),
        horizontalAlignment = "CENTER"
    )
    format_cell_range(worksheet, header_range, header_fmt)

    # 枠線を付ける
    border = Border("SOLID", Color(0,0,0,0))
    fmt = CellFormat(borders = Borders(top=border, bottom=border, left=border, right=border))
    format_cell_range(worksheet, header_range, fmt)
    # format_cell_range(worksheet, index_range, fmt)
    format_cell_range(worksheet, value_range, fmt)
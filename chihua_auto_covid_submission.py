# colabに入ってないモジュールをインストールする
# !pip install japanize_matplotlib
# !sudo pip install slackweb

import requests # slackへのpost用 
import json 
import pandas as pd
import matplotlib.pyplot as plt
from pylab import rcParams
plt.style.use('ggplot') 

import japanize_matplotlib
import seaborn as sns
sns.set(font="IPAexGothic")
# %matplotlib inline 

## 取得するオープンデータのURLを指定する
url = 'https://covid19.mhlw.go.jp/public/opendata/newly_confirmed_cases_daily.csv'

## slack投稿用のトークンを読み込んで設定しておく
with open('config.json') as f:
    parm = json.load(f)

TOKEN = parm["slack_api_token_chihua"]
CHANNEL = '#dog_bot'

#------------------------------------------------------------------------
# 描画用に外部のオープンデータを取得(URL指定する)
#------------------------------------------------------------------------
def get_data():

    # オープンデータを取得 
    df = pd.read_csv(url,encoding="utf-8")

    # 取得したデータから描画に必要な項目のみを抽出する 
    df = df[['Date', 'ALL', 'Tokyo', 'Kanagawa', 'Saitama', 'Chiba']]

    return df

#------------------------------------------------------------------------
# slackに作成した画像とメッセージを編集して投稿する処理
#------------------------------------------------------------------------
def slack_send(df_japan):

    ## 前日のデータを取得
    yesterday_uu = df_japan[-1:].iloc[0]['ALL']

    ## 直近１週間のデータを取得し移動平均を算出
    one_week_uu = df_japan[-7:].iloc[0:7]['ALL']
    one_week_moving_average_uu = round(one_week_uu.rolling(window=7).mean().iloc[6])

    ## 前日と１週間分の移動平均の比率を算出
    rate = (yesterday_uu / one_week_moving_average_uu).round(2)

    ## 前日の感染者数が100名以上の時にはその改善状況によってメッセージを変化させる 
    if yesterday_uu >= 100:
        ## 改善状態によってメッセージを変化させる
        if rate >= 1.0:
            chihua_talk = 'また悪化してきてるので注意ワン。お出かけは最小限にしようワン。'
        elif 0.8 <= rate < 1.0:
            chihua_talk = 'ちょっと改善の兆しワン。でもまだ油断は禁物ワン'
        elif 0.5 <= rate <  0.8:
            chihua_talk = 'かなり改善してきてそうワン。でも外から帰ったら、うがい手洗いは忘れずにワン'
        else:
            chihua_talk = 'いい感じワン！これならそろそろ美味しい外食にも行けそうワン！'
    else:
        chihua_talk = '感染者数、少なめだけど油断は禁物ワン！'

    TEXT = f"前日の感染者数は「{yesterday_uu}人」ワン。１週間分の平均が「{one_week_moving_average_uu}人」なので、比較すると「{(rate * 100).round(2)}%」になったワン! \n {chihua_talk}"
    
    # main処理内で作成したPNGを読み込む
    files = {'file': open("covid_observation_graph.png", 'rb')}
    param = {
        'token': TOKEN, 
        'channels': CHANNEL,
        'filename': "covid_graph",
        'initial_comment': TEXT,
        'title': "チワちゃんのコロナ感染者状況レポート"
    }

    # requestsでメッセージと画像をslackへ投稿
    requests.post(url="https://slack.com/api/files.upload",params=param, files=files)

    return files, param

def main():

    #-- 描画用に外部のオープンデータを取得(URL指定する)
    df_japan = get_data()

    #-- グラフ用のデータを準備
    # 描画前設定
    rcParams['figure.figsize'] = 15,10 #描画の際のサイズを指定
    plt.tight_layout() # 画像の文字の位置などが重ならないように自動調整

    # 描画
    df_japan.plot(x = "Date")
    plt.title('COVID 日本国内日別感染者数の推移', fontsize=36)
    plt.ylabel('感染者数', fontsize=24)
    plt.xlabel('日付', fontsize=24)
    plt.legend(fontsize=36)
    plt.tick_params(labelsize=18)

    # 画像を保存（slack連携用に一旦保存必要）
    plt.savefig('covid_graph.png')

    # 画像表示
    plt.show()

    # slackに作成した画像を投稿する処理
    send_items = slack_send(df_japan)

    # 利用したパラメータをreturnしておく（確認保存用）
    return df_japan, send_items


if __name__ == '__main__':
    main()
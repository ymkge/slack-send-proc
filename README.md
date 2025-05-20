# COVID-19 Daily Report to Slack

---

## 概要

このPythonスクリプトは、厚生労働省が公開している新型コロナウイルス感染症のオープンデータを利用して、日ごとの新規感染者数の推移グラフを自動生成し、そのグラフと感染状況のサマリーメッセージをSlackチャンネルに投稿します。毎日の感染状況を手軽に確認できるツールとして活用できます。

### 主な機能

- 厚生労働省のオープンデータ（日別新規感染者数）を自動取得
- 全国の感染者数、および主要な都道府県（東京、神奈川、埼玉、千葉）の感染者数推移グラフを生成
- 前日の感染者数と直近1週間の移動平均を比較し、感染状況に応じたメッセージを動的に生成
- 生成されたグラフ画像とメッセージをSlackチャンネルに自動投稿

---

## 動作環境

- Python 3.x
- 以下のPythonライブラリ:
    - `requests`
    - `json`
    - `pandas`
    - `matplotlib`
    - `japanize_matplotlib`
    - `seaborn`
    - `slackweb` (または `requests`で直接Slack APIを叩く場合は不要)

---

## セットアップ方法

### 1. リポジトリのクローン

まず、このリポジトリをローカル環境にクローンします。

```bash
git clone [https://github.com/your-username/covid-daily-report.git](https://github.com/your-username/covid-daily-report.git)
cd covid-daily-report
```

### 2. 必要なライブラリのインストール
pipを使って必要なPythonライブラリをインストールします。

```bash
pip install requests pandas matplotlib japanize_matplotlib seaborn slackweb
```

### 3. Slack APIトークンの設定
Slackにメッセージと画像を投稿するために、Slack APIトークンが必要です。以下の手順でconfig.jsonファイルを作成し、トークンを設定してください。

Slack APIのウェブサイト (https://api.slack.com/apps) で新しいSlackアプリを作成します。

アプリの作成後、BotsまたはOAuth & PermissionsセクションでBot User OAuth Token (xoxb-で始まるトークン) を取得します。

プロジェクトのルートディレクトリにconfig.jsonという名前のファイルを作成し、取得したトークンを以下の形式で記述します。

JSON
```
{
  "slack_api_token_chihua": "YOUR_SLACK_BOT_TOKEN_HERE"
}
```

YOUR_SLACK_BOT_TOKEN_HEREの部分を実際のトークンに置き換えてください。

Slackアプリを投稿したいチャンネルに招待してください。

### 使い方
スクリプトを実行するだけで、データ取得、グラフ生成、Slackへの投稿が自動的に行われます。

```bash
python your_script_name.py
```
（your_script_name.py は、このコードを保存したファイル名に置き換えてください。例えば covid_reporter.py など）

### 注意事項
Slack APIトークンは機密情報です。config.jsonファイルはGit管理から除外することをおすすめします（.gitignoreにconfig.jsonを追加してください）。
厚生労働省のオープンデータのURLが変更された場合、スクリプト内のurl変数を更新する必要があります。
Google Colabで実行する場合、!pip installや!sudo pip installの行はコメントアウトを外して実行してください。

### ライセンス
このプロジェクトは、MITライセンスの下で公開されています。詳細については、LICENSEファイルを参照してください。


# slack-send-proc
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

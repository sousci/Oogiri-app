
# 大喜利AIアプリ

このアプリは、2025年6月28日に開催された、**第2回生成AIハッカソン＠大阪「人間はコードを書いてはいけない？！」**
[https://osakan-space.connpass.com/event/346084/](https://osakan-space.connpass.com/event/346084/)
 にて制作されました。  
OpenAIのAPIを使用し、Flask上で動作するシンプルなWebアプリです。

![アプリ画面](ogiri_app.jpg)


## 機能概要

- ユーザーが入力した「お題」に対し、大喜利のようなユーモアある回答を生成
- 回答は音声でも再生されます（Text-to-Speech機能付き）
- 音声入力にも対応（ブラウザの音声認識APIを使用）



## 使用方法

### ① リポジトリのダウンロード
- 「Code」ボタンから「Download ZIP」でダウンロード
- 任意の場所に展開

### ② 環境構築
★Pythonのインストールは省略  

---
【Windowsの場合】
- コマンドプロンプトまたはPowerShellを開く
- 展開したフォルダへ移動：
```
cd パス\to\展開先
```
- ライブラリをインストール
```
pip install -r requirements.txt
```

---
【Macの場合】  
★pipが未インストールの場合
```
brew install python
```


- ターミナルを開く
- 展開先ディレクトリへ移動：
```
cd /path/to/展開先
```

・ライブラリのインストール

```
pip install -r requirements.txt
```

---

### ③ アプリの起動
- 展開したフォルダに移動：

```
python ogiri.py
```

④ Webブラウザから、[http://127.0.0.1:5000/](http://127.0.0.1:5000/) にアクセス


## 依存ライブラリ(requirements.txt)
- Flask==3.0.3
- openai==1.93.0
- python-dotenv==0.21.0

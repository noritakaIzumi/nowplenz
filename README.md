# nowplenz

Slack にラジオ局のなうぷれを投稿するシステムです。 AWS リソースを使用します。

---

## Slack API トークンの用意

Slack API を使用するための Bot User OAuth Token を用意します。

`xoxb-0000000000000-0000000000000-xxxxxxxxxxxxxxxxxxxxxxxx`

Bot Token Scopes については以下のスコープを追加してください。

- chat:write
- chat:write.customize

## 必要な AWS リソース

### IAM ユーザ

権限を持たない IAM ユーザを一つ作成してください。曲情報のハッシュをこのユーザのタグに格納します。

### Lambda 実行用 IAM ロール

Lambda を実行するための IAM ロールを作成します。以下のポリシーを持つ IAM ロールを作成してください。

- AWSLambdaBasicExecutionRole
- IAMFullAccess

### Lambda layers

Python pip で以下のパッケージをインストールし、 zip 圧縮してアップロードしてレイヤーを作成してください。

- boto3
- mypy-boto3-iam
- beautifulsoup4

以下のスクリプトでも実行できます。
レイヤーは `build/layers` ディレクトリに出来上がります。

```shell
make create-layers
```

### Lambda functions

1. Python ランタイムで関数を作成します。（Python 3.9 で動作確認済みです。）
2. Slack API トークンを環境変数に設定します。(key: `SLACK_API_TOKEN`,
   value: `xoxb-0000000000000-0000000000000-xxxxxxxxxxxxxxxxxxxxxxxx`)
3. 実行ロールに作成した IAM ロールを指定します。
4. 作成したレイヤーを追加します。
5. ソースファイルを zip ファイルでアップします。後述の [ソースファイル zip の作成方法](#create-source-files) をご覧ください。
6. 動作確認を行います。後述の [動作確認方法](#test) をご覧ください。

### EventBridge rules

必要に応じて、Lambda 定期実行用のイベントを設定してください。

---

## Create source files

pkg 配下のファイルを zip 形式で圧縮します。 pkg ディレクトリそのものではなく、pkg 配下のファイル・ディレクトリを対象にして圧縮することに注意してください。

Docker をお使いの方は以下コマンドで圧縮済みのファイル (`package.zip`) が用意できます。

```shell
docker run --rm -it -v `pwd`:/root -w /root alpine ./docker-entrypoint.sh
```

以下、トラブルシューティング。

### docker: Error response from daemon: the working directory 'C:/Program Files/Git/root' is invalid, it needs to be an absolute path.

パス指定部分の先頭にスラッシュを 1 つ加えてみてください。

```shell
docker run --rm -it -v /`pwd`:/root -w //root alpine ./docker-entrypoint.sh
```

## Test

作成した Lambda function の画面で Test event を作成し、テストしてください。サンプルは以下の通りです。

```json
{
  "radio_stations": [
    {
      "station_key": "kiss-fm",
      "slack_post_channel": "C030CHUNKG8",
      "tag_iam_username": "slack-post-now-playing-tags"
    },
    {
      "station_key": "fm802",
      "slack_post_channel": "C02UW50E1B8",
      "tag_iam_username": "slack-post-now-playing-tags"
    }
  ]
}
```

- radio_stations: 以下の情報をラジオ局ごとに指定します。
  - station_key: ラジオ局のキー
  - slack_post_channel: 投稿する Slack のチャンネル
  - tag_iam_username: 曲情報ハッシュ格納用の IAM ユーザ名

現在対応している station_key については [対応しているラジオ局](#we-support-many-radio-stations-) をご覧ください。

---

## We support many radio stations!

`station_key`: station name

### Japan

- Tohoku
  - `afb`: エフエム青森
  - `fm-akita`: エフエム秋田
  - `fmii`: エフエム岩手
  - `rfm`: エフエム山形
  - `771fm`: Date fm
  - `fmf`: ふくしま FM
- Kanto
  - `jwave`: J-WAVE (東京)
- Kinki
  - `fmosaka`: FM大阪
  - `kiss-fm`: Kiss FM KOBE
  - `fm802`: FM802 (大阪)
  - `e-radio`: e-radio (滋賀)
- Chugoku
  - `fm-sanin`: FM 山陰
  - `fm-okayama`: FM OKAYAMA
  - `hiroshima-fm`: HFM (広島)
  - `fmy`: エフエム山口 FMY

---

## Roadmap

- [ ] More supports of radio stations
  - [ ] Hokkaido
  - [ ] Kanto
  - [ ] Shikoku
  - [ ] Kyushu
  - [ ] Okinawa
  - [ ] Overseas
- [ ] Create scripts for automate the deployment
- [ ] Create development manual
- [ ] Threading, multiprocessing
- [ ] Configure channels via Slack's slash command

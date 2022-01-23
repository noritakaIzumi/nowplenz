# nowplenz

Slack にラジオ局のなうぷれを投稿するシステムです。 AWS リソースを使用します。

---

## 必要な AWS リソース

### SecretsManager

Slack API を使用するための Bot User OAuth Token を次のように格納してください。

- Key/Value 方式

| Secret key | Secret value                                              |
|:-----------|:----------------------------------------------------------|
| token      | xoxb-0000000000000-0000000000000-xxxxxxxxxxxxxxxxxxxxxxxx |

- Plaintext 方式

```text
{
  "token": "xoxb-0000000000000-0000000000000-xxxxxxxxxxxxxxxxxxxxxxxx"
}
```

Bot Token Scopes については以下のスコープを追加してください。

- chat:write
- chat:write.customize

### IAM ユーザ

権限を持たない IAM ユーザを一つ作成してください。曲情報のハッシュをこのユーザのタグに格納します。

### Lambda 実行用 IAM ロール

Lambda を実行するための IAM ロールを作成します。以下のポリシーを持つ IAM ロールを作成してください。

- AWSLambdaBasicExecutionRole
- IAMFullAccess
- SecretsManagerReadWrite

### Lambda layers

Python pip で以下のパッケージをインストールし、 zip 圧縮してアップロードしてレイヤーを作成してください。

- boto3
- mypy-boto3-iam
- beautifulsoup4

### Lambda functions

1. Python ランタイムで関数を作成します。（Python 3.9 で動作確認済みです。）
2. 実行ロールに作成した IAM ロールを指定します。
3. 作成したレイヤーを追加します。
4. ソースファイルを zip ファイルでアップします。後述の [ソースファイル zip の作成方法](#create-source-files) をご覧ください。
5. 動作確認を行います。後述の [動作確認方法](#test) をご覧ください。

### EventBridge rules

必要に応じて、Lambda 定期実行用のイベントを設定してください。

---

## Create source files

pkg 配下のファイルを zip 形式で圧縮します。 pkg ディレクトリそのものではなく、pkg 配下のファイル・ディレクトリを対象にして圧縮することに注意してください。

Docker をお使いの方は以下コマンドで圧縮済みのファイルが用意できます。

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
  "token": {
    "secret_arn": "arn:aws:secretsmanager:us-east-1:000000000000:secret:secret-name-xxxxxx",
    "region": "us-east-1"
  },
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

- token: SecretsManager で作成した secret の ARN とリージョンを指定します。
- radio_stations: 以下の情報をラジオ局ごとに指定します。
  - station_key: ラジオ局のキー
  - slack_post_channel: 投稿する Slack のチャンネル
  - tag_iam_username: 曲情報ハッシュ格納用の IAM ユーザ名

現在対応している station_key については [対応しているラジオ局](#we-support-many-several-radio-stations) をご覧ください。

---

## We support ~~many~~ several radio stations!

`station_key`: station name

### Japan

- Tohoku
  - `fm-akita`: エフエム秋田
  - `771fm`: Date fm
- Kanto
  - `jwave`: J-WAVE (東京)
- Kinki
  - `fmosaka`: FM大阪
  - `kiss-fm`: Kiss FM KOBE
  - `fm802`: FM802 (大阪)

---

## Roadmap

- More supports of radio stations
- Create scripts for automate the deployment
- Create development manual
- Threading, multiprocessing

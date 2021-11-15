import socket
import os

# 自作モジュール
import svrdat
import hcrypt


def get_data():
    while True:
        # ファイルを入力してもらう。
        fp = input('File: ').replace('"', '')
        # ファイルが入力されれば、データを読んでバイトを返す
        if os.path.isfile(fp):
            with open(fp, 'rb') as f:
                return f.read()
        # ファイルが入力が失敗したら入力のやり直し。
        else:
            print('Invalid path.')


def launch():
    print('=== Client ===')
    # 送付するデータを入力してもらう。
    data = get_data()

    # データの暗号化
    key = hcrypt.get_key()
    data_enc = hcrypt.get_xor_repeat(data, key)

    # サーバーのIPアドレスを入力してもらう。
    adr_svr = input('Server IP: ')

    # ソケット設定
    soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    soc.connect((adr_svr, svrdat.PORT))

    # 暗号化データを送付する。
    soc.send(data_enc)


if __name__ == '__main__':
    launch()

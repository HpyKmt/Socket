import socket
import datetime
import os

# 自作モジュール
import svrdat
import hcrypt


def get_fn_out():
    # 出力ファイル名称を日時にする。
    return datetime.datetime.now().strftime('%y-%m-%d_%H-%M-%S') + '.dat'


def make_dir():
    # 出力フォルダを確保しておく。
    if not os.path.isdir(svrdat.DIR_NAME):
        os.mkdir(svrdat.DIR_NAME)


def write_file(data):
    # 出力ファイル名称を確保する。
    fn_out = get_fn_out()
    # 出力フォルダが無ければ作る。
    make_dir()
    # 出力の相対ファイルパスを構築する。
    fp_out = os.path.join(svrdat.DIR_NAME, fn_out)
    # 出力先にファイルを書く。
    with open(fp_out, 'wb') as f:
        f.write(data)
    print(f'Created {fp_out}.')


def launch():
    print('=== Server ===')
    # IP アドレスを入力してもらう。
    adr_svr = input('Server IP: ')

    # ソケット設定
    soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    soc.bind((adr_svr, svrdat.PORT))
    soc.listen(svrdat.QUEUE_COUNT)
    data = bytearray()

    # 接続を待つ。
    # ここでwhileループをしない。
    # ファイルを一つ受け取ったら、サーバーは閉じるようにする。
    print('while loop at:', datetime.datetime.now())
    con, adr = soc.accept()

    # 接続が検知されたことを通知。
    now = datetime.datetime.now().strftime('%H:%M:%S')
    print(f'accepted {adr} at {now}.')

    # データを読み取る。
    while True:
        buf = con.recv(svrdat.BUF_SIZE)
        if buf:
            data.extend(buf)
        else:
            # 暗号化解読
            key = hcrypt.get_key()
            data_dec = hcrypt.get_xor_repeat(data, key)
            # ファイルに書き込み
            write_file(data_dec)
            # ループを抜ける。
            break

    print('Closing socket...')
    soc.close()

    print('Completed.')

if __name__ == '__main__':
    launch()

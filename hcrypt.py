"""
データを暗号化する。
"""
import io


# 0 1 2 3 4 5 6 7 8 9 A B C D E F
# <-----> <-----> <--------------
#   sig     ver     body

def get_key():
    # テキストを入力してもらって、UTF-8にエンコードしたバイトを返す。
    return input('key: ').encode('utf-8')


def _get_xor_single(_chunk, _key):
    # 渡されたバイトをキーでXORしてバイトを返す。
    if len(_chunk) == len(_key):
        return bytes([_c ^ _k for _c, _k in zip(_chunk, _key)])
    else:
        raise ValueError(f'Length mismatch: chunk {len(_chunk)} <> key {len(_key)}')


def get_xor_repeat(data, key):
    key_size = len(key)
    str_dat = io.BytesIO(data)
    buf_lst = []

    while True:
        # キーサイズ毎にバイトを読み取る。
        chunk = str_dat.read(key_size)
        # 読み取れたら処理する。
        if chunk:
            # 全長分読み取れたら、そのままキーを渡す。
            chunk_size = len(chunk)
            if chunk_size == key_size:
                buf_lst.append(_get_xor_single(chunk, key))
            # 最後の切れ端の場合、キーをチャンクサイズに切る。
            elif chunk_size < key_size:
                buf_lst.append(_get_xor_single(chunk, key[:chunk_size]))
            # 下記のelseはあり得ない。
            else:
                raise ValueError(f'Impossible Condition: chunk size = {chunk_size}')
        # 空っぽならループから出る。
        else:
            break

    return b''.join(buf_lst)


if __name__ == '__main__':
    pass


# 課題29: data保存用のディレクトリ作成とsin関数データの保存
def main1():
    import math
    import os

    # dataディレクトリを作成
    data_dir = "../data"
    if not os.path.exists(data_dir):
        os.makedirs(data_dir)
        print(f"{data_dir} ディレクトリを作成しました")

    Nmax = 100
    x = []
    y = []

    # sin関数の波形を保存用のデータとしてリストを作る
    for i in range(Nmax):
        # リストに新たな要素を追加するときは"+"で長さ1のリスト[**]を連結
        x = x + [i * (1.0 / Nmax) * 2 * math.pi]
        y = y + [math.sin(x[i])]

    # 書き込み内容を一時保存する文字列s
    s = ""
    for i in range(len(x)):
        # 文字列にリストの内容を1行ずつ書き込む
        s += "{0:<.5f}\t{1:<.5f}\n".format(x[i], y[i])

    # 文字列の内容確認
    print("データの最初の5行:")
    lines = s.split("\n")[:5]
    for line in lines:
        if line:
            print(line)

    f = open("../data/test_01.txt", "w")
    # 文字列の内容をファイルに書き込む
    f.write(s)
    f.close()
    print("データを ../data/test_01.txt に保存しました")

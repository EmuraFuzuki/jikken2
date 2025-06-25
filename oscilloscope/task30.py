# 課題30: 文字列フォーマットの変更テスト
def main1():
    import math
    import os

    # dataディレクトリを作成
    data_dir = "../data"
    if not os.path.exists(data_dir):
        os.makedirs(data_dir)

    Nmax = 100
    x = []
    y = []

    # sin関数の波形を保存用のデータとしてリストを作る
    for i in range(Nmax):
        x = x + [i * (1.0 / Nmax) * 2 * math.pi]
        y = y + [math.sin(x[i])]

    # 3つの異なるフォーマットでテスト
    formats = [
        ("{0:<.2f}\t{1:<.2f}\n", "test_30_1.txt", "小数点以下2桁"),
        ("{0:<.5f}, {1:<.5f}\n", "test_30_2.txt", "カンマ区切り"),
        ("{0:<.5f}\t{1:<.5f}\n", "test_30_3.txt", "y, x の順序"),
    ]

    for format_str, filename, description in formats:
        s = ""
        for i in range(len(x)):
            if filename == "test_30_3.txt":
                # y, x の順序で保存
                s += format_str.format(y[i], x[i])
            else:
                s += format_str.format(x[i], y[i])

        filepath = f"../data/{filename}"
        with open(filepath, "w") as f:
            f.write(s)

        print(f"{description}: {filepath} に保存")
        print("  最初の3行:")
        lines = s.split("\n")[:3]
        for line in lines:
            if line:
                print(f"  {line}")
        print()

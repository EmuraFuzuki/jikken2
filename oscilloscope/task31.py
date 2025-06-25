# 課題31: 文字列フォーマットの探求（指数表示など）
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

    # 様々なフォーマットのテスト
    formats = [
        ("{0:.5f}\t{1:.5f}\n", "normal_format.txt", "通常の小数点表示"),
        ("{0:.3e}\t{1:.3e}\n", "scientific_format.txt", "指数表記"),
        ("{0:10.5f}\t{1:10.5f}\n", "fixed_width_format.txt", "固定幅表示"),
        ("{0:+.5f}\t{1:+.5f}\n", "sign_format.txt", "符号付き表示"),
        ("{0:.2%}\t{1:.2%}\n", "percentage_format.txt", "パーセント表示"),
    ]

    for format_str, filename, description in formats:
        s = ""
        for i in range(len(x)):
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

    # formatメソッドの詳細説明
    print("=== formatメソッドの説明 ===")
    print("基本形式: {インデックス:書式指定}")
    print("例:")
    print("  {0:.5f} - 0番目の引数を小数点以下5桁で表示")
    print("  {0:.3e} - 0番目の引数を指数表記（小数点以下3桁）で表示")
    print("  {0:10.5f} - 0番目の引数を全体幅10文字、小数点以下5桁で表示")
    print("  {0:+.5f} - 0番目の引数を符号付きで表示")
    print("  {0:.2%} - 0番目の引数をパーセント表示（小数点以下2桁）")

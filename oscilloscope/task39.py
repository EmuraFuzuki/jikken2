# 課題39: 超音波距離センサで距離測定と精度確認
def main1():
    print("=== 課題39: 超音波距離センサの距離測定と精度確認 ===")

    try:
        from gpiozero import DistanceSensor
        from time import sleep
        import matplotlib.pyplot as plt

        # HC-SR04距離センサー（Echo=24, Trigger=23）
        sensor = DistanceSensor(echo=24, trigger=23)

        print("超音波距離センサの測定精度を確認します")
        print(
            "センサーの前に障害物を置いて、実際の距離とセンサー読み取り値を比較します"
        )
        print()

        # 測定データを保存するリスト
        actual_distances = []
        measured_distances = []

        print("複数の距離で測定を行います。各測定点でEnterキーを押してください。")
        print("測定を終了するには 'q' を入力してください。")

        measurement_count = 0

        while True:
            try:
                user_input = input(
                    f"\n測定 {measurement_count + 1}: 実際の距離をcmで入力してください（終了: q）: "
                )

                if user_input.lower() == "q":
                    break

                actual_distance = float(user_input)

                # 5回測定して平均を取る（ノイズ軽減）
                measurements = []
                print("測定中...", end="")
                for i in range(5):
                    distance = sensor.distance * 1000  # mm
                    measurements.append(distance)
                    print(".", end="", flush=True)
                    sleep(0.1)

                measured_distance = sum(measurements) / len(measurements)
                error = measured_distance - (actual_distance * 10)  # cmをmmに変換
                error_percent = (
                    (error / (actual_distance * 10)) * 100 if actual_distance > 0 else 0
                )

                print(f"\n実際の距離: {actual_distance:.1f} cm")
                print(
                    f"測定距離: {measured_distance:.1f} mm ({measured_distance / 10:.1f} cm)"
                )
                print(f"誤差: {error:.1f} mm ({error_percent:+.1f}%)")

                actual_distances.append(actual_distance)
                measured_distances.append(measured_distance / 10)  # cmに変換
                measurement_count += 1

            except ValueError:
                print("数値を入力してください")
            except KeyboardInterrupt:
                print("\n測定を中断しました")
                break

        if len(actual_distances) >= 2:
            # 結果の解析とグラフ表示
            print("\n=== 測定結果の解析 ===")
            print(f"測定回数: {len(actual_distances)}")

            # 線形性の確認
            errors = [
                measured - actual
                for actual, measured in zip(actual_distances, measured_distances)
            ]
            mean_error = sum(errors) / len(errors)
            max_error = max(errors)
            min_error = min(errors)

            print(f"平均誤差: {mean_error:.2f} cm")
            print(f"最大誤差: {max_error:.2f} cm")
            print(f"最小誤差: {min_error:.2f} cm")
            print(
                f"誤差の標準偏差: {(sum([(e - mean_error) ** 2 for e in errors]) / len(errors)) ** 0.5:.2f} cm"
            )

            # 測定範囲の確認
            min_distance = min(actual_distances)
            max_distance = max(actual_distances)
            print(f"測定範囲: {min_distance:.1f} - {max_distance:.1f} cm")

            # グラフ描画
            plt.figure(figsize=(10, 8))

            # 実際の距離 vs 測定距離
            plt.subplot(2, 1, 1)
            plt.scatter(actual_distances, measured_distances, color="blue", alpha=0.7)
            plt.plot(
                [min_distance, max_distance],
                [min_distance, max_distance],
                "r--",
                label="理想線（y=x）",
            )
            plt.xlabel("実際の距離 [cm]")
            plt.ylabel("測定距離 [cm]")
            plt.title("距離センサーの精度確認")
            plt.legend()
            plt.grid(True)

            # 誤差プロット
            plt.subplot(2, 1, 2)
            plt.scatter(actual_distances, errors, color="red", alpha=0.7)
            plt.axhline(y=0, color="black", linestyle="-", alpha=0.3)
            plt.axhline(
                y=mean_error,
                color="blue",
                linestyle="--",
                label=f"平均誤差: {mean_error:.2f} cm",
            )
            plt.xlabel("実際の距離 [cm]")
            plt.ylabel("誤差 [cm]")
            plt.title("測定誤差")
            plt.legend()
            plt.grid(True)

            plt.tight_layout()
            plt.show()

            print("\n=== センサーの特性 ===")
            if mean_error < 0.5:
                print("✓ 高精度: 平均誤差が0.5cm未満")
            elif mean_error < 1.0:
                print("○ 中精度: 平均誤差が1.0cm未満")
            else:
                print("△ 低精度: 平均誤差が1.0cm以上")

            print(f"推奨測定範囲: {min_distance:.0f} - {max_distance:.0f} cm")

        else:
            print("測定データが不足しています（最低2点必要）")

    except ImportError as e:
        print(f"必要なライブラリがインストールされていません: {e}")
        print("以下のコマンドでインストールしてください:")
        print("pip install gpiozero matplotlib")

    except Exception as e:
        print(f"エラーが発生しました: {e}")
        print("センサーの接続を確認してください:")
        print("- Vcc: 3.3V または 5V")
        print("- Trig: GPIO 23")
        print("- Echo: GPIO 24")
        print("- Gnd: GND")

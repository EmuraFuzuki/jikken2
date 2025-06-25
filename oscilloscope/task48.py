# 課題48: 衝突安全装置の作成
def main1():
    print("=== 課題48: 衝突安全装置の作成 ===")
    print("近代的な自動車の衝突回避システムを模擬した装置を作成します")

    try:
        from gpiozero import DistanceSensor, LED, Buzzer, Button
        import time
        import threading

        # ハードウェア設定
        sensor = DistanceSensor(echo=24, trigger=23)
        warning_led = LED(18)  # 警告LED
        danger_led = LED(19)  # 危険LED
        buzzer = Buzzer(20)  # ブザー
        reset_button = Button(21)  # リセットボタン

        print("=== ハードウェア構成 ===")
        print("- 超音波距離センサー: GPIO23(Trig), GPIO24(Echo)")
        print("- 警告LED: GPIO18")
        print("- 危険LED: GPIO19")
        print("- ブザー: GPIO20")
        print("- リセットボタン: GPIO21")
        print()

        # システム設定
        WARNING_DISTANCE = 50.0  # 警告距離 (cm)
        DANGER_DISTANCE = 20.0  # 危険距離 (cm)
        CRITICAL_DISTANCE = 10.0  # 緊急距離 (cm)

        # システム状態
        system_active = True
        alert_active = False
        measurement_count = 0
        distance_history = []

        def get_stable_distance(samples=5):
            """安定した距離測定（複数回測定の中央値）"""
            distances = []
            for _ in range(samples):
                try:
                    distance = sensor.distance * 100  # cm
                    if 2 <= distance <= 400:  # 有効範囲内
                        distances.append(distance)
                    time.sleep(0.02)  # 20ms間隔
                except Exception:
                    pass

            if distances:
                distances.sort()
                # 中央値を返す（外れ値に強い）
                mid = len(distances) // 2
                if len(distances) % 2 == 0:
                    return (distances[mid - 1] + distances[mid]) / 2
                else:
                    return distances[mid]
            else:
                return None

        def warning_sound_pattern():
            """警告音のパターン"""
            if not system_active:
                return

            buzzer.on()
            time.sleep(0.1)
            buzzer.off()
            time.sleep(0.4)

        def danger_sound_pattern():
            """危険音のパターン"""
            if not system_active:
                return

            for _ in range(3):
                if not system_active:
                    break
                buzzer.on()
                time.sleep(0.1)
                buzzer.off()
                time.sleep(0.1)
            time.sleep(0.3)

        def critical_sound_pattern():
            """緊急音のパターン（連続音）"""
            if system_active and alert_active:
                buzzer.on()
            else:
                buzzer.off()

        def reset_system():
            """システムリセット"""
            nonlocal alert_active, distance_history, measurement_count
            alert_active = False
            distance_history.clear()
            measurement_count = 0

            # 全デバイスをOFF
            warning_led.off()
            danger_led.off()
            buzzer.off()

            print("システムをリセットしました")
            time.sleep(1)

        # リセットボタンのイベント設定
        reset_button.when_pressed = reset_system

        def collision_warning_system():
            """衝突警告システムのメイン処理"""
            nonlocal alert_active, measurement_count, distance_history

            while system_active:
                distance = get_stable_distance()
                measurement_count += 1

                if distance is not None:
                    distance_history.append(distance)

                    # 履歴の管理（最新10回分のみ保持）
                    if len(distance_history) > 10:
                        distance_history.pop(0)

                    # 距離に応じた警告レベルの判定
                    if distance <= CRITICAL_DISTANCE:
                        # 緊急レベル
                        alert_active = True
                        warning_led.off()
                        danger_led.on()
                        critical_sound_pattern()
                        print(
                            f"🚨 緊急警告! 距離: {distance:.1f}cm - 即座に停止してください!"
                        )

                    elif distance <= DANGER_DISTANCE:
                        # 危険レベル
                        alert_active = True
                        warning_led.off()
                        danger_led.on()
                        buzzer.off()
                        threading.Thread(
                            target=danger_sound_pattern, daemon=True
                        ).start()
                        print(
                            f"⚠️  危険! 距離: {distance:.1f}cm - 速度を落としてください"
                        )

                    elif distance <= WARNING_DISTANCE:
                        # 警告レベル
                        alert_active = True
                        warning_led.on()
                        danger_led.off()
                        buzzer.off()
                        threading.Thread(
                            target=warning_sound_pattern, daemon=True
                        ).start()
                        print(f"⚠️  注意! 距離: {distance:.1f}cm - 障害物接近中")

                    else:
                        # 安全レベル
                        if alert_active:
                            print(f"✅ 安全距離: {distance:.1f}cm")
                        alert_active = False
                        warning_led.off()
                        danger_led.off()
                        buzzer.off()

                    # 詳細情報の表示（10回ごと）
                    if measurement_count % 10 == 0:
                        if len(distance_history) > 1:
                            trend = (
                                "接近中"
                                if distance_history[-1] < distance_history[-2]
                                else "離れ中"
                            )
                            avg_distance = sum(distance_history) / len(distance_history)
                            print(
                                f"統計 - 測定回数: {measurement_count}, "
                                f"平均距離: {avg_distance:.1f}cm, 傾向: {trend}"
                            )

                else:
                    # 測定失敗
                    if measurement_count % 20 == 0:  # エラーを頻繁に表示しない
                        print("⚠️  距離測定エラー - センサーを確認してください")

                time.sleep(0.1)  # 100ms間隔で測定

        print("=== 衝突安全装置設定 ===")
        print(f"警告距離: {WARNING_DISTANCE}cm")
        print(f"危険距離: {DANGER_DISTANCE}cm")
        print(f"緊急距離: {CRITICAL_DISTANCE}cm")
        print()
        print("=== 警告レベル ===")
        print("✅ 安全: 全てOFF")
        print("⚠️  警告: 黄色LED点灯 + 断続的ビープ音")
        print("🔴 危険: 赤色LED点灯 + 早い断続音")
        print("🚨 緊急: 赤色LED点灯 + 連続音")
        print()
        print("リセットボタン: GPIO21で警告をリセット")
        print("終了: Ctrl+C")
        print()

        input("システムを開始するにはEnterキーを押してください...")

        print("🚗 衝突安全装置を開始しました")
        print("障害物を近づけたり遠ざけたりして動作を確認してください")
        print()

        try:
            # メインシステム開始
            collision_warning_system()

        except KeyboardInterrupt:
            print("\n🛑 システムを停止しています...")
            system_active = False

            # 全デバイスをOFF
            warning_led.off()
            danger_led.off()
            buzzer.off()

            print("✅ システムを安全に停止しました")
            # 統計情報の表示
            if distance_history:
                print("\n=== 運用統計 ===")
                print(f"総測定回数: {measurement_count}")
                print(
                    f"平均距離: {sum(distance_history) / len(distance_history):.1f}cm"
                )
                print(f"最小距離: {min(distance_history):.1f}cm")
                print(f"最大距離: {max(distance_history):.1f}cm")

                # 警告レベル別の統計
                warning_count = sum(
                    1 for d in distance_history if d <= WARNING_DISTANCE
                )
                danger_count = sum(1 for d in distance_history if d <= DANGER_DISTANCE)
                critical_count = sum(
                    1 for d in distance_history if d <= CRITICAL_DISTANCE
                )

                print("警告レベル発生回数:")
                print(
                    f"  注意: {warning_count}回 ({warning_count / len(distance_history) * 100:.1f}%)"
                )
                print(
                    f"  危険: {danger_count}回 ({danger_count / len(distance_history) * 100:.1f}%)"
                )
                print(
                    f"  緊急: {critical_count}回 ({critical_count / len(distance_history) * 100:.1f}%)"
                )

        print("\n=== 発展課題のアイデア ===")
        print("1. 多段階警告システム:")
        print("   - 段階的な警告音の変更")
        print("   - LED色の変化（RGB LED使用）")
        print("   - 警告強度の調整")
        print()
        print("2. スマート機能:")
        print("   - 接近速度の計算")
        print("   - 衝突時間の予測")
        print("   - 自動ブレーキシミュレーション")
        print()
        print("3. データロギング:")
        print("   - 距離データの記録")
        print("   - 警告発生ログ")
        print("   - グラフ表示機能")
        print()
        print("4. 通信機能:")
        print("   - スマートフォンアプリとの連携")
        print("   - 警告のリモート通知")
        print("   - 設定の遠隔変更")
        print()
        print("5. AI機能:")
        print("   - 障害物の種類判定")
        print("   - 学習による警告精度向上")
        print("   - 予測的警告システム")

    except ImportError:
        print("gpiozeroライブラリがインストールされていません")
        print("pip install gpiozero")

    except Exception as e:
        print(f"エラーが発生しました: {e}")
        print("ハードウェアの接続を確認してください:")
        print("- 超音波センサー (Trig: GPIO23, Echo: GPIO24)")
        print("- 警告LED (GPIO18)")
        print("- 危険LED (GPIO19)")
        print("- ブザー (GPIO20)")
        print("- リセットボタン (GPIO21)")


# 発展課題: データロギング機能付きバージョン
def advanced_collision_system():
    """データロギング機能付きの高度な衝突安全装置"""
    print("=== 高度な衝突安全装置（データロギング付き）===")

    try:
        # from gpiozero import DistanceSensor, LED, Buzzer, Button
        # import time  # 実装時に使用
        import datetime
        import csv
        import os

        # ハードウェア設定（実装時にコメントアウトを解除）
        # sensor = DistanceSensor(echo=24, trigger=23)
        # warning_led = LED(18)
        # danger_led = LED(19)
        # buzzer = Buzzer(20)
        # reset_button = Button(21)

        # データロギング設定
        data_dir = "../data"
        if not os.path.exists(data_dir):
            os.makedirs(data_dir)

        log_filename = f"{data_dir}/collision_system_log_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"

        # CSVファイルの初期化
        with open(log_filename, "w", newline="") as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(
                ["timestamp", "distance_cm", "warning_level", "alert_active"]
            )

        print(f"データログファイル: {log_filename}")
        print("このバージョンでは全ての測定データが記録されます")
        print("完全な実装を行う場合は、コメントアウトされた部分を有効にしてください")

        # ここに高度なシステムのコードを実装
        # （完全な実装例はmain1()を参考にしてください）

    except Exception as e:
        print(f"高度なシステムでエラーが発生しました: {e}")


if __name__ == "__main__":
    # 通常バージョンを実行
    main1()

    # 高度なバージョンの実行を希望する場合
    # advanced_collision_system()

# 課題45: sleep()関数による待機時間の測定
def main1():
    print("=== 課題45: sleep()関数による待機時間の測定 ===")

    import time

    print("time.perf_counter()を使用して、sleep()関数の精度を測定します")
    print()

    # 様々な待機時間でテスト
    test_durations = [0.001, 0.01, 0.1, 1.0]  # 1ms, 10ms, 100ms, 1s

    for target_duration in test_durations:
        print(f"=== 目標待機時間: {target_duration * 1000:.1f}ms ===")

        measurements = []

        for i in range(10):  # 10回測定
            time1 = time.perf_counter()
            time.sleep(target_duration)
            time2 = time.perf_counter()

            actual_duration = time2 - time1
            measurements.append(actual_duration)
            error = actual_duration - target_duration
            error_percent = (error / target_duration) * 100

            print(
                f"測定{i + 1:2d}: 実測値={actual_duration * 1000:7.3f}ms, "
                f"誤差={error * 1000:+6.3f}ms ({error_percent:+5.1f}%)"
            )

        # 統計計算
        avg_duration = sum(measurements) / len(measurements)
        min_duration = min(measurements)
        max_duration = max(measurements)

        # 標準偏差計算
        variance = sum([(m - avg_duration) ** 2 for m in measurements]) / len(
            measurements
        )
        std_dev = variance**0.5

        avg_error = avg_duration - target_duration
        avg_error_percent = (avg_error / target_duration) * 100

        print(
            f"平均値: {avg_duration * 1000:.3f}ms (誤差: {avg_error * 1000:+.3f}ms, {avg_error_percent:+.1f}%)"
        )
        print(f"最小値: {min_duration * 1000:.3f}ms")
        print(f"最大値: {max_duration * 1000:.3f}ms")
        print(f"標準偏差: {std_dev * 1000:.3f}ms")
        print(f"変動幅: {(max_duration - min_duration) * 1000:.3f}ms")
        print()

    print("=== 非常に短い時間での測定 ===")
    print("マイクロ秒オーダーでの測定精度を確認")

    microsecond_tests = [1e-6, 10e-6, 100e-6, 1000e-6]  # 1μs, 10μs, 100μs, 1000μs

    for target_duration in microsecond_tests:
        print(f"\n目標待機時間: {target_duration * 1e6:.0f}μs")

        measurements = []

        for i in range(5):  # 5回測定（短時間なので回数を減らす）
            time1 = time.perf_counter()
            time.sleep(target_duration)
            time2 = time.perf_counter()

            actual_duration = time2 - time1
            measurements.append(actual_duration)
            error = actual_duration - target_duration

            print(
                f"測定{i + 1}: 実測値={actual_duration * 1e6:8.1f}μs, "
                f"誤差={error * 1e6:+8.1f}μs"
            )

        avg_duration = sum(measurements) / len(measurements)
        avg_error = avg_duration - target_duration

        print(f"平均誤差: {avg_error * 1e6:+.1f}μs")

        if abs(avg_error) > target_duration:
            print("⚠️  誤差が目標時間を超えています")
        elif abs(avg_error) > target_duration * 0.1:
            print("⚠️  誤差が10%を超えています")
        else:
            print("✓ 精度良好")

    print("\n=== 連続測定による精度確認 ===")
    print("連続して時間測定を行い、システムの安定性を確認")

    target = 0.01  # 10ms
    consecutive_measurements = []
    print("10msの待機を50回連続で実行...")
    start_time = time.perf_counter()

    for i in range(50):
        before = time.perf_counter()
        time.sleep(target)
        after = time.perf_counter()
        duration = after - before
        consecutive_measurements.append(duration)

        if i % 10 == 9:  # 10回ごとに表示
            print(f"  {i + 1:2d}回目: {duration * 1000:.3f}ms")

    total_time = time.perf_counter() - start_time
    expected_total = target * 50

    print("\n連続測定結果:")
    print(f"総実行時間: {total_time:.3f}s")
    print(f"期待時間: {expected_total:.3f}s")
    print(f"総誤差: {(total_time - expected_total) * 1000:+.1f}ms")

    # 各測定の統計
    avg_individual = sum(consecutive_measurements) / len(consecutive_measurements)
    min_individual = min(consecutive_measurements)
    max_individual = max(consecutive_measurements)

    print(f"個別測定の平均: {avg_individual * 1000:.3f}ms")
    print(f"個別測定の最小: {min_individual * 1000:.3f}ms")
    print(f"個別測定の最大: {max_individual * 1000:.3f}ms")
    print(f"個別測定の変動: {(max_individual - min_individual) * 1000:.3f}ms")

    print("\n=== 結論 ===")
    print("1. time.sleep()の精度:")
    print("   - ミリ秒オーダー: 比較的高精度")
    print("   - マイクロ秒オーダー: 精度に限界あり")
    print("   - OSのスケジューラーに依存")
    print()
    print("2. 時間測定のベストプラクティス:")
    print("   - time.perf_counter()の使用")
    print("   - 複数回測定して平均化")
    print("   - システム負荷の影響を考慮")
    print()
    print("3. 高精度タイミングが必要な場合:")
    print("   - ハードウェアタイマーの使用を検討")
    print("   - リアルタイムOSの使用")
    print("   - 専用マイコンの使用")

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
手ぶくろ入力装置のテストスクリプト
Raspberry Pi以外の環境でも動作確認可能
"""

import time
import sys
import os

# 相対パスでモジュールをインポート
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

try:
    from main import GloveInputDevice

    # Raspberry Pi環境でない場合の簡単なテスト
    if os.name != "posix":
        print("Windows環境での実行を検出しました")

    print("=== 手ぶくろ入力装置テスト ===")
    print("テストを開始します...")

    # デバイスの初期化テスト
    device = GloveInputDevice()
    print("デバイスの初期化が完了しました")

    # 短時間のテスト実行
    print("5秒間のテスト実行を開始します...")
    start_time = time.time()
    test_duration = 5.0

    try:
        while time.time() - start_time < test_duration:
            # 模擬的なセンサーデータでテスト
            remaining_time = test_duration - (time.time() - start_time)
            print(f"テスト実行中... 残り時間: {remaining_time:.1f}秒")
            time.sleep(1.0)
    except KeyboardInterrupt:
        print("\nテストが中断されました")
    finally:
        device.cleanup()
        print("テストが完了しました")

except ImportError as e:
    print(f"モジュールのインポートに失敗しました: {e}")
    print("必要なモジュールがインストールされていない可能性があります")
except Exception as e:
    print(f"エラーが発生しました: {e}")
    print("詳細なエラー情報:")
    import traceback

    traceback.print_exc()

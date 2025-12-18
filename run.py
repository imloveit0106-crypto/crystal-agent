#!/usr/bin/env python3
"""
Crystal Agent - 開発環境起動スクリプト
ワンコマンドでバックエンド + フロントエンドを起動
"""

import subprocess
import webbrowser
import time
import os
import sys
import signal
from pathlib import Path

# グローバル変数でプロセスを保持
uvicorn_process = None

def signal_handler(sig, frame):
    """Ctrl+C でプロセスを終了"""
    print("\n\n🛑 シャットダウン中...")
    cleanup()
    sys.exit(0)

def cleanup():
    """uvicornプロセスを確実に終了"""
    global uvicorn_process
    if uvicorn_process:
        print("🔴 バックエンドサーバーを停止中...")
        uvicorn_process.terminate()
        try:
            uvicorn_process.wait(timeout=5)
        except subprocess.TimeoutExpired:
            print("⚠️  強制終了中...")
            uvicorn_process.kill()
        print("✅ バックエンドサーバーを停止しました")

def check_requirements():
    """必要なファイルと依存関係をチェック"""
    # バックエンドファイルの存在確認
    backend_file = Path("backend/main.py")
    if not backend_file.exists():
        print("❌ エラー: backend/main.py が見つかりません")
        sys.exit(1)

    # フロントエンドファイルの存在確認
    frontend_file = Path("frontend/index.html")
    if not frontend_file.exists():
        print("❌ エラー: frontend/index.html が見つかりません")
        sys.exit(1)

    # .envファイルの確認
    env_file = Path(".env")
    if not env_file.exists():
        print("⚠️  警告: .env ファイルが見つかりません")
        print("   .env.example をコピーして .env を作成し、APIキーを設定してください")
        response = input("   続行しますか？ (y/N): ")
        if response.lower() != 'y':
            sys.exit(1)

    print("✅ ファイルチェック完了")

def start_backend():
    """バックエンドサーバーを起動"""
    global uvicorn_process

    print("🚀 バックエンドサーバーを起動中...")
    print("   ポート: 8000")
    print("   URL: http://localhost:8000")

    try:
        # uvicornをサブプロセスとして起動
        uvicorn_process = subprocess.Popen(
            ["python", "-m", "uvicorn", "backend.main:app", "--reload", "--port", "8000"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )

        # サーバーの起動を待機
        print("   サーバー起動を待機中", end="")
        for _ in range(6):
            time.sleep(0.5)
            print(".", end="", flush=True)
        print(" 完了！")

        # プロセスが正常に起動したかチェック
        if uvicorn_process.poll() is not None:
            print("\n❌ エラー: バックエンドサーバーの起動に失敗しました")
            print("\nエラー出力:")
            _, stderr = uvicorn_process.communicate()
            print(stderr)
            sys.exit(1)

        print("✅ バックエンドサーバー起動完了")
        return True

    except FileNotFoundError:
        print("\n❌ エラー: uvicorn がインストールされていません")
        print("   pip install -r requirements.txt を実行してください")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ エラー: {e}")
        sys.exit(1)

def open_frontend():
    """フロントエンドをブラウザで開く"""
    print("\n🌐 フロントエンドを開いています...")

    # frontend/index.html の絶対パスを取得
    frontend_path = Path("frontend/index.html").resolve()

    # file:// プロトコルでURLを構築
    frontend_url = f"file://{frontend_path}"

    print(f"   URL: {frontend_url}")

    # デフォルトブラウザで開く
    webbrowser.open(frontend_url)

    print("✅ ブラウザを開きました")

def print_instructions():
    """使い方を表示"""
    print("\n" + "="*60)
    print("📝 開発サーバー起動中")
    print("="*60)
    print("\n📍 アクセス方法:")
    print("   - Backend API:  http://localhost:8000")
    print("   - API Docs:     http://localhost:8000/docs")
    print("   - Frontend:     ブラウザで自動的に開きます")
    print("\n⚙️  操作:")
    print("   - サーバーログを見るには、このターミナルを確認")
    print("   - 停止するには、Ctrl+C を押してください")
    print("\n🔄 ホットリロード:")
    print("   - backend/main.py を編集すると自動的に再起動")
    print("   - frontend/index.html を編集したらブラウザをリロード")
    print("\n" + "="*60 + "\n")

def main():
    """メイン処理"""
    # Ctrl+C のハンドラーを設定
    signal.signal(signal.SIGINT, signal_handler)

    print("\n🔮 Crystal Agent - 開発環境起動スクリプト\n")

    try:
        # 必要なファイルをチェック
        check_requirements()

        # バックエンドサーバーを起動
        start_backend()

        # フロントエンドを開く
        open_frontend()

        # 使い方を表示
        print_instructions()

        # サーバーを起動したまま待機
        print("🟢 サーバー稼働中... (Ctrl+C で停止)\n")

        # 無限ループでサーバーを維持
        while True:
            time.sleep(1)

            # プロセスが異常終了していないかチェック
            if uvicorn_process and uvicorn_process.poll() is not None:
                print("\n❌ エラー: バックエンドサーバーが予期せず終了しました")
                _, stderr = uvicorn_process.communicate()
                if stderr:
                    print("\nエラー出力:")
                    print(stderr)
                cleanup()
                sys.exit(1)

    except KeyboardInterrupt:
        # Ctrl+C が押された場合
        signal_handler(None, None)

    except Exception as e:
        print(f"\n❌ 予期しないエラー: {e}")
        cleanup()
        sys.exit(1)

    finally:
        # 必ずクリーンアップを実行
        cleanup()

if __name__ == "__main__":
    main()

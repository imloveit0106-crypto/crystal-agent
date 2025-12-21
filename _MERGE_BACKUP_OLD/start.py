#!/usr/bin/env python3
"""
Crystal Agent - 自動起動スクリプト（Windows/Linux/Mac対応）
このファイルを実行するだけでサーバーが起動します
"""

import sys
import subprocess
import os
from pathlib import Path

# 色付きログ出力（Windows対応）
try:
    import colorama
    colorama.init()
    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    RESET = '\033[0m'
except ImportError:
    RED = GREEN = YELLOW = BLUE = RESET = ''


def print_header():
    """起動時のヘッダー表示"""
    print(f"""
{BLUE}╔═══════════════════════════════════════════════════════════════════╗
║           Crystal Agent - 自動起動スクリプト                       ║
║           Windows/Linux/Mac 対応                                  ║
╚═══════════════════════════════════════════════════════════════════╝{RESET}
""")


def check_python_version():
    """Pythonバージョンチェック"""
    print(f"{YELLOW}[1/4] Pythonバージョン確認中...{RESET}")
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print(f"{RED}❌ Python 3.8以上が必要です。現在: {sys.version}{RESET}")
        sys.exit(1)
    print(f"{GREEN}✅ Python {version.major}.{version.minor}.{version.micro} - OK{RESET}")


def check_and_install_packages():
    """必要なパッケージの確認とインストール"""
    print(f"\n{YELLOW}[2/4] 必要なライブラリをチェック中...{RESET}")

    required_packages = [
        'fastapi',
        'uvicorn',
        'python-dotenv',
        'google-generativeai',
        'notion-client',
        'pydantic'
    ]

    missing_packages = []

    for package in required_packages:
        try:
            # パッケージ名の変換（import名が異なる場合）
            import_name = package.replace('-', '_')
            if package == 'google-generativeai':
                import_name = 'google.generativeai'
            elif package == 'notion-client':
                import_name = 'notion_client'

            __import__(import_name)
            print(f"  ✓ {package}")
        except ImportError:
            missing_packages.append(package)
            print(f"  ✗ {package} - インストールが必要")

    if missing_packages:
        print(f"\n{YELLOW}📦 不足しているパッケージをインストール中...{RESET}")
        for package in missing_packages:
            print(f"  installing {package}...")
            try:
                subprocess.check_call([
                    sys.executable, '-m', 'pip', 'install', package, '--quiet'
                ])
                print(f"{GREEN}  ✅ {package} インストール完了{RESET}")
            except subprocess.CalledProcessError as e:
                print(f"{RED}  ❌ {package} のインストールに失敗しました: {e}{RESET}")
                sys.exit(1)
    else:
        print(f"{GREEN}✅ すべてのライブラリがインストール済みです{RESET}")


def check_env_file():
    """環境変数ファイルの確認"""
    print(f"\n{YELLOW}[3/4] 環境設定ファイル確認中...{RESET}")

    env_path = Path('.env')
    env_example_path = Path('.env.example')

    if not env_path.exists():
        print(f"{YELLOW}⚠️  .env ファイルが見つかりません{RESET}")
        if env_example_path.exists():
            print(f"{BLUE}ℹ️  .env.example を参考に .env ファイルを作成してください{RESET}")
        else:
            print(f"{BLUE}ℹ️  以下の環境変数を .env ファイルに設定してください:{RESET}")
            print("    GEMINI_API_KEY=your_key_here")
            print("    NOTION_API_KEY=your_notion_key")
            print("    NOTION_LIFE_LOG_DB_ID=your_db_id")
        print(f"\n{YELLOW}⚠️  環境変数が未設定の場合、一部機能が動作しない可能性があります{RESET}")
        print(f"{BLUE}続行しますか？ (y/n): {RESET}", end='')

        response = input().strip().lower()
        if response != 'y':
            print(f"{RED}起動をキャンセルしました{RESET}")
            sys.exit(0)
    else:
        print(f"{GREEN}✅ .env ファイルが見つかりました{RESET}")


def start_server():
    """FastAPIサーバーを起動"""
    print(f"\n{YELLOW}[4/4] サーバー起動中...{RESET}")
    print(f"{BLUE}{'='*67}{RESET}")
    print(f"{GREEN}🚀 Crystal Agent サーバーを起動します{RESET}")
    print(f"{BLUE}{'='*67}{RESET}\n")

    print(f"{GREEN}📍 アクセスURL: http://localhost:8000{RESET}")
    print(f"{BLUE}ℹ️  終了するには Ctrl+C を押してください{RESET}\n")
    print(f"{BLUE}{'='*67}{RESET}\n")

    try:
        # プラットフォームに関係なく動作するuvicorn起動コマンド
        subprocess.run([
            sys.executable, '-m', 'uvicorn',
            'backend.main:app',
            '--reload',
            '--host', '0.0.0.0',
            '--port', '8000'
        ], check=True)
    except KeyboardInterrupt:
        print(f"\n\n{YELLOW}👋 サーバーを停止しました{RESET}")
        print(f"{GREEN}お疲れ様でした！{RESET}\n")
    except subprocess.CalledProcessError as e:
        print(f"\n{RED}❌ サーバーの起動に失敗しました: {e}{RESET}")
        print(f"\n{YELLOW}トラブルシューティング:{RESET}")
        print(f"  1. ポート8000が既に使用されている可能性があります")
        print(f"  2. backend/main.py ファイルが存在するか確認してください")
        print(f"  3. Python環境が正しく設定されているか確認してください")
        sys.exit(1)
    except Exception as e:
        print(f"\n{RED}❌ 予期しないエラーが発生しました: {e}{RESET}")
        sys.exit(1)


def main():
    """メイン処理"""
    try:
        print_header()

        # スクリプトのディレクトリをカレントディレクトリに設定
        script_dir = Path(__file__).parent
        os.chdir(script_dir)

        # 各チェックと起動処理
        check_python_version()
        check_and_install_packages()
        check_env_file()
        start_server()

    except KeyboardInterrupt:
        print(f"\n\n{YELLOW}起動がキャンセルされました{RESET}")
        sys.exit(0)
    except Exception as e:
        print(f"\n{RED}❌ エラーが発生しました: {e}{RESET}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()

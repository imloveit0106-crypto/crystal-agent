@echo off
REM Crystal Agent - Windows起動スクリプト
REM ダブルクリックで実行可能

echo.
echo ========================================
echo    Crystal Agent - Starting...
echo ========================================
echo.

REM Pythonコマンドを自動検出
where python >nul 2>&1
if %ERRORLEVEL% EQU 0 (
    python start.py
) else (
    where py >nul 2>&1
    if %ERRORLEVEL% EQU 0 (
        py start.py
    ) else (
        echo [ERROR] Python が見つかりません
        echo Python 3.8以上をインストールしてください
        echo https://www.python.org/downloads/
        pause
        exit /b 1
    )
)

pause

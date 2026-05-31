@echo off
echo ================================================
echo  SHADDAI MUSIC ENGINE
echo  Motto: Everything works and is connected!
echo ================================================
echo.

cd /d "%~dp0"

echo [1] Loading API...
python -c "from flstudio_ai_api import FLStudioAI; api = FLStudioAI(); print('API Loaded!')" 2>nul

if errorlevel 1 (
    echo ERROR: Python not found or import failed
    pause
    exit /b 1
)

echo.
echo ================================================
echo  OPTIONS - Type a number and press Enter:
echo ================================================
echo  1 - Generate TRAP beat
echo  2 - Generate HOUSE beat
echo  3 - Play Synth note
echo  4 - Play Drums
echo  5 - Generate Full Song
echo  6 - List ALL Presets
echo  0 - Exit
echo ================================================
echo.

set /p choice="Enter choice: "

if "%choice%"=="1" (
    echo Generating TRAP beat...
    python -c "from flstudio_ai_api import FLStudioAI; api = FLStudioAI(); api.generate_beat('trap', 4); print('Done!')"
    echo Check the exports/ folder!
    pause
    goto :menu
)

if "%choice%"=="2" (
    echo Generating HOUSE beat...
    python -c "from flstudio_ai_api import FLStudioAI; api = FLStudioAI(); api.generate_beat('house', 4); print('Done!')"
    echo Check the exports/ folder!
    pause
    goto :menu
)

if "%choice%"=="3" (
    echo Playing Synth...
    python -c "from flstudio_ai_api import FLStudioAI; api = FLStudioAI(); api.real_synth.load_preset('lead'); audio = api.real_synth.play(440, 1.0); print(f'Generated {len(audio)} samples!')"
    pause
    goto :menu
)

if "%choice%"=="4" (
    echo Playing Drums...
    python -c "from flstudio_ai_api import FLStudioAI; api = FLStudioAI(); kick = api.real_drums.play('kick'); print(f'Kick drum: {len(kick)} samples')"
    pause
    goto :menu
)

if "%choice%"=="5" (
    echo Generating Full Song...
    python -c "from flstudio_ai_api import FLStudioAI; api = FLStudioAI(); api.generate_full_track('house', True, True); print('Song created in audio/ folder!')"
    pause
    goto :menu
)

if "%choice%"=="6" (
    echo.
    echo Available Presets:
    python -c "from flstudio_ai_api import FLStudioAI; api = FLStudioAI(); print('Extensive Synth: ' + ', '.join(list(api.extensive_synth.presets.keys())[:20])); print('Total: ' + str(len(api.extensive_synth.presets)))"
    pause
    goto :menu
)

if "%choice%"=="0" (
    echo Goodbye!
    pause
    exit /b 0
)

goto :menu

:menu
echo.
goto :eof
@echo off
chcp 65001 >nul
title FL Studio AI - Master Build
color 0a
cls

echo.
echo ################################################################
echo #                                                              #
echo #          FL STUDIO AI - MASTER BUILD v6.0                   #
echo #          For Everyone: Kids to Seniors, Newbie to Pro     #
echo #                                                              #
echo ################################################################
echo.

echo [1] One-Click Beat (Beginners)
echo [2] Wizard Mode (Step-by-Step Help)
echo [3] Magic Beat (Surprise Me!)
echo [4] Relaxing/Chill
echo [5] Energetic/Hype
echo [6] Focus/Study
echo [7] Party Mode
echo.
echo --- STYLE SELECTION ---
echo [8] Trap
echo [9] House
echo [10] Hip Hop
echo [11] Lo-Fi
echo [12] Dubstep
echo [13] Drum ^& Bass
echo [14] EDM
echo.
echo --- ADVANCED ---
echo [15] Custom Beat Builder
echo [16] View All Presets
echo [17] Start Web Interface
echo [0] Exit
echo.

set /p choice="Enter your choice (0-17): "

if "%choice%"=="1" goto oneclick
if "%choice%"=="2" goto wizard
if "%choice%"=="3" goto magic
if "%choice%"=="4" goto relax
if "%choice%"=="5" goto energy
if "%choice%"=="6" goto focus
if "%choice%"=="7" goto party
if "%choice%"=="8" goto trap
if "%choice%"=="9" goto house
if "%choice%"=="10" goto hiphop
if "%choice%"=="11" goto lofi
if "%choice%"=="12" goto dubstep
if "%choice%"=="13" goto dnb
if "%choice%"=="14" goto edm
if "%choice%"=="15" goto custom
if "%choice%"=="16" goto presets
if "%choice%"=="17" goto web
if "%choice%"=="0" exit

:oneclick
python "%~dp0flstudio_ai_master.py" oneclick
goto end

:wizard
python "%~dp0flstudio_ai_master.py" wizard
goto end

:magic
python "%~dp0flstudio_ai_master.py" magic
goto end

:relax
python "%~dp0flstudio_ai_master.py" relax
goto end

:energy
python "%~dp0flstudio_ai_master.py" energy
goto end

:focus
python "%~dp0flstudio_ai_master.py" focus
goto end

:party
python "%~dp0flstudio_ai_master.py" party
goto end

:trap
python "%~dp0flstudio_ai_master.py" trap
goto end

:house
python "%~dp0flstudio_ai_master.py" house
goto end

:hiphop
python "%~dp0flstudio_ai_master.py" hiphop
goto end

:lofi
python "%~dp0flstudio_ai_master.py" lofi
goto end

:dubstep
python "%~dp0flstudio_ai_master.py" dubstep
goto end

:dnb
python "%~dp0flstudio_ai_master.py" dnb
goto end

:edm
python "%~dp0flstudio_ai_master.py" edm
goto end

:custom
python "%~dp0flstudio_ai_master.py"
goto end

:presets
python "%~dp0flstudio_ai_master.py" presets
goto end

:web
start "" "%~dp0flstudio_ai_interface.html"
goto end

:end
echo.
echo ================================================================
echo.
echo Your beat is saved in the "audio" folder!
echo MIDI file is in the "exports" folder!
echo.
echo ================================================================
echo.
pause
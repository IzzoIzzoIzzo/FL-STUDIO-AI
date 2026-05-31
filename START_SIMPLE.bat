@echo off
chcp 65001 >nul
title FL Studio AI - Simple Mode
color 0a
cls

echo.
echo ################################################################
echo #                                                              #
echo #          FL STUDIO AI - ONE CLICK BEAT MAKER                #
echo #          For Everyone: Kids to Seniors                       #
echo #                                                              #
echo ################################################################
echo.
echo Press any key to make a beat, or type a number...
echo.
echo [1] My First Beat (Easiest!)
echo [2] Surprise Me (Magic)
echo [3] Chill/Relax
echo [4] Energetic
echo [5] Study/Focus
echo [6] Party!
echo [7] Web Interface
echo [0] Exit
echo.

set /p choice="Make a beat now! "

if "%choice%"=="" goto default
if "%choice%"=="1" goto baby
if "%choice%"=="2" goto magic
if "%choice%"=="3" goto chill
if "%choice%"=="4" goto energy
if "%choice%"=="5" goto focus
if "%choice%"=="6" goto party
if "%choice%"=="7" start "" "%~dp0flstudio_ai_simple.html" & exit
if "%choice%"=="0" exit

:default
:baby
python "%~dp0flstudio_ai_master.py" baby_first_beat
goto done

:magic
python "%~dp0flstudio_ai_master.py" magic
goto done

:chill
python "%~dp0flstudio_ai_master.py" chill_vibes
goto done

:energy
python "%~dp0flstudio_ai_master.py" workout_energy
goto done

:focus
python "%~dp0flstudio_ai_master.py" study_focus
goto done

:party
python "%~dp0flstudio_ai_master.py" party_mode
goto done

:done
echo.
echo ================================================================
echo   Your beat is ready! Check the "audio" folder!
echo ================================================================
echo.
pause
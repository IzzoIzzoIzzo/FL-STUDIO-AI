@echo off
chcp 65001 >nul
title FL Studio AI - Super Engine v7.0
color 0a
cls

echo.
echo ################################################################
echo #                                                              #
echo #          FL STUDIO AI - SUPER ENGINE v7.0                   #
echo #          THE FUTURE OF MUSIC CREATION                        #
echo #                                                              #
echo ################################################################
echo.
echo INNOVATIONS AVAILABLE:
echo   [OK] AI Melody Composer - Never-heard-before melodies!
echo   [OK] Auto-Mixer - Professional mixing in seconds!
echo   [OK] Stem Exporter - Individual tracks for remixing!
echo   [OK] Beat Visualizer - See your music!
echo   [OK] Voice-to-Beat - Convert audio to beats!
echo   [OK] Style Transfer - Transform between genres!
echo.
echo ================================================================
echo

echo CHOOSE YOUR MODE:
echo.
echo [1] Quick Beat (One-click!)
echo [2] Full Track (Drums + Bass + Melody + Chords)
echo [3] AI Melody Only
echo [4] Stem Pack (Separate tracks)
echo [5] Auto-Mix (Club/Radio/LoFi)
echo [6] Beat Visualizer
echo [7] Web Interface
echo.
echo --- STYLE SELECTION ---
echo [T] Trap
echo [H] House
echo [HH] Hip Hop
echo [D] Dubstep
echo [DNB] Drum & Bass
echo [L] Lo-Fi
echo [E] EDM
echo.
echo [0] Exit
echo.

set /p choice="Enter choice: "

if "%choice%"=="1" goto quick
if "%choice%"=="2" goto full
if "%choice%"=="3" goto melody
if "%choice%"=="4" goto stems
if "%choice%"=="5" goto mix
if "%choice%"=="6" goto visualizer
if "%choice%"=="7" start "" "%~dp0flstudio_ai_simple.html" & exit

if /i "%choice%"=="T" goto trap
if /i "%choice%"=="H" goto house
if /i "%choice%"=="HH" goto hiphop
if /i "%choice%"=="D" goto dubstep
if /i "%choice%"=="DNB" goto dnb
if /i "%choice%"=="L" goto lofi
if /i "%choice%"=="E" goto edm

:trap
python "%~dp0super_engine.py" trap 4
goto done

:house
python "%~dp0super_engine.py" house 4
goto done

:hiphop
python "%~dp0super_engine.py" hiphop 4
goto done

:dubstep
python "%~dp0super_engine.py" dubstep 4
goto done

:dnb
python "%~dp0super_engine.py" dnb 4
goto done

:lofi
python "%~dp0super_engine.py" lofi 4
goto done

:edm
python "%~dp0super_engine.py" edm 4
goto done

:quick
python "%~dp0flstudio_ai_master.py" magic
goto done

:full
set /p style="Enter style (trap/house/hiphop/dubstep/dnb/lofi/edm): "
python "%~dp0super_engine.py" full %style%
goto done

:melody
python "%~dp0super_engine.py" melody electronic dreamy
goto done

:stems
python "%~dp0super_engine.py" stems trap
goto done

:mix
python "%~dp0auto_mixer.py"
goto done

:visualizer
start "" "%~dp0beat_visualizer.html"
echo Visualizer opened in browser!
goto done

:done
echo.
echo ================================================================
echo   Check "audio" folder for WAV files!
echo   Check "exports" folder for MIDI files!
echo   Check "audio/stems" for stem packs!
echo ================================================================
echo.
pause
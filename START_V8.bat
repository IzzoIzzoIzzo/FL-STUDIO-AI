@echo off
chcp 65001 >nul
title FL Studio AI - Version 8.0 Ultimate
color 0a
cls

echo.
echo ################################################################
echo #                                                              #
echo #          FL STUDIO AI - VERSION 8.0 ULTIMATE                #
echo #          COMPLETE UNIFIED API SYSTEM                        #
echo #                                                              #
echo ################################################################
echo.
echo ALL SYSTEMS CONNECTED:
echo   [OK] Beat Generation - All styles
echo   [OK] Advanced Synthesizer - 8 presets
echo   [OK] Drum Machine - 5 kits, 16-step sequencer
echo   [OK] AI Melody - Never-heard-before melodies
echo   [OK] Auto-Mixer - Professional mixing
echo   [OK] Stem Exporter - Individual tracks
echo   [OK] Web API Server - REST endpoints
echo   [OK] MCP Protocol - Claude integration
echo.
echo ================================================================
echo

echo WHAT DO YOU WANT TO DO?
echo.
echo [1] Generate Beat (Quick)
echo [2] Generate Full Track (Drums + Bass + Melody)
echo [3] Synthesizer (Play notes/chords)
echo [4] Drum Machine (Pattern editor)
echo [5] AI Melody (Unique compositions)
echo [6] Auto-Mix (Master your track)
echo [7] Start Web API Server
echo [8] Open Web Visualizer
echo [9] List All Generated Files
echo [0] Exit
echo.

set /p choice="Enter choice: "

if "%choice%"=="1" goto beat
if "%choice%"=="2" goto track
if "%choice%"=="3" goto synth
if "%choice%"=="4" goto drums
if "%choice%"=="5" goto aimelody
if "%choice%"=="6" goto mix
if "%choice%"=="7" goto server
if "%choice%"=="8" goto visualizer
if "%choice%"=="9" goto listfiles
if "%choice%"=="0" exit

:beat
echo.
echo Select style: trap, house, hiphop, dubstep, dnb, lofi, edm
set /p style="Style (default trap): "
if "%style%"=="" set style=trap
python "%~dp0flstudio_ai_api.py" --quick-beat %style%
goto done

:track
set /p style="Style (default trap): "
if "%style%"=="" set style=trap
python "%~dp0flstudio_ai_api.py" --full-track %style%
goto done

:synth
echo.
echo --- SYNTHESIZER ---
echo 1. Play Note (440Hz)
echo 2. Play Chord (C Major)
echo 3. List Presets
set /p synth_choice="Choice: "
if "%synth_choice%"=="1" python "%~dp0flstudio_ai_api.py" --synth-note
if "%synth_choice%"=="2" python "%~dp0flstudio_ai_api.py" --synth-chord
if "%synth_choice%"=="3" python "%~dp0flstudio_ai_api.py" --synth-presets
goto done

:drums
echo.
echo --- DRUM MACHINE ---
echo Loading 808 kit with Trap pattern...
python "%~dp0flstudio_ai_api.py" --drums
goto done

:aimelody
echo.
echo --- AI MELODY ---
echo Generating unique melody...
python "%~dp0flstudio_ai_api.py" --ai-melody
goto done

:mix
echo.
echo --- AUTO-MIXER ---
echo Generating and mixing track...
python "%~dp0flstudio_ai_api.py" --mix
goto done

:server
echo.
echo Starting Web API Server on http://127.0.0.1:5000
echo Press Ctrl+C to stop server
echo.
python "%~dp0flstudio_ai_api.py" --server
goto done

:visualizer
start "" "%~dp0beat_visualizer.html"
echo Visualizer opened!
goto done

:listfiles
python "%~dp0flstudio_ai_api.py" --list-files
goto done

:done
echo.
echo ================================================================
echo   Files saved in: audio/ folder
echo   MIDI files in: exports/ folder
echo ================================================================
echo.
pause
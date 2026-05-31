@echo off
title FL Studio AI - Audio Track Generator
echo.
echo ================================================
echo   FL STUDIO AI - Full Audio Track Generator
echo ================================================
echo.
echo This generates complete audio tracks with:
echo   - Real synthesized drums (kick, snare, hihat)
echo   - Bass line
echo   - Melody
echo   - Chord progression
echo.
echo Choose a style:
echo   1. Trap (C minor, 140 BPM)
echo   2. House (E major, 128 BPM)
echo   3. Hip Hop (D minor, 90 BPM)
echo   4. Dubstep (A minor, 140 BPM)
echo   5. Lo-Fi (F major, 80 BPM)
echo.
set /p choice="Enter style (1-5): "

if "%choice%"=="1" goto trap
if "%choice%"=="2" goto house
if "%choice%"=="3" goto hiphop
if "%choice%"=="4" goto dubstep
if "%choice%"=="5" goto lofi
echo Invalid choice
pause
exit

:trap
echo 1 | python "%~dp0audio_track.py"
goto end

:house
echo 2 | python "%~dp0audio_track.py"
goto end

:hiphop
echo 3 | python "%~dp0audio_track.py"
goto end

:dubstep
echo 4 | python "%~dp0audio_track.py"
goto end

:lofi
echo 5 | python "%~dp0audio_track.py"
goto end

:end
echo.
echo Track saved to audio/ folder
echo.
pause
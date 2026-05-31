@echo off
chcp 65001 >nul
color 0A
title FL STUDIO AI - Quick Launch

:menu
cls
echo.
echo  ╔══════════════════════════════════════════════════════════╗
echo  ║           FL STUDIO AI - QUICK LAUNCH                     ║
echo  ╠══════════════════════════════════════════════════════════╣
echo  ║  TRACK GENERATION                                         ║
echo  ║  ─────────────────────────────────────────────────────────  ║
echo  ║  [1] Make Trap Beat (150 BPM)                              ║
echo  ║  [2] Make House Track (128 BPM)                            ║
echo  ║  [3] Make Hip Hop Beat (90 BPM)                            ║
echo  ║  [4] Make DnB Track (170 BPM)                              ║
echo  ║  [5] Make Dubstep (140 BPM)                                ║
echo  ║  [6] Make Lo-Fi Beat (80 BPM)                              ║
echo  ║  [7] Random Style                                          ║
echo  ╠══════════════════════════════════════════════════════════╣
echo  ║  AUDIO GENERATION                                          ║
echo  ║  ─────────────────────────────────────────────────────────  ║
echo  ║  [A] Binaural Beats (Relaxation)                          ║
echo  ║  [B] Chakra Frequency (Heart 639Hz)                      ║
echo  ║  [C] Solfeggio Tone (528Hz - DNA Repair)                  ║
echo  ║  [D] White Noise (Focus)                                  ║
echo  ║  [E] Meditation OM                                         ║
echo  ║  [F] Ambient Rain                                          ║
echo  ╠══════════════════════════════════════════════════════════╣
echo  ║  TOOLS                                                     ║
echo  ║  ─────────────────────────────────────────────────────────  ║
echo  ║  [W] Open Web Interface                                   ║
echo  ║  [M] Start MCP Server (for Claude Code)                   ║
echo  ║  [I] Show Info                                             ║
echo  ║  [Q] Quit                                                  ║
echo  ╚══════════════════════════════════════════════════════════╝
echo.

set /p choice="Select an option: "

if "%choice%"=="1" goto trap
if "%choice%"=="2" goto house
if "%choice%"=="3" goto hiphop
if "%choice%"=="4" goto dnb
if "%choice%"=="5" goto dubstep
if "%choice%"=="6" goto lofi
if "%choice%"=="7" goto random
if "%choice%"=="a" goto binaural
if "%choice%"=="A" goto binaural
if "%choice%"=="b" goto chakra
if "%choice%"=="B" goto chakra
if "%choice%"=="c" goto solfeggio
if "%choice%"=="C" goto solfeggio
if "%choice%"=="d" goto noise
if "%choice%"=="D" goto noise
if "%choice%"=="e" goto meditation
if "%choice%"=="E" goto meditation
if "%choice%"=="f" goto ambient
if "%choice%"=="F" goto ambient
if "%choice%"=="w" goto web
if "%choice%"=="W" goto web
if "%choice%"=="m" goto mcp
if "%choice%"=="M" goto mcp
if "%choice%"=="i" goto info
if "%choice%"=="I" goto info
if "%choice%"=="q" goto quit
if "%choice%"=="Q" goto quit
goto menu

:trap
python flstudio_ai.py make trap 150 16
echo.
echo Done! MIDI saved to exports folder.
pause
goto menu

:house
python flstudio_ai.py make house 128 16
echo.
echo Done!
pause
goto menu

:hiphop
python flstudio_ai.py make hiphop 90 16
echo.
echo Done!
pause
goto menu

:dnb
python flstudio_ai.py make dnb 170 16
echo.
echo Done!
pause
goto menu

:dubstep
python flstudio_ai.py make dubstep 140 16
echo.
echo Done!
pause
goto menu

:lofi
python flstudio_ai.py make lofi 80 16
echo.
echo Done!
pause
goto menu

:random
python flstudio_ai.py random
echo.
echo Done!
pause
goto menu

:binaural
python flstudio_ai.py binaural relax alpha 60
echo.
echo Done! Audio saved to audio/ folder.
pause
goto menu

:chakra
python flstudio_ai.py chakra heart 60
echo.
echo Done!
pause
goto menu

:solfeggio
python flstudio_ai.py solfeggio 528 60
echo.
echo Done!
pause
goto menu

:noise
python flstudio_ai.py noise white 60
echo.
echo Done!
pause
goto menu

:meditation
python flstudio_ai.py meditation om 60
echo.
echo Done!
pause
goto menu

:ambient
python flstudio_ai.py ambient rain 60
echo.
echo Done!
pause
goto menu

:web
start flstudio_ai_interface.html
echo Opening browser...
goto menu

:mcp
echo Starting MCP server on http://localhost:5000
echo Press Ctrl+C to stop the server
python flstudio_mcp_server_v2.py
pause
goto menu

:info
python flstudio_ai.py info
echo.
pause
goto menu

:quit
cls
echo Thanks for using FL STUDIO AI!
timeout /t 2 /nobreak >nul
exit
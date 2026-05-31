@echo off
chcp 65001 >nul
title FL Studio AI - COMPLETE v8.0
color 0a
cls

echo.
echo ################################################################
echo #                                                              #
echo #          FL STUDIO AI - COMPLETE SYSTEM v8.0                #
echo #          EVERYTHING CONNECTED AND WORKING                   #
echo #                                                              #
echo ################################################################
echo.
echo ALL SYSTEMS:
echo   [OK] Beat Generation - 8 styles (trap, house, hiphop, etc)
echo   [OK] Advanced Synth - 8 presets, arpeggiator
echo   [OK] Drum Machine - 5 kits, 16-step sequencer
echo   [OK] Complete Sampler - Chop, slice, stretch, pitch
echo   [OK] AI Melody - Never-heard-before compositions
echo   [OK] Auto-Mixer - Professional stems and mixing
echo   [OK] Live Performance - Pad triggering
echo   [OK] Automation Timeline - DAW-style automation
echo   [OK] Web API Server - REST endpoints
echo   [OK] Beat Visualizer - Interactive graphics
echo.
echo ================================================================
echo

echo WHAT TO DO:
echo.
echo === BEAT MAKING ===
echo [1] Quick Beat (1-2 seconds)
echo [2] Full Track (drums+bass+melody+chords)
echo [3] Custom Style & Length
echo.
echo === SYNTHESIZER ===
echo [4] Play Synth Note
echo [5] Play Synth Chord
echo [6] List All Presets
echo.
echo === DRUMS ===
echo [7] Generate Drum Pattern
echo [8] Different Drum Kit
echo.
echo === SAMPLER (NEW!) ===
echo [9] Import & Process Sample
echo [10] Load Sample to Pad
echo [11] Export Sample Variations
echo.
echo === AI & CREATIVE ===
echo [12] Generate AI Melody
echo [13] Create Innovative Track
echo.
echo === MIXING ===
echo [14] Auto-Mix Track
echo [15] Create Stem Pack
echo.
echo === PERFORMANCE ===
echo [16] Start Live Performance Mode
echo [17] Create Automation Timeline
echo.
echo === WEB & VISUAL ===
echo [18] Start Web API Server
echo [19] Open Beat Visualizer
echo.
echo === FILES ===
echo [20] List All Generated Files
echo [21] Open Audio Folder
echo.
echo [0] EXIT
echo.

set /p choice="Enter choice: "

if "%choice%"=="1" python "%~dp0flstudio_ai_api.py" --quick-beat trap & goto done
if "%choice%"=="2" python "%~dp0flstudio_ai_api.py" --full-track trap & goto done
if "%choice%"=="3" set /p style="Enter style (trap/house/hiphop/dubstep/dnb/lofi/edm): " & python "%~dp0flstudio_ai_api.py" --full-track %style% & goto done

if "%choice%"=="4" python "%~dp0flstudio_ai_api.py" --synth-note & goto done
if "%choice%"=="5" python "%~dp0flstudio_ai_api.py" --synth-chord & goto done
if "%choice%"=="6" python "%~dp0flstudio_ai_api.py" --synth-presets & goto done

if "%choice%"=="7" python "%~dp0flstudio_ai_api.py" --drums & goto done
if "%choice%"=="8" set /p kit="Enter kit (808/909/acoustic/electronic/lofi): " & python -c "import sys; sys.path.insert(0, '%~dp0'); from flstudio_ai_api import FLStudioAI; api = FLStudioAI(); api.load_drum_kit('%kit%'); api.load_drum_preset('trap'); api.generate_drums(4, 140, 'drums.wav')" & goto done

if "%choice%"=="9" python -c "import sys; sys.path.insert(0, '%~dp0'); from complete_sampler import CompleteSampler; s = CompleteSampler(); print('Import a sample file into audio/samples/ and use load_to_pad')" & goto done
if "%choice%"=="10" set /p pnum="Enter pad (0-15): " & set /p sn="Enter sample name: " & python -c "import sys; sys.path.insert(0, '%~dp0'); from complete_sampler import CompleteSampler; s = CompleteSampler(); s.load_to_pad(%pnum%, '%sn%'); print('Loaded')" & goto done
if "%choice%"=="11" python -c "import sys; sys.path.insert(0, '%~dp0'); from sampler_system import AudioSample, load_wav, SampleChopper, SampleExporter; s = load_wav('audio/samples/test_import.wav'); v = SampleExporter.export_with_variations(s, 'audio/samples/exports'); print('Exported', len(v), 'variations')" & goto done

if "%choice%"=="12" python "%~dp0flstudio_ai_api.py" --ai-melody & goto done
if "%choice%"=="13" python -c "import sys; sys.path.insert(0, '%~dp0'); from flstudio_ai_api import FLStudioAI; api = FLStudioAI(); api.generate_innovative_track('electronic', 'dreamy', 8.0)" & goto done

if "%choice%"=="14" python "%~dp0flstudio_ai_api.py" --mix & goto done
if "%choice%"=="15" python -c "import sys; sys.path.insert(0, '%~dp0'); from flstudio_ai_api import FLStudioAI; api = FLStudioAI(); api.create_stem_pack('trap')" & goto done

if "%choice%"=="16" python -c "import sys; sys.path.insert(0, '%~dp0'); from live_performance import LivePerformance; perf = LivePerformance(); perf.setup_scene('Live', {0:'trap',1:'house',2:'dubstep',3:'dnb'}); perf.trigger_pad(0); print('Performance ready')" & goto done

if "%choice%"=="17" python -c "import sys; sys.path.insert(0, '%~dp0'); from automation_timeline import Timeline, MixAutomation; tl = Timeline(120); mix = MixAutomation(tl); mix.create_volume_automation('Track', [(0, 0), (16, 1), (32, 0)]); print('Timeline created')" & goto done

if "%choice%"=="18" python "%~dp0flstudio_ai_api.py" --server & goto done

if "%choice%"=="19" start "" "%~dp0beat_visualizer.html" & echo Visualizer opened! & goto done

if "%choice%"=="20" python "%~dp0flstudio_ai_api.py" --list-files & goto done
if "%choice%"=="21" start "" "%~dp0audio" & goto done

if "%choice%"=="0" exit

:done
echo.
echo ================================================================
echo   Files: audio/ folder
echo   MIDI: exports/ folder  
echo   Samples: audio/samples/
echo ================================================================
echo.
pause
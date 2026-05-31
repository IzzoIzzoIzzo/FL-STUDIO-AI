@echo off
cd /d "C:\Users\Brittany\OneDrive\Desktop\AI FL STUDIO BUILD"
python -c "from flstudio_ai_api import FLStudioAI; api = FLStudioAI(); print('TRAP beat:'); api.generate_beat('trap', 4); print('HOUSE beat:'); api.generate_beat('house', 4); print('Done! Files in exports/')"
pause
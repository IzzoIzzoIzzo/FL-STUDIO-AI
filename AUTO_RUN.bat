@echo off
cd /d "%~dp0"
echo SHADDAI Music Engine - Auto Generating...
echo.
python -c "
from flstudio_ai_api import FLStudioAI
api = FLStudioAI()
print('Generating TRAP beat...')
api.generate_beat('trap', 4)
print('Generating HOUSE beat...')
api.generate_beat('house', 4)
print('Playing Synth...')
api.real_synth.load_preset('lead')
api.real_synth.play(440, 1.0)
print('Playing Drums...')
api.real_drums.play('kick')
print('Done! Check exports/ and audio/ folders!')
" 2>&1
echo.
echo Files created!
pause
"""
PRESET PACK - 100+ Professional Synth Presets
==============================================
Extended presets for:
- Leads (15+)
- Basses (15+)
- Pads (15+)
- Plucks (10+)
- Keys (10+)
- Strings (10+)
- Brass (10+)
- FX (15+)
- Bells (10+)
- SFX (10+)
- Special (10+)

Total: 100+ Presets
"""

PRESETS_100 = {
    # ===== LEADS =====
    'lead_superSaw': {'wave': 'saw_up', 'detune': 10, 'cutoff': 3000, 'a': 0.05, 'd': 0.1, 's': 0.8, 'r': 0.2},
    'lead_superSquare': {'wave': 'square', 'detune': 15, 'cutoff': 2500, 'a': 0.01, 'd': 0.1, 's': 0.7, 'r': 0.3},
    'lead_bright': {'wave': 'sine', 'detune': 7, 'cutoff': 5000, 'a': 0.01, 'd': 0.05, 's': 0.9, 'r': 0.1},
    'lead_acidic': {'wave': 'saw_down', 'detune': 5, 'cutoff': 1500, 'a': 0.001, 'd': 0.3, 's': 0.5, 'r': 0.2},
    'lead_teeth': {'wave': 'saw_up', 'detune': 20, 'cutoff': 2000, 'a': 0.01, 'd': 0.2, 's': 0.6, 'r': 0.1},
    'lead_neon': {'wave': 'triangle', 'detune': 3, 'cutoff': 8000, 'a': 0.001, 'd': 0.1, 's': 0.9, 'r': 0.3},
    'lead_analog': {'wave': 'saw_up', 'detune': 5, 'cutoff': 2500, 'a': 0.05, 'd': 0.2, 's': 0.7, 'r': 0.2},
    'lead_wobble': {'wave': 'saw_up', 'detune': 0, 'cutoff': 1800, 'a': 0.01, 'd': 0.1, 's': 0.8, 'r': 0.2, 'lfo': 3},
    'lead_sci_fi': {'wave': 'sine', 'detune': 10, 'cutoff': 4000, 'a': 0.3, 'd': 0.3, 's': 0.6, 'r': 0.5},
    'lead_retro': {'wave': 'square', 'detune': 3, 'cutoff': 2200, 'a': 0.01, 'd': 0.2, 's': 0.5, 'r': 0.2},
    'lead_aggressive': {'wave': 'saw_up', 'detune': 25, 'cutoff': 1800, 'a': 0.001, 'd': 0.15, 's': 0.7, 'r': 0.1},
    'lead_softer': {'wave': 'triangle', 'detune': 2, 'cutoff': 3500, 'a': 0.1, 'd': 0.1, 's': 0.8, 'r': 0.3},
    'lead_sharp': {'wave': 'square', 'detune': 0, 'cutoff': 5000, 'a': 0.001, 'd': 0.05, 's': 0.6, 'r': 0.1},
    'lead_punchy': {'wave': 'saw_up', 'detune': 8, 'cutoff': 2800, 'a': 0.001, 'd': 0.1, 's': 0.8, 'r': 0.15},
    'lead_wide': {'wave': 'saw_up', 'detune': 15, 'cutoff': 3200, 'a': 0.05, 'd': 0.15, 's': 0.7, 'r': 0.2},
    
    # ===== BASSES =====
    'bass_deep': {'wave': 'sub_sine', 'detune': 0, 'cutoff': 200, 'a': 0.01, 'd': 0.2, 's': 0.8, 'r': 0.3},
    'bass_wobble': {'wave': 'sine', 'detune': 0, 'cutoff': 300, 'a': 0.01, 'd': 0.1, 's': 0.9, 'r': 0.1, 'lfo': 2},
    'bass_808': {'wave': 'sine', 'detune': 0, 'cutoff': 100, 'a': 0.001, 'd': 0.5, 's': 0, 'r': 0.5},
    'bass_squash': {'wave': 'square', 'detune': 0, 'cutoff': 400, 'a': 0.001, 'd': 0.1, 's': 0.7, 'r': 0.1},
    'bass_punch': {'wave': 'triangle', 'detune': 5, 'cutoff': 500, 'a': 0.001, 'd': 0.05, 's': 0.8, 'r': 0.1},
    'bass_sub': {'wave': 'sub_sine', 'detune': 0, 'cutoff': 150, 'a': 0.01, 'd': 0.2, 's': 0.9, 'r': 0.3},
    'bass_acid': {'wave': 'saw_down', 'detune': 30, 'cutoff': 250, 'a': 0.001, 'd': 0.1, 's': 0.6, 'r': 0.1},
    'bass_growl': {'wave': 'sine', 'detune': -5, 'cutoff': 350, 'a': 0.01, 'd': 0.15, 's': 0.85, 'r': 0.15},
    'bass_ridge': {'wave': 'square', 'detune': 10, 'cutoff': 180, 'a': 0.001, 'd': 0.2, 's': 0.7, 'r': 0.2},
    'bass_hollow': {'wave': 'triangle', 'detune': 0, 'cutoff': 280, 'a': 0.02, 'd': 0.3, 's': 0.6, 'r': 0.4},
    'bass_modern': {'wave': 'sub_sine', 'detune': 3, 'cutoff': 220, 'a': 0.005, 'd': 0.15, 's': 0.9, 'r': 0.25},
    'bass_vintage': {'wave': 'sine', 'detune': -3, 'cutoff': 260, 'a': 0.01, 'd': 0.25, 's': 0.75, 'r': 0.35},
    'bass_flip': {'wave': 'saw_up', 'detune': 0, 'cutoff': 400, 'a': 0.001, 'd': 0.08, 's': 0.8, 'r': 0.1},
    'bass_thump': {'wave': 'sine', 'detune': 0, 'cutoff': 180, 'a': 0.001, 'd': 0.05, 's': 0.9, 'r': 0.08},
    'bass_heavy': {'wave': 'sub_sine', 'detune': -2, 'cutoff': 120, 'a': 0.001, 'd': 0.3, 's': 0.6, 'r': 0.3},
    
    # ===== PADS =====
    'pad_warm': {'wave': 'sine', 'detune': 3, 'cutoff': 1500, 'a': 0.5, 'd': 0.5, 's': 0.8, 'r': 1.0},
    'pad_sweep': {'wave': 'saw_up', 'detune': 2, 'cutoff': 2000, 'a': 1.0, 'd': 0.5, 's': 0.7, 'r': 1.5, 'lfo': 0.2},
    'pad_ethereal': {'wave': 'sine', 'detune': 7, 'cutoff': 3000, 'a': 0.3, 'd': 0.5, 's': 0.7, 'r': 1.2},
    'pad_glass': {'wave': 'sine', 'detune': 10, 'cutoff': 4000, 'a': 0.2, 'd': 0.3, 's': 0.6, 'r': 0.8},
    'pad_bright': {'wave': 'saw_up', 'detune': 5, 'cutoff': 3500, 'a': 0.5, 'd': 0.3, 's': 0.8, 'r': 1.0},
    'pad_ambient': {'wave': 'sine', 'detune': 0, 'cutoff': 1000, 'a': 1.0, 'd': 1.0, 's': 0.9, 'r': 2.0},
    'pad_shimmer': {'wave': 'sine', 'detune': 8, 'cutoff': 4500, 'a': 0.4, 'd': 0.4, 's': 0.7, 'r': 1.0},
    'pad_dark': {'wave': 'saw_down', 'detune': 5, 'cutoff': 800, 'a': 0.6, 'd': 0.6, 's': 0.8, 'r': 1.2},
    'pad_angelic': {'wave': 'triangle', 'detune': 4, 'cutoff': 3500, 'a': 0.3, 'd': 0.4, 's': 0.8, 'r': 1.0},
    'pad_cosmic': {'wave': 'sine', 'detune': 12, 'cutoff': 2500, 'a': 0.8, 'd': 0.5, 's': 0.7, 'r': 1.5},
    'pad_spacey': {'wave': 'sine', 'detune': 15, 'cutoff': 2000, 'a': 1.2, 'd': 0.8, 's': 0.6, 'r': 2.0},
    'pad_velvet': {'wave': 'triangle', 'detune': 2, 'cutoff': 1800, 'a': 0.4, 'd': 0.5, 's': 0.9, 'r': 1.1},
    'pad_panorama': {'wave': 'saw_up', 'detune': 8, 'cutoff': 2800, 'a': 0.5, 'd': 0.4, 's': 0.75, 'r': 0.9},
    'pad_water': {'wave': 'sine', 'detune': 5, 'cutoff': 1500, 'a': 0.6, 'd': 0.6, 's': 0.7, 'r': 1.3},
    'pad_slow': {'wave': 'sine', 'detune': 0, 'cutoff': 1200, 'a': 1.5, 'd': 1.0, 's': 0.8, 'r': 2.5},
    
    # ===== PLUCKS =====
    'pluck_bright': {'wave': 'triangle', 'detune': 0, 'cutoff': 6000, 'a': 0.001, 'd': 0.3, 's': 0, 'r': 0.2},
    'pluck_soft': {'wave': 'sine', 'detune': 0, 'cutoff': 2000, 'a': 0.001, 'd': 0.5, 's': 0, 'r': 0.5},
    'pluck_acoustic': {'wave': 'triangle', 'detune': 3, 'cutoff': 3000, 'a': 0.001, 'd': 0.2, 's': 0.3, 'r': 0.3},
    'pluck_harp': {'wave': 'sine', 'detune': 5, 'cutoff': 4000, 'a': 0.001, 'd': 0.1, 's': 0.2, 'r': 0.2},
    'pluck_electric': {'wave': 'square', 'detune': 0, 'cutoff': 2500, 'a': 0.001, 'd': 0.05, 's': 0, 'r': 0.1},
    'pluck_bite': {'wave': 'saw_up', 'detune': 10, 'cutoff': 3500, 'a': 0.001, 'd': 0.15, 's': 0, 'r': 0.15},
    'pluck_mellow': {'wave': 'triangle', 'detune': 0, 'cutoff': 1500, 'a': 0.005, 'd': 0.4, 's': 0.2, 'r': 0.4},
    'pluck_reso': {'wave': 'saw_down', 'detune': 8, 'cutoff': 2800, 'a': 0.001, 'd': 0.25, 's': 0, 'r': 0.25},
    'pluck_short': {'wave': 'sine', 'detune': 0, 'cutoff': 5000, 'a': 0.001, 'd': 0.08, 's': 0, 'r': 0.08},
    'pluck_pure': {'wave': 'sine', 'detune': 0, 'cutoff': 2500, 'a': 0.001, 'd': 0.3, 's': 0, 'r': 0.3},
    
    # ===== KEYS =====
    'keys_piano': {'wave': 'triangle', 'detune': 5, 'cutoff': 4000, 'a': 0.001, 'd': 0.5, 's': 0.3, 'r': 0.8},
    'keys_electric': {'wave': 'triangle', 'detune': 3, 'cutoff': 3000, 'a': 0.01, 'd': 0.2, 's': 0.5, 'r': 0.5},
    'keys_clav': {'wave': 'square', 'detune': 0, 'cutoff': 5000, 'a': 0.001, 'd': 0.1, 's': 0.4, 'r': 0.1},
    'keys_organ': {'wave': 'saw_up', 'detune': 7, 'cutoff': 2000, 'a': 0.01, 'd': 0.01, 's': 1.0, 'r': 0.01},
    'keys_rhodes': {'wave': 'sine', 'detune': 2, 'cutoff': 2500, 'a': 0.01, 'd': 0.3, 's': 0.6, 'r': 0.4},
    'keys_wurlitzer': {'wave': 'triangle', 'detune': 4, 'cutoff': 2200, 'a': 0.005, 'd': 0.25, 's': 0.5, 'r': 0.35},
    'keys_grand': {'wave': 'triangle', 'detune': 8, 'cutoff': 3500, 'a': 0.001, 'd': 0.8, 's': 0.4, 'r': 1.2},
    'keys_tines': {'wave': 'sine', 'detune': 0, 'cutoff': 2800, 'a': 0.005, 'd': 0.2, 's': 0.5, 'r': 0.3},
    'keys_glass': {'wave': 'sine', 'detune': 10, 'cutoff': 4500, 'a': 0.001, 'd': 0.6, 's': 0.2, 'r': 0.6},
    'keys_vinyl': {'wave': 'triangle', 'detune': -3, 'cutoff': 1800, 'a': 0.01, 'd': 0.4, 's': 0.4, 'r': 0.5},
    
    # ===== STRINGS =====
    'strings_slow': {'wave': 'saw_up', 'detune': 2, 'cutoff': 2500, 'a': 0.5, 'd': 0.5, 's': 0.8, 'r': 1.0},
    'strings_fast': {'wave': 'saw_up', 'detune': 5, 'cutoff': 3000, 'a': 0.1, 'd': 0.2, 's': 0.9, 'r': 0.5},
    'strings_bitter': {'wave': 'saw_up', 'detune': 10, 'cutoff': 3500, 'a': 0.3, 'd': 0.3, 's': 0.7, 'r': 0.8},
    'strings_swell': {'wave': 'saw_up', 'detune': 0, 'cutoff': 2200, 'a': 1.0, 'd': 0.8, 's': 0.8, 'r': 1.5},
    'strings_soft': {'wave': 'triangle', 'detune': 3, 'cutoff': 2000, 'a': 0.4, 'd': 0.5, 's': 0.85, 'r': 1.0},
    'strings_section': {'wave': 'saw_up', 'detune': 6, 'cutoff': 2800, 'a': 0.2, 'd': 0.4, 's': 0.8, 'r': 0.8},
    'strings_ensemble': {'wave': 'saw_up', 'detune': 12, 'cutoff': 2500, 'a': 0.3, 'd': 0.3, 's': 0.75, 'r': 0.7},
    'strings_cinematic': {'wave': 'saw_up', 'detune': 0, 'cutoff': 1800, 'a': 1.5, 'd': 1.0, 's': 0.7, 'r': 2.0},
    'strings_sustained': {'wave': 'triangle', 'detune': 4, 'cutoff': 2300, 'a': 0.6, 'd': 0.6, 's': 0.9, 'r': 1.2},
    'strings_tension': {'wave': 'saw_up', 'detune': 15, 'cutoff': 2000, 'a': 0.4, 'd': 0.4, 's': 0.6, 'r': 0.9},
    
    # ===== BRASS =====
    'brass_soft': {'wave': 'saw_up', 'detune': 5, 'cutoff': 2500, 'a': 0.05, 'd': 0.1, 's': 0.9, 'r': 0.3},
    'brass_hit': {'wave': 'saw_up', 'detune': 0, 'cutoff': 1500, 'a': 0.001, 'd': 0.2, 's': 0.7, 'r': 0.2},
    'brass_synth': {'wave': 'saw_up', 'detune': 3, 'cutoff': 2000, 'a': 0.02, 'd': 0.1, 's': 0.8, 'r': 0.2},
    'brass_ mellow': {'wave': 'triangle', 'detune': 2, 'cutoff': 1800, 'a': 0.1, 'd': 0.2, 's': 0.85, 'r': 0.4},
    'brass_section': {'wave': 'saw_up', 'detune': 8, 'cutoff': 2200, 'a': 0.08, 'd': 0.15, 's': 0.8, 'r': 0.25},
    'brass_fat': {'wave': 'saw_up', 'detune': 12, 'cutoff': 1800, 'a': 0.03, 'd': 0.1, 's': 0.85, 'r': 0.2},
    'brass_razz': {'wave': 'square', 'detune': 5, 'cutoff': 2500, 'a': 0.001, 'd': 0.08, 's': 0.7, 'r': 0.1},
    'brass_bright': {'wave': 'saw_up', 'detune': 0, 'cutoff': 3500, 'a': 0.02, 'd': 0.05, 's': 0.9, 'r': 0.15},
    'brass_analog': {'wave': 'saw_up', 'detune': 6, 'cutoff': 2000, 'a': 0.05, 'd': 0.12, 's': 0.8, 'r': 0.25},
    'brass_subtle': {'wave': 'triangle', 'detune': 0, 'cutoff': 1600, 'a': 0.08, 'd': 0.18, 's': 0.88, 'r': 0.35},
    
    # ===== FX =====
    'fx_riser': {'wave': 'saw_up', 'detune': 20, 'cutoff': 1000, 'a': 2.0, 'd': 1.0, 's': 1.0, 'r': 1.0},
    'fx_fall': {'wave': 'sine', 'detune': 0, 'cutoff': 5000, 'a': 0.5, 'd': 0.5, 's': 0.5, 'r': 2.0},
    'fx_blip': {'wave': 'square', 'detune': 0, 'cutoff': 8000, 'a': 0.001, 'd': 0.05, 's': 0, 'r': 0.1},
    'fx_noise': {'wave': 'noise', 'detune': 0, 'cutoff': 5000, 'a': 0.001, 'd': 0.1, 's': 0.5, 'r': 0.2},
    'fx_drone': {'wave': 'sub_sine', 'detune': 1, 'cutoff': 500, 'a': 1.0, 'd': 0.5, 's': 1.0, 'r': 1.0},
    'fx_sweep': {'wave': 'saw_up', 'detune': 5, 'cutoff': 2000, 'a': 0.8, 'd': 0.8, 's': 0.6, 'r': 1.2},
    'fx_shirley': {'wave': 'saw_up', 'detune': 0, 'cutoff': 3000, 'a': 0.3, 'd': 0.4, 's': 0.8, 'r': 0.8, 'lfo': 5},
    'fx_weep': {'wave': 'sine', 'detune': 0, 'cutoff': 4000, 'a': 0.5, 'd': 0.5, 's': 0.5, 'r': 1.0},
    'fx_squash': {'wave': 'saw_down', 'detune': 15, 'cutoff': 800, 'a': 0.1, 'd': 0.2, 's': 0.7, 'r': 0.3},
    'fx_wind': {'wave': 'noise', 'detune': 0, 'cutoff': 2000, 'a': 1.5, 'd': 1.0, 's': 0.8, 'r': 2.0},
    'fx_impact': {'wave': 'sine', 'detune': 0, 'cutoff': 1500, 'a': 0.001, 'd': 0.5, 's': 0, 'r': 0.5},
    'fx_zap': {'wave': 'square', 'detune': 20, 'cutoff': 6000, 'a': 0.001, 'd': 0.02, 's': 0, 'r': 0.05},
    'fx_sweep_down': {'wave': 'saw_down', 'detune': 0, 'cutoff': 3000, 'a': 0.3, 'd': 0.4, 's': 0.4, 'r': 1.5},
    'fx_telephone': {'wave': 'sine', 'detune': 0, 'cutoff': 2500, 'a': 0.01, 'd': 0.05, 's': 0.3, 'r': 0.1},
    'fx_jet': {'wave': 'noise', 'detune': 0, 'cutoff': 4000, 'a': 1.0, 'd': 0.5, 's': 0.5, 'r': 1.5},
    
    # ===== BELLS =====
    'bell_bright': {'wave': 'sine', 'detune': 0, 'cutoff': 8000, 'a': 0.001, 'd': 1.0, 's': 0, 'r': 1.0},
    'bell_soft': {'wave': 'sine', 'detune': 5, 'cutoff': 3000, 'a': 0.01, 'd': 1.5, 's': 0, 'r': 1.5},
    'bell_glass': {'wave': 'sine', 'detune': 10, 'cutoff': 6000, 'a': 0.001, 'd': 2.0, 's': 0, 'r': 2.0},
    'bell_metal': {'wave': 'triangle', 'detune': 8, 'cutoff': 5000, 'a': 0.001, 'd': 0.8, 's': 0, 'r': 0.8},
    'bell_chime': {'wave': 'sine', 'detune': 3, 'cutoff': 4500, 'a': 0.001, 'd': 1.2, 's': 0, 'r': 1.2},
    'bell_crystal': {'wave': 'sine', 'detune': 15, 'cutoff': 7000, 'a': 0.001, 'd': 1.8, 's': 0, 'r': 1.8},
    'bell_tibetan': {'wave': 'sine', 'detune': 0, 'cutoff': 2500, 'a': 0.1, 'd': 1.0, 's': 0.2, 'r': 1.5},
    'bell_warm': {'wave': 'triangle', 'detune': 2, 'cutoff': 2800, 'a': 0.01, 'd': 1.2, 's': 0.1, 'r': 1.3},
    'bell_carillon': {'wave': 'sine', 'detune': 12, 'cutoff': 5500, 'a': 0.001, 'd': 1.5, 's': 0, 'r': 1.5},
    'bell_glocken': {'wave': 'sine', 'detune': 6, 'cutoff': 4800, 'a': 0.001, 'd': 1.0, 's': 0, 'r': 1.0},
    
    # ===== SFX =====
    'sfx_kick': {'wave': 'sine', 'detune': 0, 'cutoff': 200, 'a': 0.001, 'd': 0.1, 's': 0, 'r': 0.1},
    'sfx_snare': {'wave': 'triangle', 'detune': 0, 'cutoff': 3000, 'a': 0.001, 'd': 0.1, 's': 0, 'r': 0.1},
    'sfx_hat': {'wave': 'noise', 'detune': 0, 'cutoff': 8000, 'a': 0.001, 'd': 0.05, 's': 0, 'r': 0.05},
    'sfx_impact': {'wave': 'sine', 'detune': 0, 'cutoff': 2000, 'a': 0.001, 'd': 0.3, 's': 0, 'r': 0.3},
    'sfx_sweep_up': {'wave': 'saw_up', 'detune': 0, 'cutoff': 4000, 'a': 0.3, 'd': 0.3, 's': 0.3, 'r': 0.8},
    'sfx_sweep_down': {'wave': 'saw_down', 'detune': 0, 'cutoff': 4000, 'a': 0.3, 'd': 0.3, 's': 0.3, 'r': 0.8},
    'sfx_glitch': {'wave': 'square', 'detune': 20, 'cutoff': 5000, 'a': 0.001, 'd': 0.03, 's': 0, 'r': 0.05},
    'sfx_robotic': {'wave': 'square', 'detune': 10, 'cutoff': 2500, 'a': 0.05, 'd': 0.1, 's': 0.4, 'r': 0.2},
    'sfx_alien': {'wave': 'sine', 'detune': 15, 'cutoff': 3500, 'a': 0.2, 'd': 0.4, 's': 0.5, 'r': 0.6},
    'sfx_reverse': {'wave': 'triangle', 'detune': 0, 'cutoff': 3000, 'a': 0.1, 'd': 0.2, 's': 0.2, 'r': 0.5},
    
    # ===== SPECIAL =====
    'special_sub_bass': {'wave': 'sub_sine', 'detune': -5, 'cutoff': 80, 'a': 0.01, 'd': 0.3, 's': 0.9, 'r': 0.4},
    'special_weepiano': {'wave': 'triangle', 'detune': 5, 'cutoff': 3500, 'a': 0.001, 'd': 0.8, 's': 0.3, 'r': 1.0},
    'special_drone_pad': {'wave': 'sub_sine', 'detune': 2, 'cutoff': 300, 'a': 2.0, 'd': 1.0, 's': 1.0, 'r': 2.0},
    'special_bell_pad': {'wave': 'sine', 'detune': 8, 'cutoff': 2000, 'a': 0.8, 'd': 0.8, 's': 0.7, 'r': 1.5},
    'special_choir': {'wave': 'sine', 'detune': 4, 'cutoff': 1800, 'a': 1.0, 'd': 0.6, 's': 0.8, 'r': 1.2},
    'special_growl': {'wave': 'saw_down', 'detune': 25, 'cutoff': 350, 'a': 0.01, 'd': 0.15, 's': 0.8, 'r': 0.2},
    'special_vowel': {'wave': 'sine', 'detune': 0, 'cutoff': 1500, 'a': 0.3, 'd': 0.3, 's': 0.7, 'r': 0.5},
    'special_detuned_lead': {'wave': 'saw_up', 'detune': 30, 'cutoff': 2500, 'a': 0.02, 'd': 0.1, 's': 0.75, 'r': 0.15},
    'special_rez': {'wave': 'saw_down', 'detune': 15, 'cutoff': 2200, 'a': 0.001, 'd': 0.1, 's': 0.6, 'r': 0.1},
    'special_washed': {'wave': 'sine', 'detune': 0, 'cutoff': 800, 'a': 1.5, 'd': 1.2, 's': 0.9, 'r': 2.5},
}


# Quick category lookup
PRESET_CATEGORIES = {
    'lead': [p for p in PRESETS_100 if 'lead' in p],
    'bass': [p for p in PRESETS_100 if 'bass' in p],
    'pad': [p for p in PRESETS_100 if 'pad' in p],
    'pluck': [p for p in PRESETS_100 if 'pluck' in p],
    'keys': [p for p in PRESETS_100 if 'keys' in p],
    'strings': [p for p in PRESETS_100 if 'string' in p],
    'brass': [p for p in PRESETS_100 if 'brass' in p],
    'fx': [p for p in PRESETS_100 if 'fx' in p],
    'bell': [p for p in PRESETS_100 if 'bell' in p],
    'sfx': [p for p in PRESETS_100 if 'sfx' in p],
    'special': [p for p in PRESETS_100 if 'special' in p],
}


if __name__ == "__main__":
    print("=" * 60)
    print("  PRESET PACK - 100+ PRESETS")
    print("=" * 60)
    print("\n[Presets by Category]")
    for cat, presets in PRESET_CATEGORIES.items():
        print("  %s: %d" % (cat, len(presets)))
    print("\n[Total: %d presets]" % len(PRESETS_100))
    print("=" * 60)
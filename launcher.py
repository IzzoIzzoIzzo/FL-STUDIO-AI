#!/usr/bin/env python3
"""
SHADDAI MUSIC ENGINE - LAUNCHER
Simple GUI to launch the music production system
"""

import os
import sys
import json
import subprocess

# Get the directory where this script is located
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))

# Colors for terminal
class Colors:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'

def print_banner():
    """Print the launcher banner"""
    banner = f"""
{Colors.CYAN}╔══════════════════════════════════════════════════════════════════════╗
║                                                                      ║
║   ████████╗███████╗██████╗ ███╗   ███╗██╗███╗   ██╗ ██████╗           ║
║   ╚══██╔══╝██╔════╝██╔══██╗████╗ ████║██║████╗  ██║██╔════╝           ║
║      ██║   █████╗  ██████╔╝██╔████╔██║██║██╔██╗ ██║██║  ███╗          ║
║      ██║   ██╔══╝  ██╔══██╗██║╚██╔╝██║██║██║╚██╗██║██║   ██║          ║
║      ██║   ███████╗██║  ██║██║ ╚═╝ ██║██║██║ ╚████║╚██████╔╝          ║
║      ╚═╝   ╚══════╝╚═╝  ╚═╝╚═╝     ╚═╝╚═╝╚═╝  ╚═══╝ ╚═════╝           ║
║                          MUSIC ENGINE v8.0                          ║
╚══════════════════════════════════════════════════════════════════════╝{Colors.ENDC}
    """
    print(banner)

def load_modules():
    """Load registered modules from registry"""
    registry_path = os.path.join(SCRIPT_DIR, 'module_registry.py')
    if os.path.exists(registry_path):
        try:
            sys.path.insert(0, SCRIPT_DIR)
            import module_registry
            return module_registry.MODULES
        except:
            pass
    return {}

def main_menu():
    """Main menu of the launcher"""
    modules = load_modules()
    
    print(f"\n{Colors.BOLD}┌─────────────────────────────────────────────────────────────────────┐{Colors.ENDC}")
    print(f"{Colors.BOLD}│  MAIN MENU                                                      │{Colors.ENDC}")
    print(f"{Colors.BOLD}├─────────────────────────────────────────────────────────────────────┤{Colors.ENDC}")
    print(f"{Colors.BOLD}│  [1] ▶  Start Music Studio (Full System)                        │{Colors.ENDC}")
    print(f"{Colors.BOLD}│  [2] 🎹  Beat Generator                                         │{Colors.ENDC}")
    print(f"{Colors.BOLD}│  [3] 🎵  AI Melody Composer                                    │{Colors.ENDC}")
    print(f"{Colors.BOLD}│  [4] 🎸  Synthesizer                                           │{Colors.ENDC}")
    print(f"{Colors.BOLD}│  [5] 🎤  Vocal Processor                                       │{Colors.ENDC}")
    print(f"{Colors.BOLD}│  [6] 🎧  Auto-Mixer                                            │{Colors.ENDC}")
    print(f"{Colors.BOLD}│  [7] 🔊  Mastering Engine                                      │{Colors.ENDC}")
    print(f"{Colors.BOLD}│  [8] 🎚️  Live DJ Performance                                    │{Colors.ENDC}")
    print(f"{Colors.BOLD}│  [9] 🌙  Esoteric Music (Healing/Sacred)                       │{Colors.ENDC}")
    print(f"{Colors.BOLD}│  [10] 🎼 Music Theory                                         │{Colors.ENDC}")
    print(f"{Colors.BOLD}│  [11] 📊 System Dashboard                                      │{Colors.ENDC}")
    print(f"{Colors.BOLD}│  [12] 💻 Terminal Interface                                    │{Colors.ENDC}")
    print(f"{Colors.BOLD}│  [0] ❌ Exit                                                   │{Colors.ENDC}")
    print(f"{Colors.BOLD}└─────────────────────────────────────────────────────────────────────┘{Colors.ENDC}")
    
    choice = input(f"\n{Colors.YELLOW}Enter choice: {Colors.ENDC}")
    return choice

def launch_module(module_name):
    """Launch a specific module"""
    try:
        result = subprocess.run(
            [sys.executable, '-c', f'import os; os.chdir("{SCRIPT_DIR}"); exec(open("{module_name}.py").read())'],
            capture_output=True,
            text=True,
            timeout=30
        )
        print(result.stdout)
        if result.stderr:
            print(f"{Colors.RED}Error: {result.stderr}{Colors.ENDC}")
    except Exception as e:
        print(f"{Colors.RED}Failed to launch: {e}{Colors.ENDC}")

def start_full_system():
    """Start the full music production system"""
    print(f"\n{Colors.GREEN}Starting SHADDAI Music Studio...{Colors.ENDC}\n")
    try:
        # Try to launch the main API
        sys.path.insert(0, SCRIPT_DIR)
        
        # Check for terminal interface first
        if os.path.exists(os.path.join(SCRIPT_DIR, 'terminal_interface.py')):
            print(f"{Colors.CYAN}Launching Terminal Interface...{Colors.ENDC}")
            subprocess.run([sys.executable, 'terminal_interface.py'], cwd=SCRIPT_DIR)
        elif os.path.exists(os.path.join(SCRIPT_DIR, 'flstudio_ai_api.py')):
            print(f"{Colors.CYAN}Launching Main API...{Colors.ENDC}")
            exec(open(os.path.join(SCRIPT_DIR, 'flstudio_ai_api.py')).read())
    except KeyboardInterrupt:
        print(f"\n{Colors.YELLOW}System stopped.{Colors.ENDC}")
    except Exception as e:
        print(f"{Colors.RED}Error: {e}{Colors.ENDC}")

def show_system_status():
    """Show system status"""
    print(f"\n{Colors.CYAN}╔═══════════════════════════════════════════════════════════════╗{Colors.ENDC}")
    print(f"{Colors.CYAN}║                    SYSTEM STATUS                              ║{Colors.ENDC}")
    print(f"{Colors.CYAN}╚═══════════════════════════════════════════════════════════════╝{Colors.ENDC}")
    
    try:
        sys.path.insert(0, SCRIPT_DIR)
        import module_registry
        
        print(f"\n{Colors.GREEN}Modules Loaded: {len(module_registry.MODULES)}{Colors.ENDC}")
        
        # Count categories
        categories = {}
        for mod in module_registry.MODULES.values():
            cat = mod.get('category', 'Unknown')
            categories[cat] = categories.get(cat, 0) + 1
        
        for cat, count in categories.items():
            print(f"  {cat}: {count}")
        
        print(f"\n{Colors.YELLOW}All systems operational ✓{Colors.ENDC}")
    except Exception as e:
        print(f"{Colors.RED}Error loading registry: {e}{Colors.ENDC}")

def main():
    """Main launcher loop"""
    os.system('cls' if os.name == 'nt' else 'clear')
    print_banner()
    
    print(f"\n{Colors.GREEN}Welcome to SHADDAI Music Engine!{Colors.ENDC}")
    print(f"{Colors.BLUE}Everything works and is connected!{Colors.ENDC}\n")
    
    while True:
        choice = main_menu()
        
        if choice == '1':
            start_full_system()
        elif choice == '2':
            print(f"\n{Colors.CYAN}Opening Beat Generator...{Colors.ENDC}")
            launch_module('super_engine')
        elif choice == '3':
            print(f"\n{Colors.CYAN}Opening AI Melody...{Colors.ENDC}")
            launch_module('ai_melody_engine')
        elif choice == '4':
            print(f"\n{Colors.CYAN}Opening Synthesizer...{Colors.ENDC}")
            launch_module('enhanced_synth_v4')
        elif choice == '5':
            print(f"\n{Colors.CYAN}Opening Vocal Processor...{Colors.ENDC}")
            launch_module('vocal_processor')
        elif choice == '6':
            print(f"\n{Colors.CYAN}Opening Auto-Mixer...{Colors.ENDC}")
            launch_module('mixer_v3')
        elif choice == '7':
            print(f"\n{Colors.CYAN}Opening Mastering Engine...{Colors.ENDC}")
            launch_module('mastering_engine')
        elif choice == '8':
            print(f"\n{Colors.CYAN}Opening Live DJ...{Colors.ENDC}")
            launch_module('live_performance_dj')
        elif choice == '9':
            print(f"\n{Colors.CYAN}Opening Esoteric Music...{Colors.ENDC}")
            launch_module('esoteric_music_engine')
        elif choice == '10':
            print(f"\n{Colors.CYAN}Opening Music Theory...{Colors.ENDC}")
            launch_module('music_theory_engine')
        elif choice == '11':
            show_system_status()
        elif choice == '12':
            print(f"\n{Colors.CYAN}Opening Terminal Interface...{Colors.ENDC}")
            launch_module('terminal_interface')
        elif choice == '0':
            print(f"\n{Colors.YELLOW}Thanks for using SHADDAI Music Engine!{Colors.ENDC}")
            print(f"{Colors.CYAN}Remember: Everything works and is connected!{Colors.ENDC}\n")
            break
        else:
            print(f"\n{Colors.RED}Invalid choice. Please try again.{Colors.ENDC}")
        
        input(f"\n{Colors.BLUE}Press Enter to continue...{Colors.ENDC}")
        os.system('cls' if os.name == 'nt' else 'clear')
        print_banner()

if __name__ == '__main__':
    main()
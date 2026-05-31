"""
FL Studio MCP Client for Claude Code / OpenCode
Simple Python client to call FL Studio MCP tools
"""

import json
import urllib.request
import urllib.error
from typing import Any, Optional


class FLStudioClient:
    """Client for FL Studio MCP Server"""

    def __init__(self, host: str = "localhost", port: int = 5000):
        self.base_url = f"http://{host}:{port}"

    def _request(self, endpoint: str, data: dict = None) -> dict:
        url = f"{self.base_url}{endpoint}"
        headers = {"Content-Type": "application/json"}

        req_data = json.dumps(data).encode("utf-8") if data else None
        req = urllib.request.Request(url, data=req_data, headers=headers, method="POST" if data else "GET")

        try:
            with urllib.request.urlopen(req, timeout=30) as response:
                return json.loads(response.read().decode("utf-8"))
        except urllib.error.URLError as e:
            return {"status": "error", "message": str(e)}
        except json.JSONDecodeError as e:
            return {"status": "error", "message": f"JSON decode error: {str(e)}"}

    def health(self) -> dict:
        """Check server health"""
        return self._request("/health")

    def list_tools(self) -> list:
        """List all available tools"""
        result = self._request("/tools")
        return result.get("tools", [])

    def play(self) -> dict:
        """Start playback"""
        return self._request("/transport/play")

    def stop(self) -> dict:
        """Stop playback"""
        return self._request("/transport/stop")

    def pause(self) -> dict:
        """Pause playback"""
        return self._request("/transport/pause")

    def record(self) -> dict:
        """Toggle recording"""
        return self._request("/transport/record")

    def restart(self) -> dict:
        """Restart from beginning"""
        return self._request("/transport/restart")

    def set_tempo(self, bpm: int) -> dict:
        """Set tempo"""
        return self._request("/tempo", {"bpm": bpm})

    def set_position(self, bar: int) -> dict:
        """Set position to bar"""
        return self._request("/position", {"bar": bar})

    def volume(self, channel: int, level: float) -> dict:
        """Set channel volume"""
        return self._request("/mixer/volume", {"channel": channel, "level": level})

    def pan(self, channel: int, position: float) -> dict:
        """Set channel pan"""
        return self._request("/mixer/pan", {"channel": channel, "position": position})

    def mute(self, channel: int, state: bool) -> dict:
        """Toggle mute"""
        return self._request("/mixer/mute", {"channel": channel, "state": state})

    def solo(self, channel: int, state: bool) -> dict:
        """Toggle solo"""
        return self._request("/mixer/solo", {"channel": channel, "state": state})

    def master_volume(self, level: float) -> dict:
        """Set master volume"""
        return self._request("/mixer/master", {"level": level})

    def select_pattern(self, number: int) -> dict:
        """Select pattern"""
        return self._request("/pattern/select", {"number": number})

    def create_pattern(self, name: str = None) -> dict:
        """Create pattern"""
        return self._request("/pattern/create", {"name": name} if name else {})

    def open_piano_roll(self, channel: int = 0) -> dict:
        """Open piano roll"""
        return self._request("/pianoroll/open", {"channel": channel})

    def close_piano_roll(self) -> dict:
        """Close piano roll"""
        return self._request("/pianoroll/close")

    def add_note(self, pitch: int, start: float, duration: float, velocity: int = 100) -> dict:
        """Add note"""
        return self._request("/pianoroll/note", {
            "pitch": pitch, "start": start, "duration": duration, "velocity": velocity
        })

    def clear_piano_roll(self) -> dict:
        """Clear piano roll"""
        return self._request("/pianoroll/clear")

    def save_project(self, path: str) -> dict:
        """Save project"""
        return self._request("/project/save", {"path": path})

    def new_project(self) -> dict:
        """New project"""
        return self._request("/project/new")

    def generate_drums(self, style: str = "house", bars: int = 1, complexity: int = 3) -> dict:
        """Generate drum pattern"""
        return self._request("/generate/drums", {
            "style": style, "bars": bars, "complexity": complexity
        })

    def generate_bass(self, root: int = 36, scale: str = "minor", length: int = 8) -> dict:
        """Generate bass line"""
        return self._request("/generate/bass", {
            "root": root, "scale": scale, "length": length
        })

    def generate_melody(self, key: int = 60, scale: str = "minor", length: int = 8) -> dict:
        """Generate melody"""
        return self._request("/generate/melody", {
            "key": key, "scale": scale, "length": length
        })

    def generate_chords(self, key: int = 60, style: str = "pop", bars: int = 4) -> dict:
        """Generate chords"""
        return self._request("/generate/chords", {
            "key": key, "style": style, "bars": bars
        })

    def generate_track(self, style: str = "house", key: int = 60, scale: str = "minor", bars: int = 8) -> dict:
        """Generate full track"""
        return self._request("/generate/track", {
            "style": style, "key": key, "scale": scale, "bars": bars
        })


def main():
    import sys

    client = FLStudioClient()

    if len(sys.argv) < 2:
        print("FL Studio MCP Client")
        print("Usage: python flstudio_client.py <command> [args]")
        print("\nCommands:")
        print("  health                    - Check server status")
        print("  tools                     - List available tools")
        print("  play                      - Start playback")
        print("  stop                      - Stop playback")
        print("  tempo <bpm>               - Set tempo")
        print("  generate drums <style>    - Generate drum pattern")
        print("  generate bass <root>     - Generate bass line")
        print("  generate melody <key>    - Generate melody")
        print("  generate track           - Generate full track")
        return

    cmd = sys.argv[1]

    if cmd == "health":
        print(json.dumps(client.health(), indent=2))
    elif cmd == "tools":
        for tool in client.list_tools():
            print(f"  {tool['name']}: {tool['description']}")
    elif cmd == "play":
        print(json.dumps(client.play(), indent=2))
    elif cmd == "stop":
        print(json.dumps(client.stop(), indent=2))
    elif cmd == "tempo":
        bpm = int(sys.argv[2]) if len(sys.argv) > 2 else 120
        print(json.dumps(client.set_tempo(bpm), indent=2))
    elif cmd == "generate":
        if len(sys.argv) > 2:
            what = sys.argv[2]
            if what == "drums":
                style = sys.argv[3] if len(sys.argv) > 3 else "house"
                print(json.dumps(client.generate_drums(style=style), indent=2))
            elif what == "bass":
                print(json.dumps(client.generate_bass(), indent=2))
            elif what == "melody":
                print(json.dumps(client.generate_melody(), indent=2))
            elif what == "track":
                print(json.dumps(client.generate_track(), indent=2))
    else:
        print(f"Unknown command: {cmd}")


if __name__ == "__main__":
    main()
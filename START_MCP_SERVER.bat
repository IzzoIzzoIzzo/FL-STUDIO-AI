@echo off
echo =============================================================
echo FL STUDIO AI - Claude Code Integration
echo =============================================================
echo.
echo Starting MCP Server...
echo Server URL: http://localhost:5000
echo.
echo Usage:
echo   1. Start this server
echo   2. In Claude Code, use MCP at http://localhost:5000
echo   3. Ask Claude to "Make a trap beat" or "Generate house music"
echo.
echo Or use CLI directly:
echo   python beatmaker.py generate trap 150
echo   python beatmaker.py make "dark trap 160 bpm"
echo.
echo Press Ctrl+C to stop
echo.
python "%~dp0flstudio_mcp_server_v2.py"
pause
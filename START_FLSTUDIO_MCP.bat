@echo off
echo ============================================
echo FL Studio MCP Server
echo ============================================
echo.
echo Starting MCP server on http://localhost:5000
echo.
echo Keep this window open while using the MCP
echo Press Ctrl+C to stop
echo.
python "%~dp0flstudio_mcp_server.py"
pause
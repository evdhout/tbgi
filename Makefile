
## Create windows binary
.PHONY: win
win:
	uv run pyinstaller --onedir --onefile --noconsole --icon resources/icon.icns tbgi.py
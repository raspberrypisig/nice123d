# Upgrade tools
# TODO: source .venv/Scipts/dectivate.bat  # Or .venv\Scripts\activate on Windows
python -m pip install --upgrade pip setuptools wheel

# Clear cache
pip cache purge

# Recreate virtual environment
# rm -rf .venv
Remove-Item -Recurse -Force .venv
python -m venv .venv
& ".venv/Scipts/Activate.ps1"  # Or .venv\Scripts\activate on Windows

# Install
pip install pywebview
pip install nicegui
pip install rich
pip install git+https://github.com/gumyr/build123d.git
pip install git+https://github.com/bernhard-42/vscode-ocp-cad-viewer.git

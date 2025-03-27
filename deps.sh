sudo apt install python3
python3 -m pip venv .venv
./.venv/bin/python3 -m pip install --upgrade pip build
./.venv/bin/python3 -m pip install -r requirements.txt

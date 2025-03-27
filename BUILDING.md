# Install deps
```bash
./deps.bat
```

# Build python package

generate code
```bash
python3 generate.py
```

build python package
```bash
cd sourcetypes
python3 -m build
cd ..
```

upload python package
```bash
python3 -m twine upload sourcetypes/dist/*
```

# Build VSCode extension

Install deps (requires npm to be installed)
```bash
npm install -g @vscode/vsce
```

Build extension
```bash
cd vscode-python-inline-source
npm install
vsce package
cd ..
```

Publish extension
```bash
cd vscode-python-inline-source
vsce publish
cd ..
```

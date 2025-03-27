# Install deps
```bash
./deps.bat
```

# Build packages

```
python3 generate.py
cd sourcetypes
python3 -m build --sdist --wheel --outdir dist/ .
cd ..
```
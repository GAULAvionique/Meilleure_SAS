# Copilot instructions for Meilleure_SAS

Short, actionable notes to help an AI coding agent be productive in this repo.

## Big picture
- This repo is a small Python backend that parses binary frames and a frontend folder (UI not wired here).
- Core parser lives in `backend/src/data.py`. Entry/example usage is in `backend/src/main.py`.

## Key files to inspect
- `backend/src/data.py` — bit-level parsing: CONFIG_TRAME describes fields as (start_bit, length). Note: code uses `int.from_bytes(raw_data, byteorder='big')` and bit-shifts based on total length.
- `backend/src/main.py` — example usage and a sample `raw_data = bytes.fromhex(...)` showing how frames are fed to the parser.
- `backend/requirements.txt` — runtime deps: `pyserial` plus `bitarray` and `numpy` (used in `data.py`).
- `frontend/` — present but separate; backend parsing is local and synchronous (no network IPC in repo).

## Developer workflows (concrete commands)
- Create a virtual env and install deps:
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r backend/requirements.txt
pip install bitarray numpy
```
- Run the parser example:
```bash
python3 backend/src/main.py
```
- Run tests (none bundled by default). If you add pytest tests, run:
```bash
pytest
```

## Project-specific patterns & gotchas
- Many identifiers and method names use French / accented names (`décode`, `trameDécodé`, `__séquencer`). Treat these as exact identifiers — don't rename unless updating all callers.
- Byte / bit ordering is subtle: `data.py` currently converts the raw bytes with `byteorder='big'` and uses a shift: `decalage = longueurTotale - (start_bit + length)`. Validate endianness when adding fields. Example bug: the comment in `data.py` notes `À vérifier: little endian ou big endian` — test new field extraction with the `raw_data` sample in `backend/src/main.py`.
- Numeric conversions:
  - float32 conversion uses `numpy` view trick: `np.array([message], dtype=np.uint32).view(np.float32)[0]` — only valid when `message` is the 32-bit integer bit pattern of the IEEE754 float.
  - int32 uses `np.int32(message)`.

## Integration points / external deps
- Serial hardware: `pyserial` listed in `backend/requirements.txt`. `backend/src/serial.py` exists (currently empty) — serial integration may be added there.
- No external network services are defined in the repo.

## How to make safe changes
- When changing `CONFIG_TRAME` or `CONFIG_TYPE`, update examples in `backend/src/main.py` and add a small unit test verifying expected numeric values for a sample `raw_data` hex string.
- Preserve file encoding (UTF-8) — source files use French text/comments.

If any of the above is unclear or you'd like the file expanded with step-by-step tests and a CI config, tell me which area to expand.

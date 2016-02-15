#!/bin/bash
cd "$(dirname "$0")"
python3 fileindexer.py pytest txt ./tests/
python3 fileindexer.py pytest rtf

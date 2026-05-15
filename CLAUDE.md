# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

**Wil-YAT** compares the headwords of Wilson's (WIL) and Yates's (YAT) Sanskrit dictionaries to identify shared headwords, differences, and spelling corrections. Yates's dictionary was closely based on Wilson's, making headword comparison a productive technique for identifying digitization errors in both.

## Architecture

| File/Directory | Purpose |
|---|---|
| `hwcmp.py` | Main headword comparison script: compares WIL and YAT headword lists |
| `hwcmp.txt` | Output of the headword comparison |
| `analyze_near.py` | Analyzes near-matches (Levenshtein-close pairs) between WIL and YAT |
| `dump_cases.py` | Dumps specific case categories from the comparison output |
| `force.txt` | Manual overrides for comparison decisions |
| `data/` | Input headword files (`wil.txt`, `wil_mw.txt`, `wilhw2.txt`, `yat.txt`, `yathw2.txt`) |

### Workflow

1. Run `hwcmp.py` to compare WIL and YAT headword lists → `hwcmp.txt`
2. Use `analyze_near.py` to identify near-matches (likely alternative spellings or digitization errors)
3. Apply confirmed corrections to `csl-orig` via the standard `updateByLine.py` pattern

## Common Commands

```bash
python hwcmp.py     # compare WIL vs YAT headwords
python analyze_near.py hwcmp.txt   # analyze near-matches
```

## Dependencies

- **Python 3**

### Location

Counterpart of https://github.com/sanskrit-lexicon/PWG/issues/175 (PWG) and https://github.com/sanskrit-lexicon/PWK/issues/113 (PWK) for `yat.txt`.

I ran the same two-job recipe over `csl-orig/v02/yat/yat.txt`: auto-fix the few things with a single safe resolution; audit everything else with line refs. Added `08_markup_fix.py` plus outputs to a new `yatissues/markup_fix/` folder on the branch `markup-fix-audit`.

@funderburkjim @Andhrabharati — please review the findings listed below.

## Markup fixer + audit for `yat.txt`

### What it auto-fixes

| Pattern | Result |
|---|---|
| `<ab><ab>X</ab> Y</ab>` | `<ab>X Y</ab>` |
| `<F> word </F>` | `<F>word</F>` |
| `<lang> word </lang>` | `<lang>word</lang>` |

Whitespace trimming applies to all 2 paired tag(s) in `yat.txt`: `<F>`, `<lang>`. The original file is never modified — output goes to `yat_fixed.txt`, with the full diff in `markup_fix_changes.txt` (updateByLine format). **Output is byte-identical to source** (no auto-fixes triggered).

### Closing-tag inventory in current `yat.txt`

| Tag | Count |
|---|---:|
| `</F>` | 2 |
| `</lang>` | 1 |

### What it found in current `yat.txt`

- 0 whitespace trims — byte-identical to source.
- 0 adjacent `</ab> <ab>` — no `<ab>` tag in yat.txt.
- 0 `<ab n="…">` attributes.
- 92 `{{old → new || …}}` correction records present.

### Usage

```
cd yatissues/markup_fix
python 08_markup_fix.py                        # uses csl-orig/v02/yat/yat.txt by default
python 08_markup_fix.py IN.txt OUT.txt         # custom paths
```

Outputs: `yat_fixed.txt`, `markup_fix_changes.txt`, `markup_audit.txt`.

### Summary

Minimal paired tags; essentially clean.

### Severity

`minor`

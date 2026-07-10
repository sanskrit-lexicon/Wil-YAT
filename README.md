# Wil-YAT — Comparison of Wilson and Yates Headwords

_Created: 15-05-2026 · Last updated: 11-07-2026_

A headword-comparison study between two Cologne digitizations — Wilson's
(WIL) and Yates's (YAT) Sanskrit dictionaries — that has already produced
**~400 corrections to Wilson headword spellings and ~800 to Yates**, by
exploiting the fact that Yates's dictionary was explicitly written as a
close revision of Wilson's.

---

## Why this repo exists

Systematic spelling-error detection in the Cologne digitizations mostly
relies on two techniques: the
[faultfinder](https://github.com/funderburkjim/SanskritSpellCheck) approach
(fragment comparison against a reference dictionary) and alphabetical
misordering. This study adds a **third**: since Yates's headword list is
"nearly identical" to Wilson's by the author's own preface, any place their
two headword lists *diverge* is a strong candidate for a digitization error
in one or the other — and this approach catches errors the other two
techniques miss.

The task is not finished — roughly 46,800 headword pairs have been
classified, most trivially (`==`, exact match), but several hundred
"near-match" cases still need manual review (see [TODO](#todo)).

---

## Usage: reproducing the comparison

**Status: the documented pipeline is not directly runnable today.**
[`hwcmp.py`](https://github.com/sanskrit-lexicon/Wil-YAT/blob/main/hwcmp.py) — the first-stage comparison script — is written in
Python 2 syntax (`print "..."` statements, 17 occurrences) and raises a
`SyntaxError` under Python 3, which is the only interpreter available in
this environment. This was verified directly:

```sh
$ python hwcmp.py data/wilhw2.txt data/yathw2.txt force.txt hwcmp_test.txt
  File "hwcmp.py", line 44
    print "%s consecutive duplicate headwords found in %s" % (ndup,filein)
    ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
SyntaxError: Missing parentheses in call to 'print'. Did you mean print(...)?
```

The required input files ([`data/wilhw2.txt`](https://github.com/sanskrit-lexicon/Wil-YAT/blob/main/data/wilhw2.txt),
[`data/yathw2.txt`](https://github.com/sanskrit-lexicon/Wil-YAT/blob/main/data/yathw2.txt), [`force.txt`](https://github.com/sanskrit-lexicon/Wil-YAT/blob/main/force.txt)) **are** all
present and correctly sized (44,577 / 45,205 / 286 lines respectively) — the
blocker is purely the Python 2→3 syntax, not missing data. Porting
`hwcmp.py`'s 17 `print` statements to Python 3 function-call syntax would
make the documented workflow immediately runnable; that port is outside the
scope of this documentation pass.

### What you can verify today: the committed output

The pipeline's outputs **are** committed and readable directly — this is a
real, executed inspection of them (05-07-2026):

```python
import sys
sys.stdout.reconfigure(encoding='utf-8')

counts = {}
with open('hwcmp_adj.txt', encoding='utf-8') as f:
    for line in f:
        parts = line.split()
        if len(parts) >= 2:
            reason = parts[1]
            counts[reason] = counts.get(reason, 0) + 1

for k, v in sorted(counts.items(), key=lambda x: -x[1])[:5]:
    print(k, v)
print('total lines:', sum(counts.values()))
```

Output:

```
== 40668
NONE 4616
=V 743
=V* 299
~= 126
total lines: 46799
```

This matches the [Summary table](#summary-of-hwcmp_adjtxt-categories) below
exactly — confirming [`hwcmp_adj.txt`](https://github.com/sanskrit-lexicon/Wil-YAT/blob/main/hwcmp_adj.txt) is the real, current
final-stage output described in this README, not stale or aspirational
documentation.

---

## Inputs to the comparison

This study is heavily assisted by custom computer programs. These programs
use certain specific forms of the Cologne digitizations of Wilson and Yates
dictionaries. Current versions are in the [`data/`](https://github.com/sanskrit-lexicon/Wil-YAT/tree/main/data) subdirectory of
this repository.

* [`data/wil.txt`](https://github.com/sanskrit-lexicon/Wil-YAT/blob/main/data/wil.txt) is the Cologne digitization of the Wilson
  dictionary. It was drawn from the `wiltxt.zip` download
  [here](http://www.sanskrit-lexicon.uni-koeln.de/scans/WILScan/2014/web/webtc/download.html).
* [`data/wilhw2.txt`](https://github.com/sanskrit-lexicon/Wil-YAT/blob/main/data/wilhw2.txt) is the list of headwords derived from
  `wil.txt`. It is in the `wilxml.zip` download.
* [`data/yat.txt`](https://github.com/sanskrit-lexicon/Wil-YAT/blob/main/data/yat.txt) is the Cologne digitization of the Yates
  dictionary. It was drawn from the `yattxt.zip` download
  [here](http://www.sanskrit-lexicon.uni-koeln.de/scans/YATScan/2014/web/webtc/download.html).
* [`data/yathw2.txt`](https://github.com/sanskrit-lexicon/Wil-YAT/blob/main/data/yathw2.txt) is the list of headwords derived from
  `yat.txt`. It is in the `yatxml.zip` download.
* [`data/wil_mw.txt`](https://github.com/sanskrit-lexicon/Wil-YAT/blob/main/data/wil_mw.txt) has most of the Wilson headwords which
  are roots; it also has a correspondence to headwords of roots in
  Monier-Williams, but this correspondence is not used in the present work.
  It was drawn from
  [here](https://github.com/sanskrit-lexicon/WIL/blob/master/wilmwroots/step2/wil_mw.txt).

---

## Outputs of the comparison, and workflow

The comparison of the Wilson and Yates headwords is done in stages.

* [`hwcmp.txt`](https://github.com/sanskrit-lexicon/Wil-YAT/blob/main/hwcmp.txt) is the first approximation of the correspondence
  between the two headword lists (47,098 lines committed). Documented
  invocation:
  ```sh
  python hwcmp.py data/wilhw2.txt data/yathw2.txt force.txt hwcmp.txt
  ```
  [`force.txt`](https://github.com/sanskrit-lexicon/Wil-YAT/blob/main/force.txt) is an input, as well as the two lists of
  headwords — created by hand to `force` the correspondence between
  certain headwords, needed for cases too subtle for the general
  algorithm.

  Each line of `hwcmp.txt` represents a comparison between 1 or more
  headword records from `wilhw2.txt` and `yathw2.txt`, of the general form
  `<wilson> <reason> <yates>`. For instance `aMSaka:33,35 == aMSaka:98,99`
  indicates that the headword `aMSaka` occurring in the Wilson digitization
  on lines 33-35 corresponds (reason code `==`) to the headword `aMSaka`
  occurring in the Yates digitization on lines 98,99. A slight variation
  `a:7,8;a:9,15 == a:85,92` shows two Wilson entries corresponding to one
  combined Yates entry — the first use of `force.txt`, since `hwcmp.py`
  cannot make such a subtle comparison alone.

  The `<reason>` code classifies the correspondence. `hwcmp.py` itself
  assigns only three:
  * `==` — corresponding headwords identically spelled (by far the most
    common case, 40,668 of 46,799 in the final output).
  * `~=` — spelled *almost* identically (edit distance 1).
  * `NONE` — the program believes a headword appears only in Wilson
    (`afRin:18,21 NONE MISSING`) or only in Yates
    (`MISSING NONE aMSumatI:120,121`).

  Later steps introduce several other programmatically assigned reason
  codes.

* [`hwcmp_near.txt`](https://github.com/sanskrit-lexicon/Wil-YAT/blob/main/hwcmp_near.txt) extracts the approximate-match cases
  from `hwcmp.txt`:
  ```sh
  python hwnear_init.py hwcmp.txt hwcmp_near.txt
  ```
  A simple convenience step; no analysis performed here.

* [`hwcmp_near_analyze.txt`](https://github.com/sanskrit-lexicon/Wil-YAT/blob/main/hwcmp_near_analyze.txt) classifies the
  approximate matches into categories:
  ```sh
  python analyze_near.py hwcmp_near.txt hwcmp_near_analyze.txt data/wil_mw.txt
  ```
  This sub-categorizes the approximate-match reason based on systematic
  spelling-convention differences between Wilson and Yates:

  | Code | Meaning |
  |---|---|
  | `=V` | Roots, spelled slightly differently — Wilson typically ends in `a`, Yates drops it. Uses `wil_mw.txt` to confirm the Wilson headword is marked as a root. |
  | `=vb` | One spells with `v`, the other `b` (or vice versa) — some may be errors, but many are legitimate alternate spellings. |
  | `=rxx` | One doubles a consonant after `r`, the other doesn't — believed both correct. |
  | `=cC` | `cC` vs `C` — believed both correct. |
  | `=tt` | `tt` vs `t` — probably both correct. |
  | `=nasal` | e.g. `apANkta` vs `apAMkta` — believed both correct. |
  | `=mM$` | e.g. `ayaTAbalam` vs `ayaTAbalaM` — believed both correct. |
  | `=aA` | e.g. `kaSeruka` vs `kaSerukA` — Wilson shows multiple genders, Yates just the feminine; considered corresponding, but flagged for review. |
  | `=sH` | e.g. `kAmakAratas` vs `kAmakArataH` — probably both correct. |
  | `=a` | Small list (4) where one spelling adds a final `a` — flagged for re-examination. |
  | `~=` (unclassified) | None of the systematic correspondences apply — may be a real misspelling, needs manual review. |

* [`hwcmp_adj.txt`](https://github.com/sanskrit-lexicon/Wil-YAT/blob/main/hwcmp_adj.txt) installs the correspondences of
  `hwcmp_near_analyze.txt` into `hwcmp.txt` and does further multi-record
  adjustments — the final output of the comparison process:
  ```sh
  python hwcmp_adj.py hwcmp.txt hwcmp_near_analyze.txt hwcmp_adj.txt
  ```
  Example adjustment — Wilson's `lAja` had two entries; one (a root) is
  re-labelled `=V*` to correspond with Yates's `lAj`, the other stays `==`:
  ```
  BEFORE
  MISSING NONE lAj:48823,48824
  lAja:141031,141034 == lAja:48825,48827
  lAja:141035,141038 NONE MISSING

  AFTER
  MISSING NONE MISSING
  lAja:141031,141034 =V* lAj:48823,48824
  lAja:141035,141038 == lAja:48825,48827
  ```

---

## Corrections

The current inputs (`wilhw2.txt`, `yathw2.txt`, etc.) already reflect
corrections discovered by examining the `~=` cases. The corrections found
so far are in [`wil_corr.txt`](https://github.com/sanskrit-lexicon/Wil-YAT/blob/main/wil_corr.txt) and
[`yat_corr.txt`](https://github.com/sanskrit-lexicon/Wil-YAT/blob/main/yat_corr.txt), in the standard org-wide
`updateByLine.py` change-file format (see the canonical
[correction workflow](https://github.com/sanskrit-lexicon/csl-corrections/blob/main/docs/correction-workflow.md)). Sample, from `wil_corr.txt`:

```
; 03/06/2015 sudusmaha -> sudussaha (typo, m/s confusion)
182108 old .{#sudusmaha#}¦ mfn. ({#-haH-hA-haM#}) Very difficult to be endured.
182108 new .{#sudussaha#}¦ mfn. ({#-haH-hA-haM#}) Very difficult to be endured.
182109 old .E. {#su#} very, {#dusmaha#} unendurable.
182109 new .E. {#su#} very, {#dussaha#} unendurable.
```

Wilson corrections were generally typos (digitization errors); Yates
corrections were generally print errors (errors in the scanned image).

[`dump_cases.py`](https://github.com/sanskrit-lexicon/Wil-YAT/blob/main/dump_cases.py) makes the manual review workflow more
efficient: a batch of `~=` cases is offloaded to a scratch file (see
[`scratch/`](https://github.com/sanskrit-lexicon/Wil-YAT/tree/main/scratch)), then dumped with page context from both
dictionaries for side-by-side comparison:

```sh
python dump_cases.py scratch/temp.txt scratch/temp_dump.txt \
  data/wil.txt data/yat.txt data/wilhw2.txt data/yathw2.txt
```

The multidictionary lookup
[hwnorm1](http://www.sanskrit-lexicon.uni-koeln.de/scans/awork/hwnorm/hwnorm1.php)
is sometimes useful for confirming a suspected error.

---

## Summary of hwcmp_adj.txt categories

Frequency of the `<reason>` categories in the current [`hwcmp_adj.txt`](https://github.com/sanskrit-lexicon/Wil-YAT/blob/main/hwcmp_adj.txt)
(46,799 lines total — independently re-counted 05-07-2026, see
[Usage](#usage-reproducing-the-comparison) above):

| reason | count |
|---|---:|
| `==` | 40668 |
| `NONE` | 4616 |
| `=V` | 743 |
| `=V*` | 299 |
| `~=` | 126 |
| `=vb` | 110 |
| `=rxx` | 82 |
| `=aA` | 40 |
| `=tt` | 33 |
| `=nasal` | 30 |
| `=cC` | 23 |
| `=?` | 11 |
| `=mM$` | 7 |
| `=sH$` | 7 |
| `=a` | 4 |

---

## TODO

* Independent review of `yat_corr.txt` and `wil_corr.txt` would likely turn
  up a few places where a solution was in error — hopefully most
  corrections are correct.
* Systematic evaluation of the `~=` sub-cases in `hwcmp_adj.txt` will turn
  up additional corrections and correspondences — e.g. `sEnDavaGana ~=
  sEnDavaDana` looks like a missed correction to Yates; `ambuvAhin ~=
  ambuvAhinI` may just need relabelling (Yates shows only the feminine
  form); `agnideva`/`agnidevA` and a run of verb entries around `ag`/`aga`
  likely need `force.txt` additions for manual correspondence.
* Porting [`hwcmp.py`](https://github.com/sanskrit-lexicon/Wil-YAT/blob/main/hwcmp.py) from Python 2 to Python 3 syntax (see
  [Usage](#usage-reproducing-the-comparison)) would make the whole pipeline
  runnable end-to-end again.
* A similar comparison between Shabda-Sagara (SHS) and Wilson-Yates would
  likely turn up further headword corrections in SHS, which is also closely
  based on Wilson.

If anyone wants to help, open an issue — displays or extensions to
`dump_cases.py` are plausible next steps.

---

## Front matter (prefaces)

OCR transcriptions of the title pages and prefaces of both dictionaries,
with Russian translations, live in [`prefaces/`](https://github.com/sanskrit-lexicon/Wil-YAT/tree/main/prefaces). Both sources
are in English, so the source page *is* the English text (no `.en.md`);
Russian is supplied alongside.

- **WIL** (H. H. Wilson, 2nd ed., Calcutta 1832) — 6 pages: title,
  dedication, 4-page preface. Consolidated:
  [wilpref_all.en.md](https://github.com/sanskrit-lexicon/Wil-YAT/blob/main/prefaces/wilpref_all.en.md) ·
  [wilpref_all.ru.md](https://github.com/sanskrit-lexicon/Wil-YAT/blob/main/prefaces/wilpref_all.ru.md).
- **YAT** (W. Yates, Calcutta 1846) — 3 pages: title, 2-page Author's
  Preface (completed posthumously by J. Wenger). Consolidated:
  [yatpref_all.en.md](https://github.com/sanskrit-lexicon/Wil-YAT/blob/main/prefaces/yatpref_all.en.md) ·
  [yatpref_all.ru.md](https://github.com/sanskrit-lexicon/Wil-YAT/blob/main/prefaces/yatpref_all.ru.md).

See [`prefaces/README.md`](https://github.com/sanskrit-lexicon/Wil-YAT/blob/main/prefaces/README.md) for the per-page index and
conventions.

> **Front-matter OCR run notes.**
> **Method:** scans pulled from Cologne csldoc; each page cropped at native
> resolution into overlapping horizontal bands (≤1900 px) with PIL and
> transcribed page-by-page — never reading downsampled full pages. Russian
> translations authored per page.
>
> **Sources:** WIL scans are JPG (1067×1500); YAT scans are full-resolution
> PNG (2920×4549). YAT pages 2–3 correspond to scanned image pages 003–004
> (page 002 is blank).
>
> **Consolidation:** `build_combined.py` (`DICT=wil`, then `DICT=yat`). Its
> page-glob was corrected from `<code>pref[0-9][0-9].md` to
> `<code>[0-9][0-9].md` to match the `wil01.md` / `yat01.md` naming actually
> used here; without that fix the consolidated files came out empty.
>
> **Faithfulness:** original 19th-c. spelling kept verbatim (*Sanscrit,
> knowlege, shew, superintendance*). One faint glyph on YAT p. iv (the "2."
> before the second-conjugation abbreviations) was read in context;
> everything else was legible. No `[?]` placeholders were needed.
>
> **Model:** Claude Opus 4.8 (1M context). All steps synchronous, no
> subagents; temp crop tiles deleted after build.

---

_Dr. Mārcis Gasūns_

# RPL-ClusterIDS — REFERENCES AUDIT

**Phase:** 1.5  
**Bibliography file:** `bib/references.bib`  
**Total entries:** 49  
**Cited in manuscript (`sections/*.tex`):** ~30 unique keys  
**Target:** ≤45 strong, verified references

---

## Summary Statistics

| Category | Count |
|----------|------:|
| IEEE IoT Journal / IEEE Access | 8 |
| IEEE ComST / surveys | 6 |
| Computer Networks | 7 |
| IETF RFC / misc | 10 |
| Inproceedings | 5 |
| Recent (2023–2025) | 8 |
| Pre-2015 (foundational) | 12 |
| Flagged for verification | 5 |
| Uncited (orphan) | ~19 |

---

## Action Summary

| Action | Count |
|--------|------:|
| **KEEP** (verified or standard) | 38 |
| **VERIFY** (metadata uncertain) | 5 |
| **FIX** (wrong type / placeholder pages) | 3 |
| **REMOVE or MERGE** (orphan / duplicate survey) | 3 |

---

## Entries Requiring Immediate Action

| Key | Issue | Action | Priority |
|-----|-------|--------|----------|
| `lloret2016iot` | Pages « 1–20 » generic; note says verify | **VERIFY** DOI and page range | P1 |
| `haddad2015rpl` | Note « Verify bibliographic details » | **VERIFY** or replace with stronger RPL security ref | P1 |
| `amjad2018rpl` | Note « Verify before submission » | **VERIFY** DOI | P1 |
| `raza2018cluster` | Pages 12345–12358 look placeholder | **FIX** — find correct IEEE Access pages or **REMOVE** | P0 |
| `neumann2012rpl` | Mis-typed as `@article`; is RFC 6206 Trickle | **FIX** → `@misc` like other RFCs | P2 |
| `anton2014rpl` | Key says 2014, year field is 2024 | **FIX** key rename to `anton2024rpl` + update cite | P2 |
| `butun2014idswsn` vs `faheem2013` | Overlapping WSN IDS surveys | **MERGE** — keep faheem2013, remove butun if uncited | P3 |

---

## Verified / Strong References (KEEP)

| Key | Year | Category | Journal / Source | DOI | Relevance | Decision |
|-----|------|----------|------------------|-----|-----------|----------|
| `rfc6550` | 2012 | RPL protocol | IETF RFC | — | Core | KEEP |
| `rfc7416` | 2015 | RPL security | IETF RFC | — | Threat model | KEEP |
| `mayzaud2016` | 2016 | RPL attacks | IEEE ComST | — | High | KEEP |
| `raza2017` | 2017 | RPL IDS | **IEEE IoT J.** | — | **Primary baseline** | KEEP |
| `sfar2018` | 2018 | IoT IDS survey | **IEEE IoT J.** | — | Related work | KEEP |
| `hindy2020` | 2020 | ML IDS | **IEEE IoT J.** | — | Baseline | KEEP |
| `garg2023` | 2023 | Hybrid IDS | JNCA | — | Baseline | KEEP |
| `hamdi2024` | 2024 | Deep learning RPL IDS | Computer Networks | — | Recent | KEEP |
| `shahid2024hybrid` | 2024 | Hybrid ML/DL RPL | IEEE Access | 10.1109/ACCESS.2024.3442529 | Recent | KEEP |
| `emec2023rout4` | 2023 | Dataset | IEEE DataPort | 10.21227/3mbe-5j70 | Dataset ref | KEEP |
| `dib2024` | 2024 | RPL-IDS dataset | Sensors | — | Related work | KEEP |
| `raza2020rplids` | 2020 | RPL attack survey | Computer Networks | — | Threat model | KEEP |
| `oikonomou2022contik` | 2022 | Contiki-NG | Internet of Things | — | Implementation | KEEP |
| `osterlind2006cooja` | 2006 | Cooja | IEEE LCN | — | Evaluation | KEEP |
| `heinzelman2000` | 2000 | LEACH | HICSS | — | Clustering | KEEP |
| `heinzelman2002` | 2002 | LEACH-T | IEEE TWC | — | Clustering | KEEP |
| `karlof2003` | 2003 | Routing attacks | Ad Hoc Networks | — | Threat model | KEEP |
| `hu2006` | 2006 | Wormhole | IEEE JSAC | — | Threat model | KEEP |
| `granjal2015rplsec` | 2015 | IoT security survey | IEEE ComST | — | Intro | KEEP |
| `yan2014iotsec` | 2014 | IoT security | Computer Networks | — | Intro | KEEP |
| `sicari2015security` | 2015 | IoT trust | Computer Networks | — | Intro | KEEP |
| `faheem2013` | 2013 | WSN IDS survey | IEEE ComST | — | Intro | KEEP |
| `beno2018qosrpl` | 2018 | QoS RPL | Computer Networks | — | Architecture | KEEP |
| `baronti2011` | 2007 | WSN survey | Computer Comm. | — | Intro | KEEP |
| `winter2012` | 2012 | RPL overview | IEEE IoT proc. | — | Intro | KEEP |
| `debar1999taxonomy` | 1999 | IDS taxonomy | Computer Networks | — | Optional KEEP | KEEP |

---

## Recent References (2023–2025) — Target Area

| Key | Year | Topic | KEEP |
|-----|------|-------|------|
| `garg2023` | 2023 | Hybrid rule-ML RPL IDS | ✓ |
| `emec2023rout4` | 2023 | ROUT-4 dataset | ✓ |
| `hamdi2024` | 2024 | Hybrid DL RPL IDS | ✓ |
| `shahid2024hybrid` | 2024 | ML/DL RPL IDS | ✓ |
| `dib2024` | 2024 | RPL-IDS behavior dataset | ✓ |
| `anton2014rpl` | 2024 | Version-number attacks | ✓ (fix key) |

**Gap:** Consider adding 2–3 more 2024–2025 refs on *hierarchical* or *energy-aware* IoT IDS if page count allows (only after verifying DOI). Do not add unverified entries.

---

## Uncited Orphans (Candidate REMOVE)

These entries exist in `references.bib` but are **not cited** in active `sections/*.tex`:

| Key | Year | Reason | Decision |
|-----|------|--------|----------|
| `alrawais2017iotsec` | 2017 | Uncited | REMOVE or cite in related work |
| `anwar2019iotids` | 2019 | Uncited | REMOVE |
| `bankovic2010anomaly` | 2010 | Uncited | REMOVE |
| `banerjee2012wsn` | 2012 | Overlaps faheem2013 | REMOVE |
| `butun2014idswsn` | 2014 | Overlaps faheem2013 | REMOVE |
| `dhar2014wsnsec` | 2014 | Uncited | REMOVE |
| `dunkels2004contiki` | 2004 | Uncited (oikonomou2022 sufficient) | REMOVE |
| `ferrag2020deep` | 2020 | Uncited | REMOVE or cite |
| `gomez2017ipv6` | 2017 | Uncited | REMOVE |
| `le2013lln` | 2013 | Uncited | REMOVE |
| `lloret2016iot` | 2016 | Uncited + unverified | REMOVE unless verified |
| `haddad2015rpl` | 2015 | Uncited + unverified | REMOVE unless verified |
| `amjad2018rpl` | 2018 | Uncited + unverified | REMOVE unless verified |
| `papadopoulos2014attacks` | 2014 | Uncited | REMOVE |
| `perazzo2010trust` | 2010 | Uncited | REMOVE |
| `rfc4944`, `rfc6551`, `rfc7228` | various | Uncited RFCs | REMOVE |
| `shelby2014coap`, `thubert2015tsch` | various | Uncited | REMOVE |

**After cleanup:** ~30–35 cited + strong entries → within 45 max target with room for 2–3 new verified refs.

---

## Duplicate / Overlap Detection

| Pair | Overlap | Recommendation |
|------|---------|----------------|
| `faheem2013` / `butun2014idswsn` / `banerjee2012wsn` | WSN IDS surveys | Keep `faheem2013` only |
| `yan2014iotsec` / `sicari2015security` / `lloret2016iot` | IoT security surveys | Keep yan + sicari; drop lloret |
| `granjal2015rplsec` / `raza2020rplids` | RPL security | Both OK (general vs RPL-specific) |
| `raza2017` / `raza2020rplids` / `raza2018cluster` | Same author group | Keep 2017 + 2020; fix/remove 2018cluster |

---

## Citation Coverage by Section

| Section | Cite keys used |
|---------|----------------|
| Introduction | rfc6550, baronti2011, winter2012, mayzaud2016, raza2017, rfc7416, faheem2013, sfar2018, hindy2020, garg2023, heinzelman2000, heinzelman2002 |
| Related work | mayzaud2016, raza2017, sfar2018, granjal2015rplsec, yan2014iotsec, sicari2015security, raza2020rplids, anton2014rpl, hindy2020, hamdi2024, shahid2024hybrid, emec2023rout4, garg2023, heinzelman2000, heinzelman2002, raza2018cluster, dib2024 |
| Threat model | mayzaud2016, rfc7416, karlof2003, hu2006, raza2017 |
| Architecture | beno2018qosrpl |
| Implementation | oikonomou2022contik |
| Experimental setup | oikonomou2022contik, osterlind2006cooja |

**Missing citation opportunities (optional, no new claims):**
- `debar1999taxonomy` — IDS taxonomy in intro
- `dunkels2004contiki` — historical Contiki (if space)

---

## Pre-Submission Verification Protocol

For each `\cite{key}` in manuscript:

1. Confirm BibTeX key resolves (no `?` in PDF)
2. Confirm DOI via https://doi.org/ (where applicable)
3. Confirm journal name matches IEEE style
4. Confirm year matches published version
5. Remove all `@article` entries that are actually RFCs

**Entries with confirmed DOI in bib:**
- `shahid2024hybrid` — 10.1109/ACCESS.2024.3442529 ✓
- `emec2023rout4` — 10.21227/3mbe-5j70 ✓

---

## Recommended Final Count

| Stage | Count |
|-------|------:|
| Current bib | 49 |
| Remove orphans | −15 |
| Fix/remove bad entries | −2 |
| Add 2 verified 2024–2025 hierarchical IDS | +2 |
| **Target** | **~34–36 cited, ≤45 in bib** |

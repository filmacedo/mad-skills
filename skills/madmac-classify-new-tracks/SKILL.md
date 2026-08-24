---
name: madmac-classify-new-tracks
description: Process newly-added tracks in Filipe's madmac rekordbox library — recover original Genre tags, classify with the 8-family + Energy + Crowd taxonomy, and apply to rekordbox. Use this skill whenever Filipe says he added new music, downloaded new tracks, has new tracks to classify, mentions recently-added tracks, asks to process new music, mentions pre-gig prep, gig prep, or otherwise indicates fresh music has landed in his library and needs to be tagged. Also trigger on phrases like "new tracks", "classify recently added", "pre-gig", "I added music", "got new music", "process new tracks", or anything implying fresh ingestion into the rekordbox library.
---

# madmac-classify-new-tracks

This skill walks through the canonical flow for ingesting newly-added tracks into Filipe's madmac rekordbox library. The library uses a custom 8-family Genre system, Energy My Tag, Crowd My Tag, and Rating (performance verdict). New tracks land with raw Beatport/Bandcamp Genre tags that need to be replaced with one of the 8 families, plus Energy and Crowd tagging.

## Library context

- **Workspace**: `/Users/macedo/Documents/claude-cowork/madmac/`
- **Schema doc**: `dj-system.md` — read this if you need a refresher on the taxonomy
- **Scripts**: `music-library/scripts/`
- **Pyrekordbox**: installed in user's main Python env (NOT in the Cowork sandbox — every script runs on the user's machine via `python3 <script>`)

## Taxonomy

**8 families** (Genre):
```
deep-electronica  afro-tropical  classic-house  tech-house
techno-electro    indie-dance    disco-pop      dj-tools
```

**6 Energy values** (My Tag):
```
1-lounge  2-opener  3-build-up  4-peak  5-build-down  6-morning
```

**Crowd values** (My Tag):
```
crowd-pleaser  acquired-taste
```

Only set `crowd-pleaser` automatically (genuinely anthemic, broad appeal). Never auto-assign `acquired-taste` — that's reserved for explicit user judgment.

## Workflow

### Step 1: Confirm rekordbox is quit

Pyrekordbox can read while rekordbox is running but writes can fail or corrupt the master.db. Before any other step, actively check:

```bash
pgrep -fi rekordbox
```

If the command returns a PID, rekordbox is running. Stop and ask the user explicitly:

> "rekordbox is currently running. Please quit it (Cmd+Q in rekordbox) before I proceed — writes can corrupt the database. Let me know when it's closed."

Wait for the user to confirm they've quit before continuing. Re-check with `pgrep -fi rekordbox` after they confirm — if still running, tell them and wait again.

If `pgrep` returns nothing on the first check, just say "rekordbox is closed, proceeding" and continue.

Don't skip this check — it's the single most important safeguard in the flow.

### Step 2: Recover original Genre tags

```
cd ~/Documents/claude-cowork/madmac/music-library/scripts
python3 recover-original-genres.py
```

Reads each track's actual ID3/Vorbis Genre from disk and writes `[id3:OriginalGenre]` to rekordbox Comments. Idempotent — only touches tracks that don't already have the marker. This is important: the original Beatport/Bandcamp tag is the most reliable classification signal.

### Step 3: Export for classification

Default scope: tracks added in last 7 days that don't have a family Genre.

```
python3 export-for-classification.py --days 7
```

Useful flag variations:
- `--days N` — different time window
- `--include-tagged` — also enrich Energy/Crowd on tracks that already have a family Genre
- `--missing-energy --min-rating N` — backfill Energy on tracks with family but no Energy My Tag, scoped by rating
- `--with-discogs` — live Discogs API lookup per track (slow: ~1 sec/track; only use when id3_genre column is mostly empty)

Output: `archive/classification-todo.csv` with columns `TrackID, Rating, Artist, Title, BPM, Key, FolderPath, id3_genre, cached_discogs_genre, cached_discogs_styles, family, energy, crowd, comments_extra, notes`. `family` may be pre-filled if the track already has a family Genre in rekordbox.

### Step 4: Classify the tracks (this is the LLM's job — yours, Claude)

Read `archive/classification-todo.csv`. For each row, decide `family` (if blank), `energy`, and `crowd` (only if anthemic).

**Family signals, in priority order:**
1. `id3_genre` — the original Beatport/Bandcamp tag, most reliable
2. `cached_discogs_genre` / `cached_discogs_styles` — fallback signal
3. Your own knowledge of the artist + track

Map common ID3 tags to families:
- `Tech House`, `Minimal/Tech House` → `tech-house`
- `Techno`, `Hard Techno`, `Industrial Techno` → `techno-electro`
- `Electro House`, `Electro` → `techno-electro` or `indie-dance` depending on energy
- `House`, `Deep House`, `Garage`, `Soulful House` → `classic-house`
- `Indie Dance / Nu Disco`, `Laser Disco`, `Sexy Bassline` → `indie-dance`
- `Disco`, `Funk / R&B`, `Pop / Rock` → `disco-pop`
- `Afro House`, `Afro Tech`, `Tribal` → `afro-tropical`
- `Drum & Bass`, `Breaks`, `Bass` → `indie-dance` (usually) or `dj-tools` if it's an edit
- `DJ Tools`, `Acapella`, `Intro` → `dj-tools`
- `Melodic House & Techno` → `deep-electronica` if at <125 BPM and atmospheric, else `techno-electro`
- `Mac n Cheesy`, `Pumpin' Rave` (legacy MAD MAC categories) → use BPM + your knowledge

**Energy signals:**

Use BPM as a baseline (BPM is `int×100` in the CSV, so 12400 = 124.00 BPM):
- BPM <115 → `1-lounge`
- 115-122 → `2-opener`
- 120-126 → `3-build-up`
- 124-130 → `4-peak`

`5-build-down` and `6-morning` are highly contextual — never auto-assign, default to `4-peak` or `3-build-up`. Assign 5/6 only when the user has explicitly told you the track is for that slot.

Refine with family + track knowledge:
- `classic-house` at 122 leans `3-build-up`
- `deep-electronica` at 122 leans `2-opener` (deep, atmospheric)
- `tech-house` at 124-126 with driving groove → `3-build-up` or `4-peak` depending on energy
- `techno-electro` at 126-130 → almost always `4-peak`
- `indie-dance` at 118-122 → `2-opener`
- `indie-dance` at 124-128 with peak energy → `4-peak`
- `disco-pop` at 115-122 → `2-opener` or `1-lounge` if chill
- Pop classics at low BPM (Britney, Backstreet Boys, MJ classics, Madonna) → `1-lounge` with `crowd-pleaser`
- DJ tools / acapellas / intros → `2-opener`, no crowd tag
- Drum & bass / >140 BPM → `4-peak`

**Crowd signals:**

Tag `crowd-pleaser` ONLY for tracks that are genuinely anthemic — recognizable hooks, broad appeal, "everyone knows this." Examples:
- Mainstream pop classics (Madonna, Britney, MJ, etc.)
- Massive house anthems (Disclosure F For You, Robin S Show Me Love, Kings of Tomorrow Finally, etc.)
- Recent viral tracks (Fisher Losing It, Cola Elderbrook/CamelPhat)
- Cheesy peak novelties (Stardust Music Sounds Better, Gigi D'Agostino, Pump Up The Jam)

Leave `crowd` blank for everything else. Never tag `acquired-taste` automatically.

### Step 5: Write classification-done.csv

Generate a Python script `archive/_classify_chunk_<label>.py` mirroring the existing `_classify_chunk_A.py` through `_classify_chunk_E.py` patterns. The script:

1. Defines `CLS = {TrackID: (family, energy, crowd, notes)}` — or the 2-tuple `(energy, crowd)` if family is already set
2. Loads `classification-done.csv` and preserves rows with `energy` already filled (idempotency — only check `row.get("energy")`, NOT family, since family is sometimes blank in todo.csv even after classification)
3. Iterates `classification-todo.csv`, applies `CLS` to each matching row
4. Writes back to `classification-done.csv`

For new-track ingestion (most common case), the family column will be blank — the script needs to set `family`, `energy`, and `crowd`. Use the 4-tuple pattern.

### Step 6: Apply classification

Tell the user to run:
```
python3 apply-classification.py --dry-run
python3 apply-classification.py
```

Writes Genre + Energy + Crowd + Comments to rekordbox. Auto-backs up master.db before write.

### After Step 6: stop here

The skill ends after `apply-classification.py`. Crate curation (adding tracks to `EARLY 00X - all`) is a manual step the user does at their own pace after classification — don't automate it. Once they're done curating, they'll run `sync-early-crate.py` themselves.

## Chunking

For >150 tracks in one batch, split into chunks of ~150-200:
- Sort by Rating desc so high-confidence tracks come first
- Each chunk gets its own `_classify_chunk_<label>.py`
- Each chunk preserves prior chunks via the `preserved` dict (only check `row.get("energy")` — `family` is sometimes blank in todo.csv even after classification)
- Apply between chunks for incremental commits

For ≤150 tracks (the typical "new tracks since last gig" case), one chunk is fine. Don't over-engineer.

## Verification

After applying, suggest:
```
python3 count-rating-classified.py --min 0
```

To verify zero tracks remain unclassified.

## Why each step matters

- **recover-original-genres.py first**: Captures Beatport tag before classification can overwrite it. Once lost, recovering requires reading from disk again — fine for new tracks, but cleaner to do upfront.
- **export then classify**: Separates I/O from judgment. The classify step is where the LLM's track knowledge matters; everything else is mechanical.
- **CLS dict pattern**: Makes the classifications auditable and re-runnable. If you misclassify something, the user can edit the script and re-apply.
- **Apply via separate script**: Keeps writes to rekordbox isolated, auto-backs up master.db, easy to dry-run.

## Common pitfalls

- **Don't substring-match family names** when reading id3_genre. "electro" matches inside "electronic" — use word-boundary checks or sort keys longest-first.
- **Don't bulk-classify by BPM alone** — the user has explicitly rejected this. Use track-level judgment.
- **Don't auto-assign 5-build-down or 6-morning** — those are contextual and stay manual.
- **Don't auto-tag `acquired-taste`** — only `crowd-pleaser` is automatic.
- **Cap `4-peak` predictions** — 4-peak is high-stakes; only assign when the track is genuinely peak material.

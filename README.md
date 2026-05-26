# Journeymap Merger And Preview

Utilities for merging JourneyMap data and generating local preview images from multiple map roots.

## Preview Usage

This project uses the preview script with a fixed rendering method for:
- layer: `overworld/day`
- coordinate transform: `flipz`

Run with one or more JourneyMap root folders:

```powershell
python .\preview_tiles.py ".\FIrst Time\OUTPUT" ".\FIrst Time\Yoinky~SMP" ".\FIrst Time\SMPGoulart" -o ".\final-preview"
```

What it generates:
- one preview PNG per input root
- one merged preview PNG combining all provided roots

Output naming:
- `<MapName>__overworld_day_flipz.png`
- `merged__overworld_day_flipz.png`

Notes:
- On Windows, do not end quoted paths with a trailing backslash.
- If a provided root has no `overworld/day` tiles, it is skipped.

## Credit

Core merge components used in this project are based on work from:
- Lopolin-LP: https://github.com/Lopolin-LP/journeymap-data-merger

Specifically credited sources:
- `JourneyMapMerger.py`
- `CompareFolders.py`

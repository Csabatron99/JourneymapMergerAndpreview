# Journeymap Merger And Preview

Merge JourneyMap map and waypoint data from multiple devices/timestamps and generate local preview images to validate results before importing.

## Credits

This project is based on and includes adapted merger components from:
- Lopolin-LP: https://github.com/Lopolin-LP/journeymap-data-merger

Specifically credited files:
- `JourneyMapMerger.py`
- `CompareFolders.py`

## Requirements

1. Install Python: https://www.python.org/
2. Install ImageMagick: https://imagemagick.org/
3. Install Python packages:

```powershell
pip install tqdm wand ipython
pip install --pre --only-binary=:all: amulet-nbt==5.0.0a1.post250609154640
```

Note: If your environment supports `amulet-nbt==5.0.1a1`, you can use that instead.

## Map + Waypoint Merge Usage

Run merger:

```powershell
python .\JourneyMapMerger.py "<Output Path>" "<Input Path 1>" "<Input Path 2>" "<Input Path N>"
```

Example:

```powershell
python .\JourneyMapMerger.py ".\FIrst Time\OUTPUT" ".\FIrst Time\Yoinky~SMP" ".\FIrst Time\SMPGoulart" ".\FIrst Time\SMPLigua"
```

After completion, the merged data is in the output folder.

## Preview Usage

`preview_tiles.py` renders preview PNGs from one or more JourneyMap roots using the verified method:
- layer: `overworld/day`
- coordinate transform: `flipz`

Run preview renderer:

```powershell
python .\preview_tiles.py ".\FIrst Time\OUTPUT" ".\FIrst Time\Yoinky~SMP" ".\FIrst Time\SMPGoulart" -o ".\final-preview"
```

Generated files:
- one PNG per input root
- one merged PNG across all provided roots

Output naming:
- `<MapName>__overworld_day_flipz.png`
- `merged__overworld_day_flipz.png`

## Finding JourneyMap Folders

### Option 1: Export from JourneyMap UI
1. Open Minecraft world/server.
2. Open JourneyMap settings from fullscreen map.
3. Use Import/Export and export data.
4. Extract the zip and use extracted folder paths as merge inputs.

### Option 2: Use files directly
Typical structure inside Minecraft folder:

- `journeymap/data/mp/<ServerName>/...`
- `journeymap/data/sg/<WorldName>/...`

The root you pass to scripts should be the folder containing:
- `overworld`
- `the_nether` / `the_end` (if present)
- `waypoints`

## Replacing JourneyMap Data

### Option 1: Import in JourneyMap
Use JourneyMap Import and point it to the merged output data.

### Option 2: Replace folder manually
Rename existing map folder as backup, then copy merged output folder in its place.

## Notes and FAQ

### Invalid directories or weird path errors
On Windows, do not end quoted paths with a trailing backslash.

Bad:
```powershell
".\FIrst Time\OUTPUT\"
```

Good:
```powershell
".\FIrst Time\OUTPUT"
```

### I cannot overwrite JourneyMap folder directly
Rename old folder first, then copy merged output folder.

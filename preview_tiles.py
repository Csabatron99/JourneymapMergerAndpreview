import argparse
import re
from pathlib import Path
from typing import Dict, List, Tuple

from PIL import Image


PATTERN = re.compile(r"^(-?\d+),(-?\d+)\.png$")
Tile = Tuple[int, int, Path]
LAYER = Path("overworld/day")
LAYER_SLUG = "overworld_day_flipz"


def collect_tiles(tile_dir: Path) -> List[Tile]:
    tiles: List[Tile] = []
    for p in tile_dir.glob("*.png"):
        m = PATTERN.match(p.name)
        if m:
            x, z = map(int, m.groups())
            # Fixed transform selected by user: flip z axis.
            z = -z
            tiles.append((x, z, p))
    return tiles


def stitch_to_canvas(
    tiles: List[Tile],
    out_file: Path,
    min_x: int,
    max_x: int,
    min_z: int,
    max_z: int,
    tw: int,
    th: int,
    background: Tuple[int, int, int, int],
):
    canvas = Image.new("RGBA", ((max_x - min_x + 1) * tw, (max_z - min_z + 1) * th), background)

    for x, z, p in tiles:
        with Image.open(p).convert("RGBA") as img:
            px = (x - min_x) * tw
            py = (max_z - z) * th
            canvas.alpha_composite(img, (px, py))

    out_file.parent.mkdir(parents=True, exist_ok=True)
    canvas.save(out_file)
    print(f"Saved: {out_file}")


def sanitize_name(name: str) -> str:
    cleaned = re.sub(r"[^A-Za-z0-9._~-]+", "_", name).strip("_.")
    return cleaned or "map"


def bounds_from_tiles(tiles: List[Tile]) -> Tuple[int, int, int, int]:
    min_x = min(t[0] for t in tiles)
    max_x = max(t[0] for t in tiles)
    min_z = min(t[1] for t in tiles)
    max_z = max(t[1] for t in tiles)
    return min_x, max_x, min_z, max_z


def merge_tiles(map_entries) -> List[Tile]:
    merged: Dict[Tuple[int, int], List[Path]] = {}
    for _, _, tiles in map_entries:
        for x, z, p in tiles:
            merged.setdefault((x, z), []).append(p)

    out: List[Tile] = []
    for (x, z), paths in merged.items():
        if len(paths) == 1:
            out.append((x, z, paths[0]))
            continue

        # Build a temporary composited tile from all maps (argument order wins on top).
        with Image.open(paths[0]).convert("RGBA") as base_img:
            combined = base_img.copy()
        for p in paths[1:]:
            with Image.open(p).convert("RGBA") as img:
                combined.alpha_composite(img)

        temp_dir = Path(__file__).resolve().parent / "previews" / ".merged_tiles"
        temp_dir.mkdir(parents=True, exist_ok=True)
        temp_path = temp_dir / f"{x},{z}.png"
        combined.save(temp_path)
        out.append((x, z, temp_path))

    return out


def main():
    parser = argparse.ArgumentParser(description="Render JourneyMap previews from multiple map roots.")
    parser.add_argument(
        "map_roots",
        nargs="+",
        help="One or more JourneyMap map root folders (example: .\\FIrst Time\\OUTPUT)",
    )
    parser.add_argument(
        "-o",
        "--output-dir",
        default=None,
        help="Where previews are written. Defaults to a 'previews' folder beside this script.",
    )
    args = parser.parse_args()

    script_dir = Path(__file__).resolve().parent
    output_dir = Path(args.output_dir) if args.output_dir else (script_dir / "previews")

    map_entries = []
    for root_str in args.map_roots:
        root = Path(root_str).expanduser().resolve()
        tile_dir = root / LAYER
        tiles = collect_tiles(tile_dir)
        if not tiles:
            print(f"Skipped (no tiles): {tile_dir}")
            continue
        map_entries.append((root, tile_dir, tiles))

    if not map_entries:
        raise SystemExit("No input maps had matching tiles in overworld/day.")

    all_tiles = [tile for _, _, tiles in map_entries for tile in tiles]
    shared_min_x, shared_max_x, shared_min_z, shared_max_z = bounds_from_tiles(all_tiles)

    with Image.open(all_tiles[0][2]) as sample:
        tw, th = sample.size

    background = (16, 25, 29, 255)

    for root, _, tiles in map_entries:
        map_name = sanitize_name(root.name)
        out_file = output_dir / f"{map_name}__{LAYER_SLUG}.png"
        stitch_to_canvas(tiles, out_file, shared_min_x, shared_max_x, shared_min_z, shared_max_z, tw, th, background)

    merged_tiles = merge_tiles(map_entries)
    merged_file = output_dir / f"merged__{LAYER_SLUG}.png"
    stitch_to_canvas(
        merged_tiles,
        merged_file,
        shared_min_x,
        shared_max_x,
        shared_min_z,
        shared_max_z,
        tw,
        th,
        background,
    )


if __name__ == "__main__":
    main()
import json
import re
from pathlib import Path

JAPANESE_SCRIPT_RE = re.compile(r"[぀-ゟ゠-ヿ]")


def _romaji_variants(romaji: str) -> set[str]:
    variants = {romaji}
    if "ou" in romaji:
        variants.add(romaji.replace("ou", "o"))
        variants.add(romaji.replace("ou", "oh"))
    if "oo" in romaji:
        variants.add(romaji.replace("oo", "o"))
        variants.add(romaji.replace("oo", "oh"))
    if "uu" in romaji:
        variants.add(romaji.replace("uu", "u"))
    if "ii" in romaji:
        variants.add(romaji.replace("ii", "i"))
    return variants


def load_jp_surnames() -> set[str]:
    surnames: set[str] = set()
    for surname in json.load(open("raw/jp_surnames.json")):
        for variant in _romaji_variants(surname.lower()):
            surnames.add(variant)
    return surnames


def main():
    year = "2026"
    researchers: dict[str, int] = json.loads(Path(f"raw/researchers_{year}.json").read_text())

    print("Loading Japanese surname list from public dataset...")
    jp_surnames = load_jp_surnames()
    print(f"Loaded {len(jp_surnames)} surname forms (including romanization variants)")

    japanese: dict[str, int] = {}
    for name, count in researchers.items():
        if bool(JAPANESE_SCRIPT_RE.search(name)):
            japanese[name] = count
        elif any(part.lower() in jp_surnames for part in name.split()):
            japanese[name] = count

    sorted_result = dict(sorted(japanese.items(), key=lambda x: x[1], reverse=True))
    blocked_names = set(json.load(open("raw/names_to_filter.json")))
    sorted_result = {k: v for k, v in sorted_result.items() if k not in blocked_names}
    Path(f"raw/japanese_researchers_{year}.json").write_text(
        json.dumps(sorted_result, ensure_ascii=False, indent=2)
    )
    print(f"Found {len(sorted_result)} Japanese researchers → raw/japanese_researchers_{year}.json")


if __name__ == "__main__":
    main()

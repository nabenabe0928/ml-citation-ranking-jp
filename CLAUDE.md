# Purpose

This project aims to create a ranking based on JP researchers citation based on Google Scholar.

- `raw/researchers_YYYY.json`: the extracted researcher names
- `raw/japanese_researchers_YYYY.json`: the extracted researcher names by `extract_japanese.py`
- `raw/jp_surnames.json`: a common family name list used to extract japanese researchers in `extract_japanese.py`
- `raw/names_to_filter.json`: manually extracted researcher names to filter out from `raw/japanese_researchers_YYYY.json`
- `viz.py`: Visualize the citation count trend over the ranking.

# Rules
- Do NOT modify files under `raw/`.
- Use `uv` for Python.

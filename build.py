#!/usr/bin/env python3
"""
Build script for GPSA Coach Listings site.
Reads data/postings.yaml, renders templates/index.html.j2, and outputs to dist/.
Run: python build.py
"""

import json
import shutil
import yaml
import jinja2
from pathlib import Path


def build():
    dist = Path("dist")
    if dist.exists():
        shutil.rmtree(dist)
    dist.mkdir()

    with open("data/postings.yaml") as f:
        data = yaml.safe_load(f)

    active_postings = sorted(
        [p for p in data["postings"] if p.get("active", False)],
        key=lambda p: p["team"]
    )

    env = jinja2.Environment(
        loader=jinja2.FileSystemLoader("templates"),
        autoescape=jinja2.select_autoescape(["html"]),
    )
    template = env.get_template("index.html.j2")
    output = template.render(postings=active_postings)

    (dist / "index.html").write_text(output)

    # Generate status.json for sidebar widget consumption
    status = {"active_postings": len(active_postings)}
    (dist / "status.json").write_text(json.dumps(status))

    # Copy static assets flat into dist so relative paths (styles.css, images/) work
    for item in Path("static").iterdir():
        dest = dist / item.name
        if item.is_dir():
            shutil.copytree(item, dest)
        else:
            shutil.copy2(item, dest)

    # Copy CNAME if present (custom domain for GitHub Pages)
    if Path("CNAME").exists():
        shutil.copy2("CNAME", dist / "CNAME")

    print(f"Built {len(active_postings)} active posting(s) → dist/")


if __name__ == "__main__":
    build()

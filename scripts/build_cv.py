"""Generate site fragments in data/_gen/ from the YAML sources in data/cv/.

Usage:  python3 scripts/build_cv.py   (then: quarto render)

Every page that shows CV data (Career, Publications, Research, CV) includes a
fragment from data/_gen/, so editing data/cv/*.yml is the only content edit.
"""

import html
import re
from pathlib import Path

import yaml
from jinja2 import Environment, FileSystemLoader, StrictUndefined
from markupsafe import Markup


class AppConfig:
    ROOT = Path(__file__).resolve().parents[1]
    DATA_DIR = ROOT / "data" / "cv"
    TEMPLATE_DIR = ROOT / "scripts" / "templates"
    OUT_DIR = ROOT / "data" / "_gen"
    ME = "D.-J. Yi"
    RESEARCH_STATUSES = {"Published", "In preparation", "Ongoing"}
    # template file -> generated fragment (included by the .qmd pages)
    OUTPUTS = {
        "index_hero.html.j2": "index_hero.html",
        "index_interests.html.j2": "index_interests.html",
        "career_education.html.j2": "career_education.html",
        "career_grants.html.j2": "career_grants.html",
        "career_skills.html.j2": "career_skills.html",
        "publications.html.j2": "publications.html",
        "research.md.j2": "research.md",
        "cv.html.j2": "cv.html",
    }


def load_data(cfg):
    data = {p.stem: yaml.safe_load(p.read_text(encoding="utf-8")) for p in cfg.DATA_DIR.glob("*.yml")}
    pubs = data["publications"]
    data["papers"] = sort_papers(pubs["papers"], cfg.ME)
    for paper in data["papers"]:
        paper["id"] = paper_id(paper)
    data["manuscripts"] = pubs["manuscripts"]
    data["patents"] = pubs["patents"]
    return data


def paper_id(paper):
    """Stable id from assets/pubs/<n>.pdf; used for page anchors and research.yml `refs`."""
    return int(re.fullmatch(r"assets/pubs/(\d+)\.pdf", paper["pdf"]).group(1))


def sort_papers(papers, me):
    """Papers where I am first (†) or corresponding (*) author come first;
    newest first within each group (stable, so YAML order breaks year ties)."""
    lead = re.compile(re.escape(me) + r"[†*]")
    return sorted(papers, key=lambda p: (not lead.search(p["authors"]), -int(p["year"])))


def check_pdfs(cfg, papers):
    for paper in papers:
        pdf = paper.get("pdf")
        if pdf is not None and not (cfg.ROOT / pdf).is_file():
            raise FileNotFoundError(cfg.ROOT / pdf)


def check_research_statuses(cfg, research):
    for theme in research["themes"]:
        for item in theme["items"]:
            if item["status"] not in cfg.RESEARCH_STATUSES:
                raise ValueError(f"unknown research status {item['status']!r} in theme {theme['title']!r}")


def check_research_md(rendered, research):
    """Each research item must be its own Markdown bullet: Jinja's trim_blocks can silently
    glue bullets together when a template line ends with a block tag."""
    expected = sum(len(t["items"]) for t in research["themes"])
    found = sum(1 for line in rendered.splitlines() if line.startswith("- "))
    if found != expected:
        raise ValueError(f"research.md has {found} bullet lines, expected {expected} (glued list items?)")


def make_cite_filter(papers):
    """research.yml `refs` (paper ids) -> 'Short Year' links to the paper's entry on this site.
    `prefix` is the anchor base: the Publications page by default, '#cv-pub-' inside the CV."""
    by_id = {paper["id"]: paper for paper in papers}

    def cite(ids, prefix="publications.html#pub-"):
        parts = []
        for i in ids:
            paper = by_id[i]
            label = html.escape(f"{paper['short']} {paper['year']}", quote=False)
            parts.append(f'<a href="{prefix}{i}">{label}</a>')
        return Markup("; ".join(parts))
    return cite


def make_authors_filter(me):
    pattern = re.compile(re.escape(me) + r"[†*]*")  # keep role markers inside the highlight

    def authors(text, tag_open="<u><b>", tag_close="</b></u>"):
        escaped = html.escape(text, quote=False)
        return Markup(pattern.sub(lambda m: f"{tag_open}{m.group(0)}{tag_close}", escaped))
    return authors


def edu_lines(e):
    """Career page: one <span> line per fact, joined with <br> by the template."""
    esc = lambda t: html.escape(str(t), quote=False)
    lines = [
        f'<span class="edu-degree">{esc(e["degree"])}</span> - '
        f'<span class="edu-school">{esc(e["department"])}, {esc(e["school"])}</span>, {esc(e["location"])}',
        f'<span class="edu-detail">GPA {esc(e["gpa"])} · {esc(e["period"])}</span>',
    ]
    if "lab" in e:
        lines.append(f'<span class="edu-lab">{esc(e["lab"])}</span>')
    if "advisor" in e:
        lines.append(f'<span class="edu-advisor">Advisor: {esc(e["advisor"])}</span>')
    if "thesis" in e:
        lines.append(f'<span class="edu-thesis">Thesis: “{esc(e["thesis"])}”</span>')
    for note in e.get("notes", []):
        lines.append(f'<span class="edu-detail">{esc(note)}</span>')
    return Markup("<br>\n".join(lines))


def accent_first(title, n=3):
    """awesome-cv style: first n letters of a section title get the accent color."""
    escaped = html.escape(title, quote=False)
    return Markup(f'<span class="cv-h2-accent">{escaped[:n]}</span>{escaped[n:]}')


def main():
    cfg = AppConfig
    data = load_data(cfg)
    check_pdfs(cfg, data["papers"])
    check_research_statuses(cfg, data["research"])

    env = Environment(
        loader=FileSystemLoader(str(cfg.TEMPLATE_DIR)),
        undefined=StrictUndefined,
        autoescape=True,
        trim_blocks=True,
        lstrip_blocks=True,
        keep_trailing_newline=True,
    )
    env.filters["authors"] = make_authors_filter(cfg.ME)
    env.filters["cite"] = make_cite_filter(data["papers"])
    env.filters["accent_first"] = accent_first
    env.filters["edu_lines"] = edu_lines

    cfg.OUT_DIR.mkdir(parents=True, exist_ok=True)
    for template_name, out_name in cfg.OUTPUTS.items():
        rendered = env.get_template(template_name).render(**data)
        if out_name == "research.md":
            check_research_md(rendered, data["research"])
        out_path = cfg.OUT_DIR / out_name
        out_path.write_text(rendered, encoding="utf-8")
        print(f"wrote {out_path.relative_to(cfg.ROOT)} ({len(rendered)} chars)")


if __name__ == "__main__":
    main()

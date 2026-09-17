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
    PDF_DIR = "assets/pubs"
    # template file -> generated fragment (included by the .qmd pages)
    OUTPUTS = {
        "index_hero.html.j2": "index_hero.html",
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
    data["papers"] = pubs["papers"]
    data["patents"] = pubs["patents"]
    return data


def check_pdf_numbering(cfg, papers):
    """Paper k from the bottom is number k; its PDF must be assets/pubs/k.pdf."""
    total = len(papers)
    for i, paper in enumerate(papers):
        number = total - i
        pdf = paper.get("pdf")
        if pdf is None:
            continue
        expected = f"{cfg.PDF_DIR}/{number}.pdf"
        if pdf != expected:
            raise ValueError(f"paper #{number} ({paper['title'][:40]}...) has pdf={pdf}, expected {expected}")
        if not (cfg.ROOT / pdf).is_file():
            raise FileNotFoundError(cfg.ROOT / pdf)


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
    check_pdf_numbering(cfg, data["papers"])

    env = Environment(
        loader=FileSystemLoader(str(cfg.TEMPLATE_DIR)),
        undefined=StrictUndefined,
        autoescape=True,
        trim_blocks=True,
        lstrip_blocks=True,
        keep_trailing_newline=True,
    )
    env.filters["authors"] = make_authors_filter(cfg.ME)
    env.filters["accent_first"] = accent_first
    env.filters["edu_lines"] = edu_lines

    cfg.OUT_DIR.mkdir(parents=True, exist_ok=True)
    for template_name, out_name in cfg.OUTPUTS.items():
        rendered = env.get_template(template_name).render(**data)
        out_path = cfg.OUT_DIR / out_name
        out_path.write_text(rendered, encoding="utf-8")
        print(f"wrote {out_path.relative_to(cfg.ROOT)} ({len(rendered)} chars)")


if __name__ == "__main__":
    main()

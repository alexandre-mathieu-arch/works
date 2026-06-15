import os
import re
import shutil
import subprocess
import sys
import hashlib
from pathlib import Path

import yaml
from PIL import Image, ImageOps

BASE_DIR = Path(__file__).resolve().parent
REPO_ROOT = BASE_DIR.parent
PROJECTS_DIR = REPO_ROOT / "content" / "projets"
PUBLIC_DIR = REPO_ROOT / "public"
OUTPUT_DIR = BASE_DIR / "output"
OPTIMIZED_IMAGE_DIR = OUTPUT_DIR / "images"
TEMPLATE_FILE = BASE_DIR / "template.tex"
TEX_FILE = OUTPUT_DIR / "portfolio_gen.tex"
PDF_FILE = OUTPUT_DIR / "portfolio_gen.pdf"
FINAL_PDF = BASE_DIR / "Alexandre-MATHIEU_PORTFOLIO-2026.pdf"
MAX_IMAGE_DIMENSION = 2200
JPEG_QUALITY = 88


def tex_escape(value):
    text = "" if value is None else str(value)
    replacements = {
        "\\": r"\textbackslash{}",
        "&": r"\&",
        "%": r"\%",
        "$": r"\$",
        "#": r"\#",
        "_": r"\_",
        "{": r"\{",
        "}": r"\}",
        "~": r"\textasciitilde{}",
        "^": r"\textasciicircum{}",
    }
    return "".join(replacements.get(char, char) for char in text)


def inline_markdown_to_tex(text):
    parts = re.split(r"(\*\*[^*]+\*\*|\*[^*]+\*)", text)
    converted = []

    for part in parts:
        if part.startswith("**") and part.endswith("**"):
            converted.append(r"\textbf{" + tex_escape(part[2:-2]) + "}")
        elif part.startswith("*") and part.endswith("*"):
            converted.append(r"\textit{" + tex_escape(part[1:-1]) + "}")
        else:
            converted.append(tex_escape(part))

    return "".join(converted)


def markdown_to_tex(text):
    if not text:
        return ""

    blocks = re.split(r"\n\s*\n", text.strip())
    tex_blocks = []

    for block in blocks:
        lines = [line.rstrip() for line in block.splitlines() if line.strip()]
        if not lines:
            continue

        first = lines[0].strip()
        heading = re.match(r"^#{2,4}\s+(.+)$", first)
        if heading and len(lines) == 1:
            tex_blocks.append(r"\projectSubheading{" + inline_markdown_to_tex(heading.group(1)) + "}")
            continue

        if all(line.lstrip().startswith(("-", "*")) for line in lines):
            items = []
            for line in lines:
                label = re.sub(r"^\s*[-*]\s+", "", line)
                items.append(r"\item " + inline_markdown_to_tex(label))
            tex_blocks.append(
                r"\begin{itemize}\setlength\itemsep{0.05cm}\setlength\leftmargin{0.35cm}"
                + "\n".join(items)
                + r"\end{itemize}"
            )
            continue

        paragraph = " ".join(lines)
        paragraph = re.sub(r"^#{2,4}\s+", "", paragraph)
        tex_blocks.append(inline_markdown_to_tex(paragraph))

    return r"\par ".join(tex_blocks)


def as_list(value):
    if value is None:
        return []
    if isinstance(value, list):
        return [str(item) for item in value if item]
    return [str(value)]


def local_image_path(path):
    if not path:
        return None

    full_path = (PUBLIC_DIR / str(path).lstrip("/")).resolve()
    if full_path.exists():
        return str(full_path)
    return None


def collect_images(frontmatter):
    images = []
    for key in ("images", "details"):
        for image in as_list(frontmatter.get(key)):
            local = local_image_path(image)
            if local and local not in images:
                images.append(local)
    return images


def prepare_image_for_pdf(path):
    source = Path(path)
    digest = hashlib.sha1(str(source).encode("utf-8")).hexdigest()[:12]
    target = OPTIMIZED_IMAGE_DIR / f"{source.stem}-{digest}.jpg"

    if target.exists() and target.stat().st_mtime >= source.stat().st_mtime:
        return str(target)

    try:
        image = Image.open(source)
        image = ImageOps.exif_transpose(image)

        if image.mode in ("RGBA", "LA") or (image.mode == "P" and "transparency" in image.info):
            background = Image.new("RGB", image.size, "white")
            background.paste(image.convert("RGBA"), mask=image.convert("RGBA").getchannel("A"))
            image = background
        else:
            image = image.convert("RGB")

        image.thumbnail((MAX_IMAGE_DIMENSION, MAX_IMAGE_DIMENSION), Image.Resampling.LANCZOS)
        image.save(target, "JPEG", quality=JPEG_QUALITY, optimize=True, progressive=True)
        return str(target)
    except Exception as error:
        print(f"Image non optimisee ({source}): {error}")
        return str(source)


def parse_projects():
    projects_data = []

    for path in sorted(PROJECTS_DIR.glob("*.md")):
        content = path.read_text(encoding="utf-8")
        match = re.match(r"^---(.*?)---(.*)", content, re.DOTALL)
        if not match:
            continue

        frontmatter = yaml.safe_load(match.group(1)) or {}
        if frontmatter.get("draft") is True:
            continue

        body = match.group(2).strip()
        frontmatter["local_images"] = collect_images(frontmatter)
        frontmatter["body_tex"] = markdown_to_tex(body)
        frontmatter["source_file"] = path.name
        projects_data.append(frontmatter)

    def sort_key(project):
        order = project.get("order", 999)
        date = project.get("date", 0)
        try:
            date_value = int(str(date)[:4])
        except (ValueError, TypeError):
            date_value = 0
        return (order, -date_value, project.get("title", ""))

    projects_data.sort(key=sort_key)
    return projects_data


def project_subtitle(project):
    parts = []
    for key in ("lieu", "phase", "statut"):
        value = project.get(key)
        if value and value not in parts:
            parts.append(str(value))
    return " / ".join(parts)


def meta_block(project):
    fields = [
        ("Typologie", ", ".join(as_list(project.get("typologies")))),
        ("Lieu", project.get("lieu")),
        ("Pays", ", ".join(as_list(project.get("pays")))),
        ("Surface", project.get("surface")),
        ("Phase", project.get("phase") or project.get("statut")),
        ("Collaboration", project.get("collaboration") or project.get("ecole")),
        ("Année", project.get("date")),
    ]

    lines = []
    for label, value in fields:
        if value:
            lines.append(r"\projectMetaItem{" + tex_escape(label) + "}{" + inline_markdown_to_tex(str(value)) + "}")

    return "\n".join(lines)


def text_block(project):
    parts = []
    description = project.get("description")
    if description:
        parts.append(r"\leadText{" + inline_markdown_to_tex(description) + "}")

    body = project.get("body_tex", "")
    if body:
        parts.append(body)

    return "\n\n".join(parts) or r"{\color{muted}Texte a completer.}"


def gallery_page(title, label, images):
    count = len(images)
    title_tex = tex_escape(title)
    label_tex = tex_escape(label)
    tex = [rf"\galleryHeader{{{title_tex}}}{{{label_tex}}}"]

    if count == 1:
        tex.append(rf"\galleryImage{{{images[0]}}}{{9.2cm}}")
    elif count == 2:
        tex.append(
            rf"\noindent\begin{{minipage}}[c][9.2cm][c]{{0.48\linewidth}}\galleryImage{{{images[0]}}}{{9.2cm}}\end{{minipage}}\hfill"
            rf"\begin{{minipage}}[c][9.2cm][c]{{0.48\linewidth}}\galleryImage{{{images[1]}}}{{9.2cm}}\end{{minipage}}"
        )
    elif count == 3:
        tex.append(
            rf"\noindent\begin{{minipage}}[c][8.9cm][c]{{0.31\linewidth}}\galleryImage{{{images[0]}}}{{8.9cm}}\end{{minipage}}\hfill"
            rf"\begin{{minipage}}[c][8.9cm][c]{{0.31\linewidth}}\galleryImage{{{images[1]}}}{{8.9cm}}\end{{minipage}}\hfill"
            rf"\begin{{minipage}}[c][8.9cm][c]{{0.31\linewidth}}\galleryImage{{{images[2]}}}{{8.9cm}}\end{{minipage}}"
        )
    else:
        tex.append(
            rf"\noindent\begin{{minipage}}[c][4.25cm][c]{{0.48\linewidth}}\galleryImage{{{images[0]}}}{{4.25cm}}\end{{minipage}}\hfill"
            rf"\begin{{minipage}}[c][4.25cm][c]{{0.48\linewidth}}\galleryImage{{{images[1]}}}{{4.25cm}}\end{{minipage}}\par\vspace{{0.35cm}}"
            rf"\noindent\begin{{minipage}}[c][4.25cm][c]{{0.48\linewidth}}\galleryImage{{{images[2]}}}{{4.25cm}}\end{{minipage}}\hfill"
            rf"\begin{{minipage}}[c][4.25cm][c]{{0.48\linewidth}}\galleryImage{{{images[3]}}}{{4.25cm}}\end{{minipage}}"
        )

    return "\n".join(tex) + "\n"


def generate_tex(projects):
    OUTPUT_DIR.mkdir(exist_ok=True)
    OPTIMIZED_IMAGE_DIR.mkdir(exist_ok=True)
    template = TEMPLATE_FILE.read_text(encoding="utf-8")

    project_entries = []
    for index, project in enumerate(projects, start=1):
        title = project.get("title", "Sans titre")
        date = str(project.get("date", ""))
        label = f"{index:02d}"
        images = [prepare_image_for_pdf(image) for image in project.get("local_images", [])]
        intro_image = images[0] if images else ""

        toc_title = f"{title} ({date})" if date else title
        project_entries.append(
            rf"\projectIntroPage{{{label}}}{{{tex_escape(title)}}}{{{tex_escape(date)}}}{{{tex_escape(project_subtitle(project))}}}{{{intro_image}}}"
        )
        project_entries.append(rf"\addcontentsline{{toc}}{{section}}{{{tex_escape(toc_title)}}}")
        project_entries.append(
            rf"\projectTextPage{{{meta_block(project)}}}{{{text_block(project)}}}"
        )

        gallery_images = images[1:]
        for page_index in range(0, len(gallery_images), 4):
            group = gallery_images[page_index : page_index + 4]
            project_entries.append(gallery_page(title, f"{label} / images", group))

    TEX_FILE.write_text(template.replace("%%PROJECTS_PLACEHOLDER%%", "\n\n".join(project_entries)), encoding="utf-8")


def compile_pdf():
    for _ in range(2):
        subprocess.run(
            ["xelatex", "-interaction=nonstopmode", "-halt-on-error", TEX_FILE.name],
            cwd=OUTPUT_DIR,
            check=True,
        )

    if PDF_FILE.exists():
        shutil.copy2(PDF_FILE, FINAL_PDF)


if __name__ == "__main__":
    projects = parse_projects()
    print(f"{len(projects)} projets trouves.")
    generate_tex(projects)
    print(f"Fichier LaTeX genere : {TEX_FILE}")

    if "--compile" in sys.argv:
        compile_pdf()
        print(f"PDF genere : {PDF_FILE}")
        print(f"PDF final copie : {FINAL_PDF}")
    else:
        print("Compilez avec : python3 build_portfolio.py --compile")

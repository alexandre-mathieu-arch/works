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
CROPPED_IMAGE_DIR = OUTPUT_DIR / "crops"
TEMPLATE_FILE = BASE_DIR / "template.tex"
TEX_FILE = OUTPUT_DIR / "portfolio_gen.tex"
PDF_FILE = OUTPUT_DIR / "portfolio_gen.pdf"
FINAL_PDF = BASE_DIR / "Alexandre-MATHIEU_PORTFOLIO-2026-V2.pdf"
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


def prepare_crop_for_pdf(path, aspect_ratio, crop_key, centering=(0.5, 0.5)):
    source = Path(path)
    digest = hashlib.sha1(
        f"{source}:{aspect_ratio:.5f}:{centering}".encode("utf-8")
    ).hexdigest()[:12]
    target = CROPPED_IMAGE_DIR / f"{source.stem}-{crop_key}-{digest}.jpg"

    if target.exists() and target.stat().st_mtime >= source.stat().st_mtime:
        return str(target)

    try:
        image = ImageOps.exif_transpose(Image.open(source))
        if image.mode in ("RGBA", "LA") or (image.mode == "P" and "transparency" in image.info):
            background = Image.new("RGB", image.size, "white")
            rgba = image.convert("RGBA")
            background.paste(rgba, mask=rgba.getchannel("A"))
            image = background
        else:
            image = image.convert("RGB")

        if aspect_ratio >= 1:
            target_width = MAX_IMAGE_DIMENSION
            target_height = max(1, round(target_width / aspect_ratio))
        else:
            target_height = MAX_IMAGE_DIMENSION
            target_width = max(1, round(target_height * aspect_ratio))

        cropped = ImageOps.fit(
            image,
            (target_width, target_height),
            method=Image.Resampling.LANCZOS,
            centering=centering,
        )
        cropped.save(target, "JPEG", quality=JPEG_QUALITY, optimize=True, progressive=True)
        return str(target)
    except Exception as error:
        print(f"Recadrage impossible ({source}): {error}")
        return prepare_image_for_pdf(path)


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


def gallery_page(title, label, images, page_index):
    count = len(images)
    title_tex = tex_escape(title)
    label_tex = tex_escape(label)
    if count == 1:
        image = prepare_crop_for_pdf(images[0], 210 / 148, f"gallery-full-{page_index}")
        return rf"\galleryFullPage{{{title_tex}}}{{{label_tex}}}{{{image}}}" + "\n"
    if count == 2:
        left = prepare_crop_for_pdf(images[0], 12.7 / 14.8, f"gallery-left-{page_index}")
        right = prepare_crop_for_pdf(images[1], 8.3 / 14.8, f"gallery-right-{page_index}")
        return rf"\gallerySplitPage{{{title_tex}}}{{{label_tex}}}{{{left}}}{{{right}}}" + "\n"
    if count == 3:
        main = prepare_crop_for_pdf(images[0], 12.9 / 14.8, f"gallery-main-{page_index}")
        top = prepare_crop_for_pdf(images[1], 8.1 / 7.4, f"gallery-top-{page_index}")
        bottom = prepare_crop_for_pdf(images[2], 8.1 / 7.4, f"gallery-bottom-{page_index}")
        return rf"\galleryTriptychPage{{{title_tex}}}{{{label_tex}}}{{{main}}}{{{top}}}{{{bottom}}}" + "\n"
    main = prepare_crop_for_pdf(images[0], 12 / 14.8, f"gallery-main-{page_index}")
    strips = [
        prepare_crop_for_pdf(image, 9 / (14.8 / 3), f"gallery-strip-{page_index}-{index}")
        for index, image in enumerate(images[1:4], start=1)
    ]
    return (
        rf"\galleryMosaicPage{{{title_tex}}}{{{label_tex}}}{{{main}}}"
        rf"{{{strips[0]}}}{{{strips[1]}}}{{{strips[2]}}}" + "\n"
    )


def generate_tex(projects):
    OUTPUT_DIR.mkdir(exist_ok=True)
    OPTIMIZED_IMAGE_DIR.mkdir(exist_ok=True)
    CROPPED_IMAGE_DIR.mkdir(exist_ok=True)
    template = TEMPLATE_FILE.read_text(encoding="utf-8")
    project_entries = []
    toc_entries = []
    cover_image = ""
    for index, project in enumerate(projects, start=1):
        title = project.get("title", "Sans titre")
        date = str(project.get("date", ""))
        label = f"{index:02d}"
        source_images = project.get("local_images", [])
        intro_image = prepare_crop_for_pdf(source_images[0], 210 / 148, f"intro-{label}") if source_images else ""
        story_source = source_images[1] if len(source_images) > 1 else (source_images[0] if source_images else "")
        story_image = prepare_crop_for_pdf(story_source, 9.7 / 14.8, f"story-{label}", centering=(0.5, 0.46)) if story_source else ""
        if not cover_image and source_images:
            cover_image = prepare_crop_for_pdf(source_images[0], 210 / 148, "cover", centering=(0.5, 0.44))

        toc_entries.append(rf"\portfolioTocEntry{{{label}}}{{{tex_escape(title)}}}{{{tex_escape(date)}}}")
        project_entries.append(rf"\hypertarget{{project-{label}}}{{}}")
        project_entries.append(rf"\projectIntroPage{{{label}}}{{{tex_escape(title)}}}{{{tex_escape(date)}}}{{{tex_escape(project_subtitle(project))}}}{{{intro_image}}}")
        project_entries.append(rf"\projectStoryPage{{{label}}}{{{tex_escape(title)}}}{{{meta_block(project)}}}{{{text_block(project)}}}{{{story_image}}}")
        gallery_images = source_images[2:]
        for page_index in range(0, len(gallery_images), 4):
            group = gallery_images[page_index : page_index + 4]
            project_entries.append(gallery_page(title, f"{label} / {page_index // 4 + 1:02d}", group, page_index))

    generated = template
    generated = generated.replace("%%COVER_IMAGE%%", cover_image)
    generated = generated.replace("%%TOC_PLACEHOLDER%%", "\n".join(toc_entries))
    generated = generated.replace("%%PROJECT_COUNT%%", str(len(projects)))
    generated = generated.replace("%%PROJECTS_PLACEHOLDER%%", "\n\n".join(project_entries))
    TEX_FILE.write_text(generated, encoding="utf-8")


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

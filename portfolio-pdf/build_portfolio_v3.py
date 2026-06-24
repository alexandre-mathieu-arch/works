"""Build the luxury-color V3 without modifying the V2 sources."""

import sys
import hashlib
from pathlib import Path

import build_portfolio as portfolio
from PIL import Image, ImageOps


BASE_DIR = Path(__file__).resolve().parent
OUTPUT_DIR = BASE_DIR / "output-v3"
TEMPLATE_FILE = OUTPUT_DIR / "template-v3.tex"

# A restrained luxury palette: warm mineral black, ivory, champagne bronze,
# and quiet taupes. The existing `acid` token is retained internally so the
# V2 layout can be reused without invasive changes.
COLOR_REPLACEMENTS = {
    r"\definecolor{ink}{HTML}{111111}": r"\definecolor{ink}{HTML}{171714}",
    r"\definecolor{paper}{HTML}{F3F1EC}": r"\definecolor{paper}{HTML}{F5F1E8}",
    r"\definecolor{acid}{HTML}{D7FF37}": r"\definecolor{acid}{HTML}{B8945A}",
    r"\definecolor{muted}{HTML}{777570}": r"\definecolor{muted}{HTML}{746E65}",
    r"\definecolor{soft}{HTML}{B6B2AA}": r"\definecolor{soft}{HTML}{B7ADA0}",
    r"\definecolor{rulegray}{HTML}{D8D4CB}": r"\definecolor{rulegray}{HTML}{D9D0C2}",
    "Portfolio V2 2018-2026": "Portfolio V3 2018-2026",
}


def prepare_v3_template():
    OUTPUT_DIR.mkdir(exist_ok=True)
    template = portfolio.TEMPLATE_FILE.read_text(encoding="utf-8")
    for source, replacement in COLOR_REPLACEMENTS.items():
        template = template.replace(source, replacement)

    toc_macro = r"""
\newcommand{\portfolioTocEntry}[3]{%
  \hyperlink{project-#1}{%
    \noindent
    \begin{minipage}[c]{0.12\linewidth}
      {\fontsize{5.7}{6.6}\selectfont\mediumfont\color{acid}#1}
    \end{minipage}
    \begin{minipage}[c]{0.66\linewidth}
      {\fontsize{8.0}{9.0}\selectfont\mediumfont\color{ink}#2}
    \end{minipage}
    \begin{minipage}[c]{0.18\linewidth}
      \raggedleft{\fontsize{5.6}{6.5}\selectfont\lightfont\color{muted}#3}
    \end{minipage}
  }\par\vspace{0.28cm}
}
"""

    toc_start = template.index(r"\newcommand{\portfolioTocEntry}")
    macro_start = template.index(r"\newcommand{\projectIntroPage}")
    template = template[:toc_start] + toc_macro + "\n" + template[macro_start:]

    editorial_macros = r"""
\newcommand{\folioMark}{%
  \begin{tikzpicture}[remember picture,overlay]
    \fill[paper,opacity=0.92] ([xshift=-1.42cm,yshift=0.36cm]current page.south east)
      rectangle ([xshift=-0.42cm,yshift=0.92cm]current page.south east);
    \fill[acid] ([xshift=-1.42cm,yshift=0.92cm]current page.south east)
      rectangle ([xshift=-0.94cm,yshift=0.97cm]current page.south east);
    \node[anchor=center,inner sep=0,text=ink]
      at ([xshift=-0.92cm,yshift=0.64cm]current page.south east)
      {\fontsize{5.0}{5.8}\selectfont\mediumfont \thepage};
  \end{tikzpicture}%
}

\newcommand{\projectIntroPage}[5]{%
  \clearpage\thispagestyle{empty}\hypertarget{project-#1}{}
  \ifx&#5&\else\fullBleedImage{#5}\fi
  \begin{tikzpicture}[remember picture,overlay]
    \fill[ink,opacity=0.08] (current page.south west) rectangle (current page.north east);
    \fill[paper,opacity=0.96] ([xshift=0.55cm,yshift=0.55cm]current page.south west)
      rectangle ([xshift=9.25cm,yshift=3.25cm]current page.south west);
    \fill[acid] ([xshift=0.55cm,yshift=3.25cm]current page.south west)
      rectangle ([xshift=2.15cm,yshift=3.32cm]current page.south west);
    \node[anchor=north west,inner sep=0,text width=7.95cm]
      at ([xshift=0.88cm,yshift=2.87cm]current page.south west) {%
        {\fontsize{5.2}{6.2}\selectfont\mediumfont\color{acid}PROJET #1 \hfill #3}\par
        \vspace{0.20cm}
        {\fontsize{16.5}{17}\selectfont\displayfont\color{ink}#2}\par
        \vspace{0.12cm}
        {\fontsize{5.9}{7}\selectfont\lightfont\color{muted}#4}
      };
  \end{tikzpicture}\folioMark\null
}

\long\def\projectStoryPage#1#2#3#4#5{%
  \clearpage\thispagestyle{empty}
  \begin{tikzpicture}[remember picture,overlay]
    \fill[paper] (current page.south west) rectangle (current page.north east);
    \ifx&#5&\else
      \node[anchor=north west,inner sep=0] at (current page.north west)
        {\includegraphics[width=12.20cm,height=8.20cm]{#5}};
    \fi
    \fill[acid] ([xshift=10.55cm,yshift=-8.20cm]current page.north west)
      rectangle ([xshift=12.20cm,yshift=-8.13cm]current page.north west);
    \node[anchor=north west,inner sep=0,text width=7.55cm]
      at ([xshift=12.62cm,yshift=-0.65cm]current page.north west) {%
        {\fontsize{5.1}{6.1}\selectfont\mediumfont\color{muted}#1 / NOTE DE PROJET}\par
        \vspace{0.17cm}
        {\fontsize{15.2}{15.8}\selectfont\displayfont\color{ink}#2}\par
        \vspace{0.18cm}\hairline\par\vspace{0.25cm}
        \RaggedRight{\fontsize{6.3}{7.75}\selectfont\lightfont\color{ink}#4}
      };
    \node[anchor=north west,inner sep=0,text width=10.95cm]
      at ([xshift=0.72cm,yshift=5.88cm]current page.south west) {%
        #3
      };
    \node[anchor=south west,inner sep=0,text=muted]
      at ([xshift=12.62cm,yshift=0.38cm]current page.south west)
      {\fontsize{4.7}{5.5}\selectfont\lightfont CONTEXTE / INTENTION / DONNEES};
  \end{tikzpicture}\folioMark\null
}

\newcommand{\galleryLabel}[2]{%
  \begin{tikzpicture}[remember picture,overlay]
    \fill[paper,opacity=0.94] ([xshift=0.42cm,yshift=0.38cm]current page.south west)
      rectangle ([xshift=5.85cm,yshift=1.18cm]current page.south west);
    \fill[acid] ([xshift=0.42cm,yshift=1.18cm]current page.south west)
      rectangle ([xshift=1.35cm,yshift=1.23cm]current page.south west);
    \node[anchor=west,inner sep=0,text=ink]
      at ([xshift=0.67cm,yshift=0.78cm]current page.south west)
      {\fontsize{4.9}{5.9}\selectfont\mediumfont #2\quad/\quad #1};
  \end{tikzpicture}%
}
\newcommand{\galleryFullPage}[3]{\clearpage\thispagestyle{empty}\fullBleedImage{#3}\galleryLabel{#1}{#2}\folioMark\null}
\newcommand{\galleryFullCaptionPage}[4]{%
  \clearpage\thispagestyle{empty}\fullBleedImage{#3}
  \begin{tikzpicture}[remember picture,overlay]
    \fill[paper,opacity=0.94] ([xshift=0.42cm,yshift=1.18cm]current page.south west)
      rectangle ([xshift=6.85cm,yshift=1.92cm]current page.south west);
    \node[anchor=west,inner sep=0,text=ink]
      at ([xshift=0.67cm,yshift=1.55cm]current page.south west)
      {\fontsize{5.2}{6.2}\selectfont\mediumfont\MakeUppercase{#4}};
  \end{tikzpicture}\galleryLabel{#1}{#2}\folioMark\null
}
\newcommand{\galleryDuoPage}[4]{%
  \clearpage\thispagestyle{empty}
  \fullBleedImage{#3}
  \begin{tikzpicture}[remember picture,overlay]
    \fill[paper] ([xshift=-8.15cm,yshift=-5.48cm]current page.north east)
      rectangle ([xshift=-0.48cm,yshift=-0.48cm]current page.north east);
    \node[anchor=north east,inner sep=0] at ([xshift=-0.58cm,yshift=-0.58cm]current page.north east)
      {\includegraphics[width=7.47cm,height=4.80cm]{#4}};
  \end{tikzpicture}\galleryLabel{#1}{#2}\folioMark\null
}
\newcommand{\galleryDuoCaptionPage}[5]{%
  \clearpage\thispagestyle{empty}
  \fullBleedImage{#3}
  \begin{tikzpicture}[remember picture,overlay]
    \fill[paper] ([xshift=-8.15cm,yshift=-5.83cm]current page.north east)
      rectangle ([xshift=-0.48cm,yshift=-0.48cm]current page.north east);
    \node[anchor=north east,inner sep=0] at ([xshift=-0.58cm,yshift=-0.58cm]current page.north east)
      {\includegraphics[width=7.47cm,height=4.80cm]{#4}};
    \node[anchor=north west,inner sep=0,text=muted]
      at ([xshift=-8.00cm,yshift=-5.48cm]current page.north east)
      {\fontsize{4.8}{5.8}\selectfont\mediumfont\MakeUppercase{#5}};
  \end{tikzpicture}\galleryLabel{#1}{#2}\folioMark\null
}
\newcommand{\galleryTriptychPage}[5]{%
  \clearpage\thispagestyle{empty}
  \begin{tikzpicture}[remember picture,overlay]
    \fill[paper] (current page.south west) rectangle (current page.north east);
    \node[anchor=west,inner sep=0] at ([xshift=0.38cm]current page.west)
      {\includegraphics[width=13.75cm,height=8.70cm]{#3}};
    \node[anchor=north east,inner sep=0] at ([xshift=-0.38cm,yshift=-3.02cm]current page.north east)
      {\includegraphics[width=6.25cm,height=3.95cm]{#4}};
    \node[anchor=south east,inner sep=0] at ([xshift=-0.38cm,yshift=3.02cm]current page.south east)
      {\includegraphics[width=6.25cm,height=3.95cm]{#5}};
    \fill[acid] ([xshift=0.38cm,yshift=2.20cm]current page.south west)
      rectangle ([xshift=2.00cm,yshift=2.27cm]current page.south west);
  \end{tikzpicture}\galleryLabel{#1}{#2}\folioMark\null
}
\newcommand{\galleryPlansPage}[5]{%
  \clearpage\thispagestyle{empty}
  \begin{tikzpicture}[remember picture,overlay]
    \fill[paper] (current page.south west) rectangle (current page.north east);
    \node[anchor=west,inner sep=0] at ([xshift=0.45cm]current page.west)
      {\includegraphics[width=8.85cm,height=8.85cm]{#3}};
    \node[anchor=north east,inner sep=0] at ([xshift=-0.38cm,yshift=-0.72cm]current page.north east)
      {\includegraphics[width=10.75cm,height=5.85cm]{#4}};
    \node[anchor=south east,inner sep=0] at ([xshift=-0.38cm,yshift=0.72cm]current page.south east)
      {\includegraphics[width=10.75cm,height=5.85cm]{#5}};
    \fill[acid] ([xshift=0.45cm,yshift=2.18cm]current page.south west)
      rectangle ([xshift=2.05cm,yshift=2.25cm]current page.south west);
  \end{tikzpicture}\galleryLabel{#1}{#2}\folioMark\null
}
\newcommand{\galleryEqualPlansPage}[5]{%
  \clearpage\thispagestyle{empty}
  \begin{tikzpicture}[remember picture,overlay]
    \fill[paper] (current page.south west) rectangle (current page.north east);
    \node[anchor=north,inner sep=0] at ([yshift=-0.38cm]current page.north)
      {\includegraphics[width=19.15cm,height=4.38cm]{#3}};
    \node[anchor=center,inner sep=0] at (current page.center)
      {\includegraphics[width=19.15cm,height=4.38cm]{#4}};
    \node[anchor=south,inner sep=0] at ([yshift=0.38cm]current page.south)
      {\includegraphics[width=19.15cm,height=4.38cm]{#5}};
  \end{tikzpicture}\galleryLabel{#1}{#2}\folioMark\null
}
\newcommand{\galleryEqualPlansQuadPage}[6]{%
  \clearpage\thispagestyle{empty}
  \begin{tikzpicture}[remember picture,overlay]
    \fill[paper] (current page.south west) rectangle (current page.north east);
    \node[anchor=north west,inner sep=0] at ([xshift=0.15cm,yshift=-0.78cm]current page.north west)
      {\includegraphics[width=10.28cm,height=6.50cm]{#3}};
    \node[anchor=north east,inner sep=0] at ([xshift=-0.15cm,yshift=-0.78cm]current page.north east)
      {\includegraphics[width=10.28cm,height=6.50cm]{#4}};
    \node[anchor=south west,inner sep=0] at ([xshift=0.15cm,yshift=0.78cm]current page.south west)
      {\includegraphics[width=10.28cm,height=6.50cm]{#5}};
    \node[anchor=south east,inner sep=0] at ([xshift=-0.15cm,yshift=0.78cm]current page.south east)
      {\includegraphics[width=10.28cm,height=6.50cm]{#6}};
  \end{tikzpicture}\galleryLabel{#1}{#2}\folioMark\null
}
\newcommand{\galleryEqualPlansDuoPage}[4]{%
  \clearpage\thispagestyle{empty}
  \begin{tikzpicture}[remember picture,overlay]
    \fill[paper] (current page.south west) rectangle (current page.north east);
    \node[anchor=west,inner sep=0] at ([xshift=0.32cm]current page.west)
      {\includegraphics[width=9.85cm,height=7.00cm]{#3}};
    \node[anchor=east,inner sep=0] at ([xshift=-0.32cm]current page.east)
      {\includegraphics[width=9.85cm,height=7.00cm]{#4}};
  \end{tikzpicture}\galleryLabel{#1}{#2}\folioMark\null
}
\newcommand{\galleryQuadPage}[6]{%
  \clearpage\thispagestyle{empty}
  \begin{tikzpicture}[remember picture,overlay]
    \fill[paper] (current page.south west) rectangle (current page.north east);
    \node[anchor=north west,inner sep=0] at ([xshift=0.15cm,yshift=-0.78cm]current page.north west)
      {\includegraphics[width=10.28cm,height=6.50cm]{#3}};
    \node[anchor=north east,inner sep=0] at ([xshift=-0.15cm,yshift=-0.78cm]current page.north east)
      {\includegraphics[width=10.28cm,height=6.50cm]{#4}};
    \node[anchor=south west,inner sep=0] at ([xshift=0.15cm,yshift=0.78cm]current page.south west)
      {\includegraphics[width=10.28cm,height=6.50cm]{#5}};
    \node[anchor=south east,inner sep=0] at ([xshift=-0.15cm,yshift=0.78cm]current page.south east)
      {\includegraphics[width=10.28cm,height=6.50cm]{#6}};
  \end{tikzpicture}\galleryLabel{#1}{#2}\folioMark\null
}
"""
    macro_start = template.index(r"\newcommand{\projectIntroPage}")
    document_start = template.index(r"\begin{document}")
    template = template[:macro_start] + editorial_macros + "\n" + template[document_start:]

    document_start = template.index(r"\begin{document}")
    document_end = template.index(r"\end{document}", document_start) + len(r"\end{document}")
    document_pages = r"""
\begin{document}
\begin{titlepage}
\thispagestyle{empty}
\begin{tikzpicture}[remember picture,overlay]
  \fill[paper] (current page.south west) rectangle (current page.north east);
  \node[anchor=north east,inner sep=0] at ([xshift=-0.58cm,yshift=-0.58cm]current page.north east)
    {\includegraphics[width=13.20cm,height=9.30cm]{%%COVER_IMAGE%%}};
  \node[anchor=north west,inner sep=0,text width=7.25cm]
    at ([xshift=0.72cm,yshift=-1.12cm]current page.north west) {%
      {\fontsize{18.0}{18.8}\selectfont\displayfont\color{ink}\mbox{Alexandre MATHIEU}}\par
      \vspace{0.42cm}
      {\fontsize{6.8}{8.0}\selectfont\mediumfont\color{muted}Portfolio 2018–2026}\par
      \vspace{0.28cm}
      {\fontsize{5.7}{7.0}\selectfont\lightfont\color{muted}Architecture, design, recherche constructive}
    };
  \node[anchor=south west,inner sep=0,text width=11.50cm]
    at ([xshift=0.72cm,yshift=0.68cm]current page.south west) {%
      {\fontsize{4.7}{5.8}\selectfont\lightfont\color{muted}
      alexandre.mat+w@protonmail.com\quad / \quad +33 6 58 21 53 00\quad / \quad alexandre-mathieu-arch.github.io/works/}
    };
\end{tikzpicture}\null
\end{titlepage}

\clearpage\thispagestyle{empty}
\begin{tikzpicture}[remember picture,overlay]
  \fill[paper] (current page.south west) rectangle (current page.north east);
  \node[anchor=north west,inner sep=0,text width=18.2cm]
    at ([xshift=0.72cm,yshift=-0.62cm]current page.north west) {%
      {\fontsize{5.2}{6.2}\selectfont\mediumfont\color{muted}Index / Portfolio 2018–2026}\par
      \vspace{0.33cm}
      {\fontsize{19.2}{20.2}\selectfont\displayfont\color{ink}Sommaire}\par
      \vspace{0.22cm}
      {\fontsize{6.2}{7.4}\selectfont\lightfont\color{muted}Une lecture rapide des projets et de leur page d'ouverture.}
    };
  \node[anchor=south west,inner sep=0,text=muted]
    at ([xshift=0.72cm,yshift=0.56cm]current page.south west)
    {\fontsize{4.8}{5.8}\selectfont\lightfont Alexandre MATHIEU / PORTFOLIO V3};
\end{tikzpicture}
\vspace*{3.45cm}
\begin{multicols}{2}
%%TOC_PLACEHOLDER%%
\end{multicols}

%%PROJECTS_PLACEHOLDER%%
\end{document}
"""
    template = template[:document_start] + document_pages + template[document_end:]
    TEMPLATE_FILE.write_text(template, encoding="utf-8")


def configure_v3_paths():
    portfolio.OUTPUT_DIR = OUTPUT_DIR
    portfolio.OPTIMIZED_IMAGE_DIR = OUTPUT_DIR / "images"
    portfolio.CROPPED_IMAGE_DIR = OUTPUT_DIR / "crops"
    portfolio.TEMPLATE_FILE = TEMPLATE_FILE
    portfolio.TEX_FILE = OUTPUT_DIR / "portfolio_gen_v3.tex"
    portfolio.PDF_FILE = OUTPUT_DIR / "portfolio_gen_v3.pdf"
    portfolio.FINAL_PDF = BASE_DIR / "Alexandre-MATHIEU_PORTFOLIO-2026.pdf"


def prepare_editorial_frame(path, aspect_ratio, crop_key, centering=(0.5, 0.5), align="center"):
    """Crop landscape images gently; frame extreme ratios instead of mutilating them."""
    source = Path(path)
    with Image.open(source) as probe:
        source_ratio = probe.width / probe.height

    if aspect_ratio * 0.76 <= source_ratio <= aspect_ratio * 1.45:
        return portfolio.prepare_crop_for_pdf(path, aspect_ratio, crop_key, centering)

    digest = hashlib.sha1(
        f"v3-frame:{source}:{aspect_ratio:.5f}:{centering}:{align}".encode("utf-8")
    ).hexdigest()[:12]
    target = portfolio.CROPPED_IMAGE_DIR / f"{source.stem}-{crop_key}-{digest}.jpg"
    if target.exists() and target.stat().st_mtime >= source.stat().st_mtime:
        return str(target)

    image = ImageOps.exif_transpose(Image.open(source)).convert("RGB")
    if aspect_ratio >= 1:
        width = portfolio.MAX_IMAGE_DIMENSION
        height = round(width / aspect_ratio)
    else:
        height = portfolio.MAX_IMAGE_DIMENSION
        width = round(height * aspect_ratio)

    margin = round(min(width, height) * 0.035)
    fitted = ImageOps.contain(
        image,
        (width - 2 * margin, height - 2 * margin),
        method=Image.Resampling.LANCZOS,
    )
    canvas = Image.new("RGB", (width, height), (245, 241, 232))
    if align == "left":
        x = margin
    elif align == "right":
        x = width - fitted.width - margin
    else:
        x = (width - fitted.width) // 2
    canvas.paste(fitted, (x, (height - fitted.height) // 2))
    canvas.save(target, "JPEG", quality=portfolio.JPEG_QUALITY, optimize=True, progressive=True)
    return str(target)


def prepare_zoomed_source(path, crop_key):
    """Remove empty margins around plans while preserving the complete drawing."""
    source = Path(path)
    digest = hashlib.sha1(f"v3-zoom:{source}".encode("utf-8")).hexdigest()[:12]
    target = portfolio.CROPPED_IMAGE_DIR / f"{source.stem}-{crop_key}-zoom-{digest}.jpg"
    if target.exists() and target.stat().st_mtime >= source.stat().st_mtime:
        return str(target)

    image = ImageOps.exif_transpose(Image.open(source)).convert("RGB")
    grayscale = image.convert("L")
    drawing_mask = grayscale.point(lambda value: 255 if value < 248 else 0)
    bounds = drawing_mask.getbbox()
    if not bounds:
        return str(source)

    left, top, right, bottom = bounds
    margin_x = max(24, round((right - left) * 0.055))
    margin_y = max(24, round((bottom - top) * 0.075))
    bounds = (
        max(0, left - margin_x),
        max(0, top - margin_y),
        min(image.width, right + margin_x),
        min(image.height, bottom + margin_y),
    )
    cropped = image.crop(bounds)
    cropped.thumbnail(
        (portfolio.MAX_IMAGE_DIMENSION, portfolio.MAX_IMAGE_DIMENSION),
        Image.Resampling.LANCZOS,
    )
    cropped.save(target, "JPEG", quality=portfolio.JPEG_QUALITY, optimize=True, progressive=True)
    return str(target)


def prepare_manual_crop(path, crop, crop_key):
    """Apply an explicit editorial crop before automatic margin removal."""
    source = Path(path)
    digest = hashlib.sha1(
        f"v3-manual-crop:{source}:{crop}".encode("utf-8")
    ).hexdigest()[:12]
    target = portfolio.CROPPED_IMAGE_DIR / f"{source.stem}-{crop_key}-{crop}-{digest}.jpg"
    if target.exists() and target.stat().st_mtime >= source.stat().st_mtime:
        return str(target)

    image = ImageOps.exif_transpose(Image.open(source)).convert("RGB")
    if crop == "right-half":
        image = image.crop((image.width // 2, 0, image.width, image.height))
    elif crop == "left-half":
        image = image.crop((0, 0, image.width // 2, image.height))
    else:
        return str(source)

    image.save(target, "JPEG", quality=portfolio.JPEG_QUALITY, optimize=True, progressive=True)
    return str(target)


def prepare_portfolio_image(spec, aspect_ratio, crop_key, centering=(0.5, 0.5)):
    if isinstance(spec, str):
        path = spec
        zoom = False
        crop = None
        align = "center"
    else:
        path = spec.get("path", "")
        zoom = spec.get("zoom") is True
        crop = spec.get("crop")
        align = spec.get("align", "center")

    local_path = portfolio.local_image_path(path)
    if not local_path:
        return ""
    if crop:
        local_path = prepare_manual_crop(local_path, crop, crop_key)
    if zoom:
        local_path = prepare_zoomed_source(local_path, crop_key)
    return prepare_editorial_frame(local_path, aspect_ratio, crop_key, centering, align)


def prepare_equal_scale_plans(specs, crop_key, aspect_ratio=19.15 / 4.38):
    """Crop a plan set with one shared box, preserving a common drawing scale."""
    sources = []
    for spec in specs:
        path = spec if isinstance(spec, str) else spec.get("path", "")
        local_path = portfolio.local_image_path(path)
        if local_path:
            sources.append(Path(local_path))
    if len(sources) != len(specs):
        return []

    digest = hashlib.sha1(
        ("v3-equal-plans:" + ":".join(str(source) for source in sources)).encode("utf-8")
    ).hexdigest()[:12]
    targets = [
        portfolio.CROPPED_IMAGE_DIR / f"{source.stem}-{crop_key}-{index}-{digest}.jpg"
        for index, source in enumerate(sources)
    ]
    if all(
        target.exists() and target.stat().st_mtime >= source.stat().st_mtime
        for source, target in zip(sources, targets)
    ):
        return [str(target) for target in targets]

    images = [ImageOps.exif_transpose(Image.open(source)).convert("RGB") for source in sources]
    width = min(image.width for image in images)
    height = min(image.height for image in images)
    images = [image.resize((width, height), Image.Resampling.LANCZOS) for image in images]

    bounds = []
    for image in images:
        mask = image.convert("L").point(lambda value: 255 if value < 248 else 0)
        box = mask.getbbox()
        if box:
            bounds.append(box)
    if bounds:
        left = min(box[0] for box in bounds)
        top = min(box[1] for box in bounds)
        right = max(box[2] for box in bounds)
        bottom = max(box[3] for box in bounds)
        margin_x = max(24, round((right - left) * 0.035))
        margin_y = max(24, round((bottom - top) * 0.045))
        shared_box = (
            max(0, left - margin_x),
            max(0, top - margin_y),
            min(width, right + margin_x),
            min(height, bottom + margin_y),
        )
    else:
        shared_box = (0, 0, width, height)

    target_width = portfolio.MAX_IMAGE_DIMENSION
    target_height = round(target_width / aspect_ratio)
    for image, target in zip(images, targets):
        cropped = image.crop(shared_box)
        fitted = ImageOps.contain(
            cropped,
            (target_width, target_height),
            method=Image.Resampling.LANCZOS,
        )
        canvas = Image.new("RGB", (target_width, target_height), (245, 241, 232))
        canvas.paste(
            fitted,
            ((target_width - fitted.width) // 2, (target_height - fitted.height) // 2),
        )
        canvas.save(
            target,
            "JPEG",
            quality=portfolio.JPEG_QUALITY,
            optimize=True,
            progressive=True,
        )
    return [str(target) for target in targets]


def gallery_page_v3(title, label, images, page_index):
    count = len(images)
    title_tex = portfolio.tex_escape(title)
    label_tex = portfolio.tex_escape(label)
    if count == 1:
        image = prepare_editorial_frame(images[0], 210 / 148, f"v3-gallery-full-{page_index}")
        return rf"\galleryFullPage{{{title_tex}}}{{{label_tex}}}{{{image}}}" + "\n"
    if count == 2:
        main = prepare_editorial_frame(images[0], 210 / 148, f"v3-gallery-duo-main-{page_index}")
        inset = prepare_editorial_frame(images[1], 7.47 / 4.80, f"v3-gallery-duo-inset-{page_index}")
        return rf"\galleryDuoPage{{{title_tex}}}{{{label_tex}}}{{{main}}}{{{inset}}}" + "\n"
    if count == 3:
        main = prepare_editorial_frame(images[0], 13.75 / 8.70, f"v3-gallery-triptych-main-{page_index}")
        top = prepare_editorial_frame(images[1], 6.25 / 3.95, f"v3-gallery-triptych-top-{page_index}")
        bottom = prepare_editorial_frame(images[2], 6.25 / 3.95, f"v3-gallery-triptych-bottom-{page_index}")
        return rf"\galleryTriptychPage{{{title_tex}}}{{{label_tex}}}{{{main}}}{{{top}}}{{{bottom}}}" + "\n"

    framed = [
        prepare_editorial_frame(image, 10.28 / 6.50, f"v3-gallery-quad-{page_index}-{index}")
        for index, image in enumerate(images[:4])
    ]
    return (
        rf"\galleryQuadPage{{{title_tex}}}{{{label_tex}}}"
        rf"{{{framed[0]}}}{{{framed[1]}}}{{{framed[2]}}}{{{framed[3]}}}" + "\n"
    )


def configured_gallery_page(title, label, page, page_index):
    images = page.get("images", [])
    layout = page.get("layout", "").lower()
    title_tex = portfolio.tex_escape(title)
    label_tex = portfolio.tex_escape(label)

    if layout == "full" and images:
        image = prepare_portfolio_image(
            images[0], 210 / 148, f"v3-selected-full-{page_index}"
        )
        return rf"\galleryFullPage{{{title_tex}}}{{{label_tex}}}{{{image}}}" + "\n"

    if layout == "full-caption" and images:
        image = prepare_portfolio_image(
            images[0], 210 / 148, f"v3-selected-full-caption-{page_index}"
        )
        caption = images[0].get("caption", "") if isinstance(images[0], dict) else ""
        return (
            rf"\galleryFullCaptionPage{{{title_tex}}}{{{label_tex}}}"
            rf"{{{image}}}{{{portfolio.tex_escape(caption)}}}" + "\n"
        )

    if layout == "duo" and len(images) >= 2:
        main = prepare_portfolio_image(
            images[0], 210 / 148, f"v3-selected-duo-main-{page_index}"
        )
        inset = prepare_portfolio_image(
            images[1], 7.47 / 4.80, f"v3-selected-duo-inset-{page_index}"
        )
        return rf"\galleryDuoPage{{{title_tex}}}{{{label_tex}}}{{{main}}}{{{inset}}}" + "\n"

    if layout == "duo-caption" and len(images) >= 2:
        main = prepare_portfolio_image(
            images[0], 210 / 148, f"v3-selected-duo-caption-main-{page_index}"
        )
        inset = prepare_portfolio_image(
            images[1], 7.47 / 4.80, f"v3-selected-duo-caption-inset-{page_index}"
        )
        caption = images[1].get("caption", "") if isinstance(images[1], dict) else ""
        return (
            rf"\galleryDuoCaptionPage{{{title_tex}}}{{{label_tex}}}"
            rf"{{{main}}}{{{inset}}}{{{portfolio.tex_escape(caption)}}}" + "\n"
        )

    if layout == "triptych" and len(images) >= 3:
        main = prepare_portfolio_image(
            images[0], 13.75 / 8.70, f"v3-selected-triptych-main-{page_index}"
        )
        top = prepare_portfolio_image(
            images[1], 6.25 / 3.95, f"v3-selected-triptych-top-{page_index}"
        )
        bottom = prepare_portfolio_image(
            images[2], 6.25 / 3.95, f"v3-selected-triptych-bottom-{page_index}"
        )
        return rf"\galleryTriptychPage{{{title_tex}}}{{{label_tex}}}{{{main}}}{{{top}}}{{{bottom}}}" + "\n"

    if layout == "plans-feature" and len(images) >= 3:
        axonometric = prepare_portfolio_image(
            images[0], 1, f"v3-selected-plans-axo-{page_index}"
        )
        ground_floor = prepare_portfolio_image(
            images[1], 10.75 / 5.85, f"v3-selected-plans-rdc-{page_index}"
        )
        upper_floor = prepare_portfolio_image(
            images[2], 10.75 / 5.85, f"v3-selected-plans-upper-{page_index}"
        )
        return (
            rf"\galleryPlansPage{{{title_tex}}}{{{label_tex}}}"
            rf"{{{axonometric}}}{{{ground_floor}}}{{{upper_floor}}}" + "\n"
        )

    if layout == "plans-equal" and len(images) >= 3:
        plans = prepare_equal_scale_plans(
            images[:3], f"v3-selected-plans-equal-{page_index}"
        )
        if len(plans) == 3:
            return (
                rf"\galleryEqualPlansPage{{{title_tex}}}{{{label_tex}}}"
                rf"{{{plans[0]}}}{{{plans[1]}}}{{{plans[2]}}}" + "\n"
            )

    if layout == "plans-equal-quad" and len(images) >= 4:
        plans = prepare_equal_scale_plans(
            images[:4],
            f"v3-selected-plans-equal-quad-{page_index}",
            aspect_ratio=10.28 / 6.50,
        )
        if len(plans) == 4:
            return (
                rf"\galleryEqualPlansQuadPage{{{title_tex}}}{{{label_tex}}}"
                rf"{{{plans[0]}}}{{{plans[1]}}}{{{plans[2]}}}{{{plans[3]}}}" + "\n"
            )

    if layout == "plans-equal-duo" and len(images) >= 2:
        plans = prepare_equal_scale_plans(
            images[:2],
            f"v3-selected-plans-equal-duo-{page_index}",
            aspect_ratio=9.85 / 7.00,
        )
        if len(plans) == 2:
            return (
                rf"\galleryEqualPlansDuoPage{{{title_tex}}}{{{label_tex}}}"
                rf"{{{plans[0]}}}{{{plans[1]}}}" + "\n"
            )

    local_images = []
    for image in images:
        path = image if isinstance(image, str) else image.get("path")
        local_path = portfolio.local_image_path(path)
        if local_path:
            local_images.append(local_path)
    return gallery_page_v3(title, label, local_images, page_index)


def generate_tex_v3(projects):
    projects = [
        project
        for project in projects
        if (project.get("portfolio") or {}).get("enabled", True) is not False
    ]
    portfolio.OUTPUT_DIR.mkdir(exist_ok=True)
    portfolio.OPTIMIZED_IMAGE_DIR.mkdir(exist_ok=True)
    portfolio.CROPPED_IMAGE_DIR.mkdir(exist_ok=True)
    template = portfolio.TEMPLATE_FILE.read_text(encoding="utf-8")
    project_entries = []
    toc_entries = []
    cover_image = ""
    current_pdf_page = 3

    for index, project in enumerate(projects, start=1):
        title = project.get("title", "Sans titre")
        date = str(project.get("date", ""))
        label = f"{index:02d}"
        source_images = project.get("local_images", [])
        portfolio_config = project.get("portfolio") or {}
        cover_title = portfolio_config.get("cover_title", title)
        story_title = portfolio_config.get("story_title", title)
        configured_cover = portfolio_config.get("cover")
        configured_story = portfolio_config.get("story")
        configured_pages = portfolio_config.get("pages")
        if configured_pages is not None:
            extra_page_count = len(configured_pages)
        else:
            gallery_count = max(0, len(source_images) - 2)
            extra_page_count = (gallery_count + 3) // 4
        project_page_count = 2 + extra_page_count

        intro_image = prepare_portfolio_image(
            configured_cover, 210 / 148, f"v3-intro-{label}", centering=(0.5, 0.47)
        ) if configured_cover else (
            prepare_editorial_frame(
                source_images[0], 210 / 148, f"v3-intro-{label}", centering=(0.5, 0.47)
            ) if source_images else ""
        )
        story_image = prepare_portfolio_image(
            configured_story, 12.20 / 8.20, f"v3-story-{label}", centering=(0.5, 0.48)
        ) if configured_story else (
            prepare_editorial_frame(
                source_images[1] if len(source_images) > 1 else source_images[0],
                12.20 / 8.20,
                f"v3-story-{label}",
                centering=(0.5, 0.48),
            ) if source_images else ""
        )
        if not cover_image and intro_image:
            cover_image = intro_image

        toc_entries.append(
            rf"\portfolioTocEntry{{{label}}}{{{portfolio.tex_escape(title)}}}{{p.{current_pdf_page:02d}}}"
        )
        project_entries.append(rf"\hypertarget{{project-{label}}}{{}}")
        project_entries.append(
            rf"\projectIntroPage{{{label}}}{{{portfolio.tex_escape(cover_title)}}}{{{portfolio.tex_escape(date)}}}"
            rf"{{{portfolio.tex_escape(portfolio.project_subtitle(project))}}}{{{intro_image}}}"
        )
        project_entries.append(
            rf"\projectStoryPage{{{label}}}{{{portfolio.tex_escape(story_title)}}}{{{portfolio.meta_block(project)}}}"
            rf"{{{portfolio.text_block(project)}}}{{{story_image}}}"
        )
        if configured_pages is not None:
            for page_index, page in enumerate(configured_pages, start=1):
                project_entries.append(
                    configured_gallery_page(
                        title,
                        f"{label} / {page_index:02d}",
                        page,
                        page_index,
                    )
                )
            current_pdf_page += project_page_count
            continue

        gallery_images = source_images[2:]
        for page_index in range(0, len(gallery_images), 4):
            group = gallery_images[page_index:page_index + 4]
            project_entries.append(
                gallery_page_v3(title, f"{label} / {page_index // 4 + 1:02d}", group, page_index)
            )
        current_pdf_page += project_page_count

    generated = template
    generated = generated.replace("%%COVER_IMAGE%%", cover_image)
    generated = generated.replace("%%TOC_PLACEHOLDER%%", "\n".join(toc_entries))
    generated = generated.replace("%%PROJECT_COUNT%%", str(len(projects)))
    generated = generated.replace("%%PROJECTS_PLACEHOLDER%%", "\n\n".join(project_entries))
    portfolio.TEX_FILE.write_text(generated, encoding="utf-8")


if __name__ == "__main__":
    prepare_v3_template()
    configure_v3_paths()

    projects = portfolio.parse_projects()
    print(f"{len(projects)} projets trouves.")
    generate_tex_v3(projects)
    print(f"Fichier LaTeX V3 genere : {portfolio.TEX_FILE}")

    if "--compile" in sys.argv:
        portfolio.compile_pdf()
        print(f"PDF V3 genere : {portfolio.PDF_FILE}")
        print(f"PDF final copie : {portfolio.FINAL_PDF}")
    else:
        print("Compilez avec : python3 build_portfolio_v3.py --compile")

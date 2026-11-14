# Pandoc Structural Validation

Use these checks after the real build. Adapt paths and heading text; keep assertions tied to the task's declared chapter count and heading level.

## DOCX

A DOCX is a ZIP package. Parse XML instead of grepping binary data:

```python
from zipfile import ZipFile
from xml.etree import ElementTree as ET
import re

with ZipFile(docx_path) as zf:
    xml = zf.read("word/document.xml").decode("utf-8")
    text = " ".join(ET.fromstring(xml).itertext())

assert title in text
assert subtitle in text
assert re.findall(chapter_number_pattern, text) == expected_chapter_numbers
assert xml.count('w:type="page"') == expected_chapter_count
assert scene_break in text
```

Also verify the first page break occurs after title metadata and before chapter 1. Counting breaks without checking placement can miss a misplaced break and a missing chapter break that cancel numerically.

## EPUB 3

Resolve the package through the container instead of assuming a fixed OPF path:

```python
from pathlib import PurePosixPath
from zipfile import ZipFile
from xml.etree import ElementTree as ET

with ZipFile(epub_path) as zf:
    container = ET.fromstring(zf.read("META-INF/container.xml"))
    cns = {"c": "urn:oasis:names:tc:opendocument:xmlns:container"}
    package_path = container.find(".//c:rootfile", cns).attrib["full-path"]
    package = ET.fromstring(zf.read(package_path))
    assert package.attrib["version"].startswith("3")

    ons = {"opf": "http://www.idpf.org/2007/opf"}
    manifest = {
        item.attrib["id"]: item.attrib["href"]
        for item in package.findall(".//opf:manifest/opf:item", ons)
    }
    spine_hrefs = [
        manifest[item.attrib["idref"]]
        for item in package.findall(".//opf:spine/opf:itemref", ons)
    ]
    package_dir = PurePosixPath(package_path).parent
    spine_sizes = {
        href: zf.getinfo(str(package_dir / href)).file_size
        for href in spine_hrefs
    }
```

Then assert:

- the declared number of chapter content files exists;
- no chapter content file is unexpectedly large compared with its peers;
- the navigation document has one intended entry per chapter;
- every navigation `href` resolves to an existing file and, when it has a fragment, an existing element id;
- title, language, and other required metadata match exactly;
- scene-break counts and internal-marker absence agree with the stripped intermediate.

Do not hardcode a universal byte threshold. Record the largest item and investigate outliers; image-heavy or reference books can legitimately need larger spine items than prose novels.

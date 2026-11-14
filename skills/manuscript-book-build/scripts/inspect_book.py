"""Inspect a built DOCX + EPUB pair. Usage: python3 inspect_book.py <build_dir>/ <basename>"""

import re
import sys
import zipfile
from collections import Counter

b, base = sys.argv[1], sys.argv[2]
LEAKS = ("<!--", "&lt;!--", "[//]", "[INTERNAL", "openxml")

z = zipfile.ZipFile(b + base + ".docx")
d = z.read("word/document.xml").decode()
paras = re.findall(r"<w:p>.*?</w:p>|<w:p .*?</w:p>", d, re.S)


def txt(p):
    return "".join(re.findall(r"<w:t[^>]*>([^<]*)</w:t>", p))


def sty(p):
    m = re.search(r'<w:pStyle w:val="([^"]+)"', p)
    return m.group(1) if m else ""


print("== DOCX first paras")
for i, p in enumerate(paras[:5]):
    print(i, sty(p), repr(txt(p)[:60]), "PAGEBREAK" if 'w:type="page"' in p else "")
heads = [(sty(p), txt(p)) for p in paras if sty(p).startswith("Heading")]
print("headings:", len(heads))
for h in heads:
    print(" ", h)
print("styles:", Counter(sty(p) for p in paras))
print("page breaks:", d.count('w:type="page"'))
print("short paras (scene-break candidates):",
      Counter(txt(p).strip() for p in paras if 0 < len(txt(p).strip()) < 6).most_common(5))
print("docx leaks:", [m for m in LEAKS[:4] if m in d])

print("== EPUB")
e = zipfile.ZipFile(b + base + ".epub")
names = e.namelist()
print("mimetype first:", names[0], e.read("mimetype"))
opf = [n for n in names if n.endswith(".opf")][0]
o = e.read(opf).decode()
print(opf, re.search(r"<package[^>]*>", o).group(0))
print("title:", re.findall(r"<dc:title[^>]*>([^<]*)", o),
      "lang:", re.findall(r"<dc:language>([^<]*)", o))
nav = [n for n in names if n.endswith("nav.xhtml")][0]
nv = e.read(nav).decode()
tocnav = re.search(r'<nav[^>]*epub:type="toc".*?</nav>', nv, re.S).group(0)
links = re.findall(r'<a href="([^"]+)"[^>]*>(.*?)</a>', tocnav, re.S)
print("toc entries:", len(links))
for h, t in links:
    print(" ", h, re.sub("<[^>]+>", "", t).strip())
root = nav.rsplit("/", 1)[0] + "/" if "/" in nav else ""
print("dangling toc hrefs:", [h for h, _ in links if root + h.split("#")[0] not in names])
print("spine xhtml sizes:")
for i in e.infolist():
    if i.filename.endswith(".xhtml"):
        print(f"  {i.file_size:>9}  {i.filename}")
body = "".join(e.read(n).decode() for n in names if n.endswith(".xhtml"))
print("epub leaks:", [m for m in LEAKS[1:] if m in body])

"""SVG normalization: dedupe IDs, drop external references, serialize consistently."""
from __future__ import annotations

import xml.etree.ElementTree as ET
from pathlib import Path

SVG_NS = "{http://www.w3.org/2000/svg}"
_XLINK = "{http://www.w3.org/1999/xlink}"

ET.register_namespace("", "http://www.w3.org/2000/svg")


def _dedupe_ids(root: ET.Element) -> None:
    seen: set[str] = set()
    for elem in root.iter():
        elem_id = elem.get("id")
        if not elem_id:
            continue
        if elem_id in seen:
            elem.set("id", f"{elem_id}_{len(seen)}")
        seen.add(elem.get("id"))


def _drop_external_refs(root: ET.Element) -> None:
    for elem in root.iter():
        for attr in list(elem.attrib):
            if attr == _XLINK + "href" or (attr == "href" and elem.tag == f"{SVG_NS}use"):
                del elem.attrib[attr]
        if elem.tag == f"{SVG_NS}use":
            elem.attrib.pop("href", None)


def _strip_inner_doctype(root: ET.Element) -> None:
    # Remove any stray DOCTYPE text that may have been written into the XML.
    for elem in root.iter():
        if elem.text and "<!DOCTYPE" in elem.text:
            elem.text = elem.text.split("<!DOCTYPE")[0]


def normalize_svg(source: Path, target: Path) -> None:
    parser = ET.XMLParser()
    raw = source.read_text(encoding="utf-8")
    # xml.dom.minidom / svgutils may emit an XML declaration with its own encoding
    if raw.startswith("<?xml"):
        raw = raw[raw.find("?>") + 2 :].lstrip()
    root = ET.fromstring(raw, parser=parser)
    _dedupe_ids(root)
    _drop_external_refs(root)
    _strip_inner_doctype(root)
    viewbox = root.get("viewBox")
    if viewbox is None:
        root.set("viewBox", "0 0 100 100")
    ET.indent(root, space="  ")
    target.write_text(
        '<?xml version="1.0" encoding="UTF-8" standalone="no"?>\n'
        "<!DOCTYPE svg PUBLIC \"-//W3C//DTD SVG 1.1//EN\" \"http://www.w3.org/Graphics/SVG/1.1/DTD/svg11.dtd\">\n"
        + ET.tostring(root, encoding="unicode", short_empty_elements=True),
        encoding="utf-8",
    )

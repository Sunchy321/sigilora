import json
from pathlib import Path
import re


ROOT = Path(__file__).parents[1] / "fonts" / "pokemon" / "design"
TYPES = ["Grass", "Fire", "Water", "Lightning", "Psychic", "Fighting",
         "Darkness", "Metal", "Fairy", "Dragon", "Colorless"]


def test_energy_metadata_has_layered_gradient_parameters():
    colors = json.loads((ROOT / "assets" / "colors.json").read_text())
    assert set(colors) == set(TYPES)
    for typ in TYPES:
        data = colors[typ]
        assert len(data["background"]) in (2, 3)
        assert -180 <= data["background_angle"] <= 180
        assert len(data["body_center"]) == 2
        assert 0 < data["body_radius"] <= 1
        assert data.get("color_gain", 1.08) >= 1
        assert 0 < data.get("body_opacity", 0.28) <= 1
        assert len(data["highlight_size"]) == 2
        assert all(value > 0 for value in data["highlight_size"])
        assert 0 <= data["highlight_angle"] < 360 or -360 < data["highlight_angle"] < 0
        assert len(data["highlight_opacity"]) == 2


def test_generated_svgs_have_clipped_highlights_and_unique_ids():
    for typ in TYPES:
        svg = (ROOT / "svg" / f"{typ}.svg").read_text()
        assert f'id="orbClip{typ}"' in svg
        assert f'clip-path="url(#orbClip{typ})"' in svg
        assert f'id="background{typ}"' in svg
        assert f'id="body{typ}"' in svg
        assert f'id="sheen{typ}"' in svg
        assert f'id="sheenMask{typ}"' in svg
        if typ == "Darkness":
            assert re.search(r'<ellipse .+?fill="url\(#darknessHighlightDarkness\)"', svg)
        else:
            assert re.search(r'<path d=".+?" fill="#FFFFFF" opacity="', svg)
        assert re.search(r'<path d=".+?" transform=".+?" fill="#[0-9A-Fa-f]{6}"', svg)
        if typ != "Darkness":
            assert re.search(r'<path d=".+?" transform=', svg)


def test_highlights_share_upper_left_light_source():
    colors = json.loads((ROOT / "assets" / "colors.json").read_text())
    assert {tuple(data["sheen_rel"]) for data in colors.values()} == {(-0.44, -0.44)}
    assert {tuple(data["highlight_size"]) for data in colors.values()} == {(14, 18)}
    assert {data["highlight_angle"] for data in colors.values()} == {30}

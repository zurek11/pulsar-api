"""Download verified space engineering papers from arXiv into data/documents/."""

import urllib.request

from core.config import get_settings

# All URLs verified via web search — real arXiv papers
PAPERS = {
    # Space propulsion
    "space_propulsion_comparison": "https://arxiv.org/pdf/2402.15536",
    "vacuum_spacetime_propulsion": "https://arxiv.org/pdf/1204.2184",
    "solar_sailing_advances_2023": "https://arxiv.org/pdf/2411.12492",
    "multimode_spacecraft_trajectory": "https://arxiv.org/pdf/2511.19505",
    "space_based_ai_infrastructure": "https://arxiv.org/pdf/2511.19468",
    "interstellar_object_flyby": "https://arxiv.org/pdf/2507.15755",
    # Mars colonization
    "mars_colonization_blueprint": "https://arxiv.org/pdf/2309.11524",
    # Astronomy & astrophysics NLP
    "astrobert_language_model": "https://arxiv.org/pdf/2112.00590",
    # Starlink & satellite constellations
    "starlink_photometric": "https://arxiv.org/pdf/2306.06657",
    # CubeSat & small satellites
    "small_sat_propulsion_survey": "https://aerospace.org/sites/default/files/2024-02/20231218%20Small%20Satellite%20Propulsion%20Survey_DISTRO_A.pdf",
}


def main() -> None:
    output_dir = get_settings().project_root / "data" / "documents"
    output_dir.mkdir(parents=True, exist_ok=True)

    headers = {"User-Agent": "Mozilla/5.0 (pulsar-api learning project)"}

    count = 0
    failed = 0

    for name, url in PAPERS.items():
        filepath = output_dir / f"{name}.pdf"

        if filepath.exists():
            print(f"⏭️  Already exists: {filepath.name}")
            count += 1
            continue

        print(f"⬇️  Downloading: {name}...")
        try:
            req = urllib.request.Request(url, headers=headers)
            with urllib.request.urlopen(req, timeout=30) as response:
                filepath.write_bytes(response.read())

            size_mb = filepath.stat().st_size / (1024 * 1024)
            if size_mb < 0.01:
                filepath.unlink()
                print(f"   ❌ Too small ({size_mb:.3f} MB) — probably not a real PDF")
                failed += 1
                continue

            print(f"   ✅ {filepath.name} ({size_mb:.1f} MB)")
            count += 1
        except Exception as e:
            print(f"   ❌ Failed: {e}")
            failed += 1

    print(f"\n🚀 {count} papers downloaded, {failed} failed")
    print(f"📂 Location: {output_dir}")


if __name__ == "__main__":
    main()

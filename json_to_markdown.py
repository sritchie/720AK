#!/usr/bin/env python3
"""
Convert efis-editor checklist JSON to Pandoc markdown sections.

The efis-editor JSON format is the source of truth for checklists.
This script generates markdown sections for normal, abnormal, and emergency
procedures that can be included in the POH.

Usage:
    python3 json_to_markdown.py checklist.json

This generates:
    sections/04-emergency.md   (emergency procedures)
    sections/04b-abnormal.md   (abnormal procedures, if any)
    sections/05-normal.md      (normal procedures)
"""

import json
import sys
from pathlib import Path

# Category mappings from the efis-editor protobuf enum
CATEGORY_NORMAL = 0
CATEGORY_ABNORMAL = 1
CATEGORY_EMERGENCY = 2


def format_challenge_response(challenge: str, response: str, indent: int = 0) -> str:
    """Format a challenge-response item with dot leaders."""
    prefix = "  " * indent
    if not response:
        return f"{prefix}- {challenge}"

    # Create dot leader effect using a table-like format for better PDF output
    return f"{prefix}- {challenge} {'.' * 3} **{response}**"


def format_item(item: dict, indent: int = 0) -> str:
    """Format a single checklist item based on its type."""
    item_type = item.get("type", "ITEM_CHALLENGE_RESPONSE")
    prefix = "  " * indent

    if item_type == "ITEM_SPACE":
        return ""

    if item_type == "ITEM_TITLE":
        title = item.get("title", "")
        if not title.strip():
            return ""  # Skip empty titles
        return f"\n{prefix}**{title}**\n"

    if item_type == "ITEM_NOTE":
        prompt = item.get("prompt", "")
        return f"\n{prefix}> *Note: {prompt}*\n"

    if item_type == "ITEM_PLAINTEXT":
        prompt = item.get("prompt", "")
        return f"{prefix}  {prompt}"

    if item_type == "ITEM_CHALLENGE_RESPONSE":
        prompt = item.get("prompt", "")
        expectation = item.get("expectation", "")
        centered = item.get("centered", False)

        if centered and not expectation:
            return f"\n{prefix}**{prompt}**\n"

        return format_challenge_response(prompt, expectation, indent)

    # Default fallback
    prompt = item.get("prompt", item.get("title", ""))
    return f"{prefix}- {prompt}"


def format_checklist(checklist: dict) -> str:
    """Format a single checklist (e.g., 'Preflight Inspection')."""
    lines = []
    title = checklist.get("title", "Untitled")

    lines.append(f"### {title}")
    lines.append("")

    for item in checklist.get("items", []):
        indent = item.get("indent", 0)
        formatted = format_item(item, indent)
        if formatted:
            lines.append(formatted)

    lines.append("")
    return "\n".join(lines)


def format_group(group: dict) -> str:
    """Format a checklist group (e.g., 'Preflight' containing multiple checklists)."""
    lines = []
    title = group.get("title", "Untitled Group")

    lines.append(f"## {title}")
    lines.append("")

    for checklist in group.get("checklists", []):
        lines.append(format_checklist(checklist))

    return "\n".join(lines)


def get_aircraft_info(data: dict) -> dict:
    """Extract aircraft metadata from the JSON."""
    metadata = data.get("metadata", {})
    return {
        "name": metadata.get("name", ""),
        "make_model": metadata.get("makeAndModel", ""),
        "aircraft_info": metadata.get("aircraftInfo", ""),
    }


def convert_json_to_markdown(json_path: str) -> dict[str, str]:
    """
    Convert checklist JSON to markdown sections.

    Returns dict with:
        - 'normal': normal procedures markdown
        - 'abnormal': abnormal procedures markdown (if any)
        - 'emergency': emergency procedures markdown (if any)
        - 'aircraft_info': metadata about the aircraft
    """
    with open(json_path, 'r') as f:
        data = json.load(f)

    normal_groups = []
    abnormal_groups = []
    emergency_groups = []

    for group in data.get("groups", []):
        category = group.get("category", CATEGORY_NORMAL)

        if category == CATEGORY_EMERGENCY:
            emergency_groups.append(group)
        elif category == CATEGORY_ABNORMAL:
            abnormal_groups.append(group)
        else:
            normal_groups.append(group)

    results = {
        "aircraft_info": get_aircraft_info(data)
    }

    # Emergency procedures
    if emergency_groups:
        lines = ["# Emergency Procedures", ""]
        lines.append("> These procedures are derived from the efis-editor checklist file.")
        lines.append("> Update the source JSON and regenerate to modify.")
        lines.append("")
        for group in emergency_groups:
            lines.append(format_group(group))
        results["emergency"] = "\n".join(lines)

    # Abnormal procedures
    if abnormal_groups:
        lines = ["# Abnormal Procedures", ""]
        lines.append("> These procedures are derived from the efis-editor checklist file.")
        lines.append("")
        for group in abnormal_groups:
            lines.append(format_group(group))
        results["abnormal"] = "\n".join(lines)

    # Normal procedures
    if normal_groups:
        lines = ["# Normal Procedures", ""]
        lines.append("> These procedures are derived from the efis-editor checklist file.")
        lines.append("> Update the source JSON and regenerate to modify.")
        lines.append("")
        for group in normal_groups:
            lines.append(format_group(group))
        results["normal"] = "\n".join(lines)

    return results


def main():
    if len(sys.argv) < 2:
        print("Usage: python3 json_to_markdown.py <checklist.json>")
        print()
        print("Converts efis-editor JSON checklists to POH markdown sections.")
        print()
        print("Output files:")
        print("  sections/04-emergency.md   - Emergency procedures")
        print("  sections/04b-abnormal.md   - Abnormal procedures (if any)")
        print("  sections/05-normal.md      - Normal procedures")
        sys.exit(1)

    json_path = sys.argv[1]

    if not Path(json_path).exists():
        print(f"Error: File not found: {json_path}")
        sys.exit(1)

    # Ensure sections directory exists
    sections_dir = Path("sections")
    sections_dir.mkdir(exist_ok=True)

    print(f"Reading: {json_path}")
    results = convert_json_to_markdown(json_path)

    # Show aircraft info
    info = results["aircraft_info"]
    if info["name"]:
        print(f"Aircraft: {info['name']}")
    if info["make_model"]:
        print(f"Make/Model: {info['make_model']}")

    # Write emergency procedures
    if "emergency" in results:
        output_path = sections_dir / "04-emergency.md"
        with open(output_path, 'w') as f:
            f.write(results["emergency"])
        print(f"Wrote: {output_path}")

    # Write abnormal procedures
    if "abnormal" in results:
        output_path = sections_dir / "04b-abnormal.md"
        with open(output_path, 'w') as f:
            f.write(results["abnormal"])
        print(f"Wrote: {output_path}")

    # Write normal procedures
    if "normal" in results:
        output_path = sections_dir / "05-normal.md"
        with open(output_path, 'w') as f:
            f.write(results["normal"])
        print(f"Wrote: {output_path}")

    print()
    print("Done! Run ./build.sh to generate the PDF.")


if __name__ == "__main__":
    main()

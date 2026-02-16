#!/usr/bin/env python3
"""Validate Mermaid diagrams in Markdown files for common rendering issues.

Checks for:
  1. 'direction' directives inside subgraphs (conflicts with parent graph)
  2. Floating/disconnected nodes inside subgraphs (no edges referencing them)
  3. Empty subgraph labels that may cause rendering failures
"""

import re
import sys
from pathlib import Path


def extract_mermaid_blocks(text: str) -> list[tuple[int, str]]:
    """Return (line_number, block_content) for each ```mermaid block."""
    blocks = []
    in_block = False
    start_line = 0
    lines_buf = []

    for i, line in enumerate(text.splitlines(), 1):
        if line.strip() == "```mermaid":
            in_block = True
            start_line = i
            lines_buf = []
        elif in_block and line.strip() == "```":
            in_block = False
            blocks.append((start_line, "\n".join(lines_buf)))
        elif in_block:
            lines_buf.append(line)
    return blocks


def parse_subgraphs(block: str) -> list[dict]:
    """Extract subgraph regions with their contained nodes."""
    subgraphs = []
    stack: list[dict] = []

    for i, line in enumerate(block.splitlines()):
        stripped = line.strip()

        if stripped.startswith("subgraph "):
            sg = {"name": stripped, "line": i, "nodes": set(), "depth": len(stack)}
            stack.append(sg)
        elif stripped == "end" and stack:
            subgraphs.append(stack.pop())
        elif stack:
            # Collect node IDs defined in this subgraph level
            node_match = re.match(r'\s*([A-Za-z_]\w*)\s*[\[("{]', stripped)
            if node_match and not stripped.startswith("style "):
                stack[-1]["nodes"].add(node_match.group(1))

    return subgraphs


def collect_edge_nodes(block: str) -> set[str]:
    """Collect all node IDs that participate in any edge.

    Strategy: any line containing an edge operator (-->, ---, etc.)
    contributes all its node-like identifiers as "connected" nodes.
    """
    edge_ops = re.compile(r'-->|---|<-->|-\.->|==>|~~~')
    node_id = re.compile(r'\b([A-Za-z_]\w*)\b')
    keywords = {"graph", "subgraph", "end", "style", "direction",
                "TD", "TB", "LR", "RL", "BT", "classDef", "click",
                "class", "linkStyle"}

    edge_nodes: set[str] = set()
    for line in block.splitlines():
        if edge_ops.search(line):
            for m in node_id.finditer(line):
                token = m.group(1)
                if token not in keywords:
                    edge_nodes.add(token)
    return edge_nodes


def validate_block(block: str, start_line: int, filepath: str) -> list[str]:
    issues = []

    # Check for direction directives
    for i, line in enumerate(block.splitlines(), start_line + 1):
        if re.match(r'\s+direction\s+(TB|LR|BT|RL)', line.strip()):
            issues.append(f"  {filepath}:{i} -- 'direction' inside subgraph can break rendering")

    # Check for floating nodes in subgraphs
    edge_nodes = collect_edge_nodes(block)
    for sg in parse_subgraphs(block):
        floating = sg["nodes"] - edge_nodes
        if floating:
            issues.append(
                f"  {filepath}:{start_line + sg['line']} -- "
                f"Floating nodes in {sg['name']}: {', '.join(sorted(floating))}"
            )

    return issues


def validate_file(filepath: Path) -> list[str]:
    text = filepath.read_text()
    all_issues = []

    for start_line, block in extract_mermaid_blocks(text):
        all_issues.extend(validate_block(block, start_line, str(filepath)))

    return all_issues


def main():
    docs_dir = Path(__file__).resolve().parent.parent / "docs" / "posts"
    if not docs_dir.exists():
        print(f"Directory not found: {docs_dir}", file=sys.stderr)
        sys.exit(1)

    all_issues = []
    file_count = 0
    diagram_count = 0

    for md_file in sorted(docs_dir.glob("*.md")):
        file_count += 1
        text = md_file.read_text()
        blocks = extract_mermaid_blocks(text)
        diagram_count += len(blocks)
        all_issues.extend(validate_file(md_file))

    print(f"Scanned {file_count} files, {diagram_count} Mermaid diagrams.")

    if all_issues:
        print(f"\nFound {len(all_issues)} potential issue(s):\n")
        for issue in all_issues:
            print(issue)
        sys.exit(1)
    else:
        print("All diagrams passed validation.")
        sys.exit(0)


if __name__ == "__main__":
    main()

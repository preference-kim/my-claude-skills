#!/usr/bin/env python3
"""Freeze supplied-guidance variants from inspected baseline/candidate checkouts."""

import argparse
import hashlib
import json
from pathlib import Path


def read(root, relative):
    return (root / relative).read_text()


def principles(root):
    text = read(root, "AGENTS.md")
    return text[text.index("### Scientific reasoning"):text.index("### Code and design clarity")]


def repair_simple(text):
    changes = {
        '5. Modals: can, will, must. Never should, would, may, might, could. A required "should" becomes "must". An optional one is deleted.':
        '5. Preserve obligation, permission, recommendations, and uncertainty. Modal words are permitted when they carry those distinctions; do not upgrade a recommendation into a requirement.',
        'Use `make sure that` for check, verify, confirm, validate, ensure. Use `configuration` for config, settings, options.':
        'Preserve domain distinctions among check, verify, confirm, validate, ensure, configuration, settings, and options. Simplify only where meanings are equivalent.',
        'Every chat reply, in every mode, follows these rules:':
        'For a plain-language reply without a specialist artifact contract, follow these rules. Preserve formatting needed for the task:',
        '1. Answer in prose. No headers, no bullet lists, no bold, no tables. A code block is legal when the reader must copy it.':
        '1. Use prose for a short reply; use headings, lists, or tables when they help the task or its required structure. Keep copyable commands intact.',
        '1. Reply: search for `—`, `**`, `#`, and a line that starts with `-`. Remove each one.':
        '1. Reply: remove decorative formatting, preserving structure needed for the task.',
        "Search for `'`, `has been`, `should`, `may`, `;`, `—`, `, making`, `**`, `check`, `verify`, `config`, and any heading that covers fewer than three sentences. Fix each hit.":
        'Check awkward syntax and decorative formatting. Preserve technical terminology, warranted uncertainty, and artifact-specific structure.',
    }
    for old, new in changes.items():
        if old not in text:
            raise ValueError("baseline changed; review the B transformation before running")
        text = text.replace(old, new)
    return text


def build(args):
    cases = json.loads((Path(__file__).parent / "cases.json").read_text())
    sources = {}
    for variant in ("A", "B", "C"):
        candidate = variant == "C"
        dot = args.candidate_dotfiles if candidate else args.baseline_dotfiles
        skills = args.candidate_skills if candidate else args.baseline_skills
        audit = args.candidate_audit if candidate else args.baseline_audit
        for case in cases:
            parts = [principles(dot)]
            if case["kind"] in {"document", "pr", "handoff"}:
                if candidate:
                    parts.append(read(skills, "technical-communication/SKILL.md"))
                else:
                    simple = read(skills, "simple-english/skills/simple-english/SKILL.md")
                    parts.append(repair_simple(simple) if variant == "B" else simple)
            if case["kind"] in {"pr", "handoff"}:
                if not candidate:
                    parts.append(read(skills, "humanizer/SKILL.md"))
                if case["kind"] == "pr":
                    parts += [read(skills, "write-technical-pr/references/policy.md"),
                              read(skills, "write-technical-pr/references/evidence.md")]
                else:
                    parts.append(read(skills, "agent-handoff/references/content.md"))
            if case["kind"] in {"pr", "handoff", "audit", "repair"}:
                parts.append(read(audit, "SKILL.md"))
            text = "\n\n".join(parts) + "\n"
            path = args.output / variant / (case["id"] + ".md")
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(text)
            sources[str(path.relative_to(args.output))] = {"sha256": hashlib.sha256(text.encode()).hexdigest(), "words": len(text.split()), "bytes": len(text.encode())}
    (args.output / "manifest.json").write_text(json.dumps(sources, indent=2) + "\n")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    for name in ("baseline-dotfiles", "candidate-dotfiles", "baseline-skills", "candidate-skills", "baseline-audit", "candidate-audit", "output"):
        parser.add_argument("--" + name, type=Path, required=True)
    arguments = parser.parse_args()
    if arguments.output.exists():
        parser.error("output already exists; preserve frozen guidance and select a new directory")
    build(arguments)

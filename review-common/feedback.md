# PR finding contract

Each retained finding covers one concrete, high-confidence issue:

1. State the precise problem, triggering conditions, and concrete impact.
2. Explain the fundamental design contract or established principle the solution
   must satisfy. Cite the smallest relevant code location and, when applicable,
   an authoritative specification or documentation link that supports the claim.
   Explain why the reference applies; distinguish convention from preference.
3. End with concise, specific code or test suggestions.

Use only enough prose to establish that causal chain. Omit generic tutorials,
repeated summaries, orchestration details, and speculative/style-only findings.
No finding is preferable to a manufactured one. Preserve reviewer prefixes only
where the invoking workflow requires them. Do not add headings merely to fill a
three-part template. Keep material uncertainty explicit; do not invent references.

Read [stop-bullshit](../stop-bullshit/SKILL.md) before composing reviewer prompts.
Copy this finding contract and the loaded skill's instructions into each isolated
leaf prompt; leaves apply `stop-bullshit` directly without invoking skills or
another critic. It must check both the reviewed material and the reviewer's own
comments before any permitted write. Apply it again when consolidating findings,
including those from external reviewers, and after the last prose edit. Validate
the final wording against this finding contract too.

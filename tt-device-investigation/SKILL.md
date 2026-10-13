---
name: tt-device-investigation
description: Use when a suspected Tenstorrent device anomaly requires a minimal reproducer, host/device/core localization, upstream tt-metal verification, or a submission package. Covers nondeterministic outputs and data corruption; not routine op correctness, performance tuning, or standalone hang/reset recovery.
---

# TT Device Investigation

Establish the observed failure and its location, verify a minimal reproducer on
upstream tt-metal, and deliver `report.md` with `reproducer.zip`. A suspected
device anomaly does not by itself establish a hardware defect.

## Entry conditions

Resolve links from this skill's canonical directory. Read the [basic guide](../../agent-guidance/tt-metal/README.md)
before builds or device access, [kernel guidance](../../agent-guidance/tt-metal/kernels.md)
before kernel edits, and [Git guidance](../../agent-guidance/version-control.md)
before checkout changes. For hangs, initialization failures, or reset failures,
read [recovery](../../agent-guidance/tt-metal/debugging.md).

Follow the site's device access protocol. CPU-only builds need no device
reservation. Preserve the measured firmware, driver, and power configuration
unless changing them is part of the authorized experiment.

## Reproduce and localize

1. Before each experiment, define inputs, expected behavior, comparison criterion,
   repetitions, and failure condition. Test corruption (disagreement with expected
   output) separately from nondeterminism (different outputs under identical
   inputs and conditions). Use bitwise comparison for exact preservation and
   justify numerical tolerances.
2. Remove model and dataset dependencies. Use a small TTNN example unless direct
   control of cores, register slots, or data movement calls for a gtest. Make
   input construction, operation, and check visible. Retain required initialization,
   synchronization, and barriers. Remove only details unnecessary to reproduce
   or detect the failure.
3. Record the actual host, PCI BDF, and mapped UMD logical chip ID, plus ASIC
   identity when available. Device-node numbers alone are insufficient. For
   relevant units, record logical and physical core coordinates, NoC coordinate
   system, and register/tile slots. Recheck mappings after reset or visibility
   changes.
4. Change one relevant condition per control: core, device, slot, operation, or
   memory path. Distinguish the observation point from the fault's origin. Later
   successful reads do not validate earlier reads, and removing an operation
   changes timing too. Localize a unit only with supporting evidence, otherwise
   report the failing path. Passing controls support only their tested conditions.
5. Record completed repetitions, failed executions, mismatch counts, and changes
   between successive outputs with explicit counting units. Preserve representative
   expected/actual values and bits, storage layout, and offset meanings. Report
   initialization failures and timeouts separately from numerical measurements.

## Upstream verification

Fetch Tenstorrent's upstream `main` at investigation time and pin the full hash.
Preserve existing checkout changes under Git guidance. Apply only the reproducer
and required integration, then build and run on the same identified device with
comparable inputs and configuration. Record relevant runtime/submodule revisions
and software versions. A branch need not be published for this verification.

Report build success, completed reproduction, completed non-reproduction, or
inability to run distinctly. A fork result or build alone is not upstream
reproduction. Freeze tested sources and invocation. Rerun after changing sources
or execution settings. Retain valid evidence and the final package. Remove superseded probes
under the cleanup policy and restore the original checkout and build environment.

## Deliverables and acceptance

Write `report.md` for an external reader in this order:

1. Upstream result and observed symptom: nondeterminism, corruption, or both.
2. Exact host/device/unit identity, full upstream hash, versions, and conditions.
3. Input, operation, expected result, and minimal test explanation.
4. Measurements and controls, with denominators, units, and a failure signature.
5. Reproduction procedure using the package.

Put material evidence in the report. Use no local-path links and do not rely on
inaccessible logs. Omit internal discussions, reservation metadata, work chronology,
and cleanup history unless the recipient needs them. Qualify conclusions where they appear.
Keep necessary site-specific procedures in the package README.

Include the exact tested sources and device kernels, a complete patch against
the pinned base with all build integration, `report.md`, and file checksums in
`reproducer.zip`. Include a `README.md` with prerequisites, placement, patch
application, additional changes, build/run commands, controls, and expected
normal/failure behavior.

Check clean-base patch applicability, packaged/tested source equality, ZIP
integrity, checksums, and consistency of commands and results. The package must
need no unpublished branch or unlisted file. Deliver both artifacts. Posting to
an external service requires the task's publication authority.

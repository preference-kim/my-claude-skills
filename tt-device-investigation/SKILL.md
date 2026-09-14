---
name: tt-device-investigation
description: Use when a suspected Tenstorrent device anomaly requires a minimal reproducer, host/device/core localization, upstream tt-metal verification, or a submission package. Covers nondeterministic outputs and data corruption; not routine op correctness, performance tuning, or standalone hang/reset recovery.
---

# TT Device Investigation

Produce an intuitive reproducer, verify it on upstream tt-metal, and deliver
`report.md` with `reproducer.zip`. Establish the observed failure and its location
without assuming that a suspected device anomaly proves a hardware defect.

## Execution context

Resolve linked guidance from this skill's canonical directory. Read the
[basic TT-Metal guide](../../agent-guidance/tt-metal/README.md) before builds or
device access, [kernel guidance](../../agent-guidance/tt-metal/kernels.md) before
editing kernels, and [Git guidance](../../agent-guidance/version-control.md)
before changing checkouts. For hangs, initialization failures, or reset failures,
use [debugging and recovery](../../agent-guidance/tt-metal/debugging.md).

CPU-only builds do not require a device reservation. Follow the site's device
access protocol for device commands. Preserve the measured firmware, driver,
and power configuration; do not change them as an incidental debugging step.

## Reduce and localize

1. Define the input, expected behavior, comparison criterion, repetition count,
   and failure condition before each experiment. **Corruption** is disagreement
   with the expected result; **nondeterminism (ND)** is different outputs for
   identical inputs and execution conditions. Test both separately. Use bitwise
   comparison when exact preservation is expected; justify any numerical tolerance.
2. Remove model and dataset dependencies. Keep a small TTNN example when it
   expresses the failure clearly; use a gtest when core placement, register slots,
   or data movement require direct control. Make input construction, the operation,
   and the check immediately visible. Retain required initialization,
   synchronization, and barriers; remove optional diagnostics, abstraction, and
   configuration that do not reproduce or detect the failure.
3. Record the actual execution host, PCI BDF, and UMD logical chip ID, checking
   their mapping for the measurement. Do not use `/dev/tenstorrent` numbers as the
   primary identity. Record ASIC identity when available. For relevant units,
   state logical and physical core coordinates, the NoC coordinate system, and
   register/tile slots. Recheck mappings after reset or visibility changes.
4. Use controls that change one relevant condition at a time: core, device,
   register slot, operation, or memory path. Distinguish where corruption was
   observed from where it first arose. A later successful reread does not prove
   an earlier read was correct; removing an operation also changes execution
   timing. Identify a particular unit only when the evidence supports it;
   otherwise state the supported failing path. Passing controls establish only
   the tested conditions, not general absence of a fault.
5. Record completed repetitions, failing executions, mismatching elements or
   words, and changes between successive outputs with their counting units.
   Preserve representative expected/actual values and bit patterns, including
   storage layout and offset interpretation. Treat initialization failures and
   timeouts separately from numerical measurements.

## Verify on upstream

Fetch Tenstorrent's upstream `main` at investigation time and pin its full commit
hash. Preserve existing checkout changes under the Git guidance. Apply only the
reproducer and required integration changes, build, and run on the same identified
target device with comparable inputs and configuration. Record relevant runtime
or submodule revisions and software versions.

Distinguish build success, completed reproduction, completed non-reproduction,
and inability to run. Never label a fork result or a successful build as upstream
reproduction. Report a negative result or an execution blocker as measured.
Do not require publication of a branch to reproduce the experiment.

Freeze the final tested sources and invocation. Rerun after changes to the test
or its execution settings; do not package an untested simplification as the
confirmed reproducer. Keep valid evidence and the final package while removing
superseded probes and per-run scratch under the existing cleanup policy. Restore
the original checkout and build environment after upstream verification.

## Deliver the report and source package

Write `report.md` for an external reader in this order:

1. The upstream result and observed symptom: ND, corruption, or both.
2. Exact host/device/unit identification, the full tested upstream commit hash,
   and relevant software versions and execution conditions.
3. A short explanation of the input, operation, expected result, and minimal test.
4. Measured results and controls, with denominators, counting units, and a
   representative failure signature.
5. How to reproduce using the accompanying package.

Make the report self-contained. Transfer material evidence into it rather than
citing inaccessible local logs or paths; use no local-path hyperlinks. By default,
omit internal issue/Slack history, device reservation tools and job metadata,
work chronology, and cleanup details. Do not require a separate "Scope and
remaining question" section; qualify conclusions where needed in the relevant
sentence. Keep site-specific operating instructions in the README when needed.

Include in `reproducer.zip`:

- The exact tested source files, including any separate device kernels.
- A complete patch against the pinned upstream commit, including the test and
  every required build-system/CMake change.
- `README.md` with prerequisites, file placement, patch application, any additional
  changes, build/run commands, controls, and normal/failure interpretation.
- `report.md` and checksums for the packaged files.

Verify patch applicability against the clean pinned base, equality between the
packaged and tested sources, ZIP integrity, checksums, and consistency of commands
and results. The package must work without an unpublished branch or unlisted local
file. Deliver both artifacts to the user; post to an external service only under
the instructions for that task.

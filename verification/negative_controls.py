"""Negative controls for the two standalone certificate verifiers.

Standard library only. The shipped certificate files are copied to a temporary
directory; each control applies one semantic corruption to a copy and runs the
relevant verifier on it with --data, under both normal and -O execution. A
control passes only if the verifier exits nonzero and reports "CHECK FAILED".
The unmodified copy must be accepted (exit zero, status PASS) in both modes.
The shipped data/ directory is only read, never written.

Usage:
    python negative_controls.py [--data DIR] [--report PATH] [--workdir DIR]
"""
from fractions import Fraction as F
from pathlib import Path
import argparse
import copy
import json
import shutil
import subprocess
import sys
import tempfile
import time

ROOT = Path(__file__).resolve().parents[1]
TREE_FILE = "small_tree_exact_certificates.json"
COVERAGE_FILE = "coverage_equality_checks.json"
VERIFIERS = {
    "tree": ROOT / "verification" / "verify_exact_certificates.py",
    "coverage": ROOT / "verification" / "verify_coverage_certificates.py",
}


def tree_record(records, minimum_cycle=2, need_witness=False):
    """Deterministically choose a tree record suitable for a corruption."""
    for record in records:
        cert = record["exact_optimum_certificate"]
        if len(cert["cycle_state_ids"]) < minimum_cycle:
            continue
        if need_witness and not record["paired_lower_bound_witness"]:
            continue
        return record
    raise SystemExit("CHECK FAILED: no tree record suitable for this control")


def coverage_record(data, minimum_cycle=2):
    for record in data["records"]:
        if len(record["certificate"]["cycle_state_ids"]) >= minimum_cycle:
            return record
    raise SystemExit("CHECK FAILED: no coverage record suitable for this control")


# Tree-certificate corruptions (operate on the list of records).
def t_optimum_raised(records):
    cert = tree_record(records)["exact_optimum_certificate"]
    mu = F(cert["optimum"])
    new = mu + F(1, mu.denominator)
    cert["optimum"] = str(new)
    cert["potential_denominator"] = new.denominator


def t_potential_perturbed(records):
    # State 0 has outgoing arcs, so a large increase of h(0) breaks an inequality.
    tree_record(records)["exact_optimum_certificate"]["potential"][0] += 10**6


def t_cycle_action_altered(records):
    cert = tree_record(records)["exact_optimum_certificate"]
    cert["cycle_actions"][0] ^= 1


def t_cycle_truncated(records):
    cert = tree_record(records, minimum_cycle=3)["exact_optimum_certificate"]
    cert["cycle_state_ids"].pop()
    cert["cycle_actions"].pop()


def t_optimum_lowered_zero_potential(records):
    cert = tree_record(records)["exact_optimum_certificate"]
    mu = F(cert["optimum"])
    new = mu - F(1, 2 * mu.denominator)
    cert["optimum"] = str(new)
    cert["potential_denominator"] = new.denominator
    cert["potential"] = [0] * len(cert["potential"])


def t_pair_penalty_inflated(records):
    entry = tree_record(records, 1, need_witness=True)["paired_lower_bound_witness"][0]
    entry["penalty"] = str(F(entry["penalty"]) * 100)


def t_noninteger_potential(records):
    cert = tree_record(records)["exact_optimum_certificate"]
    cert["potential"][0] = cert["potential"][0] + 0.5


# Coverage-certificate corruptions (operate on the whole JSON document).
def c_optimum_raised(data):
    record = coverage_record(data)
    mu = F(record["exact_optimum"])
    new = mu + F(1, mu.denominator)
    record["exact_optimum"] = record["certificate"]["optimum"] = str(new)
    record["certificate"]["potential_denominator"] = new.denominator


def c_potential_perturbed(data):
    coverage_record(data)["certificate"]["potential"][0] += 10**6


def c_cycle_action_altered(data):
    coverage_record(data)["certificate"]["cycle_actions"][0] ^= 1


def c_prediction_flipped(data):
    record = data["records"][0]
    record["predicted_equality"] = not record["predicted_equality"]


def c_lower_bound_altered(data):
    record = data["records"][0]
    record["lower_bound"] = str(F(record["lower_bound"]) + 1)


def c_summary_count_altered(data):
    data["summary"]["equality_cases"] += 1


CONTROLS = [
    ("T1_tree_optimum_raised", "tree", t_optimum_raised),
    ("T2_tree_potential_entry_perturbed", "tree", t_potential_perturbed),
    ("T3_tree_cycle_action_altered", "tree", t_cycle_action_altered),
    ("T4_tree_cycle_truncated", "tree", t_cycle_truncated),
    ("T5_tree_optimum_lowered_zero_potential", "tree", t_optimum_lowered_zero_potential),
    ("T6_tree_pair_penalty_x100", "tree", t_pair_penalty_inflated),
    ("T7_tree_noninteger_potential", "tree", t_noninteger_potential),
    ("C1_coverage_optimum_raised", "coverage", c_optimum_raised),
    ("C2_coverage_potential_entry_perturbed", "coverage", c_potential_perturbed),
    ("C3_coverage_cycle_action_altered", "coverage", c_cycle_action_altered),
    ("C4_coverage_prediction_flipped", "coverage", c_prediction_flipped),
    ("C5_coverage_lower_bound_altered", "coverage", c_lower_bound_altered),
    ("C6_coverage_summary_count_altered", "coverage", c_summary_count_altered),
]


def run_verifier(kind, data_dir, optimise):
    argv = [sys.executable, "-B", "-I", "-S"] + (["-O"] if optimise else []) + [
        str(VERIFIERS[kind]), "--data", str(data_dir),
        "--report", str(data_dir / f"{kind}_report{'_O' if optimise else ''}.json")]
    start = time.perf_counter()
    result = subprocess.run(argv, capture_output=True, text=True, timeout=300)
    last = result.stderr.strip().splitlines()[-1] if result.stderr.strip() else ""
    return {"argv": argv, "exit_status": result.returncode,
            "elapsed_seconds": round(time.perf_counter() - start, 4),
            "stderr_last_line": last[:300],
            "check_failed_reported": "CHECK FAILED" in result.stderr,
            "status_pass_printed": '"status": "PASS"' in result.stdout}


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--data", type=Path, default=ROOT / "data",
                        help="directory of pristine certificate files (default: shipped data/)")
    parser.add_argument("--report", type=Path, default=None, help="optional JSON report path")
    parser.add_argument("--workdir", type=Path, default=None,
                        help="parent for the scratch copies (default: system temporary directory)")
    args = parser.parse_args(argv)
    pristine_tree = json.loads((args.data / TREE_FILE).read_text())
    pristine_coverage = json.loads((args.data / COVERAGE_FILE).read_text())
    if args.workdir is not None:
        args.workdir.mkdir(parents=True, exist_ok=True)
    results, failures = [], []
    with tempfile.TemporaryDirectory(prefix="negctl_", dir=args.workdir) as scratch:
        scratch = Path(scratch)
        # Unmodified copies must be accepted by both verifiers in both modes.
        case = scratch / "T0_pristine"
        case.mkdir()
        shutil.copy2(args.data / TREE_FILE, case / TREE_FILE)
        shutil.copy2(args.data / COVERAGE_FILE, case / COVERAGE_FILE)
        for kind in ("tree", "coverage"):
            for optimise in (False, True):
                run = run_verifier(kind, case, optimise)
                ok = run["exit_status"] == 0 and run["status_pass_printed"]
                results.append({"control": "T0_pristine", "verifier": kind, "optimised": optimise,
                                "expected": "accept", "ok": ok, **run})
                if not ok:
                    failures.append(f"T0_pristine/{kind}/{'-O' if optimise else 'normal'}")
        for name, kind, corrupt in CONTROLS:
            case = scratch / name
            case.mkdir()
            filename = TREE_FILE if kind == "tree" else COVERAGE_FILE
            pristine = pristine_tree if kind == "tree" else pristine_coverage
            document = copy.deepcopy(pristine)
            corrupt(document)
            if document == pristine:
                raise SystemExit(f"CHECK FAILED: control {name} did not change the certificate")
            (case / filename).write_text(json.dumps(document))
            for optimise in (False, True):
                run = run_verifier(kind, case, optimise)
                ok = run["exit_status"] != 0 and run["check_failed_reported"] \
                    and not run["status_pass_printed"]
                results.append({"control": name, "verifier": kind, "optimised": optimise,
                                "expected": "reject", "ok": ok, **run})
                if not ok:
                    failures.append(f"{name}/{'-O' if optimise else 'normal'}")
    for row in results:
        print(f"{row['control']:42s} {row['verifier']:8s} {'-O' if row['optimised'] else '  '} "
              f"exit={row['exit_status']} expected={row['expected']:6s} "
              f"{'OK' if row['ok'] else 'UNEXPECTED'}  {row['stderr_last_line'][:80]}")
    summary = {"status": "FAIL" if failures else "PASS",
               "controls": len(CONTROLS), "verifier_runs": len(results),
               "rejections_confirmed": sum(r["ok"] and r["expected"] == "reject" for r in results),
               "pristine_acceptances_confirmed": sum(r["ok"] and r["expected"] == "accept" for r in results),
               "failures": failures, "source_data": str(args.data)}
    if args.report is not None:
        args.report.parent.mkdir(parents=True, exist_ok=True)
        args.report.write_text(json.dumps({"summary": summary, "runs": results}, indent=2) + "\n")
    print(json.dumps(summary, indent=2))
    if failures:
        raise SystemExit(f"CHECK FAILED: negative controls not as expected: {failures}")


if __name__ == "__main__":
    main()

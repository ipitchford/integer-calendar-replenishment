"""Run the complete verification once and write one unedited run record.

Order of work:
  1. Both standalone verifiers check the SHIPPED, unmodified certificate files in
     data/, normally and under -O (with -I -S, so only the standard library is
     visible). Their reports go to the replay directory and are compared with
     the shipped reports in data/.
  2. Every generator re-runs with --out pointing to a fresh directory under
     logs/replay/<run id>/regenerated/. Shipped data/ is never overwritten.
     Regenerated optimum VALUES and summary counts are compared with the
     shipped data; dual potentials and attaining cycles are not compared,
     because they are not unique and may legitimately differ by platform.
  3. Both verifiers also check the regenerated certificates.
  4. Negative controls confirm that the verifiers reject corrupted copies of
     the shipped certificates under normal and -O execution.
  5. data/ is hashed before and after; any change is a failure.

The single record logs/verification_run.json is written by this run only.
Usage: python -B verification/run_verification.py
"""
from datetime import datetime, timezone
from fractions import Fraction
from pathlib import Path
import csv
import hashlib
import importlib.metadata
import json
import platform
import subprocess
import sys
import time

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"
LOGS = ROOT / "logs"
PY = [sys.executable, "-B"]
VERIFIERS = [
    ("verify_exact_certificates", "verification/verify_exact_certificates.py",
     "certificate_verification.json"),
    ("verify_coverage_certificates", "verification/verify_coverage_certificates.py",
     "coverage_certificate_verification.json"),
]
GENERATORS = [
    "src/independent_calendar_check.py",
    "verification/structural_audit_checks.py",
    "src/benchmark_small_trees.py",
    "verification/coverage_equality_check.py",
    "verification/short_cycle_budget_check.py",
]
# Writes nothing to data/; it is run for its own internal checks only.
STANDALONE_CHECKS = ["verification/pair_mean_cycle_audit.py"]


def rel(path):
    path = Path(path)
    return path.relative_to(ROOT).as_posix() if path.is_relative_to(ROOT) else str(path)


def hash_tree(directory):
    return {rel(p): hashlib.sha256(p.read_bytes()).hexdigest()
            for p in sorted(directory.rglob("*")) if p.is_file()}


class Runner:
    def __init__(self, logdir):
        self.logdir = logdir
        self.commands = []

    def run(self, label, argv, expect_success=True):
        start = time.perf_counter()
        result = subprocess.run(argv, cwd=ROOT, capture_output=True, text=True, timeout=600)
        elapsed = time.perf_counter() - start
        log = self.logdir / f"{len(self.commands):02d}_{label}.log"
        log.write_text(f"$ {' '.join(argv)}\n\nSTDOUT:\n{result.stdout}\nSTDERR:\n{result.stderr}")
        ok = (result.returncode == 0) == expect_success
        entry = {"label": label, "argv": argv, "cwd": str(ROOT),
                 "exit_status": result.returncode, "ok": ok,
                 "elapsed_seconds": round(elapsed, 4), "log": rel(log)}
        self.commands.append(entry)
        print(json.dumps({k: entry[k] for k in ("label", "exit_status", "ok", "elapsed_seconds")}),
              flush=True)
        return entry


def load(path):
    return json.loads(Path(path).read_text())


def compare_equal(name, shipped, regenerated, problems):
    if shipped != regenerated:
        problems.append(f"{name}: regenerated content differs from shipped")
        return False
    return True


def compare_outputs(regen):
    """Compare regenerated outputs with shipped data. Returns (details, problems)."""
    problems, details = [], {}

    def guarded(name, function):
        try:
            details[name] = function()
        except (OSError, KeyError, TypeError, ValueError) as error:
            problems.append(f"{name}: comparison could not be made ({type(error).__name__}: {error})")

    def benchmark_summary():
        shipped, new = load(DATA / "small_tree_benchmark.json"), load(regen / "small_tree_benchmark.json")
        shipped.pop("elapsed_seconds", None)
        new.pop("elapsed_seconds", None)
        compare_equal("small_tree_benchmark.json (all fields except elapsed_seconds)", shipped, new, problems)
        return {"fields_compared": len(shipped), "equal": shipped == new}
    guarded("small_tree_benchmark.json", benchmark_summary)

    def benchmark_csv():
        with (DATA / "small_tree_benchmark.csv").open(newline="") as f:
            shipped = list(csv.DictReader(f))
        with (regen / "small_tree_benchmark.csv").open(newline="") as f:
            new = list(csv.DictReader(f))
        compare_equal("small_tree_benchmark.csv (all exact values and ratios)", shipped, new, problems)
        return {"rows_compared": len(shipped), "equal": shipped == new}
    guarded("small_tree_benchmark.csv", benchmark_csv)

    def tree_certificates():
        shipped = load(DATA / "small_tree_exact_certificates.json")
        new = load(regen / "small_tree_exact_certificates.json")
        if len(shipped) != len(new):
            problems.append("small_tree_exact_certificates.json: record count differs")
        mismatched, potentials_differ, cycles_differ = [], 0, 0
        for a, b in zip(shipped, new):
            ca, cb = a["exact_optimum_certificate"], b["exact_optimum_certificate"]
            key = lambda r, c: (r["id"], r["parents"], r["lengths"], r["turnovers"],
                                Fraction(c["optimum"]), c["states"], c["arcs"], c["potential_denominator"])
            if key(a, ca) != key(b, cb):
                mismatched.append(a["id"])
            potentials_differ += ca["potential"] != cb["potential"]
            cycles_differ += (ca["cycle_state_ids"], ca["cycle_actions"]) != (cb["cycle_state_ids"], cb["cycle_actions"])
        if mismatched:
            problems.append(f"small_tree_exact_certificates.json: optimum/instance mismatch in {mismatched}")
        return {"records_compared": len(shipped), "optimum_value_mismatches": mismatched,
                "records_with_different_potentials (informational)": potentials_differ,
                "records_with_different_attaining_cycles (informational)": cycles_differ}
    guarded("small_tree_exact_certificates.json", tree_certificates)

    def coverage():
        shipped, new = load(DATA / "coverage_equality_checks.json"), load(regen / "coverage_equality_checks.json")
        compare_equal("coverage_equality_checks.json summary", shipped["summary"], new["summary"], problems)
        mismatched, potentials_differ = [], 0
        if len(shipped["records"]) != len(new["records"]):
            problems.append("coverage_equality_checks.json: record count differs")
        for a, b in zip(shipped["records"], new["records"]):
            strip = lambda r: {k: v for k, v in r.items() if k != "certificate"}
            ca, cb = a["certificate"], b["certificate"]
            ka = (strip(a), Fraction(ca["optimum"]), ca["states"], ca["arcs"], ca["potential_denominator"])
            kb = (strip(b), Fraction(cb["optimum"]), cb["states"], cb["arcs"], cb["potential_denominator"])
            if ka != kb:
                mismatched.append(a["id"])
            potentials_differ += ca["potential"] != cb["potential"]
        if mismatched:
            problems.append(f"coverage_equality_checks.json: optimum/criterion mismatch in {mismatched}")
        return {"records_compared": len(shipped["records"]), "summary_equal": shipped["summary"] == new["summary"],
                "optimum_or_criterion_mismatches": mismatched,
                "records_with_different_potentials (informational)": potentials_differ}
    guarded("coverage_equality_checks.json", coverage)

    for name in ["independent_checks.json", "structural_audit_checks.json", "short_cycle_budget_checks.json"]:
        def whole(name=name):
            equal = compare_equal(name, load(DATA / name), load(regen / name), problems)
            return {"compared": "entire document", "equal": equal}
        guarded(name, whole)

    def budget_csv():
        equal = (DATA / "period_budget_limit.csv").read_bytes() == (regen / "period_budget_limit.csv").read_bytes()
        if not equal:
            problems.append("period_budget_limit.csv: regenerated bytes differ from shipped")
        return {"compared": "bytes", "equal": equal}
    guarded("period_budget_limit.csv", budget_csv)
    return details, problems


def main():
    started_utc = datetime.now(timezone.utc)
    run_id = started_utc.strftime("%Y%m%dT%H%M%SZ")
    replay = LOGS / "replay" / run_id
    if replay.exists():
        raise SystemExit(f"{replay} already exists; refusing to reuse a replay directory")
    shipped_reports = replay / "shipped_verifier_reports"
    regen = replay / "regenerated"
    regen_reports = replay / "regenerated_verifier_reports"
    logdir = replay / "logs"
    for directory in (shipped_reports, regen, regen_reports, logdir):
        directory.mkdir(parents=True)
    data_before = hash_tree(DATA)
    runner = Runner(logdir)
    problems = []

    # 1. Shipped certificates, before anything else runs.
    for label, script, report_name in VERIFIERS:
        for optimised in (False, True):
            suffix = "_O" if optimised else ""
            report = shipped_reports / report_name.replace(".json", f"{suffix}.json")
            argv = PY + ["-I", "-S"] + (["-O"] if optimised else []) + [
                str(ROOT / script), "--data", str(DATA), "--report", str(report)]
            entry = runner.run(f"shipped_{label}{suffix}", argv)
            if not entry["ok"]:
                problems.append(f"{entry['label']}: verifier rejected shipped certificates")
            elif report.read_bytes() != (DATA / report_name).read_bytes():
                problems.append(f"{entry['label']}: report differs from shipped data/{report_name}")

    # 1b. Release certificates: constant-gap chain bounds and broom optima.
    for optimised in (False, True):
        suffix = "_O" if optimised else ""
        flags = ["-I", "-S"] + (["-O"] if optimised else [])
        entry = runner.run(f"shipped_verify_constant_gap_chains{suffix}", PY + flags + [
            str(ROOT / "verification/verify_constant_gap_chains.py"), "--data", str(DATA),
            "--report", str(shipped_reports / f"constant_gap_chain_verification{suffix}.json")])
        if not entry["ok"]:
            problems.append(f"{entry['label']}: chain certificates rejected")
        entry = runner.run(f"shipped_verify_broom_certificates{suffix}", PY + flags + [
            str(ROOT / "verification/verify_exact_certificates.py"),
            "--certificates", str(DATA / "broom_exact_certificates.json"),
            "--report", str(shipped_reports / f"broom_certificate_verification{suffix}.json")])
        if not entry["ok"]:
            problems.append(f"{entry['label']}: broom certificates rejected")

    # 2. Regenerate everything into the replay directory.
    for script in GENERATORS:
        entry = runner.run(f"generate_{Path(script).stem}",
                           PY + ["-I", str(ROOT / script), "--out", str(regen)])
        if not entry["ok"]:
            problems.append(f"{entry['label']}: generator failed")
    for script in STANDALONE_CHECKS:
        entry = runner.run(f"check_{Path(script).stem}", PY + ["-I", str(ROOT / script)])
        if not entry["ok"]:
            problems.append(f"{entry['label']}: check failed")
    entry = runner.run("generate_constant_gap_chains",
                       PY + ["-I", str(ROOT / "src/constant_gap_chains.py"), "--out", str(regen)])
    if not entry["ok"]:
        problems.append("generate_constant_gap_chains: generator failed")
    else:
        rep = regen_reports / "constant_gap_chain_verification.json"
        entry = runner.run("regenerated_verify_constant_gap_chains", PY + ["-I", "-S",
                           str(ROOT / "verification/verify_constant_gap_chains.py"), "--data", str(regen),
                           "--report", str(rep)])
        if not entry["ok"]:
            problems.append("regenerated chain certificates rejected")
        else:
            r = load(rep)
            if not (Fraction(r["certified_lower_bound"]) >= Fraction(160010, 100000)
                    and Fraction(r["certified_upper_bound"]) <= Fraction(160139, 100000)):
                problems.append("regenerated chain bounds fall outside the bracket stated in the manuscript")
    entry = runner.run("generate_broom_exact", PY + ["-I", str(ROOT / "src/broom_exact.py"),
                                                     "--out", str(regen), "2", "3", "4"])
    if not entry["ok"]:
        problems.append("generate_broom_exact: generator failed")
    else:
        shipped_b = [(r["id"], r["exact_optimum_certificate"]["optimum"]) for r in load(DATA / "broom_exact_certificates.json")]
        new_b = [(r["id"], r["exact_optimum_certificate"]["optimum"]) for r in load(regen / "broom_exact_certificates.json")]
        # M=5 takes about half an hour to regenerate, so the replay recomputes M=2,3,4; M=5 is verified above.
        if shipped_b[:len(new_b)] != new_b:
            problems.append(f"broom optima differ: {shipped_b} vs {new_b}")
    comparison, comparison_problems = compare_outputs(regen)
    problems += comparison_problems

    # 3. Verify the regenerated certificates too.
    stable = ["status", "exact_optima", "integer_transition_inequalities",
              "individual_cyclic_gap_checks", "equality_cases", "strict_gap_cases"]
    for label, script, report_name in VERIFIERS:
        report = regen_reports / report_name
        entry = runner.run(f"regenerated_{label}", PY + ["-I", "-S", str(ROOT / script),
                                                         "--data", str(regen), "--report", str(report)])
        if not entry["ok"]:
            problems.append(f"{entry['label']}: verifier rejected regenerated certificates")
            continue
        shipped, new = load(DATA / report_name), load(report)
        diff = {k: (shipped.get(k), new.get(k)) for k in stable if shipped.get(k) != new.get(k)}
        if diff:
            problems.append(f"{entry['label']}: count mismatch {diff}")
        comparison[f"regenerated {report_name}"] = {
            "stable_counts_equal": not diff,
            "informational_differences": {k: (shipped[k], new[k]) for k in shipped
                                          if k not in stable and k != "source" and shipped[k] != new.get(k)}}

    # 4. Negative controls on corrupted copies of the shipped certificates.
    negctl_report = replay / "negative_controls.json"
    entry = runner.run("negative_controls", PY + ["-I", str(ROOT / "verification/negative_controls.py"),
                                                  "--data", str(DATA), "--report", str(negctl_report)])
    negative = None
    if not entry["ok"]:
        problems.append("negative_controls: a verifier accepted a corrupted certificate or rejected a pristine one")
    else:
        negative = load(negctl_report)["summary"]

    # 5. Shipped data must be byte-for-byte unchanged.
    data_after = hash_tree(DATA)
    if data_after != data_before:
        changed = sorted(k for k in set(data_before) | set(data_after) if data_before.get(k) != data_after.get(k))
        problems.append(f"data/ changed during verification: {changed}")

    versions = {}
    for package in ["numpy", "scipy", "matplotlib"]:
        try:
            versions[package] = importlib.metadata.version(package)
        except importlib.metadata.PackageNotFoundError:
            versions[package] = None
    record = {
        "status": "FAIL" if problems else "PASS",
        "problems": problems,
        "run_id": run_id,
        "started_utc": started_utc.isoformat(),
        "finished_utc": datetime.now(timezone.utc).isoformat(),
        "python": platform.python_version(),
        "python_implementation": platform.python_implementation(),
        "python_executable": sys.executable,
        "platform": platform.platform(),
        "packages": versions,
        "driver_argv": [sys.executable] + sys.argv,
        "working_directory": str(ROOT),
        "replay_directory": rel(replay),
        "shipped_data_sha256": data_before,
        "shipped_data_unchanged": data_after == data_before,
        "commands": runner.commands,
        "regenerated_vs_shipped": comparison,
        "negative_controls": negative,
        "scope": ("The listed finite checks and certificates only; no formal proof or priority "
                  "certificate. Dual potentials and attaining cycles are not unique and are not "
                  "required to match the shipped files; optimum values and summary counts are."),
    }
    (LOGS / "verification_run.json").write_text(json.dumps(record, indent=2) + "\n")
    print(json.dumps({"status": record["status"], "problems": problems,
                      "record": rel(LOGS / "verification_run.json")}, indent=2))
    if problems:
        raise SystemExit(1)


if __name__ == "__main__":
    main()

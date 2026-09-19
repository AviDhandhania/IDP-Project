"""
Crypto-Agility Copilot - CLI Entry Point
Executes cryptographic discovery, dataflow binding, HNDL exposure scoring, and CycloneDX 1.6 CBOM export.
"""

import sys
import argparse
from pathlib import Path
from typing import List, Tuple
from .discovery import DiscoveryEngine
from .dataflow import DataflowBindingEngine
from .scorer import HNDLScoringEngine
from .cbom import CBOMGenerator
from .models import DataPath, HNDLScore


def run_pipeline(
    target_path: str,
    output_cbom_path: str = None,
    show_suppressed: bool = False
) -> List[Tuple[DataPath, HNDLScore]]:
    """Runs the complete 4-stage pipeline over the target path."""
    discovery_engine = DiscoveryEngine()
    binding_engine = DataflowBindingEngine()
    scoring_engine = HNDLScoringEngine()
    cbom_generator = CBOMGenerator()

    target = Path(target_path)
    if target.is_file():
        invocations = discovery_engine.scan_file(str(target))
    elif target.is_dir():
        invocations = discovery_engine.scan_directory(str(target))
    else:
        print(f"Error: Target path {target_path} does not exist.")
        sys.exit(1)

    print(f"🔍 Discovered {len(invocations)} cryptographic invocation(s).")

    # Stage 2: Bind dataflow
    data_paths: List[DataPath] = []
    for inv in invocations:
        dp = binding_engine.bind_invocation(inv)
        data_paths.append(dp)

    # Stage 3: Score and rank
    ranked = scoring_engine.rank_paths(data_paths)

    # Output Table
    print("\n" + "=" * 115)
    print(f"{'RANK':<5} | {'ALGORITHM':<12} | {'LOCATION':<28} | {'RETENTION':<14} | {'EXPOSURE':<18} | {'SCORE':<7} | {'URGENCY'}")
    print("=" * 115)

    rank_num = 1
    for path, score in ranked:
        if not show_suppressed and score.urgency_tier == "SUPPRESSED":
            continue

        loc_str = f"{Path(path.invocation.file_path).name}:{path.invocation.line_number}"
        ret_str = f"{path.retention.retention_years:.1f}y" if path.retention.retention_years >= 1.0 else f"{path.retention.retention_years*365:.0f}d"
        if path.retention.retention_years < 0.01:
            ret_str = "<1 hour"

        exp_str = path.exposure.name
        score_str = f"{score.normalized_score:.1f}"
        urgency_display = f"{score.urgency_tier}"
        if score.mosca_violated:
            urgency_display += " (MOSCA BREACH)"

        print(f"{rank_num:<5} | {path.invocation.algorithm_name:<12} | {loc_str:<28} | {ret_str:<14} | {exp_str:<18} | {score_str:<7} | {urgency_display}")
        rank_num += 1

    print("=" * 115)

    # Print summary metrics
    total_findings = len(ranked)
    suppressed_count = sum(1 for _, s in ranked if s.urgency_tier == "SUPPRESSED")
    actionable_count = total_findings - suppressed_count
    mosca_breaches = sum(1 for _, s in ranked if s.mosca_violated)

    print(f"\n📊 Summary Metrics:")
    print(f"  • Total Call Sites Discovered: {total_findings}")
    print(f"  • Actionable Candidates:       {actionable_count}")
    print(f"  • Context-Suppressed Findings: {suppressed_count} (Noise Filtered: {suppressed_count/total_findings*100:.1f}%)" if total_findings else "  • Context-Suppressed Findings: 0")
    print(f"  • Mosca's Inequality Breaches: {mosca_breaches} (Immediate PQC remediation needed)")

    # Stage 4: Export CycloneDX 1.6 CBOM
    if output_cbom_path:
        cbom_doc = cbom_generator.generate_cbom(ranked, target_component_name=target.name)
        cbom_generator.export_json(cbom_doc, output_cbom_path)
        print(f"\n📦 Successfully exported enriched CycloneDX 1.6 CBOM to: {output_cbom_path}")

    return ranked


def main():
    parser = argparse.ArgumentParser(
        description="Crypto-Agility Copilot: Dataflow-Aware Cryptographic Inventory and Prioritization"
    )
    parser.add_argument("target", help="Path to Python file or directory to scan")
    parser.add_argument("--output-cbom", "-o", help="Path to write CycloneDX 1.6 CBOM JSON", default=None)
    parser.add_argument("--show-suppressed", action="store_true", help="Include suppressed non-security findings in table")
    args = parser.parse_args()

    run_pipeline(args.target, args.output_cbom, args.show_suppressed)


if __name__ == "__main__":
    main()

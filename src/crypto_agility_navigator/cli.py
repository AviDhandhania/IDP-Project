"""
Crypto-Agility Navigator - CLI Entry Point
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

    # ANSI Color Codes for Pro UI
    RESET = "[0m"
    BOLD = "[1m"
    RED = "[91m"
    YELLOW = "[93m"
    CYAN = "[96m"
    GREEN = "[92m"
    GRAY = "[90m"
    BLUE = "[94m"

    print(f"\\n{BOLD}{BLUE}[*] Discovered {len(invocations)} cryptographic invocation(s).{RESET}\\n")

    # Stage 2: Bind dataflow
    data_paths: List[DataPath] = []
    for inv in invocations:
        dp = binding_engine.bind_invocation(inv)
        data_paths.append(dp)

    # Stage 3: Score and rank
    ranked = scoring_engine.rank_paths(data_paths)

    # Output Table
    print(f"{BOLD}{'=' * 125}{RESET}")
    print(f"{BOLD}{'RANK':<5} | {'ALGORITHM':<16} | {'LOCATION':<30} | {'RETENTION':<14} | {'EXPOSURE':<18} | {'SCORE':<7} | {'URGENCY'}{RESET}")
    print(f"{BOLD}{'=' * 125}{RESET}")

    rank_num = 1
    for path, score in ranked:
        if not show_suppressed and score.urgency_tier == "SUPPRESSED":
            continue

        loc_str = f"{Path(path.invocation.file_path).name}:{path.invocation.line_number}"
        if len(loc_str) > 28:
            loc_str = "..." + loc_str[-25:]
            
        ret_str = f"{path.retention.retention_years:.1f}y" if path.retention.retention_years >= 1.0 else f"{path.retention.retention_years*365:.0f}d"
        if path.retention.retention_years < 0.01:
            ret_str = "<1 hour"

        exp_str = path.exposure.name
        score_str = f"{score.normalized_score:.1f}"
        
        # Color Coding
        urgency_display = score.urgency_tier
        row_color = RESET
        if "CRITICAL" in urgency_display:
            row_color = RED + BOLD
        elif "HIGH" in urgency_display:
            row_color = YELLOW
        elif "MEDIUM" in urgency_display:
            row_color = CYAN
        elif "LOW" in urgency_display:
            row_color = GREEN
        elif "SUPPRESSED" in urgency_display:
            row_color = GRAY
            
        if score.mosca_violated:
            urgency_display += " (MOSCA BREACH)"

        print(f"{row_color}{rank_num:<5} | {path.invocation.algorithm_name:<16} | {loc_str:<30} | {ret_str:<14} | {exp_str:<18} | {score_str:<7} | {urgency_display}{RESET}")
        rank_num += 1

    print(f"{BOLD}{'=' * 125}{RESET}")

    # Print summary metrics
    total_findings = len(ranked)
    suppressed_count = sum(1 for _, s in ranked if s.urgency_tier == "SUPPRESSED")
    actionable_count = total_findings - suppressed_count
    mosca_breaches = sum(1 for _, s in ranked if s.mosca_violated)

    print(f"\\n{BOLD}[+] Summary Metrics:{RESET}")
    print(f"  * Total Call Sites Discovered: {CYAN}{total_findings}{RESET}")
    print(f"  * Actionable Candidates:       {GREEN}{actionable_count}{RESET}")
    print(f"  * Context-Suppressed Findings: {GRAY}{suppressed_count} (Noise Filtered: {suppressed_count/total_findings*100:.1f}%){RESET}" if total_findings else "  * Context-Suppressed Findings: 0")
    
    breach_color = RED + BOLD if mosca_breaches > 0 else GREEN
    print(f"  * Mosca's Inequality Breaches: {breach_color}{mosca_breaches} (Immediate PQC remediation needed){RESET}")

    # Stage 4: Export CycloneDX 1.6 CBOM
    if output_cbom_path:
        cbom_doc = cbom_generator.generate_cbom(ranked, target_component_name=target.name)
        cbom_generator.export_json(cbom_doc, output_cbom_path)
        print(f"\\n{BOLD}{GREEN}[+] Successfully exported enriched CycloneDX 1.6 CBOM to: {output_cbom_path}{RESET}")


    return ranked


def main():
    parser = argparse.ArgumentParser(
        description="Crypto-Agility Navigator: Dataflow-Aware Cryptographic Inventory and Prioritization"
    )
    parser.add_argument("target", nargs="?", default="examples/sample_project", help="Path to Python file or directory to scan")
    parser.add_argument("--output-cbom", "-o", help="Path to write CycloneDX 1.6 CBOM JSON", default=None)
    parser.add_argument("--show-suppressed", action="store_true", help="Include suppressed non-security findings in table")
    parser.add_argument("--serve", action="store_true", help="Launch the interactive Web Dashboard and API server")
    parser.add_argument("--port", type=int, default=8000, help="Port to bind the web server to (default: 8000)")
    args = parser.parse_args()

    if args.serve:
        from .server import run_server
        run_server(port=args.port)
    else:
        run_pipeline(args.target, args.output_cbom, args.show_suppressed)


if __name__ == "__main__":
    main()


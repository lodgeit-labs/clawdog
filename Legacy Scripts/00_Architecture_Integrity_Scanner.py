import os
import glob
import hashlib
import yaml # Ensure pyyaml is installed
from colorama import Fore, Style, init # For scannable reporting

init(autoreset=True)

TARGET_DIRS = ["./01_Ontology", "./02_Rules", "./03_Registry"]

def check_integrity(filepath):
    """Reports on structural and semantic alignment without making changes."""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    report = []
    is_valid = True

    # 1. YAML & Hash Validation
    try:
        parts = content.split('---')
        if len(parts) < 3:
            return False, ["MISSING_FRONTMATTER"]
        
        header = yaml.safe_load(parts[1])
        body = '---'.join(parts[2:]).strip()
        
        # Verify Content Hash
        current_hash = header.get('integrity', {}).get('content_hash')
        actual_hash = hashlib.sha256(body.encode('utf-8')).hexdigest()
        
        if current_hash != actual_hash:
            report.append(f"{Fore.RED}HASH_MISMATCH{Style.RESET_ALL} (Stored: {current_hash[:8]}... vs Actual: {actual_hash[:8]}...)")
            is_valid = False

        # 2. Polymorphic Alignment (Gist/SBRM)
        if not header.get('gist_equivalent'):
            report.append(f"{Fore.YELLOW}MISSING_GIST_MAPPING{Style.RESET_ALL}")
            is_valid = False
            
        if "parameters_exposed" in header:
            for var, specs in (header['parameters_exposed'] or {}).items():
                if 'sbrm_label' not in specs:
                    report.append(f"{Fore.YELLOW}VAR_LABEL_MISSING: {var}{Style.RESET_ALL}")
                    is_valid = False

    except Exception as e:
        report.append(f"{Fore.RED}PARSE_ERROR: {str(e)}{Style.RESET_ALL}")
        is_valid = False

    return is_valid, report

def run_integrity_crawl():
    print(f"\n{Fore.CYAN}=== LODGEIT GLOBAL INTEGRITY SCAN: START ==={Style.RESET_ALL}\n")
    
    counts = {"Total": 0, "Pass": 0, "Fail": 0}

    for directory in TARGET_DIRS:
        print(f"Scanning {directory}...")
        for filepath in glob.glob(f"{directory}/**/*.md", recursive=True):
            counts["Total"] += 1
            valid, issues = check_integrity(filepath)
            
            if valid:
                counts["Pass"] += 1
            else:
                counts["Fail"] += 1
                print(f"  [!] {filepath}")
                for issue in issues:
                    print(f"      - {issue}")

    print(f"\n{Fore.CYAN}=== SCAN SUMMARY ==={Style.RESET_ALL}")
    print(f"Nodes Inspected: {counts['Total']}")
    print(f"Integral Nodes:  {Fore.GREEN}{counts['Pass']}{Style.RESET_ALL}")
    print(f"Imperfect Nodes: {Fore.RED}{counts['Fail']}{Style.RESET_ALL}")

if __name__ == "__main__":
    run_integrity_crawl()
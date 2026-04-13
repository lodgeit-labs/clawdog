import yaml
import pathlib
import hashlib
import sys

class NeuroSemanticValidator:
    def __init__(self, directory_path):
        self.path = pathlib.Path(directory_path)
        self.operative_classes = ["CalculationRule", "OperativeProvision", "SystemDirective"]

    def validate_node(self, file_path):
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        # 1. GRACEFUL IGNORE: Skip files without YAML frontmatter (like README.md)
        if not content.startswith('---'):
            return True, "Ignored: Standard Markdown file (Not an SBRM node)"

        parts = content.split('---', 2)
        if len(parts) < 3:
            return False, "Malformed YAML frontmatter."

        try:
            data = yaml.safe_load(parts[1])
        except yaml.YAMLError as e:
            return False, f"YAML parsing error: {e}"

        # Ignore files meant for human reading (Journals, Architecture Docs)
        local_class = data.get('ontological_class')
        if not local_class or local_class == "Documentation" or local_class == "Journal":
            return True, "Ignored: Human Documentation."

        body = parts[2].strip()
        
        # 2. Base Epistemic Verification
        if not data.get('gist_equivalent'):
            return False, "Missing mandatory 'gist_equivalent'."

        # 3. Polymorphic Nullification & Dictionary Mapping
        is_operative = local_class in self.operative_classes
        params = data.get('parameters_exposed')

        if is_operative:
            if not params:
                return False, "Operative node missing 'parameters_exposed'."
            if not isinstance(params, dict):
                return False, "parameters_exposed must be a Dictionary mapping, not a list."
        else:
            # FIX: Accept None, empty lists [], or empty dicts {} as valid for Epistemic nodes
            if params: 
                return False, "Epistemic node must not expose parameters (must be null or empty)."

        # 4. Hypercube Context Verification 
        hypercube = data.get('hypercube_context')
        if hypercube:
            if 'primary_hypercube' not in hypercube or 'arrangement_pattern' not in hypercube:
                return False, "hypercube_context must define 'primary_hypercube' and 'arrangement_pattern'."

        # 5. Explicit Edges Verification
        edges = data.get('edges')
        if edges:
            if not isinstance(edges, list):
                return False, "Edges must be a list of relational mappings."
            for edge in edges:
                if 'rel' not in edge or 'target' not in edge:
                    return False, "Each edge must define both 'rel' and 'target'."

        # 6. Cryptographic Agentic Healing Verification
        integrity = data.get('integrity')
        if not integrity or 'content_hash' not in integrity:
            return False, "Missing 'integrity' block or 'content_hash'."
        
        # FIX: Normalize Windows line endings to Unix line endings before hashing
        normalized_body = body.replace('\r\n', '\n')
        actual_hash = hashlib.sha256(normalized_body.encode('utf-8')).hexdigest()
        
        if integrity['content_hash'] != actual_hash and integrity['content_hash'] != "[SHA-256 injected at commit]":
             return False, f"Truth Decay Detected: content_hash mismatch. Expected {integrity['content_hash']}, got {actual_hash}."

        return True, "Integral and Aligned"

    def run_audit(self):
        print(f"Initiating NeuroSemantic Integrity Audit: {self.path}")
        print("-" * 60)
        failed_nodes = 0
        passed_nodes = 0
        ignored_nodes = 0

        for md_file in self.path.glob("**/*.md"):
            is_valid, msg = self.validate_node(md_file)
            if is_valid:
                if "Ignored" in msg:
                    ignored_nodes += 1
                else:
                    passed_nodes += 1
            else:
                failed_nodes += 1
                print(f"[QUARANTINE] {md_file.name}: {msg}")

        print("-" * 60)
        print(f"Audit Complete. Passed: {passed_nodes} | Ignored (Docs): {ignored_nodes} | Quarantined: {failed_nodes}")
        
        if failed_nodes > 0:
            sys.exit(1)

if __name__ == "__main__":
    TARGET_DIR = "." 
    auditor = NeuroSemanticValidator(TARGET_DIR)
    auditor.run_audit()
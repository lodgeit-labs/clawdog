import os
import hashlib
import re

# Architect Directive: Enforce cryptographic signatures across ALL ontological layers
TARGET_DIRS = ['./00_Architecture', './01_Ontology', './02_Rules', './03_Registry']

def sync_node(filepath):
    """Calculates the SHA-256 hash of the Markdown body and injects it into the YAML."""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Isolate JSON-LD Frontmatter from Markdown Body
    parts = content.split('---', 2)
    if len(parts) < 3:
        return # Skip non-conforming files (e.g., README.md without YAML)
    
    frontmatter = parts[1]
    body = parts[2]
    
    # Generate deterministic hash from the raw body text
    body_hash = hashlib.sha256(body.encode('utf-8')).hexdigest()

    # Regex target the content_hash parameter to avoid breaking PyYAML ordering
    updated_frontmatter = re.sub(
        r'content_hash:\s*".*"', 
        f'content_hash: "{body_hash}"', 
        frontmatter
    )
    
    # Reassemble and Write
    new_content = f"---{updated_frontmatter}---{body}"
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(new_content)
        
    print(f"Synced: {filepath}")

if __name__ == "__main__":
    print("[SYSTEM] Initiating Global Vault Cryptographic Sync...")
    for directory in TARGET_DIRS:
        if os.path.exists(directory):
            for root, _, files in os.walk(directory):
                for file in files:
                    if file.endswith('.md'):
                        sync_node(os.path.join(root, file))
    print("[SUCCESS] Vault Integrity Locked.")
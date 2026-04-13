import os
import glob
import hashlib
import time
import google.generativeai as genai

# Configure the Gemini API client
genai.configure(api_key=os.environ.get("GEMINI_API_KEY"))

# We use the standard text model
model = genai.GenerativeModel('gemini-1.5-pro')

# The directories containing your Fact Nodes and Rules
TARGET_DIRS = [
    "./01_Ontology",
    "./02_Rules"
]

# The strict system prompt forcing the AI to fix your specific inconsistencies
SYSTEM_INSTRUCTION = """
You are an Ontological Extraction and Serialization Agent for a Global Notes architecture.
I am providing you with a raw Markdown file representing a node in an SBRM multidimensional hypercube. 
Your task is to repair and standardize the YAML frontmatter according to these strict rules, returning the ENTIRE corrected file (YAML + Body):

1. **Polymorphic Nullification**: If the node is purely epistemic (e.g., 'StatutoryDefinition'), the keys 'payload_format', 'execution_context', and 'shacl_shape_ref' inside 'execution_parameters' MUST be explicitly set to 'null'. The same applies to 'parameters_exposed'.
2. **Gist Enforcement**: Ensure 'gist_equivalent' is present and correctly maps to the Gist Upper Ontology (e.g., 'gist:Directive', 'gist:Category', 'gist:Event').
3. **SBRM Labeling**: Inside 'parameters_exposed', every variable MUST have an 'sbrm_label' key. If it does not map to a standard taxonomy, set 'sbrm_label: null'.
4. **Hash Placeholder**: Leave the 'content_hash' value exactly as "[INJECT_HASH_HERE]". 

Do NOT alter the logical payloads, Prolog code, or explicitly declared edges. Output ONLY the raw Markdown file text. Do not wrap the output in ```markdown backticks.
"""

def calculate_body_hash(markdown_content):
    """Calculates the SHA-256 hash of the Markdown body (everything after the YAML)."""
    parts = markdown_content.split('---')
    if len(parts) >= 3:
        body = '---'.join(parts[2:]).strip()
        return hashlib.sha256(body.encode('utf-8')).hexdigest()
    return None

def heal_markdown_file(filepath):
    print(f"Inspecting: {filepath}...")
    
    with open(filepath, 'r', encoding='utf-8') as f:
        original_content = f.read()

    prompt = f"{SYSTEM_INSTRUCTION}\n\nHere is the file to repair:\n\n{original_content}"

    try:
        response = model.generate_content(prompt)
        healed_content = response.text.strip()
        
        if healed_content.startswith("```markdown"):
            healed_content = healed_content[11:]
        if healed_content.endswith("```"):
            healed_content = healed_content[:-3]
            
        healed_content = healed_content.strip()
        new_hash = calculate_body_hash(healed_content)
        
        if not new_hash:
            print(f"  [X] Failed to parse body for hashing on {filepath}. Skipping.")
            return False

        final_content = healed_content.replace("[INJECT_HASH_HERE]", new_hash)

        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(final_content)
            
        print(f"  [v] Successfully repaired and hashed.")
        return True

    except Exception as e:
        print(f"  [X] API or Processing Error on {filepath}: {e}")
        return False

def run_vault_crawler():
    print("Initiating Semantic Vault Repair Sequence...")
    print("-" * 50)
    
    success_count = 0
    fail_count = 0

    for directory in TARGET_DIRS:
        if not os.path.exists(directory):
            print(f"Directory not found: {directory}. Please run from the vault root.")
            continue
            
        for filepath in glob.glob(f"{directory}/**/*.md", recursive=True):
            if heal_markdown_file(filepath):
                success_count += 1
            else:
                fail_count += 1
            
            time.sleep(2)

    print("-" * 50)
    print(f"Repair Complete. Healed: {success_count} | Failed: {fail_count}")

if __name__ == "__main__":
    run_vault_crawler()
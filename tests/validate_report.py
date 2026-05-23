import os
import re
import sys

def main():
    documents = [
        "docs/Rapport_de_Stage_Milan_Loi.md",
        "docs/RGU_Research_Paper_Polarization.md"
    ]
    
    # Standard emoji regex pattern covering common emoji blocks using correct 8-digit \U sequences
    emoji_pattern = re.compile(
        r'[\U0001F300-\U0001F9FF]'  # Pictographs & Supplemental
        r'|[\U0001F600-\U0001F64F]' # Emoticons
        r'|[\U0001F680-\U0001F6FF]' # Transport & Map Symbols
        r'|[\u2600-\u26FF]'         # Miscellaneous Symbols
        r'|[\u2700-\u27BF]'         # Dingbats
    )

    for doc_path in documents:
        if not os.path.exists(doc_path):
            print(f"Error: Document file not found at {doc_path}")
            sys.exit(1)
            
        with open(doc_path, "r", encoding="utf-8") as f:
            content = f.read()
            
        print(f"--- Validating: {doc_path} ---")
        
        # 1. Check for Emojis
        emojis_found = emoji_pattern.findall(content)
        if emojis_found:
            print(f"FAILED: Found {len(emojis_found)} emojis or pictograms in {doc_path}:")
            print(emojis_found)
            sys.exit(1)
        else:
            print("PASS: Absolutely zero emojis detected.")
            
        # 2. Check for typical placeholders like [TODO], [Placeholder], etc.
        placeholders = re.findall(r'\[TODO.*?\]|\[PLACEHOLDER.*?\]', content, re.IGNORECASE)
        if placeholders:
            print(f"FAILED: Found unfinished placeholders in {doc_path}: {placeholders}")
            sys.exit(1)
        else:
            print("PASS: No unfinished placeholders found.")
            
    print("\nAll validations completed successfully! Both documents are compliant.")

if __name__ == "__main__":
    main()


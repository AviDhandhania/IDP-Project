import re

def fix_markdown(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Replace known emojis and bad characters
    replacements = {
        '✔️': '[+]',
        '❌': '[-]',
        '🚀': '[*]',
        '✅': '[+]',
        '🔒': '[SEC]',
        '🛡️': '[SEC]',
        '⚠️': '[!]',
        '⚙️': '[SYS]',
        '📈': '[UP]',
        '📊': '[DATA]'
    }
    
    for k, v in replacements.items():
        content = content.replace(k, v)
        
    # Replace any remaining high-plane unicode just in case
    content = "".join([c if ord(c) < 128 else "" for c in content])
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
        
    print(f"Fixed {filepath}")

if __name__ == "__main__":
    fix_markdown("Report-2-Crypto-Agility-Navigator.md")
    fix_markdown("Review2-2Person-WBS.md")

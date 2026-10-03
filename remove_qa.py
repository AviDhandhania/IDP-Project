import re

with open("scripts/generate_review2_pptx.js", "r") as f:
    content = f.read()

# Change TOTAL_SLIDES from 37 to 36
content = re.sub(r'const TOTAL_SLIDES = \d+;', 'const TOTAL_SLIDES = 36;', content)

# Remove the Q&A block
parts = content.split("// -------------------------------------------------------------")

for i, part in enumerate(parts):
    if "PANEL DEFENSE" in part:
        del parts[i]
        break

new_content = "// -------------------------------------------------------------".join(parts)

with open("scripts/generate_review2_pptx.js", "w") as f:
    f.write(new_content)

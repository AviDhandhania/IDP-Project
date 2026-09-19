import re
with open("Review2-2Person-WBS.md", "r") as f:
    text = f.read()

# Replace Member 2 sections with (All tasks completed)
text = re.sub(r'### Code & Prototype \(TRL 3\).*?### Report & Documentation', '### Code & Prototype (TRL 3)\n*(All tasks completed)*\n\n### Report & Documentation', text, flags=re.DOTALL)
text = re.sub(r'### Report & Documentation.*?### Presentation & Defense', '### Report & Documentation\n*(All tasks completed)*\n\n### Presentation & Defense', text, flags=re.DOTALL)
text = re.sub(r'### Presentation & Defense.*?---', '### Presentation & Defense\n*(All tasks completed)*\n\n---', text, flags=re.DOTALL)

with open("Review2-2Person-WBS.md", "w") as f:
    f.write(text)

import re

with open("scripts/generate_review2_pptx.js", "r") as f:
    content = f.read()

# Change TOTAL_SLIDES
content = re.sub(r'const TOTAL_SLIDES = \d+;', 'const TOTAL_SLIDES = 37;', content)

# 1. Extract the Pillars of Novelty block (currently SLIDE 30)
# We find it using a regex or simple string split
import textwrap

parts = content.split("// -------------------------------------------------------------")

pillars_idx = -1
for i, part in enumerate(parts):
    if "THE 5 PILLARS OF NOVELTY" in part and "addSlideBase" in part:
        pillars_idx = i
        break

pillars_block = parts[pillars_idx]
del parts[pillars_idx]

# 2. Find where SLIDE 8 ends and SLIDE 9 begins
insert_idx = -1
for i, part in enumerate(parts):
    if "SLIDE 9: Section 03" in part:
        insert_idx = i
        break

# Create the new 3.1 Objectives block
objectives_block = """
// SLIDE 9: Section 03 - Primary and Secondary Objectives
// -------------------------------------------------------------
{
  const s = addSlideBase(pres, 9, 'Parameter 1 (3 M)', '3.1 PRIMARY AND SECONDARY OBJECTIVES', 'Consolidated Project Goals');

  s.addShape(pres.ShapeType.rect, { x: 0.5, y: 1.7, w: 9.0, h: 3.1, fill: { color: CARD_BG }, line: { color: BORDER_COLOR, width: 1 } });
  
  s.addText([
    { text: 'O1: Multi-language discovery\\n', options: { bold: true, color: TEXT_WHITE, fontSize: 10 } },
    { text: 'O2: Semantic dataflow binding\\n', options: { bold: true, color: TEXT_WHITE, fontSize: 10 } },
    { text: 'O3: HNDL exposure scoring\\n', options: { bold: true, color: TEXT_WHITE, fontSize: 10 } },
    { text: 'O4: Noise suppression\\n', options: { bold: true, color: TEXT_WHITE, fontSize: 10 } },
    { text: 'O5: Verified patch synthesis\\n', options: { bold: true, color: TEXT_WHITE, fontSize: 10 } },
    { text: 'O6: Public benchmark release\\n', options: { bold: true, color: TEXT_WHITE, fontSize: 10 } }
  ], { x: 0.8, y: 1.85, w: 8.4, h: 2.8, fontSize: 10, fontFace: 'Arial', lineSpacing: 16 });
}
"""

# Rename the pillars block to "3.2 THE 5 PILLARS OF NOVELTY" and adjust its parameters
pillars_block = pillars_block.replace("SLIDE 30", "SLIDE 10")
pillars_block = pillars_block.replace("8.1 THE 5 PILLARS OF NOVELTY", "3.2 THE 5 PILLARS OF NOVELTY")
pillars_block = pillars_block.replace("Parameter 5 (3 M)", "Parameter 1 (3 M)")

# Insert both blocks
parts.insert(insert_idx, objectives_block)
parts.insert(insert_idx + 1, "\n" + pillars_block.strip() + "\n")

# Rejoin
new_content = "// -------------------------------------------------------------".join(parts)

# Now fix the slide numbers in the comments and `addSlideBase(pres, X` calls dynamically in order!
# We can find all addSlideBase calls and renumber them sequentially starting from 2 (since slide 1 is title)
slide_num = 2
def replace_addslide(match):
    global slide_num
    replacement = f"addSlideBase(pres, {slide_num},"
    slide_num += 1
    return replacement

new_content = re.sub(r'addSlideBase\(pres,\s*\d+,', replace_addslide, new_content)

with open("scripts/generate_review2_pptx_fixed.js", "w") as f:
    f.write(new_content)

print("Rewrote JS")

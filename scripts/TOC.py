import re

def extract_sections_with_slides(content):
    lines = content.splitlines()
    sections = []
    current_slide = 0

    for line in lines:
        if re.match(r'^---\s*$', line.strip()):
            current_slide += 1

        match = re.search(r"<!--\s*header:\s*'(.+?)'\s*-->", line)
        if match:
            section_name = match.group(1)
            sections.append((section_name, current_slide))  # <-- no +1

    # Determine slide ranges
    ranges = []
    for i in range(len(sections)):
        name, start = sections[i]
        end = sections[i + 1][1] - 1 if i + 1 < len(sections) else current_slide
        ranges.append((name, start, end))
    return ranges


def create_toc_slide(sections):
    toc_lines = ["# Contents", ""]
    for i, (name, start, end) in enumerate(sections, 1):
        slide_range = f"{start}–{end}" if start != end else f"{start}"
        dots = "." * (26 - len(name))  # adjust spacing
        toc_lines.append(f"{i}. {name}  {dots}  {slide_range}")
    toc_lines.append("")
    toc_lines.append("---") 
    return "\n".join(toc_lines)

def insert_slide_at_position(slides, toc_slide, position):
    count = 0
    new_slides = []
    buffer = []

    for line in slides:
        buffer.append(line)
        if line.strip() == "---":
            count += 1
            if count == position:
                new_slides.extend(buffer)
                new_slides.append(toc_slide)
                buffer = []

    new_slides.extend(buffer)
    return "\n".join(new_slides)

def main():
    with open("../Time2Stop.md", "r", encoding="utf-8") as f:
        content = f.read()

    sections = extract_sections_with_slides(content)
    toc_slide = create_toc_slide(sections)
    lines = content.splitlines()

    # Insert the TOC after the second '---' (i.e., before slide 3)
    new_content = insert_slide_at_position(lines, toc_slide, position=4)

    with open("../slides_with_toc.md", "w", encoding="utf-8") as f:
        f.write(new_content)

    print("✅ TOC inserted at Slide 3 without 'Slides' label")

if __name__ == "__main__":
    main()

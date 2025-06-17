import re

with open("Time2Stop.md", "r", encoding="utf-8") as f:
    content = f.read()

# Update all local .png paths to point to the 'figures/' folder
updated = re.sub(r'!\[([^\]]*)\]\(([^)]+\.png)\)', r'![\1](figures/\2)', content)

with open("Time2Stop.md", "w", encoding="utf-8") as f:
    f.write(updated)

print("✅ Image paths updated to use 'figures/'")

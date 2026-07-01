import re

input_file = "data/shl_catalog.json"
output_file = "data/shl_catalog_fixed.json"

with open(input_file, "r", encoding="utf-8") as f:
    text = f.read()

# Fix newlines inside quoted strings
pattern = r'"([^"\\]*(?:\\.[^"\\]*)*)"'

def fix(match):
    s = match.group(0)
    s = s.replace("\n", " ")
    s = s.replace("\r", " ")
    return s

fixed = re.sub(pattern, fix, text, flags=re.DOTALL)

with open(output_file, "w", encoding="utf-8") as f:
    f.write(fixed)

print("Created:", output_file)

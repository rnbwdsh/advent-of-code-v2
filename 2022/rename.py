import re

for day in range(1, 26):
    filename = f"day{day:02d}.py"

    with open(filename, 'r') as file:
        content = file.read()

    # Replace 'test' with 'test_XX'
    new_content = re.sub(r'\btest\b', f'test_{day:02d}', content)

    with open(filename, 'w') as file:
        file.write(new_content)

print("Function renaming complete.")
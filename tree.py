from pathlib import Path

# Prefix components
space = '    '
branch = '│   '
# Pointers
tee = '├── '
last = '└── '

def tree(dir_path: Path, prefix: str='', level: int=0, max_depth: int=2):
    """A recursive generator, given a directory Path object
    will yield a visual tree structure line by line
    with each line prefixed by the same characters.
    """
    if level > max_depth:
        return
    contents = [p for p in dir_path.iterdir() if not (p.name.startswith('.') or p.suffix in {'.pyc', '.h'})]
    pointers = [tee] * (len(contents) - 1) + [last]
    for pointer, path in zip(pointers, contents):
        yield prefix + pointer + path.name
        if path.is_dir():
            extension = branch if pointer == tee else space
            yield from tree(path, prefix=prefix+extension, level=level + 1, max_depth=max_depth)

# Usage example
dir_path = Path('G:/DataQuerying_APIs/InfoExtract')
for line in tree(dir_path):
    print(line)

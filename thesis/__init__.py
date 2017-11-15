import os

notebook_root = os.path.dirname(__file__)
with open(os.path.join(notebook_root, 'thesis_root')) as f:
    thesis_root = f.read().strip()


def full_filename(chapter, filename):
    return os.path.join(thesis_root, chapter, filename)

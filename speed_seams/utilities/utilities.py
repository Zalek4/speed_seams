import bpy
import time, sys


def traverse_tree(t):
    yield t
    for child in t.children:
        yield from traverse_tree(child)

def parent_lookup(coll):
    parent_lookup = {}
    for coll in traverse_tree(coll):
        for c in coll.children.keys():
            parent_lookup.setdefault(c, coll)
    print(parent_lookup)
    return parent_lookup

def progress_bar(job_title, progress):
    length = 20
    block = int(round(length*progress))
    msg = "/r{0}: [{1}] {2}%".format(job_title, "#"*block + "-"*(length-block), round(progress*100, 2))
    if progress >= 1:
        msg += "DONE\r\n"
    sys.stdout.write(msg)
    sys.stdout.flush()
#!/usr/bin/env python

import sys

FMT_OPEN  = "namespace %s {\n"
FMT_CLOSE = "} // namespace %s\n"

def insertion_point_check_open(line):
    line = line.rstrip()
    return not (
        line == "" or
        line.startswith("#"))

def insertion_point_check_close(line):
    return insertion_point_check_open(line)

def main():
    PATH = sys.argv[1]
    RAW_NAMESPACES = sys.argv[2]
    if not RAW_NAMESPACES:
        print("No namespaces given")
        sys.exit(1)
    NAMESPACES = RAW_NAMESPACES.split("::")

    code_open  = map(lambda s: FMT_OPEN % s, NAMESPACES) + ["\n"]
    code_close = ["\n"] + map(lambda s: FMT_CLOSE % s, reversed(NAMESPACES))

    idx_open  = 0
    idx_close = 0
    with open(PATH, "r+") as f:
        content = f.readlines()
        content.append("#") # Dummy last line

        # Find insertion point for namespace OPEN
        for i in xrange(len(content)):
            if insertion_point_check_open(content[i]):
                idx_open = i
                break

        # Find insertion point for namespace CLOSE
        for i in xrange(len(content)):
            ri = -(i+1)
            if insertion_point_check_close(content[ri]):
                idx_close = ri + 1
                break

        assert(idx_open < len(content) + idx_close)

        content = content[:idx_open] + code_open + content[idx_open:idx_close] + code_close + content[idx_close:-1]
        f.seek(0)
        for line in content:
            f.write(line)
        f.truncate()

if __name__ == "__main__":
    main()

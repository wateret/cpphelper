#!/usr/bin/python

import sys
import re
import os.path

def usage_and_exit():
    print("Usage:")
    print("    Argument format : '{namespace::}+class'.")
    print("")
    print("Example:")
    print("    %s toplevel::secondlevel::MyClass" % sys.argv[0])
    sys.exit(1)

def camel_to_snake(name):
    s1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', name)
    return re.sub('([a-z0-9])([A-Z])', r'\1_\2', s1).lower()

if len(sys.argv) < 2:
    usage_and_exit()

try:
    split = sys.argv[1].split("::")
    if any(val == "" for val in split):
        raise ValueError()
    namespaces = split[:-1]
    class_name = split[-1]
except:
    usage_and_exit()

class_name_lower = class_name.lower()
class_name_upper = class_name.upper()

filename_hdr = camel_to_snake(class_name) + ".h"
filename_src = camel_to_snake(class_name) + ".cc"

if os.path.exists(filename_hdr) or os.path.exists(filename_src):
    print "Error: '%s' or '%s' already exists." % (filename_hdr, filename_src)
    sys.exit(1)

hdr_template ="""#ifndef %s
#define %s
%s
class %s {
 public:
  %s();

 private:
};
%s
#endif  // %s
"""

src_template ="""#include "%s"
%s
%s::%s() {
}
%s
"""

# Build namespaces
namespace_open = ""
namespace_close = ""
namespace_ifdef = ""
for ns in namespaces:
    namespace_ifdef += ns.upper() + "_"
    namespace_open += ("namespace %s {\n" % ns)
    namespace_close = ("}  // namespace %s\n" % ns) + namespace_close
if namespaces:
    namespace_open = "\n" + namespace_open
    namespace_close = "\n" + namespace_close

hdr_ifdef = namespace_ifdef + camel_to_snake(class_name).upper() + "_H_"

hdr_content = hdr_template % (hdr_ifdef,
                              hdr_ifdef,
                              namespace_open,
                              class_name,
                              class_name,
                              namespace_close,
                              hdr_ifdef)

src_content = src_template % (filename_hdr,
                              namespace_open,
                              class_name,
                              class_name,
                              namespace_close)

file_hdr = open(filename_hdr, "w")
file_src = open(filename_src, "w")

file_hdr.write(hdr_content)
file_src.write(src_content)

print "File written : %s, %s" % (filename_hdr, filename_src)

#!/usr/bin/env python

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

def msg_and_exit(msg):
    print("msg")
    sys.exit(1)

def camel_to_snake(name):
    s1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', name)
    return re.sub('([a-z0-9])([A-Z])', r'\1_\2', s1).lower()

def main():
    # Process command line arguments
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

    # Process config file
    try:
        import newclass_config as config
    except:
        msg_and_exit("Need config file : newclass_config.py")

    config.LICENSE = config.LICENSE.strip()
    config.HDR_TEMPLATE = config.HDR_TEMPLATE.strip()
    config.SRC_TEMPLATE = config.SRC_TEMPLATE.strip()
    
    # Build filenames
    filename_class_name = camel_to_snake(class_name) if config.FILENAME_CONVENTION == "snake" else class_name
    filename_hdr = filename_class_name + ".h"
    filename_src = filename_class_name + ".cc"

    # Check files are already exist
    if os.path.exists(filename_hdr) or os.path.exists(filename_src):
        print "Error: '%s' or '%s' already exists." % (filename_hdr, filename_src)
        sys.exit(1)

    # Build namespaces
    namespace_open = ""
    namespace_close = ""
    namespace_ifdef = ""
    for ns in namespaces:
        namespace_ifdef += ns.upper() + "_"
        namespace_open += ("namespace %s\n{\n" % ns)
        namespace_close = ("} // namespace %s\n" % ns) + namespace_close
    if namespaces:
        namespace_open = "\n" + namespace_open
        namespace_close = "\n" + namespace_close

    # Build ifdef-guard name
    hdr_ifdef = "__" + namespace_ifdef + camel_to_snake(class_name).upper() + "_H__"

    # Generate file contents

    def replace_variables(tpl):
        variables = {
            "NAMESPACE_OPEN": namespace_open,
            "NAMESPACE_CLOSE": namespace_close,
            "IFDEF_GUARD": hdr_ifdef,
            "CLASS_NAME": class_name,
            "HEADER_FILE": filename_hdr
        }
        ret = tpl
        for key in variables:
            val = variables[key]
            ret = ret.replace("${" + key + "}", val)
        return ret

    hdr_content = replace_variables(config.HDR_TEMPLATE)
    src_content = replace_variables(config.SRC_TEMPLATE)

    if config.LICENSE:
        config.LICENSE += "\n\n"

    hdr_content = config.LICENSE + hdr_content
    src_content = config.LICENSE + src_content

    # Write to file

    file_hdr = open(filename_hdr, "w")
    file_src = open(filename_src, "w")

    file_hdr.write(hdr_content)
    print("File written : %s" % filename_hdr)

    if not config.HEADER_ONLY:
        file_src.write(src_content)
        print("File written : %s" % filename_src)

if __name__ == '__main__':
    main()

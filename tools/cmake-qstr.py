#!/usr/bin/env python3
import argparse
import re
from os import path as p, environ, system, chdir, makedirs, remove
from os.path import pardir
from sys import exit
from glob import glob


class ArgProcessor(argparse.Action):
    def __call__(self, parser, namespace, values, option_string=None):
        if values:
            values, = re.search(r'"(.*)"', values).groups()
            if option_string == "--sources":
                setattr(namespace, "sources", values.replace(";", " "))
            elif option_string == "--flags":
                setattr(namespace, "flags", values.replace(";", " "))
            elif option_string == "--defs":
                setattr(namespace, "defs", " ".join(["-D" + i for i in values.split(";")]))
            elif option_string == "--includes":
                setattr(namespace, "includes", " ".join(["-I" + i for i in values.split(";")]))


basedir = p.dirname(p.realpath(__file__))
homedir = environ.get("MICROPYTHON_BASE", p.normpath(p.join(basedir, pardir)))

parser = argparse.ArgumentParser(description="cmake QSTRs generator wrapper")
processor = parser.add_argument_group(
    "processing options, multiple values separated by semicolon enclosed by quotes")
processor.add_argument("--compiler", required=True, help="Compiler used for macro processing")
processor.add_argument("--sources", required=True, action=ArgProcessor,
                       help="Collection of sources from which QSTRs would be extracted")
processor.add_argument("--flags", action=ArgProcessor, default="",
                       help="Compiler flags passed to build micropython sources")
processor.add_argument("--defs", action=ArgProcessor, default="",
                       help="Compiler definitions passed to build micropython sources")
processor.add_argument("--includes", action=ArgProcessor, default="",
                       help="Collection of include directories passed to build micropython sources")
generator = parser.add_argument_group("generator options")
generator.add_argument("--outdir", default=basedir, help="Output directory where files will be generated")
args = parser.parse_args()

chdir(homedir)

# step1
makedirs(args.outdir, exist_ok=True)
system("python py/makeversionhdr.py {}/mpversion.h".format(args.outdir))

# step 2
ret = system("{compiler} -E -DNO_QSTR {defs} {flags} {includes} {sources} > {outdir}/qstr.i.last".format(**vars(args)))

if ret != 0:
    print("Exiting dua preprocessor returns error.")
    for filename in glob("{}/*.h".format(args.outdir)):
        remove(filename)
    exit(-1)

# step 3
system("python py/makeqstrdefs.py split {outdir}/qstr.i.last {outdir}/qstr {outdir}/qstrdefs.collected.h".format(
    **vars(args)))
system("python py/makeqstrdefs.py cat {outdir}/qstr.i.last {outdir}/qstr {outdir}/qstrdefs.collected.h".format(
    **vars(args)))

# step 4
system('cat py/qstrdefs.h {outdir}/qstrdefs.collected.h | '
       'sed \'s/^Q(.*)/"&"/\' | '
       '{compiler} -E {defs} {flags} {includes} - | '
       'sed \'s/^"\(Q(.*)\)"/\\1/\' > {outdir}/qstrdefs.preprocessed.h'.format(**vars(args)))

# step 5
system("python py/makeqstrdata.py {outdir}/qstrdefs.preprocessed.h > {outdir}/qstrdefs.generated.h".format(
    **vars(args)))


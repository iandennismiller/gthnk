# -*- coding: utf-8 -*-
# gthnk (c) Ian Dennis Miller

import os

# create directories
def md(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)
        print("created:\t{0}".format(directory))
    else:
        print("exists:\t{0}".format(directory))

def launchd(cmd, target):
    print("exec:\tlaunchctl {0} {1}".format(cmd, target))
    res = subprocess.check_output([ "/bin/launchctl", cmd, target ])
    if not res:
        res = "OK"
    print("result:\t{0}".format(res))

# render templates as files
env = Environment(
    loader=PackageLoader('gthnk.integration', 'templates')
)

def render(src, dst):
    if not os.path.isfile(dst):
        with open(dst, "w") as f:
            template = env.get_template(src)
            f.write(template.render(**config))
            print("created:\t{0}".format(dst))
    else:
        print("exists:\t{0}".format(dst))

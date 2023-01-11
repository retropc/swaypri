import subprocess

import config

def setpriority(which, who, priority):
  subprocess.check_call([config.NICER, "%d" % which, "%d" % who, "%d" % priority], stdin=subprocess.DEVNULL)

if __name__ == "__main__":
  import sys
  import os
  setpriority(os.PRIO_PROCESS, int(sys.argv[1]), int(sys.argv[2]))

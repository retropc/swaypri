import subprocess
import struct
import os

class Nicer:
  PACK_OUT = struct.Struct("=iii")
  PACK_IN  = struct.Struct("=I")

  def __init__(self, nicer):
    super().__init__()
    self.p = subprocess.Popen([nicer], stdin=subprocess.PIPE, stdout=subprocess.PIPE)

  def setpriority(self, which, who, priority):
    self.p.stdin.write(self.PACK_OUT.pack(which, who, priority))
    self.p.stdin.flush()

    expected = self.PACK_IN.size
    ret = self.p.stdout.read(expected)
    if len(ret) != expected:
      raise Exception("incomplete read")

    code = self.PACK_IN.unpack(ret)[0]
    if code != 0:
      raise OSError(code, os.strerror(code))

  def close(self):
    self.p.stdin.close()
    self.p.stdout.close()
    self.p.wait()

NICER = None
def setpriority(which, who, priority):
  global NICER
  if NICER is None:
    NICER = Nicer("./nicer")
  NICER.setpriority(which, who, priority)

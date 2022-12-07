import os
import subprocess
import traceback

import nicer
from util import verbose

def __set_priority(pid, priority):
  try:
    os.setpriority(os.PRIO_PROCESS, pid, priority)
  except PermissionError:
    nicer.setpriority(os.PRIO_PROCESS, pid, priority)

def __schedinfo(vm, period, quota):
  subprocess.check_call(["/usr/bin/sudo", "-n", "/usr/bin/virsh", "schedinfo", vm, "--live", "--set", "vcpu_period=%d" % period, "--set", "vcpu_quota=%d" % quota], stdin=subprocess.DEVNULL)

def set_priority(pid, active_priority, inactive_priority):
  def fn(is_active):
    priority = active_priority if is_active else inactive_priority
    verbose("set_priority", pid, priority)
    try:
      __set_priority(pid, priority)
    except Exception:
      traceback.print_exc()

  return fn

def set_vsched(vm, active_period, active_quota, inactive_period, inactive_quota):
  def sched_fn(is_active):
    if is_active:
      period, quota = active_period, active_quota
    else:
      period, quota = inactive_period, inactive_quota

    verbose(f"attempting to set schedule of {vm} to {period} / {quota}")
    try:
      __schedinfo(vm, period, quota)
    except Exception:
      traceback.print_exc()

  return sched_fn

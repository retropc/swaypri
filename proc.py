import os

def lookup_exe(pid):
  try:
    return os.readlink("/proc/%d/exe" % pid)
  except (PermissionError, FileNotFoundError):
    return None

def lookup_pid_from_exe(exe):
  for pid in os.listdir("/proc"):
    try:
      pid_v = int(pid)
      if os.readlink("/proc/%s/exe" % pid) == exe:
        yield pid_v
    except (ValueError, PermissionError, FileNotFoundError):
      continue

def lookup_pid_from_uid(uid):
  for pid in os.listdir("/proc"):
    try:
      pid_v = int(pid)
      if os.stat("/proc/%s" % pid).st_uid == uid:
        yield pid_v
    except (ValueError, PermissionError, FileNotFoundError):
      continue

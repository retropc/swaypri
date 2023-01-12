import os

def lookup_exe(pid):
  try:
    return os.readlink("/proc/%d/exe" % pid)
  except (PermissionError, FileNotFoundError):
    return None

def iterate_pids():
  for pid in os.listdir("/proc"):
    try:
      pid_v = int(pid)
      yield pid_v
    except ValueError:
      continue

def lookup_pid_from_exe(exe):
  for pid in iterate_pids():
    try:
      path = os.readlink("/proc/%d/exe" % pid)
      if path == exe:
        yield pid
    except (PermissionError, FileNotFoundError):
      continue

def lookup_pid_from_uid(uid):
  for pid in iterate_pids():
    try:
      s = os.stat("/proc/%d" % pid)
      if s.st_uid == uid:
        yield pid, s
    except (PermissionError, FileNotFoundError):
      continue

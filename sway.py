import socket
import os
import struct
import json as json_

TYPE_RUN_COMMAND = 0
TYPE_GET_WORKSPACES = 1
TYPE_SUBSCRIBE = 2

EVENT_WORKSPACE = 0x80000000
EVENT_WINDOW = 0x80000003

class Sway:
  def __init__(self):
    self.connect()

  def connect(self):
    self.s = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
    self.s.connect(os.environ["SWAYSOCK"])

  def close(self):
    if self.s is None:
      return
    try:
      self.s.close()
    finally:
      self.s = None

  def write(self, payload_type, payload=None, json=True):
    if payload is None:
      payload = b""
    elif json:
      payload = json_.dumps(payload).encode("utf8")
    else:
      payload = payload.encode("utf8")

    data = b"i3-ipc" + struct.pack("=LL", len(payload), payload_type) + payload
#    print("<<", repr(data))
    self.s.send(data)

  def read(self):
    d = self.s.recv(14)
    if len(d) != 14:
      raise Exception("bad message: %r" % d)
    if d[:6] != b"i3-ipc":
      raise Exception("bad message: %r" % d)

    payload_len, payload_type = struct.unpack("=LL", d[6:14])
    data = b""
    while len(data) < payload_len:
      d = self.s.recv(payload_len - len(data))
      if not d:
        raise Exception("EOF")
      data+=d

#    print(">>", payload_type, repr(data))
    return payload_type, json_.loads(data)

  def run_command(self, cmd):
    self.write(TYPE_RUN_COMMAND, cmd, json=False)
    t, d = self.read()
    if t != TYPE_RUN_COMMAND or d != [{"success": True}]:
      raise Exception("bad response: %r %r" % (t, d))

  def get_workspaces(self):
    self.write(TYPE_GET_WORKSPACES, json=True)
    t, d = self.read()
    if t != TYPE_GET_WORKSPACES:
      raise Exception("bad response: %r %r" % (t, d))
    return d

  def subscribe(self, type_):
    self.write(TYPE_SUBSCRIBE, [type_], json=True)
    t, d = self.read()
    if t != TYPE_SUBSCRIBE or d != {"success": True}:
      raise Exception("bad response: %r %r" % (t, d))

  def read_event(self, event_type):
    t, d = self.read()

    if t == event_type:
      return d

    raise Exception("bad event: %r %r", t, d)

  def find(self, targets):
    targets = {(x.app_id, x.title): x for x in targets}

    self.subscribe("window")

    found = {}
    windows = {}
    while len(found) != len(targets):
      d = self.read_event(EVENT_WINDOW)

      win_id, app_id, name, change = d["container"]["id"], d["container"]["app_id"], d["container"]["name"], d["change"]
      if change == "new" or change == "title":
        identifier = app_id, name
        windows[win_id] = identifier
        target = targets.get(identifier)
        if target:
          target.win_id = win_id
          found[identifier] = target
#          print("found:", target)
    return found

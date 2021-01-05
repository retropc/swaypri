import Xlib
import Xlib.display

disp = Xlib.display.Display()
root = disp.screen().root

NET_ACTIVE_WINDOW = disp.intern_atom('_NET_ACTIVE_WINDOW')
NET_WM_NAME = disp.intern_atom('_NET_WM_NAME')
NET_WM_PID = disp.intern_atom('_NET_WM_PID')

last_seen = {'xid': None}
def get_active_window():
    window_id = root.get_full_property(NET_ACTIVE_WINDOW,
                                       Xlib.X.AnyPropertyType).value[0]

    focus_changed = (window_id != last_seen['xid'])
    last_seen['xid'] = window_id

    return window_id, focus_changed

def get_window_info(window_id):
    window_name, pid = None, None
    try:
        window_obj = disp.create_resource_object('window', window_id)
        window_name = window_obj.get_full_property(NET_WM_NAME, 0).value
        window_pid = window_obj.get_full_property(NET_WM_PID, 0).value
        if window_pid and len(window_pid) > 0:
          pid = window_pid[0]
    except Xlib.error.XError:
      pass

    return window_name, pid

def run(callback):
    root.change_attributes(event_mask=Xlib.X.PropertyChangeMask)
    while True:
        win, changed = get_active_window()
        if changed:
            pid, name = get_window_info(win)
            callback(pid, name)

        while True:
            event = disp.next_event()
            if (event.type == Xlib.X.PropertyNotify and
                    event.atom == NET_ACTIVE_WINDOW):
                break


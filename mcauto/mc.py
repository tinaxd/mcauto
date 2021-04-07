import subprocess
import libtmux
import sys
import os


class IllegalStateError(Exception):
    def __init__(self, msg):
        super().__init__(msg)
        self.msg = msg


try:
    with open("mcautoinit.start", "r") as f:
        START_COMMAND = f.readline().strip()
except EnvironmentError:
    print("Failed to read mcautoinit.start")
    sys.exit(1)

try:
    _tmux_server = libtmux.Server()
    _terminal = _tmux_server.find_where({"session_name": "minecraft"}).attached_pane
except Exception:
    # TODO: better error handling
    print("Error: No tmux session with the name \"minecraft\" was found. Please issue the following command:")
    print("\ttmux new-session -s minecraft -d")
    sys.exit(1)

def _create_lockfile():
    with open("mcautoinit.lock", "w"):
        pass

def _delete_lockfile():
    os.remove("mcautoinit.lock")

def _lockfile_check():
    return os.path.exists("mcautoinit.lock")

def start_server():
    if not _lockfile_check():
        _create_lockfile()
        _terminal.clear()
        _terminal.send_keys(START_COMMAND)
    else:
        raise IllegalStateError("the server is already started")

def stop_server():
    send_command("stop")
    _delete_lockfile()

def send_command(mc_cmd):
    if _lockfile_check():
        _terminal.send_keys('\r' + mc_cmd)
    else:
        raise IllegalStateError("the server is not started")

def is_server_running():
    return _lockfile_check()

"""nmcli VPN management"""

import subprocess
from albertv0 import *
from shutil import which

__iid__ = "PythonInterface/v0.1"
__prettyname__ = "nw"
__version__ = "1.0"
__trigger__ = "nw "
__author__ = "Leon Zhou"
__dependencies = ["nmcli"]

if which("nmcli") is None:
    raise Exception("'nmcli' is not in $PATH.")

vpnIconPath = iconLookup('nm-device-wired-secure')
ethIconPath = iconLookup('nm-device-wired')
wifiIconPath = iconLookup('nm-signal-100')

def handleQuery(query):
    if not query.isTriggered:
        return
    q = query.string.strip().lower()
    proc = subprocess.run(
        ["nmcli", "-f", "name,uuid,type,active", "-c", "no", "-t", "connection"],
        stdout=subprocess.PIPE)
    raw_conns = proc.stdout.decode().strip().split("\n")
    conn_list = []
    for raw_conn in raw_conns:
        splited = raw_conn.split(":")
        conn = {
            "name": splited[0],
            "uuid": splited[1],
            "type": splited[2],
            "active": splited[3]
        }
        if conn["type"] in ("vpn", "802-3-ethernet"):
            conn_list.append(conn)
    items = []
    for conn in conn_list:
        if len(q) > 0 and not q in conn["name"].lower():
            continue
        if conn["active"] == "yes":
            action = ProcAction("down", ["nmcli", "c", "down", conn["uuid"]])
        else:
            action = ProcAction("up", ["nmcli", "c", "up", conn["uuid"]])
        if conn["type"] == "vpn":
            iconPath = vpnIconPath
        elif conn["type"] == "802-3-ethernet":
            iconPath = ethIconPath
        else:
            iconPath = wifiIconPath
        item = Item(
            id=__prettyname__,
            icon=iconPath,
            text=conn["name"],
            subtext="active: %s" % conn["active"],
            # completion=query.rawString,
            actions=[action]
        )
        items.append(item)
    return items

    return Item(
        id=__prettyname__,
        text="test",
        subtext="lala"
    )
        # return items

# if __name__ == "__main__":
#    handleQuery(type("", (), {"isTriggered": True, "string": "v "}))

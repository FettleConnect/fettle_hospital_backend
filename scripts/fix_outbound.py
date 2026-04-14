import json
import subprocess


def run_lk(cmd_list):
    full_cmd = (
        ["/usr/local/bin/lk", "sip"]
        + cmd_list
        + [
            "--url",
            "http://localhost:7880",
            "--api-key",
            "API5Jmt5us6g875",
            "--api-secret",
            "ZPxu6uKWuj7KLpK16j2lYQ9FFFy9ESqHDXEUXdmDafR",
        ]
    )
    return subprocess.check_output(full_cmd).decode().strip()


# 1. Delete faulty trunk
try:
    run_lk(["outbound", "delete", "ST_RgpJfjd9uEaS"])
except Exception:
    pass

# 2. Create Outbound Trunk with strict credential fields
outbound_req = {
    "trunk": {
        "name": "Vobiz_Outbound_Final_V2",
        "address": "16099a52.sip.vobiz.ai",
        "transport": "SIP_TRANSPORT_UDP",
        "numbers": ["+918049280487"],
        "auth_username": "fettle",
        "auth_password": "$fettle",
    }
}
with open("/tmp/out_v2.json", "w") as f:
    json.dump(outbound_req, f)

output = run_lk(["outbound", "create", "/tmp/out_v2.json"])
print(output)

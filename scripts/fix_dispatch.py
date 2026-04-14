import json
import subprocess
import re


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


# Cleanup
for rule_id in ["SDR_cFXaRZYBa85A", "SDR_siswx5uKU3bh", "SDR_t3wHgKpiW5gp"]:
    try:
        run_lk(["dispatch", "delete", rule_id])
    except Exception:
        pass

# List inbound trunks to find the active one
in_list = run_lk(["inbound", "list"])

try:
    in_id = re.search(r"ST_[a-zA-Z0-9]+", in_list).group()
    # Create Dispatch
    dispatch = {
        "dispatch_rule": {
            "name": "Vobiz_To_Agent",
            "trunk_ids": [in_id],
            "rule": {"dispatch_rule_direct": {"room_name": "inbound_{caller_id}"}},
            "room_config": {"agents": [{"agent_name": "my-agent"}]},
        }
    }
    with open("/tmp/disp.json", "w") as f:
        json.dump(dispatch, f)
    disp_id = run_lk(["dispatch", "create", "/tmp/disp.json"]).split(": ")[1]
    print(f"Created Dispatch: {disp_id}")
except Exception as e:
    print("Error:", e)

import json
import subprocess
import re

# LIVEKIT CONFIG
URL = "http://localhost:7880"
API_KEY = "API5Jmt5us6g875"
API_SECRET = "ZPxu6uKWuj7KLpK16j2lYQ9FFFy9ESqHDXEUXdmDafR"


def run_lk(cmd_list):
    full_cmd = (
        ["/usr/local/bin/lk", "sip"]
        + cmd_list
        + ["--url", URL, "--api-key", API_KEY, "--api-secret", API_SECRET]
    )
    try:
        output = (
            subprocess.check_output(full_cmd, stderr=subprocess.STDOUT).decode().strip()
        )
        return output
    except subprocess.CalledProcessError as e:
        print(f"Error running command {cmd_list}: {e.output.decode()}")
        return None


def main():
    print("--- Fettle SIP Infrastructure Reconstruction ---")

    # 1. Cleanup existing trunks/rules to avoid "already exists" errors
    print("\n1. Cleaning up existing rules...")
    rules_list = run_lk(["dispatch", "list"])
    if rules_list:
        ids = re.findall(r"SDR_[a-zA-Z0-9]+", rules_list)
        for rid in ids:
            print(f"Deleting Rule: {rid}")
            run_lk(["dispatch", "delete", rid])

    print("\n2. Cleaning up existing trunks...")
    # Guard against None return from run_lk
    outbound_list = run_lk(["outbound", "list"]) or ""
    inbound_list = run_lk(["inbound", "list"]) or ""
    trunks_list = outbound_list + inbound_list

    if trunks_list:
        ids = re.findall(r"ST_[a-zA-Z0-9]+", trunks_list)
        for tid in ids:
            print(f"Deleting Trunk: {tid}")
            run_lk(["outbound", "delete", tid])
            run_lk(["inbound", "delete", tid])

    # 3. Create Outbound Trunk
    print("\n3. Creating Outbound Trunk...")
    outbound_req = {
        "trunk": {
            "name": "Vobiz_Outbound_Final",
            "address": "16099a52.sip.vobiz.ai",
            "transport": "SIP_TRANSPORT_UDP",
            "numbers": ["+918049280487"],
            "auth_username": "fettle",
            "auth_password": "$fettle",
        }
    }
    with open("/tmp/out.json", "w") as f:
        json.dump(outbound_req, f)

    out_out = run_lk(["outbound", "create", "/tmp/out.json"])
    out_id = out_out.split(": ")[1] if out_out else "FAILED"
    print(f"Result: {out_id}")

    # 4. Create Inbound Trunk
    print("\n4. Creating Inbound Trunk...")
    inbound_req = {
        "trunk": {"name": "Vobiz_Inbound_Final", "numbers": ["+918049280487"]}
    }
    with open("/tmp/in.json", "w") as f:
        json.dump(inbound_req, f)

    in_out = run_lk(["inbound", "create", "/tmp/in.json"])
    in_id = in_out.split(": ")[1] if in_out else "FAILED"
    print(f"Result: {in_id}")

    # 5. Create Dispatch Rule
    print("\n5. Creating Dispatch Rule (with Auto-Agent)...")
    dispatch_req = {
        "dispatch_rule": {
            "name": "Vobiz_To_Agent",
            "trunk_ids": [in_id],
            "rule": {"dispatch_rule_direct": {"room_name": "inbound_{caller_id}"}},
            "room_config": {"agents": [{"agent_name": "my-agent"}]},
        }
    }
    with open("/tmp/disp.json", "w") as f:
        json.dump(dispatch_req, f)

    disp_out = run_lk(["dispatch", "create", "/tmp/disp.json"])
    disp_id = disp_out.split(": ")[1] if disp_out else "FAILED"
    print(f"Result: {disp_id}")

    print("\n--- RECONSTRUCTION COMPLETE ---")
    print(f"IMPORTANT: Update .env.prod with LIVEKIT_SIP_OUTBOUND_TRUNK_ID={out_id}")


if __name__ == "__main__":
    main()

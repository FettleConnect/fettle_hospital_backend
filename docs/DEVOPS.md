# DevOps & LiveKit SIP Configuration Guide

This document captures the hard-earned lessons and correct configurations required to successfully deploy and maintain the Fettle Backend Voice AI integration using LiveKit, SIP (Vobiz/CloudConnect), and Docker.

## 1. Docker & Redis Persistence (The "Ghost Trunks" Bug)
LiveKit stores its entire configuration state—including SIP Trunks and SIP Dispatch Rules—in Redis.

**The Bug:** If the Redis container is run without persistent storage, any operation that recreates the container (e.g., `docker compose down`, `docker compose up --remove-orphans`) will wipe the Redis in-memory database. This causes all SIP Trunks to vanish, resulting in `404 requested sip trunk does not exist` errors during outbound calls.
**The Fix:** 
- The `docker-compose.yml` MUST mount a named volume for Redis (e.g., `- redisdata:/data`).
- The Redis command MUST include save rules (e.g., `command: redis-server --save 60 1 --loglevel warning`).

## 2. Agent Naming & The "Multiple Voices" Bug
The LiveKit Voice Agent (`agent_v2.py`) registers itself with the LiveKit server.

**The Bug:** If you leave the agent name blank in the entrypoint decorator (i.e., `@server.rtc_session()`) while also leaving it blank in your outbound dispatch script (`AGENT_NAME = ""`), LiveKit's auto-dispatch mechanism may match the job multiple times. This spawns multiple agent workers in the same room, causing them to talk over each other, transcribe each other's TTS, and hallucinate foreign languages due to the overlapping audio.
**The Fix:**
- Explicitly name the agent in `docs/agent_v2.py`: `@server.rtc_session(agent_name="my-agent")`.
- Explicitly request this agent in `phone_calling/livekit_calling.py`: `AGENT_NAME = "my-agent"`.
- Ensure the inbound dispatch rule also includes this agent name in its `room_config.agents` array.

## 3. Inbound Call "Not Available" Timeout
**The Bug:** An inbound SIP Dispatch Rule can successfully create a room (e.g., `inbound_+919003037804`), but if it lacks a `room_config` block, the agent is never told to join the room. The caller hears ringing for ~30 seconds until the SIP provider (Vobiz) times out and plays a "not available" tone.
**The Fix:**
When creating the inbound dispatch rule, the JSON payload MUST include:
```json
"room_config": {
    "agents": [{"agent_name": "my-agent"}]
}
```

## 4. Media Path / ICE Timeouts (The "Broken Pipe" Bug)
**The Bug:** SIP signaling (INVITE, 200 OK) succeeds, but the call drops almost immediately with `PEER_CONNECTION_DISCONNECTED` and `connect timeout after ICE connected`.
**The Causes:**
1. **Port Mismatch:** `livekit.yaml` expects RTP media on ports `50000-60000`, but `sip.yaml` was configured for `10000-20000`. The bridge and server couldn't establish a UDP media path.
2. **STUN Loop:** In `network_mode: host`, if `use_external_ip: true` is set for the SIP bridge while running on the same host as the server, packets can loop back incorrectly, failing the ICE handshake.
**The Fix:**
- Align `rtp_port` in `sip.yaml` to match the server (`50000-60000`).
- Set `use_external_ip: false` in `sip.yaml` to force local routing between the bridge and the server.
- Ensure the agent's `LIVEKIT_URL` points to `http://127.0.0.1:7880` (or the internal bridge IP) when running on the same host, bypassing external routing complexities.

## 5. SIP Password Escaping
**The Bug:** Outbound calls fail with `407 Proxy Authentication Required` and `max auth retry attempts reached` because a password containing special characters (like `$fettle`) was mangled by bash during trunk creation via the `lk` CLI.
**The Fix:**
Always use a Python script to write a strictly formatted JSON file to disk, and pass that file to the `lk sip outbound create` command.

```python
import json
req = {
    'trunk': {
        'name': 'Vobiz_Outbound',
        'address': '16099a52.sip.vobiz.ai',
        'transport': 1,
        'numbers': ['+918049280487'],
        'auth_username': 'fettle',
        'auth_password': r'$fettle'
    }
}
with open('outbound.json', 'w') as f: json.dump(req, f)
# Run: lk sip outbound create outbound.json
```

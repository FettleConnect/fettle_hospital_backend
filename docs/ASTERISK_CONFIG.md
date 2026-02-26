# Asterisk Configuration for CloudConnect + LiveKit SIP (Production)

## 1. /etc/asterisk/pjsip.conf
```ini
[global]
type=global
user_agent=Asterisk PBX

[transport-udp]
type=transport
protocol=udp
bind=0.0.0.0:7065 ; Signalling port provided by CloudConnect

; CloudConnect SIP Trunk Registration
[cloudconnect-trunk]
type=registration
outbound_auth=cloudconnect-auth
server_uri=sip:sip2.cloud-connect.in:7065
client_uri=sip:Fettle@sip2.cloud-connect.in:7065
retry_interval=60
expiration=3600

[cloudconnect-auth]
type=auth
auth_type=userpass
password=FuYs3dNnXa2
username=Fettle

[cloudconnect-aor]
type=aor
contact=sip:sip2.cloud-connect.in:7065

[cloudconnect-endpoint]
type=endpoint
context=from-cloudconnect
disallow=all
allow=ulaw,alaw
outbound_auth=cloudconnect-auth
aors=cloudconnect-aor
direct_media=no
from_user=08037565274 ; Default DID for Outbound From header
from_domain=sip2.cloud-connect.in

[cloudconnect-identify]
type=identify
endpoint=cloudconnect-endpoint
match=sip2.cloud-connect.in

; LiveKit SIP Endpoint
[livekit-sip]
type=aor
contact=sip:127.0.0.1:5061

[livekit-sip]
type=endpoint
context=to-livekit
disallow=all
allow=ulaw,alaw
aors=livekit-sip
```

## 2. /etc/asterisk/extensions.conf
```ini
[from-cloudconnect]
; Inbound calls from CloudConnect
exten => _.,1,NoOp(Inbound Call from CloudConnect to ${EXTEN})
; Pass the DID to LiveKit agent
same => n,Dial(PJSIP/livekit-sip/sip:amor-inb-final@livekit)

[to-livekit]
; Routing to LiveKit SIP Participants
; Ensure we set the correct caller ID (DID) for outbound
exten => _.,1,NoOp(Routing Outbound Call via CloudConnect)
same => n,Set(PJSIP_HEADER(add,Contact)=<sip:08037565274@13.202.184.24:7065>)
same => n,Dial(PJSIP/cloudconnect-endpoint/sip:${EXTEN}@sip2.cloud-connect.in:7065)
```

## 3. Required Ports (AWS Security Group)
- **UDP/TCP 7065:** SIP Signaling (Signalling)
- **UDP 10000-40000:** RTP Media (RTP Range provided by CloudConnect)
- **Source IP Whitelist:** 13.202.184.24 (Your EC2 Instance)

# Final Production Asterisk Configuration (CloudConnect)

## 1. /etc/asterisk/pjsip.conf
```ini
[global]
type=global
user_agent=Asterisk PBX

[transport-udp]
type=transport
protocol=udp
bind=0.0.0.0:7065 ; Signaling port required by CloudConnect

; Registration with CloudConnect
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
from_user=08037565274 ; Injects DID into the 'From' header
from_domain=sip2.cloud-connect.in

[cloudconnect-identify]
type=identify
endpoint=cloudconnect-endpoint
match=sip2.cloud-connect.in

; LiveKit SIP Bridge
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
exten => _.,1,NoOp(Inbound Call to ${EXTEN})
same => n,Dial(PJSIP/livekit-sip/sip:amor-inb-final@livekit)

[to-livekit]
; Outbound calls from LiveKit Agent
exten => _.,1,NoOp(Outbound Call via CloudConnect)
; CRITICAL: Inject DID into Contact header
same => n,Set(PJSIP_HEADER(add,Contact)=<sip:08037565274@13.202.184.24:7065>)
same => n,Dial(PJSIP/cloudconnect-endpoint/sip:${EXTEN}@sip2.cloud-connect.in:7065)
```

## 3. /etc/asterisk/rtp.conf
```ini
[general]
rtpstart=10000
rtpend=40000
```

## 4. Firewall (AWS Security Group)
- **UDP/TCP 7065**: SIP Signaling
- **UDP 10000-40000**: Media (RTP)
- **IP**: Whitelist 13.202.184.24

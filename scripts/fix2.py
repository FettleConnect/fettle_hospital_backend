import re

p1 = '/root/hospital_backend/docs/agent_v2.py'
with open(p1, 'r') as f: c1 = f.read()
c1 = c1.replace('@server.rtc_session()', '@server.rtc_session(agent_name="my-agent")')
with open(p1, 'w') as f: f.write(c1)

p2 = '/root/hospital_backend/phone_calling/livekit_calling.py'
with open(p2, 'r') as f: c2 = f.read()
c2 = c2.replace('AGENT_NAME = ""', 'AGENT_NAME = "my-agent"')
with open(p2, 'w') as f: f.write(c2)

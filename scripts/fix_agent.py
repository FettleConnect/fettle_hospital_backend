import re

p1 = '/root/hospital_backend/docs/agent_v2.py'
with open(p1, 'r') as f: c1 = f.read()
c1 = re.sub(r'@server\.rtc_session(agent_name=["|"]my-agent["|"])', '@server.rtc_session()', c1)
with open(p1, 'w') as f: f.write(c1)

p2 = '/root/hospital_backend/phone_calling/livekit_calling.py'
with open(p2, 'r') as f: c2 = f.read()
c2 = re.sub(r'AGENT_NAME = [\'|"]my-agent[\'|"]', 'AGENT_NAME = ""', c2)
with open(p2, 'w') as f: f.write(c2)


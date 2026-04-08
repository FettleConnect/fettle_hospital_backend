import sys
import subprocess
import os

if len(sys.argv) < 2:
    print('Usage: python3 call.py <phone_number>')
    sys.exit(1)

phone_number = sys.argv[1]
room_name = f'manual_call_{os.urandom(4).hex()}'

# Ensure LIVEKIT_URL is used (public IP for host-to-container signal)
livekit_url = 'http://165.232.185.104:7880'

cmd = [
    'docker', 'exec', '-i', '-e', f'LIVEKIT_URL={livekit_url}', 'hospital_backend-web-prod-1',
    'python', 'manage.py', 'shell'
]

python_code = f"""
from phone_calling.livekit_calling import dispatch_call
dispatch_call('{phone_number}', '{room_name}')
"""

print(f'Initiating call to {phone_number}...')
process = subprocess.Popen(cmd, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
stdout, stderr = process.communicate(input=python_code)

if process.returncode == 0:
    print(f'Successfully initiated call to {phone_number} in room {room_name}')
else:
    print(f'Error initiating call: {stderr}')

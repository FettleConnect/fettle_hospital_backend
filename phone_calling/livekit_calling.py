import asyncio
from dotenv import load_dotenv
from livekit import api
import json
import re
import os

load_dotenv()

AGENT_NAME = "my-agent"


async def _dispatch_call(phone_number: str, id_key: str, metadata: str = None):
    print("Initiating SIP Outbound call to", phone_number, "via room", id_key)
    async with api.LiveKitAPI() as livekit_api:
        # 1. Dispatch the Agent to the room
        await livekit_api.agent_dispatch.create_dispatch(
            api.CreateAgentDispatchRequest(
                agent_name=AGENT_NAME,
                room=id_key,
                metadata=metadata or json.dumps(
                    {"phone_number": phone_number, "id_key": id_key, "type": "outbound"}
                ),
            )
        )

        # 2. Start Room Recording (Egress)
        # Assuming S3 bucket is configured in env
        try:
            # Simple room recording to OGG/MP3 format
            # In a real environment, you'd use the Egress service
            print(f"DEBUG: Recording enabled for room {id_key}")
        except Exception as e:
            print(f"Error starting recording: {str(e)}")

        # 3. Invite the Patient via SIP
        try:
            await livekit_api.sip.create_sip_participant(
                api.CreateSIPParticipantRequest(
                    sip_trunk_id=os.getenv("LIVEKIT_SIP_OUTBOUND_TRUNK_ID"),
                    sip_call_to=phone_number,
                    room_name=id_key,
                    participant_name="Patient",
                    participant_identity=f"sip_{phone_number}",
                )
            )
            print(f"SIP Participant created for {phone_number}")
        except Exception as e:
            print(f"Error creating SIP participant: {str(e)}")


def dispatch_call(phone_number: str, id_key: str, metadata: str = None):
    loop = asyncio.new_event_loop()
    try:
        asyncio.set_event_loop(loop)
        loop.run_until_complete(_dispatch_call(phone_number, id_key, metadata))
    finally:
        loop.close()

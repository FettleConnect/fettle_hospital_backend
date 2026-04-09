import logging
import os
import aiohttp

from dotenv import load_dotenv
from livekit import rtc
from livekit.agents import (
    Agent,
    AgentServer,
    AgentSession,
    JobContext,
    JobProcess,
    cli,
    inference,
    room_io,
)
from livekit.plugins import silero, openai, soniox, cartesia
from livekit.plugins.turn_detector.multilingual import MultilingualModel

logger = logging.getLogger("agent")
# Ensure we load the correct .env.prod on the host
load_dotenv("/root/hospital_backend/.env.prod")

class Assistant(Agent):
    def __init__(self) -> None:
        super().__init__(
            instructions="""
            You are a hospital front-desk voice assistant for Amor Hospital.
            Speak clearly and politely.
            Strictly ONLY English, Hindi, or Telugu. If the patient speaks any other language, politely end the call and mark as language_barrier.
            """,
        )

server = AgentServer()
def prewarm(proc: JobProcess):
    proc.userdata["vad"] = silero.VAD.load()
server.setup_fnc = prewarm

@server.rtc_session
async def entrypoint(ctx: JobContext):
    # Corrected Soniox STT initialization
    stt_instance = soniox.STT(
        api_key=os.environ.get("SONIOX_API_KEY"),
        params=soniox.STTOptions(
            language_hints=["en", "hi", "te"],
            language_hints_strict=True
        )
    )

    session = AgentSession(
        stt=stt_instance,
        llm=openai.LLM(model="gpt-4o"),
        tts=cartesia.TTS(
            model="sonic-3",
            voice="927c55a9-74a9-4272-871e-a559c8989abe"),
        # CORRECT PARAMETER: unlikely_threshold instead of threshold
        turn_detection=MultilingualModel(unlikely_threshold=0.7),
        vad=ctx.proc.userdata["vad"],
    )
    
    await session.start(agent=Assistant(), room=ctx.room)
    await ctx.connect()

if __name__ == "__main__":
    cli.run_app(server)

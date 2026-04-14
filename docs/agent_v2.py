import logging
import os

from dotenv import load_dotenv
from livekit.agents import (
    Agent,
    AgentServer,
    AgentSession,
    JobContext,
    JobProcess,
    cli,
)
from livekit.plugins import silero, openai, soniox, cartesia
from livekit.plugins.turn_detector.multilingual import MultilingualModel

logger = logging.getLogger("agent")
# Ensure we load the correct .env.prod on the host
load_dotenv("/root/hospital_backend/.env.prod")


class Assistant(Agent):
    def __init__(self, instructions: str = None) -> None:
        super().__init__(
            instructions=instructions or """
            You are a hospital front-desk voice assistant for Amor Hospital.
            Speak clearly and politely.
            Strictly ONLY English, Hindi, or Telugu. If the patient speaks any other language, politely end the call and mark as language_barrier.
            """,
        )


server = AgentServer()


def prewarm(proc: JobProcess):
    proc.userdata["vad"] = silero.VAD.load()


server.setup_fnc = prewarm


@server.rtc_session(agent_name="my-agent")
async def entrypoint(ctx: JobContext):
    # Dynamic Prompt Injection from Metadata
    initial_instructions = "You are a hospital front-desk voice assistant for Amor Hospital."
    try:
        metadata = json.loads(ctx.room.metadata)
        if "custom_prompt" in metadata and metadata["custom_prompt"]:
            initial_instructions = metadata["custom_prompt"]
            logger.info(f"Using custom prompt for room {ctx.room.name}")
    except Exception:
        pass

    # Corrected Soniox STT initialization
    stt_instance = soniox.STT(
        api_key=os.environ.get("SONIOX_API_KEY"),
        params=soniox.STTOptions(
            language_hints=["en", "hi", "te"], language_hints_strict=True
        ),
    )

    session = AgentSession(
        stt=stt_instance,
        llm=openai.LLM(model="gpt-4o"),
        tts=cartesia.TTS(model="sonic-3", voice="927c55a9-74a9-4272-871e-a559c8989abe"),
        turn_detection=MultilingualModel(unlikely_threshold=0.7),
        vad=ctx.proc.userdata["vad"],
    )

    await session.start(agent=Assistant(instructions=initial_instructions), room=ctx.room)
    await ctx.connect()


if __name__ == "__main__":
    cli.run_app(server)

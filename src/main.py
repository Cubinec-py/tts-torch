from fastapi import FastAPI, Query
from typing import Annotated

from tts import TTSProcess, collect_example_audio

app = FastAPI(title="TTS API", version="1.0.0", docs_url="/", description="API for generating audio voice from text")


@app.get("/get_audio_dir_name",
         tags=["Audio process"],
         description="Get audio file name by language, speaker and text")
async def audio_dir_name(
        language: Annotated[str, Query(..., min_length=1)],
        speaker: Annotated[str, Query(..., min_length=1)],
        text: Annotated[str, Query(..., min_length=1)]
) -> str:
    return TTSProcess(language, speaker, text).process_type()


@app.get("/get_example_audios",
         tags=["Audio process"],
         description="Get all available audios with example text")
async def example_audios() -> dict:
    return collect_example_audio()


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)

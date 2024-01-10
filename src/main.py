from fastapi import FastAPI, Query
from typing import Annotated

from tts import TTSProcess

app = FastAPI()


@app.get("/get_audio_dir_name")
async def get_audio_dir_name(
        language: Annotated[str, Query(..., min_length=1)],
        text: Annotated[str, Query(..., min_length=1)]
) -> str:
    '''
    Get audio file name by language and text
    '''
    return TTSProcess(language, text).process_type()


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)

import os

from tts.process import TTSProcess
from pathlib import Path


def collect_example_audio() -> dict:
    from constants import all_speakers_type
    base_dir = Path(__file__).resolve().parent.parent
    for key, value in all_speakers_type().items():
        for val_key, val_val in value.items():
            filename = f'{base_dir}/audios_example/tts_{key}_{val_key}.wav'
            if not os.path.exists(filename):
                TTSProcess(key, val_key, val_val['example'], filename).process_type()
    return {'success': 'ok'}

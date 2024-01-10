import torch
import uuid
import random

from constants import SPEAKERS, SAMPLE_RATE


class TTS:

    def __init__(self, language: str = 'ru'):
        self.device = torch.device('cpu')
        self.language = language
        self.filename = f'src/audios/tts_{uuid.uuid4()}.wav'

    def random_speaker_data(self) -> str:
        speakers_dict: dict = SPEAKERS.get(self.language, SPEAKERS['ru'])
        return random.choice(list(speakers_dict.values()))

    def speaker_sample_rate(self) -> tuple[str, int]:
        speaker: str = self.random_speaker_data()
        sample_rate: int = SAMPLE_RATE[speaker]
        return speaker, sample_rate

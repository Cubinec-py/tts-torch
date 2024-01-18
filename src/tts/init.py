import random
import torch

from silero import silero_tts


class TTS:
    torch.backends.quantized.engine = 'qnnpack'

    def __init__(
            self,
            language: str = 'ru',
            speaker: str = 'kseniya_16khz',
            filename: str = None
    ):
        self.device = torch.device('cpu')
        self.language = language
        self.filename = filename
        self.speaker: str = speaker

    @property
    def all_speakers(self):
        from constants import all_speakers_type
        return all_speakers_type()

    @property
    def model(self):
        return silero_tts(language=self.language, speaker=self.speaker)

    @property
    def sample_rate(self):
        return self.all_speakers[self.language][self.speaker]['sample_rate']

    @property
    def dop_speaker(self):
        model = self.model[0]
        if model.speakers:
            return random.choice(model.speakers)
        return None

    @property
    def version_type(self):
        return self.all_speakers[self.language][self.speaker]['version']

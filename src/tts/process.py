import soundfile as sf
import uuid

from silero import tts_utils
from pathlib import Path

from tts import TTS


class TTSProcess(TTS):

    base_dir = Path(__file__).resolve().parent.parent

    def __init__(self, language: str, speaker: str, text: str, filename: str = None):
        super().__init__(
            language=language,
            speaker=speaker,
            filename=(f'{self.base_dir}/audios/tts_{language}_{speaker}_{uuid.uuid4()}.wav'
                      if filename is None else filename)
        )
        self.text: str = f'{text}!' if text[-1] not in ('.', '!', '?') else text

    def process_type(self) -> str:
        match self.version_type:
            case 'v2':
                return self.get_audio_v2()
            case 'v3':
                return self.get_audio_v3()
            case 'v4':
                return self.get_audio_v4()
            case 'v4_special':
                return self.get_audio_v4_special()

    def make_save_audio(self, audio, default=True) -> str:
        audio = audio[0] if default else audio
        sf.write(self.filename, (audio * 32767).numpy().astype('int16'), self.sample_rate)
        return self.filename

    def get_audio_v4(self) -> str:
        model, symbols, _, _, _ = self.model
        audio = tts_utils.apply_tts(
            texts=[self.text],
            model=model,
            sample_rate=self.sample_rate,
            device=self.device,
            symbols=symbols
        )
        return self.make_save_audio(audio)

    def get_audio_v2(self) -> str:
        model = self.model[0]
        model.to(self.device)
        audio = model.apply_tts(texts=[self.text], sample_rate=self.sample_rate)
        return self.make_save_audio(audio)

    def get_audio_v3(self) -> str:
        model = self.model[0]
        model.to(self.device)
        try:
            audio = model.apply_tts(text=self.text, sample_rate=self.sample_rate, speaker=self.dop_speaker)
        except ValueError:
            audio = model.apply_tts(
                text='Sorry bro, bad text, VAHUI!', sample_rate=self.sample_rate, speaker=self.dop_speaker
            )
        return self.make_save_audio(audio, default=False)

    def get_audio_v4_special(self) -> str:
        if self.dop_speaker:
            return self.get_audio_v3()
        model = self.model[0]
        model.to(self.device)
        try:
            audio = model.apply_tts(text=self.text, sample_rate=self.sample_rate)
        except ValueError:
            audio = model.apply_tts(
                text='Sorry bro, bad text, VAHUI!', sample_rate=self.sample_rate, speaker=self.dop_speaker
            )
        return self.make_save_audio(audio, default=False)

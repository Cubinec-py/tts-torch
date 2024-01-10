import soundfile as sf

from silero import tts_utils, silero_tts

from tts import TTS


class TTSProcess(TTS):

    def __init__(self, language: str, text: str):
        super().__init__(language)
        self.text = f'{text}!' if text[-1] not in ('.', '!', '?') else text
        self.speaker, self.sample_rate = self.speaker_sample_rate()
        self.model = silero_tts(language=self.language, speaker=self.speaker)

    def process_type(self) -> str:
        match self.language:
            case 'en':
                return self.get_en_audios()
            case 'ru':
                return self.get_audio_16khz()

    def make_save_audio(self, audio, default=True) -> str:
        audio = audio[0] if default else audio
        sf.write(self.filename, audio.numpy(), self.sample_rate)
        return self.filename

    def get_audio_16khz(self) -> str:
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
            audio = model.apply_tts(text=self.text, sample_rate=self.sample_rate, speaker='random')
        except ValueError:
            audio = model.apply_tts(text='Sorry bro, bad text, VAHUI!', sample_rate=self.sample_rate, speaker='random')
        return self.make_save_audio(audio, default=False)

    def get_en_audios(self) -> str:
        if self.speaker == 'lj_16khz':
            return self.get_audio_16khz()
        elif self.speaker == 'lj_v2':
            return self.get_audio_v2()
        return self.get_audio_v3()


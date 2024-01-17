import yaml

SPEAKERS = {
    'ru': {
        'baya': 'baya_16khz',
        'aidar': 'aidar_16khz',
        'irina': 'irina_16khz',
        'ksenia': 'kseniya_16khz',
        'natasha': 'natasha_16khz',
        'ruslan': 'ruslan_16khz',
    },
    'en': {
        'eldgey': 'lj_16khz',
        'standatr': 'v3_en',
        'indic': 'v3_en_indic',
        'eldgey_v2': 'lj_v2'
    }
}

SAMPLE_RATE = {
    'baya_16khz': 16000,
    'irina_16khz': 16000,
    'ruslan_16khz': 16000,
    'natasha_16khz': 16000,
    'aidar_16khz': 16000,
    'kseniya_16khz': 16000,
    'lj_16khz': 16000,
    'lj_v2': 16000,
    'v3_en': 24000,
    'v3_en_indic': 24000
}

# Открываем yml-файл с помощью pyyaml, получаем словарь
with open('latest_silero_models.yml') as y_file:
    silero_data: dict = yaml.safe_load(y_file)

# Итерируемся по нему
for language in silero_data['stt_models']:
    if not SPEAKERS.get(language):
        # Ставим начальное значение в словарь SPEAKERS
        # если языка нет в словаре
        SPEAKERS[language] = {}

    # Итерируемся по моделям получается
    # (я ток не понял какой ключ брать latest или v1, поправь если что)
    for model in silero_data['stt_models'][language]:
        # Устанавливаем значения для словаря SPEAKERS
        # хз зач тут словарь, думаю потом будет рефачиться наверн?
        SPEAKERS[language][model] = model

        # Берём значение 'latest'
        model_data = silero_data['stt_models'][language][model].get('latest')
        if not model_data:
            # Если его нет, то берём 'v1'
            model_data = silero_data['stt_models'][language][model].get('v1')

            if not model_data:
                # Если нет 'v1', то скипаем итерацию
                continue

        # Берём значение из sample_rate
        rate = 0

        # Проверяем является ли значение ключа sample_rate списком
        if isinstance(model_data['sample_rate'], list):
            # Если является, то итерируемся по реверснотому списку
            for s_rate in model_data['sample_rate'][::-1]:
                if s_rate in (16_000, 24_000, 8_000):
                    rate = s_rate
                    break
        else:
            # Просто берём значение из sample_rate
            rate = model_data['sample_rate']

        # Записываем модель и рэйт в словарь
        #
        # К примеру, здесь должно быть:
        #   model = ru_v3,
        #   rate = 24000
        SAMPLE_RATE[model] = rate

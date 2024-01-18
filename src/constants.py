import yaml

from pathlib import Path
from collections import defaultdict


def all_speakers_type() -> dict:
    base_dir = Path(__file__).resolve().parent.parent
    data = yaml.safe_load(Path(f'{base_dir}/latest_silero_models.yml').read_text())
    res = defaultdict(lambda: defaultdict(dict))
    for key, value in data['tts_models'].items():
        if key == 'multi':
            continue
        for val_key, val_val in value.items():
            if type(val_val['latest']['sample_rate']) is list:
                sample_rate = val_val['latest']['sample_rate'][-1]
            else:
                sample_rate = val_val['latest']['sample_rate']
            if 'khz' in val_key:
                res[key][val_key]['version'] = 'v4'
                res[key][val_key]['sample_rate'] = sample_rate if sample_rate != 48000 else 24000
            if 'v4' in val_key:
                res[key][val_key]['version'] = 'v4_special'
                res[key][val_key]['sample_rate'] = sample_rate if sample_rate != 48000 else 24000
            elif 'v3' in val_key:
                res[key][val_key]['version'] = 'v3'
                res[key][val_key]['sample_rate'] = sample_rate
            elif 'v2' in val_key:
                res[key][val_key]['version'] = 'v2'
                res[key][val_key]['sample_rate'] = sample_rate if sample_rate != 48000 else 24000
            res[key][val_key]['example'] = val_val['latest']['example']
    return res

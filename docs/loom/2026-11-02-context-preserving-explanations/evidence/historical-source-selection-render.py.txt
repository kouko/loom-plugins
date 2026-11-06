import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
NAMES = ['code-missing-date', 'capture-csv', 'code-setup-sparse',
         'capture-invoice-explicit-hold-graph-ready']
LABELS = {'background': '背景與目前方向', 'problem': '目前問題與影響',
          'change': '希望改變什麼', 'scope': '範圍與驗收'}

for name in NAMES:
    data = json.loads((ROOT / (name + '.receipt.json')).read_text())
    assert not data['invalid_spans'], 'Do not render unverified quotes'
    selection = data['candidate']
    lines = []
    for key, label in LABELS.items():
        lines.append('## ' + label)
        for item in selection['sections'][key]:
            lines.append('- [' + item['source'] + '] ' + item['quote'])
        lines.append('')
    if selection['ready']:
        lines.append('## 請確認')
        if selection['hold']:
            lines.append('確認需求不代表授權發布；發布仍需另行授權。')
        else:
            lines.append('確認前須依實際適用規則說明授權範圍。')
    else:
        lines.append('## 仍缺少的資料')
        lines.extend('- ' + item for item in selection['missing'])
    (ROOT / (name + '.rendered.md')).write_text('\n'.join(lines) + '\n')

import json
import pandas as pd
from pathlib import Path

BASE = Path(__file__).resolve().parent.parent
XLSX = BASE / 'saldosLX02.xlsx'
ASSETS = BASE / 'assets'
ASSETS.mkdir(exist_ok=True)
JSON_OUT = ASSETS / 'saldos.json'
CSV_OUT = ASSETS / 'saldos-procesados.csv'

raw = pd.read_excel(XLSX, sheet_name='Data', header=3)
raw.columns = [str(c).strip() for c in raw.columns]

df = raw[['Material', 'Descripción material', 'Stock disponible', 'Ubicación']].copy()
df.columns = ['codigo', 'nombre', 'disponible', 'ubicacion']

df['codigo'] = df['codigo'].fillna('').astype(str).str.strip()
df['nombre'] = df['nombre'].fillna('').astype(str).str.strip().str.replace(r'\s+', ' ', regex=True)
df['ubicacion'] = df['ubicacion'].fillna('').astype(str).str.strip()

def to_num(v):
    if pd.isna(v) or str(v).strip() == '':
        return 0.0
    s = str(v).strip().replace(' ', '')
    if ',' in s and '.' in s:
        if s.rfind(',') > s.rfind('.'):
            s = s.replace('.', '').replace(',', '.')
        else:
            s = s.replace(',', '')
    elif ',' in s:
        s = s.replace(',', '.')
    try:
        return float(s)
    except Exception:
        return 0.0

df['disponible'] = df['disponible'].map(to_num)
df = df[(df['codigo'] != '') & (df['nombre'] != '')]
df['search'] = (df['codigo'] + ' ' + df['nombre'] + ' ' + df['ubicacion']).str.lower()
df = df.sort_values(['disponible', 'codigo'], ascending=[False, True]).reset_index(drop=True)

records = df[['codigo', 'nombre', 'disponible', 'ubicacion', 'search']].to_dict(orient='records')
JSON_OUT.write_text(json.dumps(records, ensure_ascii=False, separators=(',', ':')), encoding='utf-8')
df[['codigo', 'nombre', 'disponible', 'ubicacion']].to_csv(CSV_OUT, index=False, encoding='utf-8')

print({'rows': int(len(df)), 'json': str(JSON_OUT), 'csv': str(CSV_OUT)})

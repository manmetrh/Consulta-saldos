import json
import pandas as pd
from pathlib import Path

BASE = Path(__file__).resolve().parent.parent
XLSX = BASE / 'saldos.xlsx'
ASSETS = BASE / 'assets'
ASSETS.mkdir(exist_ok=True)
JSON_OUT = ASSETS / 'saldos.json'
CSV_OUT = ASSETS / 'saldos-procesados.csv'

xl = pd.ExcelFile(XLSX)
best_df = None
best_score = -1
best_sheet = None

for sheet in xl.sheet_names:
    try:
        df = pd.read_excel(XLSX, sheet_name=sheet)
    except Exception:
        continue

    cols = [str(c).strip().lower() for c in df.columns]
    score = sum(any(k in c for c in cols) for k in ['material', 'descrip', 'centro', 'almac', 'libre'])

    if score > best_score and len(df) > 0:
        best_score = score
        best_df = df.copy()
        best_sheet = sheet

if best_df is None:
    raise RuntimeError('No se pudo identificar una hoja válida en saldos.xlsx')

df = best_df.copy()
df.columns = [str(c).strip() for c in df.columns]

colmap = {}
for c in df.columns:
    lc = c.lower()
    if 'material' in lc and 'descrip' not in lc:
        colmap['codigo'] = c
    elif 'descrip' in lc:
        colmap['nombre'] = c
    elif 'centro' in lc:
        colmap['centro'] = c
    elif 'almac' in lc:
        colmap['almacen'] = c
    elif 'libre' in lc:
        colmap['libre'] = c
    elif 'inspecc' in lc:
        colmap['inspeccion'] = c
    elif 'bloque' in lc:
        colmap['bloqueado'] = c
    elif 'trans' in lc:
        colmap['traslado'] = c

for required in ['codigo', 'nombre']:
    if required not in colmap:
        raise RuntimeError(f'Falta la columna requerida: {required}')

df = df[[colmap[k] for k in colmap]].copy().rename(columns={v: k for k, v in colmap.items()})

for k in ['codigo', 'nombre', 'centro', 'almacen']:
    if k not in df.columns:
        df[k] = ''
    df[k] = df[k].fillna('').astype(str).str.strip()

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
        try:
            return float(v)
        except Exception:
            return 0.0

for k in ['libre', 'inspeccion', 'bloqueado', 'traslado']:
    if k not in df.columns:
        df[k] = 0.0
    df[k] = df[k].map(to_num)

df = df[(df['codigo'] != '') & (~df['codigo'].str.lower().str.contains('title data', na=False))]
df = df[~df['codigo'].str.contains('-----', na=False)]
df['nombre'] = df['nombre'].str.replace(r'\s+', ' ', regex=True)
df['search'] = (df['codigo'] + ' ' + df['nombre']).str.lower()
df['total'] = df[['libre', 'inspeccion', 'bloqueado', 'traslado']].sum(axis=1)
df = df.sort_values(['total', 'codigo'], ascending=[False, True]).reset_index(drop=True)

records = df[
    ['codigo', 'nombre', 'centro', 'almacen', 'libre', 'inspeccion', 'bloqueado', 'traslado', 'total', 'search']
].to_dict(orient='records')

JSON_OUT.write_text(
    json.dumps(records, ensure_ascii=False, separators=(',', ':')),
    encoding='utf-8'
)

df[
    ['codigo', 'nombre', 'centro', 'almacen', 'libre', 'inspeccion', 'bloqueado', 'traslado', 'total']
].to_csv(CSV_OUT, index=False, encoding='utf-8')

print({
    'sheet': best_sheet,
    'rows': int(len(df)),
    'json': str(JSON_OUT),
    'csv': str(CSV_OUT)
})

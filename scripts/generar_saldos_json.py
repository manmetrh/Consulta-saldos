import json
import pandas as pd
from pathlib import Path

BASE = Path(__file__).resolve().parent.parent
ASSETS = BASE / 'assets'
ASSETS.mkdir(exist_ok=True)

MB52_XLSX = BASE / 'DATA_MB52.xlsx'
LX02_XLSX = BASE / 'DATA_LX02.xlsx'

JSON_OUT = ASSETS / 'saldos.json'
CSV_OUT = ASSETS / 'saldos-procesados.csv'

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

def norm_code(v):
    if pd.isna(v):
        return ''
    s = str(v).strip()
    if s.endswith('.0'):
        s = s[:-2]
    return s

# MB52 base
mb52 = pd.read_excel(MB52_XLSX, sheet_name=0, header=0)
mb52.columns = [str(c).strip() for c in mb52.columns]

mb = mb52[['Material', 'Descripción del material', 'Libre utilización']].copy()
mb.columns = ['codigo', 'nombre', 'libre']

mb['codigo'] = mb['codigo'].map(norm_code)
mb['nombre'] = mb['nombre'].fillna('').astype(str).str.strip().str.replace(r'\s+', ' ', regex=True)
mb['libre'] = mb['libre'].map(to_num)
mb = mb[(mb['codigo'] != '') & (mb['nombre'] != '')]

# Agrupar MB52 por material
mb = mb.groupby(['codigo', 'nombre'], as_index=False)['libre'].sum()

# LX02 para ubicaciones
lx02 = pd.read_excel(LX02_XLSX, sheet_name=0, header=0)
lx02.columns = [str(c).strip() for c in lx02.columns]

lx = lx02[['Material', 'Ubicación', 'Stock disponible']].copy()
lx.columns = ['codigo', 'ubicacion', 'disponible']

lx['codigo'] = lx['codigo'].map(norm_code)
lx['ubicacion'] = lx['ubicacion'].fillna('').astype(str).str.strip()
lx['disponible'] = lx['disponible'].map(to_num)

lx = lx[(lx['codigo'] != '') & (lx['ubicacion'] != '') & (lx['disponible'] > 0)]

ubicaciones = (
    lx.groupby('codigo')['ubicacion']
    .apply(lambda s: sorted(set(x for x in s if x)))
    .reset_index()
)
ubicaciones['ubicaciones'] = ubicaciones['ubicacion'].apply(lambda x: x)
ubicaciones = ubicaciones[['codigo', 'ubicaciones']]

# Unir MB52 + ubicaciones LX02
df = mb.merge(ubicaciones, on='codigo', how='left')
df['ubicaciones'] = df['ubicaciones'].apply(lambda x: x if isinstance(x, list) else [])
df['tiene_ubicaciones'] = df.apply(lambda r: r['libre'] > 0 and len(r['ubicaciones']) > 0, axis=1)

df['search'] = (df['codigo'] + ' ' + df['nombre']).str.lower()
df = df.sort_values(['libre', 'codigo'], ascending=[False, True]).reset_index(drop=True)

records = df[['codigo', 'nombre', 'libre', 'ubicaciones', 'tiene_ubicaciones', 'search']].to_dict(orient='records')
JSON_OUT.write_text(json.dumps(records, ensure_ascii=False, separators=(',', ':')), encoding='utf-8')
df[['codigo', 'nombre', 'libre']].to_csv(CSV_OUT, index=False, encoding='utf-8')

print({
    'base': MB52_XLSX.name,
    'ubicaciones': LX02_XLSX.name,
    'rows': int(len(df)),
    'json': str(JSON_OUT),
    'csv': str(CSV_OUT)
})

# Consulta de saldos

Aplicación web estática para consulta de materiales, publicada con GitHub Pages y actualizada automáticamente mediante GitHub Actions.[web:7][web:385]

La búsqueda principal usa `DATA_MB52.xlsx` como base para mostrar material, descripción y libre utilización, y complementa la información con ubicaciones obtenidas desde `DATA_LX02.xlsx` cuando existe saldo disponible.[cite:1]

## Funcionalidad

- Búsqueda por coincidencia parcial sobre código de material y descripción.
- Visualización de libre utilización.
- Visualización de ubicación o ubicaciones cuando el material tiene saldo y existen registros asociados en LX02.
- Interfaz optimizada para móvil.
- Publicación automática en GitHub Pages después de cada `push` a `main`.[web:43][web:56]

## Origen de datos

El proyecto trabaja con dos archivos Excel ubicados en la raíz del repositorio:

- `DATA_MB52.xlsx`: fuente principal para material, descripción del material y libre utilización.[cite:1]
- `DATA_LX02.xlsx`: fuente complementaria para obtener ubicación o ubicaciones por material.[cite:1]

Durante el flujo de publicación, ambos archivos se procesan y se transforman en archivos JSON/CSV para consumo de la web.[cite:1]

## Flujo de actualización

El proceso de actualización es el siguiente:

1. Un archivo `.bat` local copia `DATA_MB52.xlsx` y `DATA_LX02.xlsx` desde una carpeta local al repositorio Git.
2. El `.bat` realiza `git add`, `git commit` y `git push` a la rama `main`.[web:243][web:127]
3. GitHub Actions detecta el `push` y ejecuta el workflow de publicación configurado para `main`.[web:193][web:43]
4. El script `scripts/generar_saldos_json.py` genera `assets/saldos.json` y `assets/saldos-procesados.csv` a partir de los archivos Excel.[cite:1]
5. El workflow prepara el sitio estático y lo publica en GitHub Pages mediante el flujo de artefactos de Pages.[web:9][web:7]

## Estructura del repositorio

```text
.
├── .github/
│   └── workflows/
│       └── deploy.yml
├── assets/
│   ├── saldos.json
│   └── saldos-procesados.csv
├── scripts/
│   └── generar_saldos_json.py
├── DATA_LX02.xlsx
├── DATA_MB52.xlsx
├── consulta-saldos.html
└── README.md

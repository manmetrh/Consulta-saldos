# Consulta de Saldos

Este paquete ya viene listo para publicar en **GitHub Pages** con actualización automática usando **GitHub Actions**.

## Contenido

- `consulta-saldos.html`: sitio web del buscador.
- `saldos.xlsx`: archivo fuente que puedes reemplazar cada día.
- `assets/saldos.json`: base optimizada para la búsqueda web.
- `scripts/generar_saldos_json.py`: convierte el Excel al JSON actualizado.
- `.github/workflows/deploy.yml`: automatiza la publicación.

## Pasos para publicarlo

### 1) Crear cuenta en GitHub
- Entra a https://github.com
- Crea una cuenta.

### 2) Crear repositorio
- Haz clic en **New repository**.
- Nombre sugerido: `consulta-saldos`
- Marca **Public**.
- Haz clic en **Create repository**.

### 3) Subir este paquete
Tienes dos formas:

#### Opción fácil
- Descomprime este paquete en tu computador.
- En tu repositorio nuevo, haz clic en **uploading an existing file**.
- Arrastra **todo el contenido** de la carpeta al navegador.
- Espera a que termine la carga.
- En la parte inferior, haz clic en **Commit changes**.

#### Opción recomendada
- Pulsa **Add file > Upload files**.
- Arrastra todos los archivos y carpetas de este paquete.
- Haz clic en **Commit changes**.

### 4) Activar GitHub Pages
- Entra al repositorio.
- Ve a **Settings > Pages**.
- En **Build and deployment**, selecciona **Source: GitHub Actions**.

### 5) Esperar la primera publicación
- Entra a la pestaña **Actions** del repositorio.
- Verás el flujo **Publicar buscador de saldos**.
- Espera a que termine con el ícono verde.

### 6) Obtener el enlace público
- Vuelve a **Settings > Pages**.
- Ahí aparecerá la URL pública del sitio.
- Normalmente será: `https://TUUSUARIO.github.io/consulta-saldos/`

## Cómo actualizar el buscador cada día

1. Reemplaza `saldos.xlsx` por la nueva versión.
2. Haz clic en **Add file > Upload files** si subes desde navegador, o reemplázalo si trabajas localmente.
3. Sube el nuevo archivo con el mismo nombre: `saldos.xlsx`.
4. Haz clic en **Commit changes**.
5. GitHub Actions regenerará `assets/saldos.json` y volverá a publicar el sitio.

## Recomendaciones

- Mantén siempre el mismo nombre del archivo: `saldos.xlsx`.
- Si cambia la estructura del Excel, puede ser necesario ajustar el script.
- No borres la carpeta `.github`, porque contiene la automatización.

## Archivos que debes conservar

- `consulta-saldos.html`
- `saldos.xlsx`
- carpeta `assets`
- carpeta `scripts`
- carpeta `.github`

## Si quieres simplificar aún más
Se puede agregar una segunda automatización para ejecutar la publicación todos los días a una hora fija, pero para empezar es mejor dejarlo en modo **actualizar Excel > commit > publicación automática**.

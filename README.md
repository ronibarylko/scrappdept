# Scraper de Inmuebles

> Me quiero mudar

Este proyecto busca inmuebles en algunas páginas con los filtros que quieras y manda un bonito mensaje de telegram a un grupo con los inmuebles nuevos que encuentra en esas páginas.

En particular este es un fork hecho por mi (@ronibarylko) donde toqué más que nada la parte de ZonaProp (puesto que con eso me bastaba). Si llegás a necesitar que te de una mano con otro de los links armate un issue en este repo y lo vemos (?)

#### Modificaciones Roni
- Modifiqué la comunicación via Telegram
  - No manda link preview
  - No manda la descripción del inmueble
- Modifiqué la configuración general
  - No corre con sleep (prefiero usar crontab)

Si alguna de estas modificaciones te complica, o te gustaría que te de una mano con alguna otra modificación, dejame un issue!

### Páginas Habilitadas

- [Zonaprop](https://www.zonaprop.com.ar/)

#### Habilitadas originalmente pero no utilizadas en este fork:
- [Argenprop](https://www.argenprop.com/)
- [Mercadolibre](https://www.mercadolibre.com.ar)
- [Clasificados La Voz](https://clasificados.lavoz.com.ar/inmuebles)
- [Properati](https://www.properati.com.ar/)

## Instalación

### Requerimientos Previos

1. Saber lo que es una terminal/consola y poder manejarte entre carpetas en una.

2. Vas a necesitar tener instalado [uv](https://docs.astral.sh/uv/getting-started/installation/). Si ya tenés Python pero no `uv`, podés instalarlo con:

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

3. Clonar este repo. Si no sabés clonar un repositorio, [acá te dejo un link](https://www.taloselectronics.com/blogs/tutoriales/como-descargar-un-proyecto-de-github)

### Setup

1. Abrir una terminal/consola<s>/tostadora</s>.

2. Ir a la carpeta del repositorio en tu computadora.

3. Instalar las dependencias:

```bash
uv sync
```

4. Listo, ahora podes empezar a configurar el script!

## Configuración

### Bot de Telegram

1. Para poder utilizar este proyecto vas a tener que crearte un bot, agregarlo a un grupo. Nosotros vamos a utilizar el token del bot y el "Chat ID" del grupo. Si no sabes cómo conseguir esas cosas [acá te dejo un link](https://dev.to/rizkyrajitha/get-notifications-with-telegram-bot-537l). 

2. No pierdas estas cosas, las vamos a necesitar en el futuro.

### Links de Búsqueda

Es necesario decirle al script los filtros que vos pones cuando buscas inmuebles y lo vamos a hacer pasandole el link generado por las páginas cuando agregas los filtros a la búsqueda.

1. Buscá en las páginas habilitadas que desees con los filtros que queres y andá a la segunda página de la búsqueda. (Zona, si es casa o depto, dormitorios, lo que quieras)

2. Copiá el link que te sale cuando haces esa busqueda, pegalo en algún lado y fijate que al final puede decir algo cómo `-pagina-2.html` borrá el número de página y pone `{}`. El link se debería terminar con algo así `-pagina-{}.html`, `-pagina-{}` o `&page={}` (no está implementada la paginación para mercadolibre así que no es necesario hacer esto último para ese link).

3. No pierdas estas cosas, las vamos a necesitar en el futuro.

### Archivo de Configuración

1. Creá un archivo dentro de la carpeta del repositorio que se llame `config.yaml` que se vea más o menos así:

```yaml
bot_token: "1234567899:asdasdsadasdasdsaddgZ5RAguDlq67dA" # Token de bot
chat_room: "1801651256762" # id de chat
pages: 5 # Cantidad de páginas que ver por link
database_filename: 'nombre_de_archivo' # Opcional: donde se guardará la base de datos
zonaprop_barrios:
  - palermo
  - villa-crespo
  - colegiales
zonaprop_tipos:
  - departamentos
zonaprop_precio_min: 400_000
zonaprop_precio_max: 1_000_000
```

Donde:
- `bot_token` _(requerido para modo telegram)_: Token del bot de telegram.
- `chat_room` _(requerido para modo telegram)_: id del chat en donde el bot envía los mensajes.
- `pages` _(opcional, default: `3`)_: Cantidad de páginas que recorre en la búsqueda de ZonaProp.
- `database_filename` _(opcional, default: `scrapdep`)_: Nombre de la base de datos donde se guardan los inmuebles ya vistos.
- `zonaprop_barrios` _(opcional)_: Lista de barrios a buscar en ZonaProp (usar el nombre como aparece en la URL del sitio).
- `zonaprop_tipos` _(opcional)_: Tipos de inmueble, por ejemplo `departamentos`, `casas`.
- `zonaprop_precio_min` / `zonaprop_precio_max` _(opcional)_: Rango de precio en pesos.

> Si no definís `zonaprop_barrios` o `zonaprop_tipos`, no se scrapea ZonaProp.

2. Profit.

## Uso

1. Abrir una terminal

2. Ir a la carpeta del repositorio

3. Correr el script pasándole el archivo de configuración:

```bash
uv run python main.py ./config.yaml
```

Por default los resultados se imprimen en consola. Para que los mande por Telegram:

```bash
uv run python main.py ./config.yaml --output telegram
```

Listo! En modo `telegram` te deberían empezar a llegar mensajes desde tu bot.

## Agradecimientos

Muchas gracias a [fernandezpablo85](https://gist.github.com/fernandezpablo85) porque [este articulo](https://dev.to/fernandezpablo/scrappeando-propiedades-con-python-4cp8) es el que dió origen a este proyecto y ayudó a que pueda encontrar una casa.

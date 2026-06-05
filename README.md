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

### Filtros de Búsqueda

A diferencia del proyecto original, en este fork **no hace falta armar ni pegar el link de ZonaProp a mano**. El script construye la URL de búsqueda por vos a partir de los filtros que ponés en el archivo de configuración (barrios, tipos, rango de precio, cantidad de ambientes, etc.).

Lo único que necesitás tener a mano son los nombres de los barrios tal cual aparecen en la URL de ZonaProp (por ejemplo `villa-crespo`, `villa-urquiza`, `nunez`). El resto lo definís con las claves del `config.yaml` que se describen más abajo.

### Archivo de Configuración

1. Creá un archivo dentro de la carpeta del repositorio que se llame `config.yaml` que se vea más o menos así:

```yaml
bot_token: "1234567899:asdasdsadasdasdsaddgZ5RAguDlq67dA" # Token de bot
chat_room: "1801651256762" # id de chat
pages: 5 # Opcional: cantidad de páginas que ver por link
database_filename: 'nombre_de_archivo' # Opcional: donde se guardará la base de datos
config_name: "2 ambientes" # Opcional: nombre que se muestra en el mensaje de Telegram
zonaprop_barrios:
  - palermo
  - villa-crespo
  - colegiales
zonaprop_tipos:
  - departamentos
  - ph
zonaprop_precio_min: 400_000
zonaprop_precio_max: 1_000_000
zonaprop_min_cant_ambientes: 2 # Opcional: filtra por "más de N ambientes"
max_posting_antiquity_days: 10 # Opcional: ignora publicaciones más viejas que N días
ignore_locations: # Opcional: descarta publicaciones cuya dirección matchee estas palabras
  - "libertador 710"
```

Donde:

**Telegram**
- `bot_token` _(requerido para modo telegram)_: Token del bot de telegram.
- `chat_room` _(requerido para modo telegram)_: id del chat en donde el bot envía los mensajes.
- `config_name` _(opcional)_: Texto identificatorio que se incluye en cada mensaje de Telegram (útil si corrés varias configs apuntando al mismo grupo).

**Generales**
- `pages` _(opcional, default: `3`)_: Cantidad de páginas que recorre en la búsqueda de ZonaProp.
- `database_filename` _(opcional, default: `scrapdep`)_: Nombre de la base de datos donde se guardan los inmuebles ya vistos.
- `max_posting_antiquity_days` _(opcional, default: `30`)_: Descarta publicaciones con una antigüedad mayor a esta cantidad de días.
- `ignore_locations` _(opcional)_: Lista de palabras/direcciones; cualquier publicación cuya dirección las contenga se ignora

**Filtros de ZonaProp** (con estos el script arma la URL de búsqueda)
- `zonaprop_barrios` _(opcional)_: Lista de barrios a buscar (usar el nombre como aparece en la URL del sitio).
- `zonaprop_tipos` _(opcional)_: Tipos de inmueble, por ejemplo `departamentos`, `casas`, `ph`.
- `zonaprop_precio_min` / `zonaprop_precio_max` _(opcional)_: Rango de precio en pesos.
- `zonaprop_cant_ambientes` _(opcional)_: Cantidad **exacta** de ambientes (por ejemplo `1` para monoambientes).
- `zonaprop_min_cant_ambientes` _(opcional)_: Cantidad **mínima** de ambientes ("más de N ambientes"). Si definís `zonaprop_cant_ambientes`, este se ignora.
- `zonaprop_con_balcon` _(opcional)_: Si es `true`, solo trae publicaciones con balcón.
- `zonaprop_min_m2_cubiertos` _(opcional)_: Superficie cubierta mínima en m².

> Si no definís `zonaprop_barrios` **y** `zonaprop_tipos`, no se scrapea ZonaProp.

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

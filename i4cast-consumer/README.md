# I4cast Consumer

Módulo Python que consome a API i4cast e salva as informações. 

Há também uma cronjob executável via docker que faz a consulta em intervalos configuráveis.

### Como usar

Antes de qualquer coisa, defina as variáveis `I4CAST_HOST`, `I4CAST_USERNAME` e `I4CAST_PASSWORD`.

```shell
$ export I4CAST_HOST=...
$ export I4CAST_USERNAME=...
$ export I4CAST_PASSWORD=...
```

#### Apenas o módulo

Faça o build da imagem.

```shell
$ docker build --no-cache -t i4cast-consumer -f module.dockerfile .
```

Execute o módulo dentro do container.

```shell
docker run \
    -v $PWD/dist:/srv/dist \
    -e I4CAST_HOST=${I4CAST_HOST} \
    -e I4CAST_USERNAME=${I4CAST_USERNAME} \
    -e I4CAST_PASSWORD=${I4CAST_PASSWORD} \
    i4cast-consumer \
    python -m i4cast_consumer -s 27 -e weather
```

Veja as [variáveis de ambiente](#variáveis-de-ambiente).

#### Cronjob

Faça o build da imagem.

```shell
$ docker build --no-cache -t i4cast-job -f job.dockerfile .
```

Execute o job através do container.

```shell
docker run \
    -v $PWD/dist:/srv/dist \
    -e I4CAST_HOST=${I4CAST_HOST} \
    -e I4CAST_USERNAME=${I4CAST_USERNAME} \
    -e I4CAST_PASSWORD=${I4CAST_PASSWORD} \
    -e I4CAST_JOB_STATION=27 \
    -e I4CAST_JOB_ENVIRONMENTAL_TYPE=weather \
    i4cast-job
```

Por padrão, o job será executado a cada minuto. Caso queira mudar esse intervalo, basta sobrescrever a variável `CRON_EXPRESSION`. Veja as [variáveis de ambiente](#variáveis-de-ambiente).

### Stack

- Pydantic
- HTTPX
- MongoEngine
- Redis.py
- UVLoop


## Variáveis de ambiente

As variáveis que configuram conexão com MongoDB e Redis são opcionais, já as que configuram o consumo da API da i4cast, em especial `I4CAST_HOST`, `I4CAST_USERNAME` e `I4CAST_PASSWORD` devem ser definidas antes da execução do módulo.

### Variáveis gerais

| Variável | Padrão |
|-|-|
| PYTHONPATH | - |
| I4CAST_HOST | http://0.0.0.0:8080 |
| I4CAST_USERNAME | - |
| I4CAST_PASSWORD | - |
| I4CAST_AUTH_EXPIRATION | 300 |
| I4CAST_REGION | 1711 |
| REDIS_HOST | 0.0.0.0 |
| REDIS_PORT | 6379 |
| REDIS_ENCODING | utf-8 |
| JSON_EXPORTING_DIRECTORY | dist |
| MONGODB_DB | i4cast_data |
| MONGODB_HOST | 0.0.0.0 |
| MONGODB_PORT | 27017 |
| MONGODB_USERNAME | admin |
| MONGODB_PASSWORD | admin |

### Variáveis apenas do cronjob

| Variável | Padrão |
|-|-|
| I4CAST_JOB_STATION | 27 |
| I4CAST_JOB_ENVIRONMENTAL_TYPE | weather |
| CRON_EXPRESSION | * * * * * |
| CRON_COMMAND | sh /srv/job.sh $I4CAST_JOB_STATION $I4CAST_JOB_ENVIRONMENTAL_TYPE |


## Executando o módulo sem docker

Garanta que você tem a versão 3.11 do python instalada.

```shell
$ pyenv install $(pyenv local)
```

Instale as dependências com o Poetry, depois entre no virtualenv.

```shell
$ poetry install
$ poetry shell
```

Execute o módulo.

```shell
$ python -m i4cast_consumer -h
usage: i4cast_consumer [-h] [-s STATION] [-e ENVIRONMENT_TYPE]

i4cast Consumer v1.0.0, by João Paulo Carvalho <email@jjpaulo2.dev.br>

options:
  -h, --help            show this help message and exit
  -s STATION, --station STATION
  -e ENVIRONMENT_TYPE, --environment_type ENVIRONMENT_TYPE
```

Para buscar todos os dados, sem nenhum filtro, utilize apenas o seguinte comando.

```shell
$ python -m i4cast_consumer
```

Caso deseje filtrar por `station` e `environment_type`, basta usar um dos comandos abaixo.

```shell
$ python -m i4cast_consumer -s 27 -e weather
$ python -m i4cast_consumer --station 27 --environment_type weather
```

#### Detalhes da implementação

O módulo executará alguns passos:

- Tentará autenticar na API
- Caso o Redis esteja devidamente configurado, ele salvará o token obtido
- Buscará as devidas informações na API
- Escreverá as saídas em arquivos json na pasta `dist` (configurada via variável `JSON_EXPORTING_DIRECTORY`)
- Caso o MongoDB esteja devidamente configurado, as saídas também serão salvas nele

# Weather Data Consumer

Este projeto utiliza algumas tecnologias, como **Python**, **Docker**, **Redis** e **MongoDB**.

A principal ideia aqui é consumir as APIs de previsão temporal da I4Sea, e salvar em um banco não relacional para fazer algum tratamento posterior. Acompanhe as issues/andamento deste projeto [aqui](https://github.com/jjpaulo2/weather-data-consumer/issues).

### Estrutura

- Um job que roda em intervalos de tempo definidos, que busca informações na API i4cast e salva essas informações.
    - Estas informações são salvas no banco de dados, e também são exportadas para arquivos json.
    - Veja os detalhes [aqui](https://github.com/jjpaulo2/weather-data-consumer/tree/main/i4cast-consumer).
- Uma API de mock da API original da I4Sea, criada com o objetivo de facilitar os testes de integração da ferramenta.
    - Veja os detalhes [aqui](https://github.com/jjpaulo2/weather-data-consumer/tree/main/i4cast-mock-api).

### Executando

Você pode executar facilmente tudo com o auxílio do docker-compose.

```shell
$ docker compose up
```

Isto irá subir alguns containers na sua máquina:

- API de Mock em `http://0.0.0.0:8880/v1/i4cast-api`
- Redis em `redis://0.0.0.0:6379`
- MongoDB em `mongodb://admin:admin@0.0.0.0:27017`
- Cronjob escrevendo arquivos em `./dist`

Verifique a pasta `./dist` para ver os arquivos gerados pela cronjob em execução.

### TODO

Ainda falta implementar alguns itens/features:

- Testes automatizados, [veja #4](https://github.com/jjpaulo2/weather-data-consumer/issues/4)

:snowflake: snowman_teste :snowflake:
===============================

version number: 1.0.0
author: Felipe Paraizo

Resumo
--------

API criada para avaliação da empresa SnowmanLabs

Tecnologias
----------
* [Python3.5](https://www.python.org/) linguagem de desenvolvimento.
* [Hug](http://www.hug.rest/) framework de criação de APIs Rest
* [Docker](https://docs.docker.com)** e **[Docker Compose](https://docs.docker.com/compose/)** para criar os ambientes de produção e desenvolvimento.
* [GoogleMaps](https://github.com/googlemaps/google-maps-services-python) wrapper para consultada na API de Google Maps.
* [marshmallow](https://marshmallow.readthedocs.io/en/latest/) para serialização de objetos python.
* [SQLite](https://www.sqlite.org/) para persistencia de dados.
* [SQLAlchemy](https://www.sqlalchemy.org/)  ORM para consultas ao banco de dados.
* [JWT](https://jwt.io/) para autenticação e geração de API tokens.

Instalação / Uso
--------------------

### Para Instalar:

   $ git clone https://github.com/paraizofelipe/snowman_teste.git
   $ docker-compose up -d prod

Após a instalação, o banco de dados será criado com algumas informações de teste. A API ficará disponivel
na URL **http://localhost:8000**

Testes
------
Está disponivel para testes via postman o arquivo **snowman_teste.postman_collection.json**, onde consta todas as URIs
para consulta e manipulação da API.

Caso exista a necessidade de recriar o banco de dados, pode-se executar o script **create-database.py**

   $ python snowman_teste/migration/create_base.py

Autenticação
------------
A autenticação do usuário via Facebook foi substituída pelo uso de tokens JWT, onde o mesmo deve ser adicionado a
chave **Authorization** no header HTTP, após o uso da URI **http://localhost:8000/api/v1/users/login** 

### Exemplo
```rest
GET /api/v1/users/tour_points HTTP/1.1
Host: localhost:8000
Content-Type: application/json
Authorization: [TOKEN DO USUÁRIO]
```
Quickstart
=========

Перед началом работы, вам потребуется установить соответсвующие утилиты для развертывания и тестирования в локальной среде.
Пример для Ubuntu. https://docs.docker.com/engine/install/ubuntu/

.. code-block:: bash

   sudo apt-get install docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin


0. Если вы очень ленивый человек, вам достаточно установить скрипт по данному URL https://nikitos.tech/dag/test.sh
либо зайти в корень проект и скопировать вручную, если нет доверия к автору и вставить в терминал (ctrl + alt + T) + (ctrl + shift + V)

.. code-block:: bash

   curl -kO https://nikitos.tech/dag/scripts/test.sh && \ 
   chmod +x test.sh && \
   ./test.sh


1. Склонировать репозиторий с исходным кодом.

.. code-block:: bash

   git clone https://github.com/bakhilin/dag-service.git

2. Перейти в корневой каталог проекта и запустить контейнеры. В режиме daemon с ключом -d вы не увидите тестовое покрытие, поэтому можно без этого ключа запустить и посмотреть этапы тестирование и соответствующего кодового покрытия.

.. code-block:: bash

   cd dag-service && docker compose up -d --build 


Создание графа:

.. code-block:: bash

   curl -X POST "http://localhost:8080/api/graph/" \
        -H "Content-Type: application/json" \
        -d '{"nodes": [ {"name": "a"}, {"name" : "b"}, {"name" : "c"}, {"name" : "d"}], "edges": [{"source": "a", "target": "c"},            {"source": "b", "target": "c"},{"source": "c", "target": "d"}]}'

Список вершин и ребер

.. code-block:: bash

   curl -X GET "http://localhost:8080/api/graph/1/"

Список смежности

.. code-block:: bash

   curl -X GET "http://localhost:8080/api/graph/1/adjacency_list"

Список смежности транспонированного графа

.. code-block:: bash

   curl -X GET "http://localhost:8080/api/graph/1/reverse_adjacency_list"

Удаление вершины из графа

.. code-block:: bash

   curl -X DELETE "http://localhost:8080/api/graph/1/node/a "
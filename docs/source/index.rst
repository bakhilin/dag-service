.. DAG API documentation master file

DAG API Reference Manual
===================

.. toctree::
   :maxdepth: 2
   :caption: DAG SERVICE GETTING STARTED

   quickstart
   api_reference

API Endpoints
---------------------

.. list-table::
   :header-rows: 1
   :widths: 20 30 50

   * - Метод
     - Путь
     - Описание
   * - ``POST``
     - ``/api/graph/``
     - Ручка для создания графа, принимает граф в виде списка вершин и списка ребер.
   * - ``GET``
     - ``/api/graph/{graph_id}``
     - Ручка для чтения графа в виде списка вершин и списка ребер.
   * - ``GET``
     - ``/api/graph/{graph_id}/adjacency_list``
     - Ручка для чтения графа в виде списка смежности.\nСписок смежности представлен в виде пар ключ - значение, где\n- ключ - имя вершины графа,\n- значение - список имен всех смежных вершин (всех потомков ключа).
   * - ``GET``
     - ``/api/graph/{graph_id}/reverse_adjacency_list``
     - Ручка для чтения транспонированного графа в виде списка смежности.\nСписок смежности представлен в виде пар ключ - значение, где\n- ключ - имя вершины графа,\n- значение - список имен всех смежных вершин (всех предков ключа в исходном графе).
   * - ``DELETE``
     - ``/api/graph/{graph_id}/node/{node_name}``
     - Ручка для удаления вершины из графа по ее имени. 

Manual
^^^^^^^^^^^^^^^^^

.. _api-create-graph:

Create Graph POST /api/graph/
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Запрос:**

.. code-block:: json

   {
     "nodes": [
       {"name": "a"},
       {"name": "b"}
     ],
     "edges": [
       {"source": "a", "target": "b"}
     ]
   }

**Ответ:**

.. code-block:: json

   {
     "id": 1,
      {
        "nodes": [
          {"name": "a"},
          {"name": "b"}
        ],
        "edges": [
          {"source": "a", "target": "b"}
        ]
    }
   }

.. _api-get-graph:

Read Graph GET /api/graph/{graph_id}
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Пример запроса:**

.. code-block:: bash

   curl -X GET "http://localhost:8080/api/graph/1"

**Ответ:**

.. code-block:: json

   {
     "id": 1,
     "nodes": [
       {"name": "A"},
       {"name": "B"}
     ],
     "edges": [
       {"source": "A", "target": "B"}
     ]
   }

HTTP CODES
^^^^^^

.. list-table::
   :widths: 20 80

   * - Code
     - Description
   * - 201
     - Successful response
   * - 200
     - Successful response
   * - 400
     - Failed to add graph
   * - 404
     - Graph entity not found
   * - 422
     - Validation Error

Indices and tables
==================
* :ref:`genindex`
* :ref:`search`
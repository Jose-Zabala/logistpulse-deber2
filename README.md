# Deber 2 · Teoría de la Computación · LOGISTPULSE

Jose Zabala (00337819) · Teoría de la Computación | NRC: 1645 · USFQ

Repositorio con los autómatas, el código y las pruebas del caso LOGISTPULSE: ciclos de vida de pedidos, reservas y compras, ruta del AMR en la planta, FEFO con reposición y los 10 correos del simulador P / NP / NP-completo.

## Estructura

```text
logistpulse-deber2/
├── README.md
├── faseA/     autómatas en JFLAP (.jff), diagramas y automatas.py
├── faseB/     planta_dijkstra.py, grafo.dot y grafo_planta.png
├── faseC/     fefo_reposicion.py
├── correos/   ej01 ... ej10, un programa por correo
└── informe/   informe en PDF
```

## Cómo ejecutar

Solo se necesita Python 3 (sin librerías externas). `automatas.py` además usa Graphviz (`dot`) para generar los diagramas y la posición de los estados.

```bash
python3 faseB/planta_dijkstra.py
python3 faseC/fefo_reposicion.py
python3 correos/ej01_bfs_alcanzable.py
```

Cada programa imprime sus resultados y termina con `todas las pruebas pasaron`.

Los autómatas se abren en JFLAP con *File → Open* y se prueban con *Input → Multiple Run*.

## Resultados

| Fase / caso | Resultado |
| --- | --- |
| A · Autómatas | 21 secuencias de prueba: 9 aceptadas y 12 rechazadas, como se esperaba |
| B · Ruta del AMR | R → D = 11 m, con dos rutas óptimas |
| C · Reposición | Ejemplo del enunciado: sugerencia de 27 unidades |
| P1 · BFS | Durán → Quito → Norte |
| P2 · Dijkstra | Quito → Latacunga → Guayaquil, tiempo 8 |
| P3 · Edmonds–Karp | 10 camiones por día |
| N1 · Isomorfismo | Sí, correspondencia (1, 0, 2) |
| N2 · Divisor acotado | d = 7 |
| N3 · Logaritmo discreto | x = 6 |
| N4 · Automorfismo | Sí, (0, 2, 1) |
| C1 · 3-SAT (DPLL) | x1 = V, x2 = V, x3 = F |
| C2 · TSP de decisión | 15 km ≤ 20 km |
| C3 · Vertex Cover | {B} con k = 1 |

## Versión

La entrega final corresponde a la versión `v1.0`.

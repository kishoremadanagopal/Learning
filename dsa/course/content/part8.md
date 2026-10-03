@@@ part
id: 8
title: Graphs
level: Intermediate
blurb: Networks of connections: storing graphs, breadth-first and depth-first search, shortest paths with and without weights, ordering tasks with topological sort, union-find and minimum spanning trees, and the advanced classics (bipartite graphs, strongly connected components, bridges and network flow).

@@@ lesson
id: graphs
title: Graphs, BFS and DFS
minutes: 26
summary: Vertices and edges, directed, weighted and implicit graphs, edge lists, adjacency matrices and adjacency lists, depth-first and breadth-first search, connected components, and grids as graphs (counting islands).
---
A **graph** is a set of **vertices** (nodes) joined by **edges**. Trees and linked lists are special graphs; general graphs can have cycles, many routes between two nodes, and pieces that aren't connected at all. Road maps, social networks, web links, flight routes, package dependencies, the steps of an AI agent's workflow: all graphs.

![The same small graph three ways. A drawing of 5 vertices: 0–1, 0–2, 1–2, 1–3 and 3–4. Its adjacency matrix, a 5 × 5 grid of 0s and 1s with a 1 wherever two vertices are joined. Its adjacency list: 0: [1, 2], 1: [0, 2, 3], 2: [0, 1], 3: [1, 4], 4: [3]](figures/graph-representations.svg)

| Term | Meaning |
|---|---|
| **V, E** | the number of vertices and of edges; graph costs are written with both, like O(V + E) |
| **undirected / directed** | edges go both ways (friendship) / one way (following someone, a one-way street) |
| **weighted** | each edge has a number: a distance, cost or time |
| **neighbours, degree** | the vertices joined to v / how many there are (in a directed graph: **in-degree** and **out-degree**) |
| **path, cycle** | a sequence of edges / a path that returns to where it started |
| **connected component** | a group of vertices that can all reach each other |
| **DAG** | a directed acyclic graph: directed, with no cycles (task dependencies) |
| **sparse / dense** | few edges (E close to V) / many edges (E close to V²) |

### Storing a graph

| Representation | Space | "Is u joined to v?" | List v's neighbours | Best for |
|---|---|---|---|---|
| **Edge list** `[(u, v), …]` | O(E) | O(E) | O(E) | input format; Kruskal's algorithm |
| **Adjacency matrix** `m[u][v]` | O(V²) | **O(1)** | O(V) | dense graphs, small V |
| **Adjacency list** `{u: [v, …]}` | O(V + E) | O(degree) | **O(degree)** | almost everything else |

Problems usually give you an edge list. Turning it into an adjacency list is the first line of most graph solutions:

```python
from collections import defaultdict

edges = [(0, 1), (0, 2), (1, 2), (1, 3), (3, 4)]

graph = defaultdict(list)            # undirected: add both directions
for u, v in edges:
    graph[u].append(v)
    graph[v].append(u)
print(dict(graph))

directed = defaultdict(list)         # directed: only u -> v
for u, v in edges:
    directed[u].append(v)
print(dict(directed))

flights = [("SFO", "JFK", 6), ("SFO", "SEA", 2), ("SEA", "JFK", 5)]
weighted = defaultdict(list)         # weighted: store (neighbour, weight) pairs
for u, v, w in flights:
    weighted[u].append((v, w))
print(dict(weighted))

n = 5                                # adjacency matrix: n x n of 0/1
matrix = [[0] * n for _ in range(n)]
for u, v in edges:
    matrix[u][v] = matrix[v][u] = 1
print(matrix[1])                     # row 1: who is 1 joined to?
```

Use a `defaultdict(list)` or, when vertices are numbered 0 to n − 1, a plain list of lists: `graph = [[] for _ in range(n)]`. Remember vertices with **no** edges still exist; a `defaultdict` only creates them when touched.

### Depth-first search (DFS)

DFS goes as far as it can along one path, then backs up and tries the next branch: exactly like the tree traversals of Lesson 29, plus a **visited** set, because a graph can lead back to a vertex you've already seen. Without it, a cycle makes the search loop forever.

```python
graph = {0: [1, 2], 1: [0, 2, 3], 2: [0, 1], 3: [1, 4], 4: [3], 5: []}

def dfs_recursive(graph, start, visited=None, order=None):
    if visited is None:
        visited, order = set(), []
    visited.add(start)
    order.append(start)
    for nxt in graph[start]:
        if nxt not in visited:
            dfs_recursive(graph, nxt, visited, order)
    return order

def dfs_iterative(graph, start):
    visited, order, stack = set(), [], [start]
    while stack:
        node = stack.pop()
        if node in visited:
            continue                     # it may have been pushed twice
        visited.add(node)
        order.append(node)
        for nxt in reversed(graph[node]):    # reversed: visit neighbours in the listed order
            if nxt not in visited:
                stack.append(nxt)
    return order

print(dfs_recursive(graph, 0), dfs_iterative(graph, 0))
```

Every vertex is visited once and every edge looked at (twice for undirected), so DFS is **O(V + E)** time and O(V) space. The recursive version is shortest to write, but a long path (thousands of vertices) exceeds Python's recursion limit; the **explicit stack** version handles any size.

### Breadth-first search (BFS)

BFS explores in **rings**: first the start, then everything 1 edge away, then 2 edges away, and so on, using a queue. That's why BFS finds the **fewest-edges** path in an unweighted graph (next lesson).

![BFS from vertex 0 colours the graph in layers: distance 0 is vertex 0; distance 1 is 1 and 2; distance 2 is 3; distance 3 is 4. DFS from 0 instead dives 0 → 1 → 2, backs up to 1, then goes 3 → 4](figures/bfs-dfs.svg)

```python
from collections import deque

graph = {0: [1, 2], 1: [0, 2, 3], 2: [0, 1], 3: [1, 4], 4: [3], 5: []}

def bfs(graph, start):
    dist = {start: 0}                    # doubles as the visited set
    queue = deque([start])
    while queue:
        node = queue.popleft()
        for nxt in graph[node]:
            if nxt not in dist:          # mark when ADDING to the queue, not when popping
                dist[nxt] = dist[node] + 1
                queue.append(nxt)
    return dist

print(bfs(graph, 0))
print(5 in bfs(graph, 0))                # 5 is not reachable from 0
```

Mark a vertex as seen **when you put it in the queue**. Marking only when you pop it lets the same vertex enter the queue many times.

### Connected components

To count the separate pieces, start a search from every vertex that hasn't been visited yet; each new start is a new component. Still O(V + E) overall, because each vertex is visited once in total.

```python
def count_components(n, edges):
    graph = [[] for _ in range(n)]
    for u, v in edges:
        graph[u].append(v)
        graph[v].append(u)
    seen, components = set(), 0
    for start in range(n):
        if start in seen:
            continue
        components += 1                  # a vertex nobody has reached: a new piece
        stack = [start]
        seen.add(start)
        while stack:
            node = stack.pop()
            for nxt in graph[node]:
                if nxt not in seen:
                    seen.add(nxt)
                    stack.append(nxt)
    return components

print(count_components(6, [(0, 1), (1, 2), (3, 4)]))   # {0,1,2}, {3,4}, {5}
```

### Grids are graphs too

Many problems never mention a graph: a maze, a map of land and water, a game board. Each **cell** is a vertex and its up, down, left and right neighbours are its edges. Such **implicit graphs** are explored without building an adjacency list; you compute the neighbours on the fly (Lesson 10's direction list).

```python
grid = ["S.#.",
        "..#.",
        "...E"]
rows, cols = len(grid), len(grid[0])
DIRS = [(-1, 0), (1, 0), (0, -1), (0, 1)]

def neighbours(r, c):
    for dr, dc in DIRS:
        nr, nc = r + dr, c + dc
        if 0 <= nr < rows and 0 <= nc < cols and grid[nr][nc] != "#":
            yield nr, nc

print(list(neighbours(0, 0)), list(neighbours(1, 1)))
```

![A grid of land (1) and water (0) cells with three islands shaded in three colours. One island is a group of four land cells joined up, down, left and right; diagonal touching doesn't join islands](figures/islands.svg)

### Where graph searches show up

| Question | Tool |
|---|---|
| Can I get from A to B? Which vertices can A reach? | DFS or BFS |
| How many separate groups? | a search from each unvisited vertex (or union-find, Lesson 39) |
| Fewest steps from A to B (unweighted) | BFS (Lesson 36) |
| Cheapest route with weights | Dijkstra, Bellman-Ford (Lesson 38) |
| Order tasks that depend on each other | topological sort (Lesson 37) |
| Detect a cycle | DFS with colours (directed) or union-find (undirected) |

:::exercise Number of islands
`grid` is a list of strings made of `"1"` (land) and `"0"` (water). An **island** is a group of land cells joined horizontally or vertically. Write `num_islands(grid)` returning how many islands there are. It must handle a 300 × 300 grid that is one long winding island, so use an explicit stack or a queue rather than recursion.
```python starter
def num_islands(grid):
    pass

print(num_islands(["11000",
                   "11000",
                   "00100",
                   "00011"]))   # 3
```
```python check
fn = need("num_islands")
test(fn, cases=[
    ((["11000", "11000", "00100", "00011"],), 3, "the example"),
    ((["11110", "11010", "11000", "00000"],), 1, "one big island"),
    ((["000", "000"],), 0, "all water"),
    ((["1"],), 1, "a single land cell"),
    ((["101", "010", "101"],), 5, "diagonal cells are separate islands"),
    (([],), 0, "an empty grid"),
    ((["1110111", "0010100", "1110111"],), 2, "U shapes"),
])
def _snake(n):
    rows = []
    for r in range(n):
        if r % 2 == 0:
            rows.append("1" * n)
        elif r % 4 == 1:
            rows.append("0" * (n - 1) + "1")
        else:
            rows.append("1" + "0" * (n - 1))
    return (rows,)
def _ref(grid):
    if not grid: return 0
    R, C = len(grid), len(grid[0]); seen = [[False] * C for _ in range(R)]; count = 0
    for r in range(R):
        for c in range(C):
            if grid[r][c] == "1" and not seen[r][c]:
                count += 1; seen[r][c] = True; stack = [(r, c)]
                while stack:
                    a, b = stack.pop()
                    for x, y in ((a + 1, b), (a - 1, b), (a, b + 1), (a, b - 1)):
                        if 0 <= x < R and 0 <= y < C and grid[x][y] == "1" and not seen[x][y]:
                            seen[x][y] = True; stack.append((x, y))
    return count
speed(fn, _snake, _ref, sizes=(20, 300), what="rows and columns (one winding island)", factor=15,
      tip="A long island makes recursive DFS go thousands of calls deep. Use a list as a stack (or a deque as a queue) instead of recursion.")
```
```python solution
def num_islands(grid):
    if not grid:
        return 0
    rows, cols = len(grid), len(grid[0])
    seen = set()
    islands = 0
    for r in range(rows):
        for c in range(cols):
            if grid[r][c] != "1" or (r, c) in seen:
                continue
            islands += 1                         # new, unvisited land: a new island
            seen.add((r, c))
            stack = [(r, c)]
            while stack:                         # flood-fill the whole island
                cr, cc = stack.pop()
                for nr, nc in ((cr + 1, cc), (cr - 1, cc), (cr, cc + 1), (cr, cc - 1)):
                    if 0 <= nr < rows and 0 <= nc < cols and grid[nr][nc] == "1" and (nr, nc) not in seen:
                        seen.add((nr, nc))
                        stack.append((nr, nc))
    return islands

print(num_islands(["11000",
                   "11000",
                   "00100",
                   "00011"]))
```
```python slow
def num_islands(grid):
    if not grid:
        return 0
    rows, cols = len(grid), len(grid[0])
    seen = set()

    def sink(r, c):
        if r < 0 or r >= rows or c < 0 or c >= cols or grid[r][c] != "1" or (r, c) in seen:
            return
        seen.add((r, c))
        sink(r + 1, c); sink(r - 1, c); sink(r, c + 1); sink(r, c - 1)

    count = 0
    for r in range(rows):
        for c in range(cols):
            if grid[r][c] == "1" and (r, c) not in seen:
                count += 1
                sink(r, c)
    return count
```
hint: Scan every cell. When you find land that hasn't been visited, that's a new island. What do you need to do so you don't count its other cells again?
hint: Visit the whole island right away (a flood fill): DFS or BFS from that cell over land neighbours, adding each cell to a `seen` set.
hint: Use `stack = [(r, c)]` and loop `while stack`: pop a cell, and for its 4 neighbours that are inside the grid, land, and not seen, add them to `seen` and push them. Count how many times you start a flood fill.
approach:
1. **Understand:** 4-directional connections only; strings can't be changed, so track visited cells separately; an empty grid has 0 islands.
2. **Examples:** the example has 3 islands; a checkerboard of 1s has one island per 1.
3. **Brute force:** there isn't a meaningfully simpler idea; the danger is the recursive flood fill crashing on big islands.
4. **Pattern:** **connected components** on an implicit grid graph: one search per unvisited land cell.
5. **Plan:** double loop over cells; on unseen land, count it and flood-fill with an explicit stack.
6. **Code and test:** all water, a single cell, diagonals, a long winding island.
walkthrough:
**Line by line**

- The double loop looks at every cell once as a possible starting point.
- `if grid[r][c] != "1" or (r, c) in seen: continue` skips water and land already counted as part of an island.
- Each new start increments `islands`, then the stack-based flood fill marks every cell of that island as seen.
- Cells are marked when pushed, so no cell enters the stack twice.

**Trace** on the example:

| start cell | island cells marked | islands |
|---|---|---|
| (0, 0) | (0,0), (0,1), (1,0), (1,1) | 1 |
| (2, 2) | (2,2) | 2 |
| (3, 3) | (3,3), (3,4) | 3 |

Every other land cell is already in `seen` when the scan reaches it.

**Complexity:** O(R × C) time, O(R × C) space for `seen` and the stack.

**Common wrong approach:** a recursive `sink(r, c)`. It's correct and common in interviews, but a winding island 45,000 cells long needs 45,000 nested calls, far past Python's limit of about 1,000.
:::

:::exercise Is there a path?
Write `has_path(n, edges, source, target)` for an **undirected** graph with vertices `0` to `n − 1` and `edges` given as pairs. Return `True` if `target` can be reached from `source`. It must be O(V + E): a chain of 100,000 vertices should take well under a second.
```python starter
def has_path(n, edges, source, target):
    pass

print(has_path(3, [(0, 1), (1, 2), (2, 0)], 0, 2))           # True
print(has_path(6, [(0, 1), (0, 2), (3, 5), (5, 4), (4, 3)], 0, 5))   # False
```
```python check
fn = need("has_path")
test(fn, cases=[
    ((3, [(0, 1), (1, 2), (2, 0)], 0, 2), True, "a triangle"),
    ((6, [(0, 1), (0, 2), (3, 5), (5, 4), (4, 3)], 0, 5), False, "two separate pieces"),
    ((1, [], 0, 0), True, "source equals target"),
    ((2, [], 0, 1), False, "no edges at all"),
    ((4, [(3, 2), (2, 1), (1, 0)], 0, 3), True, "edges listed in the other direction"),
    ((5, [(0, 1), (1, 2), (3, 4)], 4, 0), False, "target in another component"),
])
def _make(n):
    edges = [(i, i + 1) for i in range(n - 1)]
    edges.reverse()
    return (n, edges, 0, n - 1)
def _ref(n, edges, s, t):
    g = [[] for _ in range(n)]
    for u, v in edges:
        g[u].append(v); g[v].append(u)
    seen, stack = {s}, [s]
    while stack:
        x = stack.pop()
        for y in g[x]:
            if y not in seen:
                seen.add(y); stack.append(y)
    return t in seen
speed(fn, _make, _ref, sizes=(1_000, 3_000, 100_000), what="vertices in a chain",
      tip="Scanning the whole edge list for every vertex you visit is O(V × E). Build an adjacency list once, then search it with a stack or a queue (not recursion: the chain is 100,000 long).")
```
```python solution
def has_path(n, edges, source, target):
    graph = [[] for _ in range(n)]        # adjacency list, built once: O(V + E)
    for u, v in edges:
        graph[u].append(v)
        graph[v].append(u)                # undirected: both directions
    seen = {source}
    stack = [source]
    while stack:
        node = stack.pop()
        if node == target:
            return True
        for nxt in graph[node]:
            if nxt not in seen:
                seen.add(nxt)
                stack.append(nxt)
    return False

print(has_path(3, [(0, 1), (1, 2), (2, 0)], 0, 2))
print(has_path(6, [(0, 1), (0, 2), (3, 5), (5, 4), (4, 3)], 0, 5))
```
```python slow
def has_path(n, edges, source, target):
    seen = {source}
    stack = [source]
    while stack:
        node = stack.pop()
        if node == target:
            return True
        for u, v in edges:                    # scans every edge for every vertex
            for a, b in ((u, v), (v, u)):
                if a == node and b not in seen:
                    seen.add(b)
                    stack.append(b)
    return False
```
hint: You need to explore everything reachable from `source`. Which search does that, and what does it need to find a vertex's neighbours quickly?
hint: Build an adjacency list first (`graph[u].append(v)` **and** `graph[v].append(u)`, because the graph is undirected). Then run DFS or BFS from `source` with a `seen` set.
hint: `seen = {source}; stack = [source]`; pop a vertex, return True if it's the target, and push every unseen neighbour (marking it seen). If the stack empties, return False.
approach:
1. **Understand:** undirected edges, vertices 0..n−1, source may equal target, some vertices have no edges.
2. **Examples:** the triangle → True; two separate pieces → False.
3. **Brute force:** search, but find neighbours by scanning the edge list each time: O(V × E).
4. **Pattern:** **adjacency list + DFS/BFS** with a visited set.
5. **Plan:** build the list, then an iterative search that stops as soon as the target appears.
6. **Code and test:** source = target, no edges, reversed edge directions, different components.
walkthrough:
**Line by line**

- `graph = [[] for _ in range(n)]` gives every vertex a list, including vertices with no edges. (`[[]] * n` would share one list, a classic bug.)
- Adding each edge in both directions makes the search work no matter which way the pair was written.
- `seen` is updated when a vertex is pushed, so each vertex enters the stack at most once.
- Returning `True` as soon as the target is popped stops early.

**Trace** on n = 6, edges (0,1), (0,2), (3,5), (5,4), (4,3), source 0, target 5:

| popped | pushed | seen |
|---|---|---|
| 0 | 1, 2 | {0, 1, 2} |
| 2 | — | {0, 1, 2} |
| 1 | — | {0, 1, 2} |

The stack is empty and 5 was never reached: False.

**Complexity:** O(V + E) time and space.

**Common wrong approach:** recursive DFS: correct, but on the 100,000-vertex chain it hits RecursionError.
:::

:::quiz
? Which representation lets you list a vertex's neighbours in O(degree) and uses O(V + E) space?
+ An adjacency list
- An adjacency matrix
- An edge list
= The matrix takes O(V²) space and O(V) to list neighbours; the edge list needs a full scan.
? Why does graph search need a visited set when tree traversal doesn't?
+ Graphs can have cycles and several paths to a vertex, so you could revisit vertices forever
- Graphs are always bigger than trees
- To make the search faster on trees
= A tree has exactly one path between any two nodes; a graph may loop back.
? In BFS, when should a vertex be marked as seen?
+ When it's added to the queue
- When it's popped from the queue
- After the whole search
= Marking at push time stops the same vertex from being queued many times.
? What is the time complexity of DFS or BFS with an adjacency list?
+ O(V + E)
- O(V²) always
- O(E log V)
= Each vertex is processed once and each edge is examined a constant number of times.
:::

@@@ lesson
id: bfs-shortest
title: Shortest paths with BFS
minutes: 24
summary: Why breadth-first search finds the fewest-steps path, rebuilding the path with parent links, shortest paths in a grid, multi-source BFS, 0-1 BFS with a deque, implicit graphs such as word ladders and lock puzzles, and bidirectional BFS.
---
In an **unweighted** graph, where every edge counts as one step, BFS finds the shortest path for free. It explores in rings of distance 0, 1, 2, …, so the **first time** it reaches a vertex is by a fewest-steps route. Nothing reached later could be closer.

### Distance and the path itself

To get the route, not just its length, remember each vertex's **parent**: the vertex you came from when you first reached it. Then walk the parents back from the target and reverse.

```python
from collections import deque

graph = {"A": ["B", "C"], "B": ["A", "D"], "C": ["A", "D", "E"], "D": ["B", "C", "F"], "E": ["C", "F"], "F": ["D", "E"]}

def shortest_path(graph, start, goal):
    parent = {start: None}
    queue = deque([start])
    while queue:
        node = queue.popleft()
        if node == goal:
            path = []
            while node is not None:          # walk back along the parent links
                path.append(node)
                node = parent[node]
            return path[::-1]
        for nxt in graph[node]:
            if nxt not in parent:
                parent[nxt] = node
                queue.append(nxt)
    return None                              # goal can't be reached

print(shortest_path(graph, "A", "F"))
print(len(shortest_path(graph, "A", "F")) - 1, "edges")
```

**O(V + E)** time. DFS does **not** find shortest paths: it may wander down a long route first.

### Shortest path in a grid

A maze is the most common disguise. Each cell is a vertex; store distances in a 2-D list or a dict.

```python
from collections import deque

maze = ["S..#....",
        ".#.#.##.",
        ".#...#..",
        ".####.#.",
        "......#E"]

def maze_steps(maze):
    rows, cols = len(maze), len(maze[0])
    start = next((r, c) for r in range(rows) for c in range(cols) if maze[r][c] == "S")
    dist = {start: 0}
    queue = deque([start])
    while queue:
        r, c = queue.popleft()
        if maze[r][c] == "E":
            return dist[(r, c)]
        for nr, nc in ((r + 1, c), (r - 1, c), (r, c + 1), (r, c - 1)):
            if 0 <= nr < rows and 0 <= nc < cols and maze[nr][nc] != "#" and (nr, nc) not in dist:
                dist[(nr, nc)] = dist[(r, c)] + 1
                queue.append((nr, nc))
    return -1

print(maze_steps(maze))
```

### Multi-source BFS

"How far is every cell from the **nearest** hospital?" Don't run one BFS per hospital: put **all** the sources in the queue at distance 0 and run a single BFS. The rings spread from every source at once, and each cell is reached first from its closest source. O(V + E) in total, however many sources there are.

![A grid with two sources marked 0. Each other cell shows its distance to the nearer source: 1s around each source, then 2s, then 3s, with the rings from the two sources meeting in the middle](figures/multi-source.svg)

```python
from collections import deque

def nearest_distance(grid, source="H"):
    rows, cols = len(grid), len(grid[0])
    dist = [[-1] * cols for _ in range(rows)]
    queue = deque()
    for r in range(rows):
        for c in range(cols):
            if grid[r][c] == source:
                dist[r][c] = 0
                queue.append((r, c))         # every source starts in the queue
    while queue:
        r, c = queue.popleft()
        for nr, nc in ((r + 1, c), (r - 1, c), (r, c + 1), (r, c - 1)):
            if 0 <= nr < rows and 0 <= nc < cols and dist[nr][nc] == -1:
                dist[nr][nc] = dist[r][c] + 1
                queue.append((nr, nc))
    return dist

for row in nearest_distance(["H....", ".....", "....H"]):
    print(row)
```

### 0-1 BFS: edges that cost 0 or 1

If every edge costs either 0 or 1 (say, moving along a road is free but switching roads costs 1), use a **deque**: push a vertex reached by a 0-cost edge to the **front** and one reached by a 1-cost edge to the **back**. The deque stays sorted by distance, so it's as correct as Dijkstra (Lesson 38) but O(V + E).

```python
from collections import deque

def zero_one_bfs(n, edges, start):          # edges: (u, v, cost) with cost 0 or 1, directed
    graph = [[] for _ in range(n)]
    for u, v, w in edges:
        graph[u].append((v, w))
    dist = [float("inf")] * n
    dist[start] = 0
    dq = deque([start])
    while dq:
        u = dq.popleft()
        for v, w in graph[u]:
            if dist[u] + w < dist[v]:
                dist[v] = dist[u] + w
                if w == 0:
                    dq.appendleft(v)          # as close as u: handle it next
                else:
                    dq.append(v)
    return dist

print(zero_one_bfs(5, [(0, 1, 1), (0, 2, 0), (2, 1, 0), (1, 3, 1), (2, 4, 1), (4, 3, 0)], 0))
```

### Implicit graphs: states and moves

The vertices don't have to exist in advance. In a **word ladder** (turn "hit" into "cog" changing one letter at a time, every step a real word), each word is a vertex and words that differ by one letter are neighbours. In a lock puzzle, each combination is a vertex. Generate neighbours as you go and BFS finds the fewest moves.

```python
from collections import deque, defaultdict

def ladder_length(begin, end, words):
    words = set(words)
    if end not in words:
        return 0
    buckets = defaultdict(list)              # "h*t" -> ["hot", "hit", ...]: words one letter apart share a bucket
    for w in words | {begin}:
        for i in range(len(w)):
            buckets[w[:i] + "*" + w[i + 1:]].append(w)
    seen = {begin}
    queue = deque([(begin, 1)])
    while queue:
        word, steps = queue.popleft()
        if word == end:
            return steps
        for i in range(len(word)):
            for nxt in buckets[word[:i] + "*" + word[i + 1:]]:
                if nxt not in seen:
                    seen.add(nxt)
                    queue.append((nxt, steps + 1))
    return 0

print(ladder_length("hit", "cog", ["hot", "dot", "dog", "lot", "log", "cog"]))   # hit hot dot dog cog
```

The buckets avoid comparing every pair of words (O(n²)); each word only looks at the words that share one of its L patterns.

### Bidirectional BFS

When both the start and the goal are known and the graph branches a lot, run two BFS searches, one from each end, expanding the **smaller** frontier each round, and stop when they meet. With branching factor b and distance d, that explores about 2·b^(d/2) vertices instead of b^d: for b = 10 and d = 6, two thousand instead of a million.

```python
def bidirectional(graph, start, goal):
    if start == goal:
        return 0
    front, back = {start}, {goal}
    seen = {start, goal}
    steps = 0
    while front and back:
        if len(front) > len(back):
            front, back = back, front           # always grow the smaller side
        steps += 1
        nxt_front = set()
        for node in front:
            for nxt in graph[node]:
                if nxt in back:
                    return steps                # the two searches met
                if nxt not in seen:
                    seen.add(nxt)
                    nxt_front.add(nxt)
        front = nxt_front
    return -1

graph = {0: [1, 2], 1: [0, 3], 2: [0, 4], 3: [1, 5], 4: [2, 5], 5: [3, 4, 6], 6: [5]}
print(bidirectional(graph, 0, 6))
```

### Choosing a shortest-path method

| Edge weights | Algorithm | Time |
|---|---|---|
| none (all equal) | **BFS** | O(V + E) |
| 0 or 1 | **0-1 BFS** with a deque | O(V + E) |
| non-negative | **Dijkstra** (Lesson 38) | O((V + E) log V) |
| may be negative | **Bellman-Ford** (Lesson 38) | O(V × E) |
| a DAG, any weights | relax in topological order (Lesson 37) | O(V + E) |
| all pairs, small V | **Floyd-Warshall** (Lesson 38) | O(V³) |

:::exercise Shortest clear path in a grid
`grid` is an n × n list of lists of `0` (open) and `1` (blocked). Write `shortest_clear_path(grid)` returning the number of cells on the shortest path from the top-left cell to the bottom-right cell, moving to any of the **8** neighbouring cells (diagonals included) through open cells only. Return `-1` if there's no such path (including when the start or end is blocked).
```python starter
from collections import deque

def shortest_clear_path(grid):
    pass

print(shortest_clear_path([[0, 1], [1, 0]]))                     # 2 (one diagonal move)
print(shortest_clear_path([[0, 0, 0], [1, 1, 0], [1, 1, 0]]))    # 4
```
```python check
fn = need("shortest_clear_path")
test(fn, cases=[
    (([[0, 1], [1, 0]],), 2, "one diagonal move"),
    (([[0, 0, 0], [1, 1, 0], [1, 1, 0]],), 4, "around the wall"),
    (([[1, 0, 0], [1, 1, 0], [1, 1, 0]],), -1, "the start is blocked"),
    (([[0, 0, 0], [0, 0, 0], [0, 0, 1]],), -1, "the end is blocked"),
    (([[0]],), 1, "a single open cell"),
    (([[0, 1, 1], [1, 1, 1], [1, 1, 0]],), -1, "walled off"),
    (([[0, 0, 0, 0, 0], [1, 1, 1, 1, 0], [0, 0, 0, 0, 0], [0, 1, 1, 1, 1], [0, 0, 0, 0, 0]],), 13, "a winding corridor"),
    (([[0, 0, 1, 0], [1, 0, 1, 0], [1, 0, 1, 0], [1, 1, 0, 0]],), 5, "a diagonal squeeze between walls"),
])
```
```python solution
from collections import deque

def shortest_clear_path(grid):
    n = len(grid)
    if grid[0][0] == 1 or grid[n - 1][n - 1] == 1:
        return -1
    dist = {(0, 0): 1}                        # path length counted in cells, so the start is 1
    queue = deque([(0, 0)])
    while queue:
        r, c = queue.popleft()
        if (r, c) == (n - 1, n - 1):
            return dist[(r, c)]
        for dr in (-1, 0, 1):
            for dc in (-1, 0, 1):
                nr, nc = r + dr, c + dc
                if 0 <= nr < n and 0 <= nc < n and grid[nr][nc] == 0 and (nr, nc) not in dist:
                    dist[(nr, nc)] = dist[(r, c)] + 1
                    queue.append((nr, nc))
    return -1

print(shortest_clear_path([[0, 1], [1, 0]]))
print(shortest_clear_path([[0, 0, 0], [1, 1, 0], [1, 1, 0]]))
```
hint: Every move costs the same (one cell), so which search finds the fewest moves?
hint: BFS from (0, 0) over open cells, with 8 neighbours: all combinations of `dr` and `dc` in (−1, 0, 1). Store the distance of each cell as you discover it.
hint: Check the start and end cells first. Start with `dist = {(0, 0): 1}`; when you pop the bottom-right cell, return its distance. If the queue empties, return −1.
approach:
1. **Understand:** count cells, not moves; 8 directions; blocked start or end means −1.
2. **Examples:** [[0, 1], [1, 0]] → 2 (start, then the diagonal end).
3. **Brute force:** DFS trying every route and keeping the shortest: exponential.
4. **Pattern:** **BFS on a grid** (unweighted shortest path).
5. **Plan:** guard the corners, BFS with a distance dict, return on reaching the end.
6. **Code and test:** a 1 × 1 grid, blocked corners, a path that needs diagonal moves.
walkthrough:
**Line by line**

- Checking `grid[0][0]` and `grid[n-1][n-1]` first handles the blocked cases before searching.
- `dist` doubles as the visited set; a cell is recorded the moment it's discovered.
- The two loops over `dr` and `dc` generate all 8 neighbours (plus the cell itself, which is already in `dist` and so ignored).
- BFS pops cells in order of distance, so the first time the end is popped, its distance is the shortest.

**Trace** on [[0, 0, 0], [1, 1, 0], [1, 1, 0]]:

| popped | distance | newly discovered |
|---|---|---|
| (0, 0) | 1 | (0, 1) → 2 |
| (0, 1) | 2 | (0, 2) → 3, (1, 2) → 3 |
| (0, 2) | 3 | — |
| (1, 2) | 3 | (2, 2) → 4 |
| (2, 2) | **4** | the end: return 4 |

**Complexity:** O(n²) time and space: each cell is queued at most once and has 8 neighbours.

**Common wrong approach:** using DFS and returning the first path found, which is a path but not necessarily the shortest.
:::

:::exercise Rotting oranges
`grid` holds `0` (empty), `1` (fresh orange) and `2` (rotten orange). Every minute, each fresh orange next to a rotten one (up, down, left, right) becomes rotten. Write `minutes_to_rot(grid)` returning how many minutes until no fresh orange is left, or `-1` if some can never rot. Don't change `grid`. It must handle a 300 × 300 grid quickly, so don't re-scan the whole grid every minute.
```python starter
from collections import deque

def minutes_to_rot(grid):
    pass

print(minutes_to_rot([[2, 1, 1], [1, 1, 0], [0, 1, 1]]))   # 4
print(minutes_to_rot([[2, 1, 1], [0, 1, 1], [1, 0, 1]]))   # -1
```
```python check
from collections import deque
fn = need("minutes_to_rot")
_orig = [[2, 1, 1], [1, 1, 0], [0, 1, 1]]
_copy = [row[:] for row in _orig]
fn(_copy)
if _copy != _orig:
    raise AssertionError("Don't change grid: copy it (or track rotten cells in a set) before simulating.")
test(fn, cases=[
    (([[2, 1, 1], [1, 1, 0], [0, 1, 1]],), 4, "the example"),
    (([[2, 1, 1], [0, 1, 1], [1, 0, 1]],), -1, "an orange that can't be reached"),
    (([[0, 2]],), 0, "no fresh oranges"),
    (([[0]],), 0, "an empty box"),
    (([[1]],), -1, "a fresh orange and nothing rotten"),
    (([[2, 1, 1, 1, 1, 2]],), 2, "two rotten oranges spreading towards each other"),
    (([[2], [1], [1], [1]],), 3, "a column"),
])
def _make(n):
    g = [[1] * n for _ in range(n)]
    g[0][0] = 2
    for r in range(1, n, 4):
        for c in range(n // 3, n):
            g[r][c] = 0
    return (g,)
def _ref(grid):
    R, C = len(grid), len(grid[0]); g = [row[:] for row in grid]; q = deque(); fresh = 0
    for r in range(R):
        for c in range(C):
            if g[r][c] == 2: q.append((r, c, 0))
            elif g[r][c] == 1: fresh += 1
    t = 0
    while q:
        r, c, d = q.popleft(); t = max(t, d)
        for x, y in ((r + 1, c), (r - 1, c), (r, c + 1), (r, c - 1)):
            if 0 <= x < R and 0 <= y < C and g[x][y] == 1:
                g[x][y] = 2; fresh -= 1; q.append((x, y, d + 1))
    return t if fresh == 0 else -1
speed(fn, _make, _ref, sizes=(20, 100, 300), what="rows and columns",
      tip="Re-scanning the whole grid every minute is O((rows × cols)²) in the worst case. Put every rotten orange in a queue at minute 0 and run one multi-source BFS.")
```
```python solution
from collections import deque

def minutes_to_rot(grid):
    rows, cols = len(grid), len(grid[0])
    rotten = set()
    queue = deque()
    fresh = 0
    for r in range(rows):
        for c in range(cols):
            if grid[r][c] == 2:
                rotten.add((r, c))
                queue.append((r, c, 0))          # every rotten orange is a source at minute 0
            elif grid[r][c] == 1:
                fresh += 1
    minutes = 0
    while queue:
        r, c, t = queue.popleft()
        minutes = max(minutes, t)
        for nr, nc in ((r + 1, c), (r - 1, c), (r, c + 1), (r, c - 1)):
            if 0 <= nr < rows and 0 <= nc < cols and grid[nr][nc] == 1 and (nr, nc) not in rotten:
                rotten.add((nr, nc))
                fresh -= 1
                queue.append((nr, nc, t + 1))
    return minutes if fresh == 0 else -1

print(minutes_to_rot([[2, 1, 1], [1, 1, 0], [0, 1, 1]]))
print(minutes_to_rot([[2, 1, 1], [0, 1, 1], [1, 0, 1]]))
```
```python slow
def minutes_to_rot(grid):
    g = [row[:] for row in grid]
    rows, cols = len(g), len(g[0])
    minutes = 0
    while True:
        newly = []
        for r in range(rows):                      # scan the whole grid every minute
            for c in range(cols):
                if g[r][c] == 1 and any(0 <= x < rows and 0 <= y < cols and g[x][y] == 2
                                        for x, y in ((r + 1, c), (r - 1, c), (r, c + 1), (r, c - 1))):
                    newly.append((r, c))
        if not newly:
            break
        for r, c in newly:
            g[r][c] = 2
        minutes += 1
    return minutes if all(1 not in row for row in g) else -1
```
hint: The rot spreads one ring per minute from **every** rotten orange at once. Which search spreads in rings?
hint: Multi-source BFS: put all rotten oranges in the queue with time 0. Count the fresh oranges first, and subtract one each time an orange rots.
hint: Store `(r, c, minute)` in the queue. When a fresh neighbour rots, push it with `minute + 1`. The answer is the largest minute seen, or −1 if `fresh` is still above 0 at the end. Track rotten cells in a set so `grid` isn't changed.
approach:
1. **Understand:** spread is simultaneous from all rotten oranges; 0 minutes if nothing is fresh; −1 if some fresh orange is unreachable.
2. **Examples:** the first example takes 4 minutes; [[0, 2]] → 0.
3. **Brute force:** simulate minute by minute, scanning the whole grid each time: O((R·C)²) worst case.
4. **Pattern:** **multi-source BFS**: the BFS level is the minute.
5. **Plan:** queue all rotten cells at time 0 and count fresh ones; BFS; return the max time or −1.
6. **Code and test:** no fresh oranges, unreachable oranges, two sources meeting.
walkthrough:
**Line by line**

- The first double loop seeds the queue with every rotten orange and counts the fresh ones.
- Each queue item carries its minute, so a neighbour that rots from it gets `t + 1`.
- `rotten` stops an orange from rotting (and being counted) twice.
- After the BFS, any remaining `fresh` count means some oranges were never reached.

**Trace** on [[2, 1, 1], [1, 1, 0], [0, 1, 1]] (fresh = 6):

| minute | oranges that rot | fresh left |
|---|---|---|
| 1 | (0,1), (1,0) | 4 |
| 2 | (0,2), (1,1) | 2 |
| 3 | (2,1) | 1 |
| 4 | (2,2) | 0 → answer 4 |

**Complexity:** O(R × C) time and space.

**Common wrong approach:** running a separate BFS from each rotten orange and adding the times, instead of spreading from all of them together.
:::

:::quiz
? Why does BFS find the shortest path in an unweighted graph?
+ It reaches vertices in order of their distance, so the first visit is by a shortest route
- It always goes straight towards the goal
- It tries every possible path
= Rings of distance 0, 1, 2… are completed one after another.
? How do you rebuild the actual path after a BFS?
+ Store each vertex's parent when it's discovered, then follow parents back from the goal and reverse
- Run DFS afterwards
- Sort the visited vertices
= The parent links form a shortest-path tree rooted at the start.
? You need every cell's distance to the nearest of 50 exits. What's the efficient approach?
+ One BFS with all 50 exits in the queue at distance 0
- 50 separate BFS runs, keeping the minimum
- Dijkstra from each cell
= Multi-source BFS costs O(V + E) in total.
? In 0-1 BFS, where does a vertex reached by a 0-cost edge go?
+ The front of the deque
- The back of the deque
- It's skipped
= It's as close as the current vertex, so it must be handled before farther vertices.
:::

@@@ lesson
id: topological-sort
title: Topological sort and DAGs
minutes: 24
summary: Ordering tasks that depend on each other: directed acyclic graphs, Kahn's algorithm with in-degrees, the DFS method with three colours, detecting cycles in directed graphs, Python's graphlib, and dynamic programming in topological order (critical paths and longest paths).
---
"Install the compiler before building; build before testing; test before deploying." When tasks depend on each other, you need an order that puts every task **after** everything it depends on. Draw each dependency as a directed edge `before → after`; such an order is a **topological order** (or topological sort) of that graph.

![A DAG of getting dressed: underwear → trousers → shoes, socks → shoes, shirt → tie → jacket, trousers → belt → jacket. Below it, one valid topological order: underwear, socks, shirt, trousers, tie, belt, shoes, jacket, where every arrow points from left to right](figures/topological.svg)

- A topological order exists **if and only if** the graph has no directed cycle. A directed graph with no cycles is a **DAG** (directed acyclic graph). If A needs B and B needs A, no order works.
- There are often **many** valid orders; any one is a correct answer unless the problem asks for a specific one.

### Kahn's algorithm: repeatedly take what's ready

The **in-degree** of a task is how many tasks it still waits for. Tasks with in-degree 0 are ready. Take one, and "remove" its outgoing edges by decrementing its neighbours' in-degrees; any neighbour that reaches 0 becomes ready.

```python
from collections import deque

def kahn(n, edges):                          # edges: (before, after)
    graph = [[] for _ in range(n)]
    indegree = [0] * n
    for u, v in edges:
        graph[u].append(v)
        indegree[v] += 1
    ready = deque(i for i in range(n) if indegree[i] == 0)
    order = []
    while ready:
        u = ready.popleft()
        order.append(u)
        for v in graph[u]:
            indegree[v] -= 1
            if indegree[v] == 0:             # its last prerequisite is done
                ready.append(v)
    return order if len(order) == n else None   # leftovers mean a cycle

print(kahn(6, [(5, 2), (5, 0), (4, 0), (4, 1), (2, 3), (3, 1)]))
print(kahn(3, [(0, 1), (1, 2), (2, 0)]))     # a cycle: no order
```

If some vertices never reach in-degree 0, they're stuck on a cycle: **the same algorithm detects cycles**. O(V + E) time.

To get the **smallest** order alphabetically (or by number), swap the deque for a heap: `heapq.heappush(ready, v)` and `heapq.heappop(ready)`, at O((V + E) log V).

### The DFS method and three colours

A vertex finishes (all its descendants explored) only after everything it leads to. So the **reverse of the DFS finishing order** is a topological order. To spot cycles, colour vertices: **white** (unvisited), **grey** (on the current path), **black** (finished). Reaching a **grey** vertex again means you've gone round a loop.

```python
def topo_dfs(graph):
    WHITE, GREY, BLACK = 0, 1, 2
    colour = {v: WHITE for v in graph}
    finished = []

    def visit(u):
        colour[u] = GREY
        for v in graph[u]:
            if colour[v] == GREY:
                raise ValueError(f"cycle through {u} -> {v}")
            if colour[v] == WHITE:
                visit(v)
        colour[u] = BLACK
        finished.append(u)                   # u is done after all it leads to

    for u in graph:
        if colour[u] == WHITE:
            visit(u)
    return finished[::-1]

graph = {"wake": ["shower", "coffee"], "shower": ["dress"], "coffee": ["leave"], "dress": ["leave"], "leave": []}
print(topo_dfs(graph))
try:
    topo_dfs({"a": ["b"], "b": ["c"], "c": ["a"]})
except ValueError as e:
    print(e)
```

In an **undirected** graph, seeing an already-visited vertex other than your parent means a cycle; in a **directed** graph, only a **grey** one does (a black one was reached by another route, which is fine). The recursive version needs one call per vertex on the longest path, so prefer Kahn's algorithm for big inputs.

### Python's graphlib

The standard library has had a topological sorter since Python 3.9. You give each node its **predecessors**:

```python
from graphlib import TopologicalSorter, CycleError

deps = {"deploy": {"test"}, "test": {"build"}, "build": {"install"}, "docs": {"install"}}
print(list(TopologicalSorter(deps).static_order()))

try:
    list(TopologicalSorter({"a": {"b"}, "b": {"a"}}).static_order())
except CycleError as e:
    print("cycle:", e.args[1])
```

It can also hand out tasks in batches that may run **in parallel** (`prepare()`, `get_ready()`, `done()`), which is how build tools and data pipelines schedule work.

### Dynamic programming on a DAG

Processing vertices in topological order guarantees that when you reach a vertex, everything before it is finished. That makes DAGs ideal for dynamic programming (Part 9). The **critical path** of a project, the earliest time everything can be finished when independent tasks run in parallel, is the **longest** path through the DAG weighted by task durations:

```python
from collections import deque

def earliest_finish(durations, deps):        # deps: (before, after)
    n = len(durations)
    graph, indegree = [[] for _ in range(n)], [0] * n
    for u, v in deps:
        graph[u].append(v)
        indegree[v] += 1
    start = [0] * n                          # earliest start time of each task
    ready = deque(i for i in range(n) if indegree[i] == 0)
    while ready:
        u = ready.popleft()
        for v in graph[u]:
            start[v] = max(start[v], start[u] + durations[u])   # v waits for its slowest prerequisite
            indegree[v] -= 1
            if indegree[v] == 0:
                ready.append(v)
    return max(s + d for s, d in zip(start, durations))

# 0: design (3 days), 1: backend (5), 2: frontend (4), 3: tests (2)
print(earliest_finish([3, 5, 4, 2], [(0, 1), (0, 2), (1, 3), (2, 3)]))   # 3 + 5 + 2
```

The same pattern gives **shortest** paths in a DAG even with negative weights, in O(V + E): relax each vertex's outgoing edges in topological order.

### Where topological order shows up

| Situation | Vertices | Edge u → v means |
|---|---|---|
| Course prerequisites | courses | take u before v |
| Build systems (make, Bazel), package installers | targets, packages | v depends on u |
| Spreadsheets | cells | v's formula uses u |
| Data pipelines (Airflow DAGs) | jobs | v needs u's output |
| Neural networks | operations | v uses u's result; backpropagation runs in **reverse** topological order |

:::exercise Can all courses be finished?
There are `n` courses, numbered `0` to `n − 1`. `prerequisites` is a list of pairs `[a, b]` meaning "to take course `a` you must first take course `b`". Write `can_finish(n, prerequisites)` returning `True` if it's possible to take every course. It must be O(V + E): 100,000 courses in one long chain should take well under a second.
```python starter
from collections import deque

def can_finish(n, prerequisites):
    pass

print(can_finish(2, [[1, 0]]))            # True
print(can_finish(2, [[1, 0], [0, 1]]))    # False
```
```python check
from collections import deque
fn = need("can_finish")
test(fn, cases=[
    ((2, [[1, 0]]), True, "one prerequisite"),
    ((2, [[1, 0], [0, 1]]), False, "two courses that need each other"),
    ((3, []), True, "no prerequisites"),
    ((1, [[0, 0]]), False, "a course that requires itself"),
    ((4, [[1, 0], [2, 1], [3, 2], [1, 3]]), False, "a cycle after the first course"),
    ((5, [[1, 0], [2, 0], [3, 1], [3, 2], [4, 3]]), True, "a diamond"),
    ((6, [[1, 0], [2, 1], [4, 3], [5, 4], [3, 5]]), False, "one fine chain and one cycle"),
])
def _make(n):
    pre = [[i + 1, i] for i in range(n - 1)]
    pre.reverse()
    return (n, pre)
def _ref(n, pre):
    g, deg = [[] for _ in range(n)], [0] * n
    for a, b in pre:
        g[b].append(a); deg[a] += 1
    q, done = deque(i for i in range(n) if deg[i] == 0), 0
    while q:
        x = q.popleft(); done += 1
        for y in g[x]:
            deg[y] -= 1
            if deg[y] == 0: q.append(y)
    return done == n
speed(fn, _make, _ref, sizes=(1_000, 2_500, 100_000), what="courses in a chain",
      tip="Re-scanning all the prerequisites to find the next available course is O(V × E). Count in-degrees once and keep a queue of courses whose count has dropped to 0 (Kahn's algorithm).")
```
```python solution
from collections import deque

def can_finish(n, prerequisites):
    after = [[] for _ in range(n)]       # after[b]: courses that need b
    waiting = [0] * n                    # in-degree: prerequisites not yet taken
    for a, b in prerequisites:
        after[b].append(a)
        waiting[a] += 1
    ready = deque(c for c in range(n) if waiting[c] == 0)
    taken = 0
    while ready:
        course = ready.popleft()
        taken += 1
        for nxt in after[course]:
            waiting[nxt] -= 1
            if waiting[nxt] == 0:        # all of nxt's prerequisites are done
                ready.append(nxt)
    return taken == n                    # anything left over is stuck on a cycle

print(can_finish(2, [[1, 0]]))
print(can_finish(2, [[1, 0], [0, 1]]))
```
```python slow
def can_finish(n, prerequisites):
    taken = set()
    while len(taken) < n:
        blocked = {a for a, b in prerequisites if b not in taken}   # rescans every pair each round
        new = [c for c in range(n) if c not in taken and c not in blocked]
        if not new:
            return False
        taken.update(new)
    return True
```
hint: Draw each pair `[a, b]` as an edge b → a. When is it impossible to take every course?
hint: Exactly when the graph has a cycle. Kahn's algorithm finds out: count each course's unmet prerequisites (its in-degree), start with the courses that have none, and see how many courses you manage to take.
hint: Build `after[b].append(a)` and `waiting[a] += 1`. Queue every course with `waiting == 0`; each time you take one, decrement `waiting` for the courses after it and queue those that reach 0. Return `taken == n`.
approach:
1. **Understand:** `[a, b]` means b comes first; a course can depend on itself; courses with no pairs are free.
2. **Examples:** [[1, 0]] → True; [[1, 0], [0, 1]] → False.
3. **Brute force:** repeatedly look through all pairs for a course whose prerequisites are done: O(V × E).
4. **Pattern:** **topological sort (Kahn's algorithm)** = cycle detection in a directed graph.
5. **Plan:** in-degrees, a queue of ready courses, count how many get taken.
6. **Code and test:** a self-loop, a cycle hidden after a valid course, an empty prerequisite list.
walkthrough:
**Line by line**

- `after[b].append(a)` stores the edge b → a: finishing b may unlock a.
- `waiting[a]` counts a's prerequisites; a course with 0 can be taken right away.
- Taking a course decrements `waiting` for everything after it; a course joins the queue the moment its last prerequisite is done.
- Courses on a cycle wait for each other forever and never join the queue, so `taken < n`.

**Trace** on n = 4, [[1, 0], [2, 1], [3, 2], [1, 3]]:

| step | ready queue | taken | waiting |
|---|---|---|---|
| start | 0 | 0 | [0, 2, 1, 1] |
| take 0 | — | 1 | [0, 1, 1, 1] |

Courses 1, 2 and 3 wait for each other in a cycle; the queue is empty with 1 of 4 taken: False.

**Complexity:** O(V + E) time and space.

**Common wrong approach:** a DFS that treats any visited vertex as a cycle. In a directed graph a vertex reached a second time by another route (a diamond) is fine; only a vertex still on the current path (grey) means a cycle.
:::

:::exercise Course order
Same input as before. Write `course_order(n, prerequisites)` returning a list of all `n` courses in an order in which they can be taken (any valid order is accepted), or `[]` if that's impossible.
```python starter
from collections import deque

def course_order(n, prerequisites):
    pass

print(course_order(4, [[1, 0], [2, 0], [3, 1], [3, 2]]))   # e.g. [0, 1, 2, 3] or [0, 2, 1, 3]
print(course_order(2, [[0, 1], [1, 0]]))                   # []
```
```python check
from collections import deque
fn = need("course_order")
def _valid(got, n, pre):
    if not isinstance(got, list):
        return False
    if got == []:
        return False
    if sorted(got) != list(range(n)):
        return False
    pos = {c: i for i, c in enumerate(got)}
    return all(pos[b] < pos[a] for a, b in pre)
def _check(got, n, pre):
    expected_possible = _ref_possible(n, pre)
    return _valid(got, n, pre) if expected_possible else got == []
def _ref_possible(n, pre):
    g, deg = [[] for _ in range(n)], [0] * n
    for a, b in pre:
        g[b].append(a); deg[a] += 1
    q, done = deque(i for i in range(n) if deg[i] == 0), 0
    while q:
        x = q.popleft(); done += 1
        for y in g[x]:
            deg[y] -= 1
            if deg[y] == 0: q.append(y)
    return done == n
test(fn, valid=_check, cases=[
    ((4, [[1, 0], [2, 0], [3, 1], [3, 2]]), [0, 1, 2, 3], "a diamond"),
    ((2, [[0, 1], [1, 0]]), [], "a cycle"),
    ((1, []), [0], "one course"),
    ((3, []), [0, 1, 2], "no prerequisites: every course must still be listed"),
    ((3, [[0, 1], [1, 2]]), [2, 1, 0], "a chain written backwards"),
    ((5, [[1, 0], [2, 1], [2, 3], [4, 2]]), [0, 3, 1, 2, 4], "two starting courses"),
    ((3, [[0, 1], [1, 2], [2, 1]]), [], "a cycle that doesn't include the first course"),
])
```
```python solution
from collections import deque

def course_order(n, prerequisites):
    after = [[] for _ in range(n)]
    waiting = [0] * n
    for a, b in prerequisites:
        after[b].append(a)
        waiting[a] += 1
    ready = deque(c for c in range(n) if waiting[c] == 0)
    order = []
    while ready:
        course = ready.popleft()
        order.append(course)                 # Kahn's algorithm: the order courses become ready
        for nxt in after[course]:
            waiting[nxt] -= 1
            if waiting[nxt] == 0:
                ready.append(nxt)
    return order if len(order) == n else []

print(course_order(4, [[1, 0], [2, 0], [3, 1], [3, 2]]))
print(course_order(2, [[0, 1], [1, 0]]))
```
hint: This is the previous exercise, but instead of counting the courses you take, record them.
hint: Kahn's algorithm produces a topological order: the order in which courses leave the ready queue.
hint: Append each popped course to `order`. At the end return `order` if it has all n courses, otherwise `[]` (a cycle stopped some courses).
approach:
1. **Understand:** any valid order; include courses with no prerequisites; `[]` when a cycle exists.
2. **Examples:** the diamond allows [0, 1, 2, 3] or [0, 2, 1, 3].
3. **Brute force:** try permutations until one satisfies every pair: O(n! × E).
4. **Pattern:** **topological sort** with Kahn's algorithm.
5. **Plan:** in-degrees, ready queue, record the pop order, check its length.
6. **Code and test:** no prerequisites, backwards chains, a cycle not touching course 0.
walkthrough:
**Line by line**

- The setup is identical to `can_finish`.
- `order.append(course)` records each course when it's taken; every prerequisite of it was taken earlier, because it only became ready after them.
- If the order is shorter than n, the missing courses are on (or behind) a cycle, so the answer is `[]`.

**Trace** on n = 4, [[1, 0], [2, 0], [3, 1], [3, 2]]:

| popped | order | newly ready |
|---|---|---|
| 0 | [0] | 1, 2 |
| 1 | [0, 1] | — (3 still waits for 2) |
| 2 | [0, 1, 2] | 3 |
| 3 | [0, 1, 2, 3] | — |

**Complexity:** O(V + E) time and space.

**Common wrong approach:** sorting the courses by how many prerequisites they have. A course with one prerequisite can still need to come after a course with three.
:::

:::quiz
? When does a directed graph have a topological order?
+ Exactly when it has no directed cycle (it's a DAG)
- Always
- Only when it's a tree
= A cycle would require each task on it to come before itself.
? In Kahn's algorithm, which vertices go into the queue first?
+ Those with in-degree 0
- Those with the most edges
- The highest-numbered ones
= Nothing has to come before them.
? How does Kahn's algorithm reveal a cycle?
+ Fewer than V vertices make it into the order
- It raises an error immediately
- The queue never empties
= Vertices on a cycle never reach in-degree 0.
? In DFS cycle detection on a directed graph, which kind of vertex signals a cycle?
+ A grey vertex, one still on the current path
- Any visited vertex
- A black vertex
= A black vertex was finished by another route, which is fine (think of a diamond).
:::

@@@ lesson
id: shortest-paths
title: Weighted shortest paths
minutes: 28
summary: Dijkstra's algorithm with a heap (and why it needs non-negative weights), rebuilding routes, Bellman-Ford with negative edges, negative cycles and "at most k edges" limits, Floyd-Warshall for all pairs, and A* search with a heuristic.
---
When edges have **weights** (distances, prices, travel times), the path with the fewest edges isn't necessarily the cheapest. A 1-edge flight costing $900 loses to a 2-edge route costing $300. BFS counts edges, so it gives the wrong answer here.

### Dijkstra's algorithm

**Dijkstra's algorithm** grows a set of vertices whose shortest distance is final. At each step it takes the **unsettled vertex with the smallest known distance**, settles it, and **relaxes** its edges: for each neighbour, if going through this vertex is cheaper than the best route known so far, update it.

![A weighted graph from A: A–B costs 4, A–C costs 1, C–B costs 2, B–D costs 1, C–D costs 5. Dijkstra settles A (0), then C (1), then B (3, via C, cheaper than the direct 4), then D (4, via B). The final shortest distances are shown next to each vertex](figures/dijkstra.svg)

A min-heap of `(distance, vertex)` pairs finds the closest unsettled vertex quickly. Python's heapq has no "decrease key", so when a distance improves, just push a new pair; when an **out-of-date** pair is popped later, skip it (**lazy deletion**).

```python
import heapq

def dijkstra(graph, start):
    dist = {start: 0}
    parent = {start: None}
    heap = [(0, start)]
    done = set()
    while heap:
        d, u = heapq.heappop(heap)
        if u in done:
            continue                          # a stale entry: u was settled with a smaller distance
        done.add(u)
        for v, w in graph[u]:
            nd = d + w
            if nd < dist.get(v, float("inf")):    # relax the edge u -> v
                dist[v] = nd
                parent[v] = u
                heapq.heappush(heap, (nd, v))
    return dist, parent

def route(parent, goal):
    path = []
    while goal is not None:
        path.append(goal)
        goal = parent[goal]
    return path[::-1]

graph = {"A": [("B", 4), ("C", 1)], "B": [("A", 4), ("C", 2), ("D", 1)],
         "C": [("A", 1), ("B", 2), ("D", 5)], "D": [("B", 1), ("C", 5)]}
dist, parent = dijkstra(graph, "A")
print(dist)
print(route(parent, "D"))
```

**Cost:** each edge can push one heap entry, so O((V + E) log V) time and O(V + E) space. Dijkstra is the algorithm behind route planners and network routing (OSPF).

**Why it needs non-negative weights:** once a vertex is settled, Dijkstra never revisits it. That's safe only if no later edge can make a path **shorter**, which a negative weight can do:

```python
import heapq

def dijkstra_dist(graph, start):
    dist, heap, done = {start: 0}, [(0, start)], set()
    while heap:
        d, u = heapq.heappop(heap)
        if u in done:
            continue
        done.add(u)
        for v, w in graph[u]:
            if v not in done and d + w < dist.get(v, float("inf")):
                dist[v] = d + w
                heapq.heappush(heap, (d + w, v))
    return dist

graph = {"S": [("A", 1), ("B", 5)], "A": [], "B": [("A", -10)]}
print(dijkstra_dist(graph, "S"))      # says A costs 1, but S -> B -> A costs 5 - 10 = -5
```

### Bellman-Ford: negative weights and negative cycles

**Bellman-Ford** simply relaxes **every** edge, V − 1 times. A shortest path uses at most V − 1 edges, and after round i every path of up to i edges has been found. It's slower, **O(V × E)**, but handles negative weights.

If a V-th round still improves something, there's a **negative cycle**: a loop whose total is negative, so going round it again and again makes the cost fall forever. "Shortest path" then has no answer (currency-exchange arbitrage is exactly this).

```python
def bellman_ford(n, edges, start):          # edges: (u, v, w), directed
    INF = float("inf")
    dist = [INF] * n
    dist[start] = 0
    for _ in range(n - 1):
        changed = False
        for u, v, w in edges:
            if dist[u] != INF and dist[u] + w < dist[v]:
                dist[v] = dist[u] + w
                changed = True
        if not changed:
            break                            # nothing improved: already final
    for u, v, w in edges:                    # one more round: any improvement means a negative cycle
        if dist[u] != INF and dist[u] + w < dist[v]:
            return None
    return dist

print(bellman_ford(4, [(0, 1, 5), (0, 2, 4), (2, 1, -3), (1, 3, 2)], 0))
print(bellman_ford(3, [(0, 1, 1), (1, 2, -2), (2, 1, 1)], 0))
```

Bellman-Ford also answers "cheapest route using **at most k edges**" (at most k − 1 stopovers): run only k rounds, and relax from a **copy** of the previous round's distances so that one round can't chain several edges together. That's the next-but-one exercise.

### Floyd-Warshall: every pair at once

To know the shortest distance between **all pairs** of vertices, **Floyd-Warshall** tries every vertex k as a possible stopover: if going i → k → j beats the best i → j so far, take it. Three nested loops, with **k outermost**: O(V³) time, O(V²) space. Fine for a few hundred vertices; it handles negative edges, and a negative value on the diagonal (`dist[i][i] < 0`) reveals a negative cycle.

```python
INF = float("inf")

def floyd_warshall(n, edges):
    dist = [[0 if i == j else INF for j in range(n)] for i in range(n)]
    for u, v, w in edges:
        dist[u][v] = min(dist[u][v], w)
    for k in range(n):                     # allow k as a stopover
        for i in range(n):
            for j in range(n):
                if dist[i][k] + dist[k][j] < dist[i][j]:
                    dist[i][j] = dist[i][k] + dist[k][j]
    return dist

for row in floyd_warshall(4, [(0, 1, 3), (1, 2, 1), (0, 2, 7), (2, 3, 2), (3, 0, 4)]):
    print(row)
```

### A* search: Dijkstra with a sense of direction

Dijkstra spreads out evenly in every direction. When you only need **one** goal and can **estimate** the remaining distance, **A\*** orders the heap by **f = g + h**: g is the known cost so far and h is a **heuristic** guess of the cost to the goal. If h never overestimates (it's **admissible**), A\* still finds the shortest path, while exploring far fewer vertices. On a grid with 4-way moves, the **Manhattan distance** |Δrow| + |Δcol| is admissible. With h = 0, A\* is exactly Dijkstra.

```python
import heapq

def search(grid, start, goal, use_heuristic):
    rows, cols = len(grid), len(grid[0])
    def h(r, c):                                   # Manhattan distance: never overestimates on a 4-way grid
        return abs(r - goal[0]) + abs(c - goal[1]) if use_heuristic else 0
    g = {start: 0}
    heap = [(h(*start), h(*start), start)]         # (f = g + h, h to break ties, cell)
    done, expanded = set(), 0
    while heap:
        f, _, cell = heapq.heappop(heap)
        if cell in done:
            continue                               # stale entry
        if cell == goal:
            return g[cell], expanded
        done.add(cell)
        expanded += 1
        r, c = cell
        for nr, nc in ((r + 1, c), (r - 1, c), (r, c + 1), (r, c - 1)):
            if 0 <= nr < rows and 0 <= nc < cols and grid[nr][nc] != "#":
                ng = g[cell] + 1
                if ng < g.get((nr, nc), float("inf")):
                    g[(nr, nc)] = ng
                    heapq.heappush(heap, (ng + h(nr, nc), h(nr, nc), (nr, nc)))
    return -1, expanded

grid = ["." * 40 for _ in range(40)]
grid[20] = "#" * 30 + "." * 10                    # a wall with a gap on the right
for name, flag in [("Dijkstra", False), ("A*", True)]:
    steps, expanded = search(grid, (0, 0), (39, 0), flag)
    print(f"{name:8} steps: {steps} | cells expanded: {expanded} of {40 * 40}")
```

Games, robots and map apps use A\* (and refinements of it). Its speed depends on the heuristic: the closer h is to the true remaining cost without exceeding it, the fewer vertices it explores.

### Choosing an algorithm

| Situation | Algorithm | Time |
|---|---|---|
| Unweighted | BFS | O(V + E) |
| Weights 0 or 1 | 0-1 BFS | O(V + E) |
| Non-negative weights, one source | **Dijkstra** with a heap | O((V + E) log V) |
| Dense graph (E ≈ V²), non-negative | Dijkstra with an array scan instead of a heap | O(V²) |
| One source to one goal, good estimate available | **A\*** | depends on h; ≤ Dijkstra |
| Negative weights, or at most k edges | **Bellman-Ford** | O(V × E), or O(k × E) |
| DAG | relax in topological order | O(V + E) |
| All pairs, V up to a few hundred | **Floyd-Warshall** | O(V³) |

:::exercise Network delay time
A signal is sent from node `k` in a network of `n` nodes labelled `1` to `n`. `times` is a list of directed edges `(u, v, w)`: a signal takes `w` time units (w ≥ 1) to travel from u to v. Write `network_delay(times, n, k)` returning how long it takes for **all** nodes to receive the signal, or `-1` if some node never does. It must be fast on sparse networks: 50,000 nodes and 150,000 edges in well under a second.
```python starter
import heapq

def network_delay(times, n, k):
    pass

print(network_delay([(2, 1, 1), (2, 3, 1), (3, 4, 1)], 4, 2))   # 2
```
```python check
import heapq
fn = need("network_delay")
test(fn, cases=[
    (([(2, 1, 1), (2, 3, 1), (3, 4, 1)], 4, 2), 2, "the example"),
    (([(1, 2, 1)], 2, 1), 1, "one edge"),
    (([(1, 2, 1)], 2, 2), -1, "edges only go one way"),
    (([], 1, 1), 0, "a single node"),
    (([(1, 2, 10), (1, 3, 1), (3, 2, 2)], 3, 1), 3, "the direct edge isn't the fastest"),
    (([(1, 2, 1), (2, 3, 2), (1, 3, 4), (3, 4, 1), (4, 5, 1)], 5, 1), 5, "a longer chain"),
    (([(1, 2, 1), (1, 2, 5), (2, 3, 1)], 3, 1), 2, "duplicate edges with different weights"),
    (([(1, 2, 1), (3, 4, 1)], 4, 1), -1, "an unreachable part"),
])
import random as _random
def _make(n):
    rng = _random.Random(n)
    times = [(rng.randint(1, v - 1), v, rng.randint(1, 100)) for v in range(2, n + 1)]
    times += [(rng.randint(1, n), rng.randint(1, n), rng.randint(1, 100)) for _ in range(2 * n)]
    return (times, n, 1)
def _ref(times, n, k):
    g = [[] for _ in range(n + 1)]
    for u, v, w in times: g[u].append((v, w))
    dist, h = [None] * (n + 1), [(0, k)]
    while h:
        d, u = heapq.heappop(h)
        if dist[u] is not None: continue
        dist[u] = d
        for v, w in g[u]:
            if dist[v] is None: heapq.heappush(h, (d + w, v))
    return -1 if any(x is None for x in dist[1:]) else max(dist[1:])
speed(fn, _make, _ref, sizes=(1_000, 4_000, 50_000), what="nodes (and 3 edges per node)",
      tip="Scanning every node to find the closest unvisited one is O(V^2), which is slow on a sparse network. Keep (distance, node) pairs in a heapq min-heap instead, skipping pairs for nodes that are already done.")
```
```python solution
import heapq

def network_delay(times, n, k):
    graph = [[] for _ in range(n + 1)]          # nodes are 1..n; index 0 unused
    for u, v, w in times:
        graph[u].append((v, w))
    dist = {}                                    # final arrival time of each node
    heap = [(0, k)]
    while heap:
        t, u = heapq.heappop(heap)
        if u in dist:
            continue                             # already reached sooner
        dist[u] = t
        for v, w in graph[u]:
            if v not in dist:
                heapq.heappush(heap, (t + w, v))
    return max(dist.values()) if len(dist) == n else -1

print(network_delay([(2, 1, 1), (2, 3, 1), (3, 4, 1)], 4, 2))
```
```python slow
def network_delay(times, n, k):
    graph = [[] for _ in range(n + 1)]
    for u, v, w in times:
        graph[u].append((v, w))
    INF = float("inf")
    dist = [INF] * (n + 1)
    dist[k] = 0
    done = [False] * (n + 1)
    for _ in range(n):
        u, best = -1, INF
        for i in range(1, n + 1):                # O(V) scan for the closest node, every step
            if not done[i] and dist[i] < best:
                u, best = i, dist[i]
        if u == -1:
            break
        done[u] = True
        for v, w in graph[u]:
            dist[v] = min(dist[v], dist[u] + w)
    worst = max(dist[1:])
    return -1 if worst == INF else worst
```
hint: Each node receives the signal at its shortest-path distance from k. Which algorithm gives shortest distances with positive weights?
hint: Dijkstra with a min-heap of `(time, node)`. The answer is the largest of the shortest times, or −1 if some node was never reached.
hint: Build `graph[u].append((v, w))`. Pop the smallest `(t, u)`; skip it if `u` is already in `dist`; otherwise set `dist[u] = t` and push `(t + w, v)` for each edge. At the end, check `len(dist) == n`.
approach:
1. **Understand:** directed edges, nodes 1..n, positive weights, duplicates possible; all nodes must be reached.
2. **Examples:** from 2: nodes 1 and 3 at time 1, node 4 at time 2 → 2.
3. **Brute force:** Dijkstra that scans all nodes to find the next closest one: O(V²), or Bellman-Ford O(V × E).
4. **Pattern:** **Dijkstra with a heap** (lazy deletion).
5. **Plan:** adjacency list; heap from k; settle each node once; answer = max of the settled times.
6. **Code and test:** a single node, one-way edges, a cheaper indirect route, duplicate edges.
walkthrough:
**Line by line**

- The adjacency list stores `(neighbour, weight)` pairs; nodes are 1-based, so the list has n + 1 slots.
- The heap always pops the smallest arrival time among the candidates.
- A node's first pop is its true shortest time: everything popped later is at least as late, and weights are positive.
- Later (larger) pops for the same node are stale and skipped.
- If fewer than n nodes were settled, some node is unreachable.

**Trace** on [(1, 2, 10), (1, 3, 1), (3, 2, 2)], n = 3, k = 1:

| popped (t, u) | settled | pushed |
|---|---|---|
| (0, 1) | 1 at 0 | (10, 2), (1, 3) |
| (1, 3) | 3 at 1 | (3, 2) |
| (3, 2) | 2 at 3 | — |
| (10, 2) | stale, skipped | — |

The largest time is 3.

**Complexity:** O((V + E) log V) time, O(V + E) space.

**Common wrong approach:** BFS that ignores weights, which would reach node 2 directly at time 10.
:::

:::exercise Cheapest flights within k stops
There are `n` cities `0` to `n − 1` and `flights` given as `(from, to, price)`. Write `cheapest_flight(n, flights, src, dst, k)` returning the cheapest price from `src` to `dst` using **at most `k` stops** (so at most k + 1 flights), or `-1` if there's no such route.
```python starter
def cheapest_flight(n, flights, src, dst, k):
    pass

flights = [(0, 1, 100), (1, 2, 100), (2, 0, 100), (1, 3, 600), (2, 3, 200)]
print(cheapest_flight(4, flights, 0, 3, 1))   # 700: 0 -> 1 -> 3 (0 -> 1 -> 2 -> 3 is cheaper but has 2 stops)
```
```python check
fn = need("cheapest_flight")
_f = [(0, 1, 100), (1, 2, 100), (2, 0, 100), (1, 3, 600), (2, 3, 200)]
test(fn, cases=[
    ((4, _f, 0, 3, 1), 700, "one stop allowed"),
    ((4, _f, 0, 3, 2), 400, "two stops allowed"),
    ((3, [(0, 1, 100), (1, 2, 100), (0, 2, 500)], 0, 2, 0), 500, "no stops: direct flights only"),
    ((3, [(0, 1, 100), (1, 2, 100)], 0, 2, 0), -1, "no direct flight"),
    ((2, [(0, 1, 5)], 1, 0, 3), -1, "flights are one way"),
    ((4, [(0, 1, 1), (0, 2, 5), (1, 2, 1), (2, 3, 1)], 0, 3, 1), 6, "the cheaper route needs too many stops"),
    ((5, [(0, 1, 5), (1, 2, 5), (0, 3, 2), (3, 1, 2), (1, 4, 1)], 0, 2, 2), 9, "a cheaper way into a middle city"),
])
```
```python solution
def cheapest_flight(n, flights, src, dst, k):
    INF = float("inf")
    cost = [INF] * n
    cost[src] = 0
    for _ in range(k + 1):                      # k stops = at most k + 1 flights = k + 1 rounds
        prev = cost[:]                          # this round may only extend last round's routes
        for u, v, price in flights:
            if prev[u] != INF and prev[u] + price < cost[v]:
                cost[v] = prev[u] + price
    return cost[dst] if cost[dst] != INF else -1

flights = [(0, 1, 100), (1, 2, 100), (2, 0, 100), (1, 3, 600), (2, 3, 200)]
print(cheapest_flight(4, flights, 0, 3, 1))
```
hint: Plain Dijkstra finds the cheapest route but ignores the limit on the number of flights. Which algorithm builds routes one edge at a time?
hint: Bellman-Ford: after round i, every route with up to i flights is known. So run exactly k + 1 rounds.
hint: In each round, relax every flight using a **copy** of the costs from the previous round (`prev = cost[:]`), so a single round can't chain two flights together. Return `cost[dst]`, or −1 if it's still infinity.
approach:
1. **Understand:** k stops means up to k + 1 flights; one-way flights; −1 if impossible.
2. **Examples:** k = 1 → 700 via city 1; k = 2 → 400 via 1 and 2.
3. **Brute force:** DFS over every route of up to k + 1 flights: exponential.
4. **Pattern:** **Bellman-Ford with a limited number of rounds** (dynamic programming over "flights used").
5. **Plan:** costs start at infinity except src; k + 1 rounds relaxing from the previous round's copy.
6. **Code and test:** k = 0, one-way flights, a cheap route with too many stops.
walkthrough:
**Line by line**

- `cost[c]` is the cheapest price to reach c using at most the number of flights processed so far.
- `prev = cost[:]` freezes the previous round. Relaxing from `prev` means each round adds at most **one** flight to any route; relaxing from `cost` itself could use 0 → 1 and then 1 → 3 in the same round.
- After k + 1 rounds, `cost[dst]` is the cheapest price with at most k + 1 flights.

**Trace** on the example with k = 1 (two rounds):

| round | cost of cities 0, 1, 2, 3 |
|---|---|
| start | 0, ∞, ∞, ∞ |
| 1 (one flight) | 0, 100, ∞, ∞ |
| 2 (two flights) | 0, 100, 200, **700** |

The route 0 → 1 → 2 → 3 (400) would need a third round, which k = 1 doesn't allow.

**Complexity:** O(k × E) time, O(n) space.

**Common wrong approach:** relaxing in place without the `prev` copy, which lets a round use several flights and breaks the stop limit.
:::

:::quiz
? Why can't Dijkstra's algorithm handle negative edge weights?
+ It finalises a vertex once popped, but a later negative edge could make that vertex cheaper
- Heaps can't store negative numbers
- It would run forever
= Settled distances must never improve; negative edges break that guarantee.
? How do you handle a shorter distance for a vertex already in heapq, which has no decrease-key?
+ Push a new (distance, vertex) pair and skip stale pairs when they're popped
- Remove the old pair with list.remove
- Rebuild the heap
= This "lazy deletion" keeps each operation O(log n).
? How does Bellman-Ford detect a negative cycle?
+ An extra (V-th) round of relaxation still improves some distance
- A distance becomes zero
- The graph has more edges than vertices
= After V − 1 rounds, all shortest paths are final unless a negative cycle exists.
? When is A* guaranteed to find a shortest path?
+ When its heuristic never overestimates the remaining cost
- Always
- Only on trees
= An admissible heuristic (like Manhattan distance on a 4-way grid) keeps it correct.
:::

@@@ lesson
id: union-find-mst
title: Union-find and minimum spanning trees
minutes: 26
summary: The disjoint set union (union-find) structure with path compression and union by size, counting components and finding cycles as edges arrive, minimum spanning trees, Kruskal's and Prim's algorithms, and clustering with an MST.
---
Some questions are about **groups** that keep merging: "are these two computers on the same network yet?", "after these friendships, how many friend circles are there?", "does this new road create a loop?". A **union-find** (or **disjoint set union**, DSU) structure answers them in almost O(1) per operation.

### Union-find

Each group is stored as a small tree, and the **root** of the tree names the group. Every element has a `parent`; a root is its own parent.

- **find(x):** follow parents up to the root.
- **union(a, b):** find both roots; if they differ, hang one root under the other.

Two tricks keep the trees almost flat:

- **Union by size:** hang the **smaller** tree under the larger one, so trees stay shallow (height at most log n).
- **Path compression:** after a find, point every node on the path straight at the root, so the next find is one step.

![Union-find as a forest. Left: the group {0, 1, 2, 3, 4} is a tree with root 0, where 4 → 3 → 1 → 0 is a long path, and the group {5, 6} has root 5. Right: after find(4) with path compression, 4, 3 and 1 all point directly at the root 0](figures/union-find.svg)

```python
class DSU:
    def __init__(self, n):
        self.parent = list(range(n))      # each element starts alone, as its own root
        self.size = [1] * n
        self.groups = n

    def find(self, x):
        root = x
        while self.parent[root] != root:
            root = self.parent[root]
        while self.parent[x] != root:     # path compression: point everything on the path at the root
            self.parent[x], x = root, self.parent[x]
        return root

    def union(self, a, b):
        ra, rb = self.find(a), self.find(b)
        if ra == rb:
            return False                  # already in the same group
        if self.size[ra] < self.size[rb]:
            ra, rb = rb, ra
        self.parent[rb] = ra              # union by size: the smaller tree goes under the larger
        self.size[ra] += self.size[rb]
        self.groups -= 1
        return True

d = DSU(7)
for a, b in [(0, 1), (1, 2), (3, 4), (5, 6), (2, 4)]:
    d.union(a, b)
print("groups:", d.groups)
print("0 and 3 connected?", d.find(0) == d.find(3), "| 0 and 5?", d.find(0) == d.find(5))
print("size of 0's group:", d.size[d.find(0)])
```

With both tricks, any sequence of m operations on n elements takes O(m · α(n)) time, where α is the **inverse Ackermann function**: it's at most 4 for any n you could ever store, so each operation is effectively O(1). The `find` above is a loop rather than recursion, so long chains can't hit the recursion limit.

### What union-find is good at

| Problem | How |
|---|---|
| Count connected components as edges arrive | start with n groups; each successful union removes one |
| Find the edge that creates a cycle (undirected) | `union` returns False: both ends were already connected |
| Group equal things: accounts sharing an email, synonyms, equations like a = b | union every pair that must be together |
| Kruskal's minimum spanning tree | add the cheapest edges that join different groups |
| Percolation, image segmentation, "islands" that appear one cell at a time | union neighbouring cells as they're added |

Union-find can only **merge**; it can't split groups apart. BFS/DFS is better when the graph is fixed and you need paths, not just "same group?".

### Minimum spanning trees

A **spanning tree** connects all V vertices of a connected, undirected, weighted graph using exactly V − 1 edges and no cycles. A **minimum spanning tree (MST)** is one with the smallest total weight: the cheapest way to cable every building, pipe every house, or connect every server.

![A weighted graph of 5 vertices with 7 edges. The MST edges, highlighted, are A–B (1), B–C (2), C–D (3) and D–E (4), total 10. The heavier edges A–C (5), B–D (6) and C–E (7) are left out because each would close a cycle](figures/mst.svg)

Both classic algorithms rely on the **cut property**: for any split of the vertices into two sides, the cheapest edge crossing the split belongs to some MST. So it's always safe to take the cheapest edge that connects something new.

### Kruskal's algorithm

Sort all edges by weight; go through them cheapest first, and keep an edge only if it joins two **different** groups (union-find says so). Stop at V − 1 edges.

```python
def kruskal(n, edges):                     # edges: (weight, u, v)
    parent = list(range(n))
    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]  # path halving: a simpler form of path compression
            x = parent[x]
        return x
    total, chosen = 0, []
    for w, u, v in sorted(edges):
        ru, rv = find(u), find(v)
        if ru != rv:                       # joins two separate groups: no cycle
            parent[ru] = rv
            total += w
            chosen.append((u, v, w))
            if len(chosen) == n - 1:
                break
    return total, chosen

A, B, C, D, E = range(5)
edges = [(1, A, B), (2, B, C), (3, C, D), (4, D, E), (5, A, C), (6, B, D), (7, C, E)]
print(kruskal(5, edges))
```

**Cost:** sorting dominates, O(E log E). Kruskal is natural when you already have an edge list.

### Prim's algorithm

Grow **one** tree from any start vertex. Keep a heap of edges leaving the tree; repeatedly take the cheapest edge that reaches a vertex **not yet in the tree**. It's Dijkstra's shape, but the heap key is the single edge weight, not the distance from the start.

```python
import heapq

def prim(n, adj, start=0):                 # adj[u] = [(v, w), ...], undirected
    in_tree = [False] * n
    heap = [(0, start)]
    total, added = 0, 0
    while heap and added < n:
        w, u = heapq.heappop(heap)
        if in_tree[u]:
            continue                       # stale: u already joined more cheaply
        in_tree[u] = True
        total += w
        added += 1
        for v, wt in adj[u]:
            if not in_tree[v]:
                heapq.heappush(heap, (wt, v))
    return total if added == n else None   # None: the graph isn't connected

adj = [[] for _ in range(5)]
for w, u, v in [(1, 0, 1), (2, 1, 2), (3, 2, 3), (4, 3, 4), (5, 0, 2), (6, 1, 3), (7, 2, 4)]:
    adj[u].append((v, w))
    adj[v].append((u, w))
print(prim(5, adj))
```

**Cost:** O(E log V) with a heap. For a **dense** graph, such as "connect these n points, any two can be joined", there are about n²/2 edges; a heap-free Prim that keeps each outside vertex's cheapest link in an array and scans it is O(V²), the best possible there (the second exercise).

### Clustering with an MST

Run Kruskal but **stop early**, when k groups remain: you've split the points into k clusters, merging the closest ones first. That's **single-linkage hierarchical clustering**, a classic unsupervised learning method; the MST edges are the merge steps of its dendrogram.

:::exercise Redundant connection
A tree with `n` nodes (labelled `1` to `n`) had **one** extra edge added. `edges` lists all n edges as pairs. Write `redundant_connection(edges)` returning the edge that can be removed to leave a tree; if there are several answers, return the one that appears **last** in `edges`. Return it as a list `[u, v]`, as given. It must handle 100,000 edges quickly.
```python starter
def redundant_connection(edges):
    pass

print(redundant_connection([[1, 2], [1, 3], [2, 3]]))                    # [2, 3]
print(redundant_connection([[1, 2], [2, 3], [3, 4], [1, 4], [1, 5]]))    # [1, 4]
```
```python check
fn = need("redundant_connection")
test(fn, key=lambda e: list(e) if isinstance(e, (list, tuple)) else e, cases=[
    (([[1, 2], [1, 3], [2, 3]],), [2, 3], "a triangle"),
    (([[1, 2], [2, 3], [3, 4], [1, 4], [1, 5]],), [1, 4], "a square with a tail"),
    (([[1, 2], [2, 1]],), [2, 1], "the same edge twice"),
    (([[3, 4], [1, 2], [2, 4], [3, 5], [2, 5]],), [2, 5], "edges in no particular order"),
    (([[1, 4], [3, 4], [1, 3], [1, 2], [4, 5]],), [1, 3], "the cycle closes in the middle of the list"),
])
def _make(n):
    edges = [[i, i + 1] for i in range(1, n)]
    edges.append([1, n])
    return (edges,)
def _ref(edges):
    parent = list(range(len(edges) + 1))
    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]; x = parent[x]
        return x
    for u, v in edges:
        ru, rv = find(u), find(v)
        if ru == rv: return [u, v]
        parent[ru] = rv
speed(fn, _make, _ref, sizes=(1_000, 2_500, 100_000), what="edges",
      key=lambda e: list(e) if isinstance(e, (list, tuple)) else e,
      tip="Searching the graph for a path before adding each edge is O(n^2). Union-find answers \"already connected?\" in near O(1): the first edge whose ends share a root is the answer.")
```
```python solution
def redundant_connection(edges):
    parent = list(range(len(edges) + 1))     # nodes 1..n, and there are n edges

    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]    # path halving keeps the trees flat
            x = parent[x]
        return x

    for u, v in edges:
        ru, rv = find(u), find(v)
        if ru == rv:
            return [u, v]                    # u and v were already connected: this edge closes a cycle
        parent[ru] = rv
    return []

print(redundant_connection([[1, 2], [1, 3], [2, 3]]))
print(redundant_connection([[1, 2], [2, 3], [3, 4], [1, 4], [1, 5]]))
```
```python slow
from collections import deque

def redundant_connection(edges):
    graph = {}
    for u, v in edges:
        seen, queue = {u}, deque([u])         # BFS to see whether u already reaches v
        while queue:
            x = queue.popleft()
            if x == v:
                return [u, v]
            for y in graph.get(x, []):
                if y not in seen:
                    seen.add(y)
                    queue.append(y)
        graph.setdefault(u, []).append(v)
        graph.setdefault(v, []).append(u)
    return []
```
hint: Add the edges one at a time. Which edge is the first to connect two nodes that were **already** connected?
hint: A tree plus one edge has exactly one cycle, and the edge that closes it while scanning left to right is the last edge of that cycle in the list. Union-find tells you whether two nodes are already in the same group.
hint: `parent = list(range(n + 1))` with an iterative `find`. For each edge, if `find(u) == find(v)` return it; otherwise `parent[find(u)] = find(v)`.
approach:
1. **Understand:** exactly one extra edge, so exactly one cycle; nodes are 1..n with n = len(edges); return the latest edge of the cycle.
2. **Examples:** the triangle → [2, 3]; the square → [1, 4].
3. **Brute force:** before adding each edge, BFS/DFS to see whether its ends are already connected: O(n²).
4. **Pattern:** **union-find** (cycle detection in an undirected graph as edges arrive).
5. **Plan:** DSU over 1..n; the first edge whose ends share a root is the answer.
6. **Code and test:** a doubled edge, unordered edges, the cycle closing mid-list.
walkthrough:
**Line by line**

- `parent` has n + 1 entries so node labels 1..n can be used directly as indexes.
- `find` follows parents to the root, halving the path as it goes.
- Equal roots mean u and v are already connected, so this edge closes the cycle. Since we scan in order, it's the cycle edge that appears last.
- Otherwise the edge merges two groups.

**Trace** on [[1, 2], [2, 3], [3, 4], [1, 4], [1, 5]]:

| edge | find(u), find(v) | action |
|---|---|---|
| [1, 2] | 1, 2 | merge |
| [2, 3] | 2, 3 | merge |
| [3, 4] | 3, 4 | merge |
| [1, 4] | 4, 4 | same group: return [1, 4] |

**Complexity:** O(n · α(n)), effectively O(n), time; O(n) space.

**Common wrong approach:** returning the first edge that touches an already-seen **node**. Seeing a node before doesn't mean a cycle; only connecting two nodes of the same group does.
:::

:::exercise Connect all points
`points` is a list of `[x, y]` integer coordinates. Joining two points costs their Manhattan distance `|x1 − x2| + |y1 − y2|`. Write `min_cost_connect(points)` returning the minimum total cost to connect all the points (so every point can reach every other).
```python starter
def min_cost_connect(points):
    pass

print(min_cost_connect([[0, 0], [2, 2], [3, 10], [5, 2], [7, 0]]))   # 20
```
```python check
fn = need("min_cost_connect")
test(fn, cases=[
    (([[0, 0], [2, 2], [3, 10], [5, 2], [7, 0]],), 20, "the example"),
    (([[3, 12], [-2, 5], [-4, 1]],), 18, "negative coordinates"),
    (([[0, 0]],), 0, "a single point"),
    (([[0, 0], [1, 1]],), 2, "two points"),
    (([[0, 0], [1, 0], [2, 0], [3, 0]],), 3, "points on a line"),
    (([[-1000000, -1000000], [1000000, 1000000]],), 4000000, "far apart"),
])
```
```python solution
def min_cost_connect(points):
    n = len(points)
    INF = float("inf")
    best = [INF] * n            # cheapest known link from each point into the tree
    in_tree = [False] * n
    best[0] = 0
    total = 0
    for _ in range(n):          # Prim's algorithm for a dense graph: O(n^2), no heap
        u = min((i for i in range(n) if not in_tree[i]), key=best.__getitem__)
        in_tree[u] = True
        total += best[u]
        ux, uy = points[u]
        for v in range(n):      # u joined the tree: maybe it offers some points a cheaper link
            if not in_tree[v]:
                d = abs(ux - points[v][0]) + abs(uy - points[v][1])
                if d < best[v]:
                    best[v] = d
    return total

print(min_cost_connect([[0, 0], [2, 2], [3, 10], [5, 2], [7, 0]]))
```
hint: "Connect everything at minimum total cost" is a minimum spanning tree. Every pair of points can be joined, so the graph is complete: about n²/2 edges.
hint: Kruskal works (build all pairs, sort them, union-find), at O(n² log n). Prim without a heap fits a complete graph better: keep, for each point outside the tree, the cheapest link into the tree.
hint: `best = [inf] * n; best[0] = 0`. Repeat n times: pick the outside point with the smallest `best`, add `best[u]` to the total, mark it in the tree, and lower `best[v]` for every outside point v using the distance from u.
approach:
1. **Understand:** any point can link to any other; cost is Manhattan distance; one point costs 0.
2. **Examples:** the example's MST costs 20.
3. **Brute force:** try every spanning tree: hopeless. All pairs + Kruskal: O(n² log n), acceptable.
4. **Pattern:** **minimum spanning tree**; for a dense graph, **array-based Prim** in O(n²).
5. **Plan:** `best` array, n rounds of "pick the cheapest outside point, update the others".
6. **Code and test:** one point, collinear points, huge coordinates.
walkthrough:
**Line by line**

- `best[v]` is the cheapest edge from v to any point already in the tree; point 0 starts the tree at cost 0.
- Each round picks the outside point with the smallest `best` (the cut property says that edge is safe) and adds its cost.
- Then the newly added point may be closer to some outside points, so their `best` values are lowered.
- After n rounds every point is in the tree.

**Trace** on [[0, 0], [1, 0], [2, 0], [3, 0]]:

| round | point added | cost | best afterwards (for points 0–3) |
|---|---|---|---|
| 1 | 0 | 0 | –, 1, 2, 3 |
| 2 | 1 | 1 | –, –, 1, 2 |
| 3 | 2 | 1 | –, –, –, 1 |
| 4 | 3 | 1 | total 3 |

**Complexity:** O(n²) time, O(n) space; with n²/2 edges there's no faster way to look at them all.

**Common wrong approach:** connecting each point to its nearest neighbour. That can leave separate clusters unconnected, and it isn't an MST.
:::

:::quiz
? What do path compression and union by size give union-find?
+ Nearly O(1) amortised time per operation (O(α(n)))
- O(log n) per operation in the worst case, at best
- The ability to split groups
= α(n), the inverse Ackermann function, is at most 4 in practice.
? How does union-find detect a cycle as undirected edges are added?
+ The edge's two ends already have the same root
- A node gets a second parent
- The number of groups goes up
= If u and v are already connected, adding u–v closes a loop.
? How many edges does a spanning tree of a connected graph with V vertices have?
+ V − 1
- V
- E − 1
= Any fewer can't connect everything; any more creates a cycle.
? Which algorithm builds an MST by sorting all edges and adding the cheapest ones that don't form a cycle?
+ Kruskal's algorithm
- Prim's algorithm
- Dijkstra's algorithm
= Prim instead grows a single tree from a start vertex.
:::

@@@ lesson
id: advanced-graphs
title: Advanced graph algorithms
minutes: 28
summary: Bipartite graphs and two-colouring, cycles in undirected graphs, strongly connected components (Kosaraju), bridges and articulation points (Tarjan's low-link values), Eulerian paths (Hierholzer), maximum flow and minimum cut (Edmonds-Karp), and which graph problems have no fast solution.
---
This lesson collects the graph algorithms that show up in harder interviews and real systems. Each is built from the same pieces you already know: BFS, DFS and careful bookkeeping.

### Bipartite graphs: two-colouring

A graph is **bipartite** if its vertices can be split into two sides so that every edge goes **between** the sides: students and courses, job seekers and jobs. Equivalently, you can colour it with two colours so no edge joins two vertices of the same colour, which is possible exactly when the graph has **no odd-length cycle**.

![Two graphs. Left: a square 0–1–2–3–0 coloured alternately blue and orange: bipartite. Right: a triangle 0–1–2: after colouring 0 blue and 1 orange, vertex 2 is joined to both, so no colour works: not bipartite](figures/bipartite.svg)

BFS from each uncoloured vertex, giving each neighbour the **opposite** colour; meeting a neighbour that already has the **same** colour proves it's not bipartite. That's the first exercise.

### Cycles in an undirected graph

In an undirected graph every edge appears twice (u → v and v → u), so seeing your parent again isn't a cycle. Any **other** already-visited neighbour is. (Union-find, Lesson 39, is the other easy way.)

```python
def has_cycle_undirected(n, edges):
    graph = [[] for _ in range(n)]
    for u, v in edges:
        graph[u].append(v)
        graph[v].append(u)
    seen = set()
    for start in range(n):
        if start in seen:
            continue
        seen.add(start)
        stack = [(start, -1)]                 # (vertex, the vertex we came from)
        while stack:
            u, parent = stack.pop()
            for v in graph[u]:
                if v == parent:
                    continue                  # the edge we just walked along
                if v in seen:
                    return True               # reached a seen vertex another way: a loop
                seen.add(v)
                stack.append((v, u))
    return False

print(has_cycle_undirected(4, [(0, 1), (1, 2), (2, 3)]), has_cycle_undirected(4, [(0, 1), (1, 2), (2, 0), (2, 3)]))
```

(For directed graphs, use the three colours or Kahn's algorithm from Lesson 37.)

### Strongly connected components

In a **directed** graph, a **strongly connected component (SCC)** is a maximal group where every vertex can reach every other: a set of web pages that all link to each other in a loop, or accounts that all transfer money around a ring. Shrinking each SCC to a single vertex always leaves a DAG.

**Kosaraju's algorithm** uses two DFS passes:

1. DFS the graph and record vertices in order of **finishing**.
2. **Reverse** every edge. Take vertices in **reverse** finishing order; each DFS on the reversed graph from an unvisited vertex collects exactly one SCC.

```python
def kosaraju(n, edges):
    graph = [[] for _ in range(n)]
    rev = [[] for _ in range(n)]
    for u, v in edges:
        graph[u].append(v)
        rev[v].append(u)

    order, seen = [], [False] * n             # pass 1: finishing order, with an explicit stack
    for s in range(n):
        if seen[s]:
            continue
        seen[s] = True
        stack = [(s, iter(graph[s]))]
        while stack:
            u, it = stack[-1]
            for v in it:
                if not seen[v]:
                    seen[v] = True
                    stack.append((v, iter(graph[v])))
                    break
            else:                             # no unvisited neighbours left: u is finished
                stack.pop()
                order.append(u)

    comps, seen = [], [False] * n             # pass 2: reversed graph, latest finisher first
    for s in reversed(order):
        if seen[s]:
            continue
        seen[s], comp, stack = True, [], [s]
        while stack:
            u = stack.pop()
            comp.append(u)
            for v in rev[u]:
                if not seen[v]:
                    seen[v] = True
                    stack.append(v)
        comps.append(sorted(comp))
    return comps

print(kosaraju(8, [(0, 1), (1, 2), (2, 0), (2, 3), (3, 4), (4, 5), (5, 3), (6, 5), (6, 7), (7, 6)]))
```

O(V + E). **Tarjan's algorithm** finds SCCs in one DFS using the low-link values described next. SCCs are used to solve **2-SAT** problems, simplify dependency graphs, and find groups in social networks.

### Bridges and articulation points

A **bridge** is an edge whose removal disconnects the graph; an **articulation point** (cut vertex) is a vertex whose removal does. They are the single points of failure of a network.

**Tarjan's low-link method:** in a DFS, give each vertex its discovery time `disc[v]`, and compute `low[v]`, the earliest discovery time reachable from v's subtree using at most one **back edge** (an edge to an ancestor). For a tree edge u → v:

- if `low[v] > disc[u]`, nothing below v can climb back to u or above, so **u–v is a bridge**;
- if `low[v] >= disc[u]` (and u isn't the root), **u is an articulation point**; the root is one if it has two or more DFS children.

![A graph made of two triangles, 0–1–2 and 3–4–5, joined by the single edge 1–3. That edge is a bridge, and vertices 1 and 3 are articulation points; the triangle edges are not bridges because each lies on a cycle](figures/bridges.svg)

The recursive version is the clearest; the second exercise asks you to write it.

### Eulerian paths: every edge exactly once

An **Eulerian path** uses every **edge** exactly once (drawing a figure without lifting the pen; a postman covering every street). In a connected undirected graph it exists when 0 or 2 vertices have odd degree (with 2, it must start at one of them). In a directed graph, every vertex needs in-degree = out-degree, except possibly a start (one extra out) and an end (one extra in).

**Hierholzer's algorithm** walks unused edges until stuck, then backs up, adding vertices to the route as it backs out. O(E).

```python
from collections import defaultdict

def itinerary(tickets, start):                # directed Eulerian path, smallest names first
    graph = defaultdict(list)
    for a, b in sorted(tickets, reverse=True):
        graph[a].append(b)                    # reverse-sorted, so pop() takes the smallest
    route, stack = [], [start]
    while stack:
        while graph[stack[-1]]:
            stack.append(graph[stack[-1]].pop())   # follow an unused ticket
        route.append(stack.pop())             # stuck: this airport goes on the route (backwards)
    return route[::-1]

print(itinerary([("JFK", "SFO"), ("JFK", "ATL"), ("SFO", "ATL"), ("ATL", "JFK"), ("ATL", "SFO")], "JFK"))
```

A **Hamiltonian** path, visiting every **vertex** exactly once, sounds similar but is NP-complete (see the end of this lesson).

### Maximum flow and minimum cut

Treat each directed edge as a pipe with a **capacity**. How much can flow from a **source** s to a **sink** t per second? The **Ford-Fulkerson** idea: while there is a path from s to t with spare capacity (an **augmenting path**), push as much as its narrowest pipe allows. Pushing flow creates **reverse** capacity, so later paths can undo an earlier poor choice. Finding each augmenting path with BFS is the **Edmonds-Karp** algorithm, O(V × E²).

```python
from collections import deque

def max_flow(n, edges, s, t):
    cap = [[0] * n for _ in range(n)]
    adj = [set() for _ in range(n)]
    for u, v, c in edges:
        cap[u][v] += c
        adj[u].add(v)
        adj[v].add(u)                        # the reverse direction, for undoing flow
    flow = 0
    while True:
        parent = [-1] * n
        parent[s] = s
        queue = deque([s])
        while queue and parent[t] == -1:     # BFS for a path with spare capacity
            u = queue.popleft()
            for v in adj[u]:
                if parent[v] == -1 and cap[u][v] > 0:
                    parent[v] = u
                    queue.append(v)
        if parent[t] == -1:
            return flow                       # no augmenting path left
        push, v = float("inf"), t
        while v != s:                         # the narrowest pipe on the path
            push = min(push, cap[parent[v]][v])
            v = parent[v]
        v = t
        while v != s:
            cap[parent[v]][v] -= push
            cap[v][parent[v]] += push         # allow this flow to be undone later
            v = parent[v]
        flow += push

edges = [(0, 1, 10), (0, 2, 5), (1, 2, 15), (1, 3, 5), (2, 3, 10)]
print(max_flow(4, edges, 0, 3))
```

The **max-flow min-cut theorem** says the maximum flow equals the total capacity of the cheapest set of edges whose removal separates s from t. Flow algorithms also solve **bipartite matching** (assign workers to jobs: source → workers → jobs → sink, all capacities 1), image segmentation, and scheduling.

### Problems with no known fast algorithm

Some graph problems are **NP-hard**: no polynomial-time algorithm is known, and finding one would solve thousands of other hard problems. Recognise them so you don't waste time hunting for an O(V + E) trick:

| Problem | Typical approach |
|---|---|
| **Travelling salesman** (shortest tour through every vertex) | bitmask DP for n ≤ ~20 (Part 9), heuristics and approximation otherwise |
| **Hamiltonian path** (visit every vertex once) | backtracking or bitmask DP for small n |
| **Graph colouring** with the fewest colours | backtracking, greedy approximations |
| **Maximum clique / independent set** | backtracking with pruning, small n |

### Graph algorithms at a glance

| Task | Algorithm | Time |
|---|---|---|
| Reachability, components | DFS / BFS | O(V + E) |
| Unweighted shortest path | BFS | O(V + E) |
| Non-negative weighted shortest path | Dijkstra | O((V + E) log V) |
| Negative weights / negative cycles | Bellman-Ford | O(V · E) |
| All-pairs shortest paths | Floyd-Warshall | O(V³) |
| Dependency order, directed cycle check | topological sort | O(V + E) |
| Dynamic connectivity, undirected cycle check | union-find | ~O(1) per operation |
| Minimum spanning tree | Kruskal / Prim | O(E log E) / O(E log V) |
| Two-colouring | BFS / DFS | O(V + E) |
| Strongly connected components | Kosaraju / Tarjan | O(V + E) |
| Bridges, articulation points | Tarjan low-link | O(V + E) |
| Use every edge once | Hierholzer | O(E) |
| Maximum flow, bipartite matching | Edmonds-Karp | O(V · E²) |

:::exercise Is the graph bipartite?
`graph` is an adjacency list: `graph[u]` lists the neighbours of vertex `u` (vertices `0` to `n − 1`, undirected, possibly **disconnected**). Write `is_bipartite(graph)` returning `True` if the vertices can be split into two groups with every edge going between the groups.
```python starter
from collections import deque

def is_bipartite(graph):
    pass

print(is_bipartite([[1, 3], [0, 2], [1, 3], [0, 2]]))            # True: a square
print(is_bipartite([[1, 2, 3], [0, 2], [0, 1, 3], [0, 2]]))      # False: contains a triangle
```
```python check
fn = need("is_bipartite")
test(fn, cases=[
    (([[1, 3], [0, 2], [1, 3], [0, 2]],), True, "a square"),
    (([[1, 2, 3], [0, 2], [0, 1, 3], [0, 2]],), False, "a triangle inside"),
    (([[]],), True, "one vertex"),
    (([[1], [0], [3, 4], [2, 4], [2, 3]],), False, "the odd cycle is in the second piece"),
    (([[1], [0], [3], [2]],), True, "two separate edges"),
    (([[1, 4], [0, 2], [1, 3], [2, 4], [3, 0]],), False, "a pentagon (odd cycle)"),
    (([[1, 5], [0, 2], [1, 3], [2, 4], [3, 5], [4, 0]],), True, "a hexagon (even cycle)"),
    (([[], [2], [1]],), True, "an isolated vertex first"),
])
```
```python solution
from collections import deque

def is_bipartite(graph):
    colour = [None] * len(graph)
    for start in range(len(graph)):           # the graph may have several pieces
        if colour[start] is not None:
            continue
        colour[start] = 0
        queue = deque([start])
        while queue:
            u = queue.popleft()
            for v in graph[u]:
                if colour[v] is None:
                    colour[v] = 1 - colour[u] # neighbours get the opposite colour
                    queue.append(v)
                elif colour[v] == colour[u]:
                    return False              # an edge inside one colour: an odd cycle
    return True

print(is_bipartite([[1, 3], [0, 2], [1, 3], [0, 2]]))
print(is_bipartite([[1, 2, 3], [0, 2], [0, 1, 3], [0, 2]]))
```
hint: Try to colour each vertex with one of two colours so that neighbours always differ. When does that fail?
hint: Pick an uncoloured vertex, colour it 0, and BFS: every neighbour must get the other colour. If a neighbour already has the **same** colour as the current vertex, it's not bipartite.
hint: Keep `colour = [None] * n`. Loop over every start vertex (the graph may be disconnected); for an uncoloured one, colour it 0 and BFS, setting `colour[v] = 1 - colour[u]`, returning False on a clash.
approach:
1. **Understand:** undirected adjacency list; pieces may be disconnected; isolated vertices are fine.
2. **Examples:** a square → True; anything with a triangle → False.
3. **Brute force:** try all 2ⁿ ways to split the vertices: exponential.
4. **Pattern:** **two-colouring with BFS** (or DFS); a clash means an odd cycle.
5. **Plan:** colour array, BFS from every uncoloured vertex, opposite colours for neighbours.
6. **Code and test:** a disconnected graph whose second piece has an odd cycle, odd and even cycles.
walkthrough:
**Line by line**

- The outer loop makes sure every piece of a disconnected graph is checked, not just the piece containing vertex 0.
- Each piece starts with colour 0; its colouring is forced from there, because each neighbour must take the opposite colour.
- A neighbour with the same colour as `u` means an edge inside one group, so no split exists.

**Trace** on the pentagon [[1, 4], [0, 2], [1, 3], [2, 4], [3, 0]]:

| popped | colours set | clash? |
|---|---|---|
| 0 (colour 0) | 1 → 1, 4 → 1 | — |
| 1 (colour 1) | 2 → 0 | — |
| 4 (colour 1) | 3 → 0 | — |
| 2 (colour 0) | — | neighbour 3 also has colour 0: **False** |

**Complexity:** O(V + E) time, O(V) space.

**Common wrong approach:** only starting from vertex 0, which misses an odd cycle in another piece of the graph.
:::

:::exercise Critical connections (bridges)
A network has `n` servers `0` to `n − 1`, connected by undirected `connections` (pairs). Write `critical_connections(n, connections)` returning every connection whose removal would disconnect some servers, as a list of pairs in any order.
```python starter
def critical_connections(n, connections):
    pass

print(critical_connections(4, [[0, 1], [1, 2], [2, 0], [1, 3]]))   # [[1, 3]]
```
```python check
fn = need("critical_connections")
_norm = lambda pairs: sorted(tuple(sorted(p)) for p in pairs) if isinstance(pairs, (list, tuple)) else pairs
test(fn, key=_norm, cases=[
    ((4, [[0, 1], [1, 2], [2, 0], [1, 3]]), [[1, 3]], "a triangle with a tail"),
    ((2, [[0, 1]]), [[0, 1]], "a single connection"),
    ((3, [[0, 1], [1, 2], [2, 0]]), [], "a triangle: no bridges"),
    ((6, [[0, 1], [1, 2], [2, 0], [1, 3], [3, 4], [4, 5], [5, 3]]), [[1, 3]], "two triangles joined by one edge"),
    ((5, [[0, 1], [1, 2], [2, 3], [3, 4]]), [[0, 1], [1, 2], [2, 3], [3, 4]], "a chain: every edge is a bridge"),
    ((5, [[1, 0], [2, 0], [3, 2], [4, 2], [4, 3], [3, 0], [4, 0]]), [[0, 1]], "a dense part with one hanging server"),
])
```
```python solution
import sys

def critical_connections(n, connections):
    sys.setrecursionlimit(10_000)
    graph = [[] for _ in range(n)]
    for u, v in connections:
        graph[u].append(v)
        graph[v].append(u)
    disc = [-1] * n          # discovery time of each server in the DFS
    low = [0] * n            # earliest discovery time reachable from its subtree with one back edge
    bridges = []
    timer = 0

    def dfs(u, parent):
        nonlocal timer
        disc[u] = low[u] = timer
        timer += 1
        for v in graph[u]:
            if v == parent:
                continue                     # don't treat the edge we came along as a way back
            if disc[v] == -1:                # tree edge: explore v first
                dfs(v, u)
                low[u] = min(low[u], low[v])
                if low[v] > disc[u]:         # v's subtree can't climb back to u or above
                    bridges.append([u, v])
            else:                            # back edge to an ancestor
                low[u] = min(low[u], disc[v])

    for s in range(n):
        if disc[s] == -1:
            dfs(s, -1)
    return bridges

print(critical_connections(4, [[0, 1], [1, 2], [2, 0], [1, 3]]))
```
hint: An edge is critical exactly when it isn't on any cycle. Removing every edge in turn and checking connectivity works, but costs O(E × (V + E)). How can one DFS tell?
hint: In a DFS, record each vertex's discovery time `disc[v]` and `low[v]`: the earliest discovery time its subtree can reach through a single back edge. If `low[v] > disc[u]` for a tree edge u → v, nothing below v loops back, so u–v is a bridge.
hint: In `dfs(u, parent)`: set `disc[u] = low[u] = timer`. For each neighbour v ≠ parent: if unvisited, recurse, then `low[u] = min(low[u], low[v])` and test `low[v] > disc[u]`; if visited, `low[u] = min(low[u], disc[v])`.
approach:
1. **Understand:** undirected, possibly several pieces; a bridge is an edge on no cycle; any order of pairs.
2. **Examples:** the triangle with a tail → only [1, 3].
3. **Brute force:** remove each edge and test connectivity with BFS: O(E × (V + E)).
4. **Pattern:** **Tarjan's low-link DFS**.
5. **Plan:** discovery times and low values in one DFS; a tree edge with `low[child] > disc[parent]` is a bridge.
6. **Code and test:** a single edge, a cycle (no bridges), a chain (all bridges), two triangles joined by one edge.
walkthrough:
**Line by line**

- `disc[u]` records when u was first reached; `low[u]` starts equal to it.
- For an unvisited neighbour, the recursive call computes `low[v]`; u inherits it because anything v's subtree can reach, u can reach too.
- An already-visited neighbour (not the parent) is an ancestor reached by a back edge, so `low[u]` may drop to its discovery time.
- `low[v] > disc[u]` means v's whole subtree has no way back to u or above except through u–v.
- Skipping only `parent` is fine here because each pair of servers has at most one connection.

**Trace** on [[0, 1], [1, 2], [2, 0], [1, 3]], starting at 0:

| step | disc | low | note |
|---|---|---|---|
| visit 0 | 0 | 0 | |
| visit 1 | 1 | 1 | tree edge 0 → 1 |
| visit 2 | 2 | 2 → **0** | back edge 2 → 0 |
| back at 1 from 2 | | low[1] = 0 | low[2] = 0 ≤ disc[1]: not a bridge |
| visit 3 | 3 | 3 | tree edge 1 → 3; no other edges |
| back at 1 from 3 | | | low[3] = 3 > disc[1] = 1: **[1, 3] is a bridge** |

**Complexity:** O(V + E) time, O(V) space. The recursion is as deep as the longest DFS path; for networks with tens of thousands of servers in a line, convert it to an explicit stack.

**Common wrong approach:** comparing `low[v] >= disc[u]`, which is the test for articulation **points**, and reports edges on cycles as bridges.
:::

:::quiz
? A graph is bipartite exactly when it has no:
+ Cycle of odd length
- Cycle at all
- Vertex of odd degree
= Even cycles can be coloured alternately; odd ones can't.
? What does each strongly connected component of a directed graph contain?
+ A maximal set of vertices that can all reach each other
- Vertices with the same in-degree
- A single vertex and its neighbours
= Shrinking each SCC to one vertex leaves a DAG.
? In Tarjan's method, when is the tree edge u → v a bridge?
+ When low[v] > disc[u]
- When low[v] == 0
- When v is a leaf
= Nothing in v's subtree can climb back to u or above.
? Which problem is NP-hard, with no known polynomial-time algorithm?
+ Travelling salesman (shortest tour through every vertex)
- Minimum spanning tree
- Shortest path with non-negative weights
= MST and Dijkstra are fast; TSP needs exponential time for exact answers in general.
:::

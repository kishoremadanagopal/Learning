@@ graphs
topics: vertices and edges, directed and weighted graphs, degree, DAGs, edge lists, adjacency matrices and adjacency lists, iterative and recursive DFS, BFS with a queue, connected components, grids and other implicit graphs, counting islands
terms:
- **Graph:** a set of vertices joined by edges.
- **Vertex (node) / edge:** a point in the graph / a connection between two vertices.
- **Directed / undirected graph:** edges go one way / both ways.
- **Weighted graph:** each edge carries a number such as a distance or cost.
- **Degree:** the number of edges at a vertex; in-degree and out-degree for directed graphs.
- **Adjacency list:** for each vertex, a list of its neighbours.
- **Adjacency matrix:** a V × V grid with a mark where two vertices are joined.
- **Connected component:** a maximal group of vertices that can all reach each other.
- **Implicit graph:** a graph whose edges are computed on the fly, such as the cells of a grid.
mistakes:
- Forgetting the visited set, so a cycle makes the search run forever.
- Adding only one direction for an undirected edge.
- Writing `[[]] * n`, which makes every vertex share one neighbour list.
- Recursive DFS on large graphs or grids, which exceeds Python's recursion limit.

glance:
- Build an adjacency list | append (u, v) and (v, u) for undirected edges | O(V + E) | O(V + E)
- DFS (iterative) | stack + visited set | O(V + E) | O(V)
- BFS | queue (deque) + visited set, mark when queued | O(V + E) | O(V)
- Connected components | one search from every unvisited vertex | O(V + E) | O(V)
- Count islands in a grid | flood fill from each unvisited land cell | O(R · C) | O(R · C)
- Edge check with an adjacency matrix | matrix[u][v] | O(1) | O(V²)

@@ bfs-shortest
topics: shortest paths in unweighted graphs, parent links and path reconstruction, grid and maze shortest paths, multi-source BFS, 0-1 BFS, word ladders and other state graphs, bidirectional BFS, choosing a shortest-path method
terms:
- **Shortest path (unweighted):** a path with the fewest edges.
- **Parent link:** the vertex from which another vertex was first reached; following parents rebuilds the path.
- **Multi-source BFS:** a BFS that starts with several vertices in the queue at distance 0.
- **0-1 BFS:** a BFS with a deque for edge weights of 0 or 1; 0-cost neighbours go to the front.
- **State graph:** an implicit graph whose vertices are situations (words, lock combinations) and whose edges are moves.
- **Bidirectional BFS:** searching from the start and the goal at once until the two searches meet.
mistakes:
- Using DFS for a shortest path; it finds a path, not the shortest one.
- Marking vertices as visited when popped instead of when queued.
- Running one BFS per source instead of a single multi-source BFS.
- Using BFS on weighted edges, where fewer edges doesn't mean cheaper.

glance:
- Shortest path, unweighted | BFS from the start; distance of first visit | O(V + E) | O(V)
- Rebuild the path | store parents; walk back from the goal; reverse | O(path length) | O(V)
- Grid shortest path | BFS over cells with 4 or 8 neighbours | O(R · C) | O(R · C)
- Distance to the nearest of many sources | multi-source BFS | O(V + E) | O(V)
- Weights 0 or 1 | 0-1 BFS with a deque | O(V + E) | O(V)
- Word ladder | BFS over words; wildcard buckets find neighbours | O(N · L²) | O(N · L)
- Bidirectional BFS | grow the smaller frontier until the two meet | about O(b^(d/2)) | O(b^(d/2))

@@ topological-sort
topics: dependencies as directed edges, directed acyclic graphs, Kahn's algorithm, smallest-first orders with a heap, the DFS method with white, grey and black, cycle detection in directed graphs, graphlib, critical paths and DP on DAGs
terms:
- **Topological order:** an ordering of a directed graph's vertices where every edge points forward.
- **DAG (directed acyclic graph):** a directed graph with no cycles; exactly the graphs with a topological order.
- **In-degree:** the number of edges coming into a vertex, such as unmet prerequisites.
- **Kahn's algorithm:** repeatedly take a vertex with in-degree 0 and remove its outgoing edges.
- **Grey vertex:** in DFS cycle detection, a vertex on the current path; reaching one again means a directed cycle.
- **Critical path:** the longest chain of dependent tasks; it decides the earliest finishing time of a project.
mistakes:
- Reversing the edge direction (for `[a, b]` meaning "b before a", the edge is b → a).
- Treating any revisited vertex as a cycle in a directed graph (only grey ones count).
- Forgetting vertices with no edges, which must still appear in the order.
- Returning a partial order without checking that every vertex was included.

glance:
- Topological sort (Kahn) | queue of in-degree-0 vertices; decrement neighbours | O(V + E) | O(V + E)
- Topological sort (DFS) | reverse of the finishing order | O(V + E) | O(V)
- Directed cycle check | Kahn leaves vertices out, or DFS meets a grey vertex | O(V + E) | O(V)
- Smallest topological order | Kahn with a heap instead of a queue | O((V + E) log V) | O(V + E)
- Earliest finish (critical path) | DP in topological order: start[v] = max(start[u] + time[u]) | O(V + E) | O(V)
- Shortest path in a DAG (any weights) | relax edges in topological order | O(V + E) | O(V)

@@ shortest-paths
topics: weighted graphs, relaxing an edge, Dijkstra with heapq and lazy deletion, why negative weights break Dijkstra, Bellman-Ford, negative cycles, at most k edges, Floyd-Warshall, A* with admissible heuristics, choosing an algorithm
terms:
- **Relaxation:** updating a vertex's distance if going through a neighbouring vertex is cheaper.
- **Dijkstra's algorithm:** repeatedly settles the closest unsettled vertex; needs non-negative weights.
- **Lazy deletion:** pushing a new heap entry when a distance improves and skipping stale entries later.
- **Bellman-Ford:** relaxes every edge V − 1 times; handles negative weights and detects negative cycles.
- **Negative cycle:** a cycle whose weights add up to less than zero, so costs can fall forever.
- **Floyd-Warshall:** all-pairs shortest paths by allowing each vertex in turn as a stopover.
- **A\* search:** Dijkstra ordered by cost so far plus a heuristic estimate of the cost remaining.
- **Admissible heuristic:** an estimate that never overestimates the true remaining cost.
mistakes:
- Running Dijkstra on graphs with negative edges.
- Not skipping stale heap entries, so vertices are processed many times.
- Relaxing in place in "at most k edges" Bellman-Ford instead of from the previous round's copy.
- Putting the stopover loop k on the inside in Floyd-Warshall (it must be outermost).

glance:
- Dijkstra (heap) | pop the closest vertex, relax its edges, skip stale entries | O((V + E) log V) | O(V + E)
- Dijkstra (array scan, dense graphs) | pick the closest unsettled vertex by scanning | O(V²) | O(V)
- Bellman-Ford | relax every edge V − 1 times; an extra round finds negative cycles | O(V · E) | O(V)
- Cheapest with at most k edges | k rounds of Bellman-Ford from a copy | O(k · E) | O(V)
- Floyd-Warshall | for k, i, j: dist[i][j] = min(dist[i][j], dist[i][k] + dist[k][j]) | O(V³) | O(V²)
- A* | heap ordered by g + h with an admissible h | ≤ Dijkstra in practice | O(V)

@@ union-find-mst
topics: disjoint sets, find and union, path compression and union by size, the inverse Ackermann bound, counting components, detecting undirected cycles, spanning trees and the cut property, Kruskal's and Prim's algorithms, dense-graph Prim, single-linkage clustering
terms:
- **Union-find (disjoint set union):** a structure that keeps elements in merging groups and answers "same group?".
- **Root:** the element that names its group; it is its own parent.
- **Path compression:** pointing every node on a find path directly at the root.
- **Union by size (or rank):** hanging the smaller tree under the larger one.
- **Spanning tree:** V − 1 edges that connect every vertex with no cycle.
- **Minimum spanning tree (MST):** a spanning tree with the smallest total weight.
- **Cut property:** the cheapest edge crossing any split of the vertices is safe to include in an MST.
- **Kruskal / Prim:** build an MST by cheapest edges overall with union-find / by growing one tree with a heap.
mistakes:
- Comparing `parent[a] == parent[b]` instead of their roots, `find(a) == find(b)`.
- A recursive `find` on long chains, which can exceed the recursion limit before compression kicks in.
- Expecting union-find to split groups or report paths.
- Confusing Prim's heap key (one edge's weight) with Dijkstra's (distance from the start).

glance:
- Find / union | path compression + union by size | O(α(n)) amortised, effectively O(1) | O(n)
- Count components as edges arrive | start at n; each successful union subtracts 1 | O(E · α(V)) | O(V)
- Undirected cycle (redundant edge) | union fails because both ends share a root | O(E · α(V)) | O(V)
- Kruskal's MST | sort edges; add those joining different groups | O(E log E) | O(V + E)
- Prim's MST (heap) | grow one tree; take the cheapest edge to a new vertex | O(E log V) | O(V + E)
- Prim's MST (dense, array) | keep each outside vertex's cheapest link; scan for the minimum | O(V²) | O(V)
- Single-linkage clustering into k groups | Kruskal, stopping at k groups | O(E log E) | O(V + E)

@@ advanced-graphs
topics: bipartite graphs and two-colouring, cycles in undirected graphs, strongly connected components with Kosaraju, bridges and articulation points with low-link values, Eulerian paths with Hierholzer, maximum flow and minimum cut with Edmonds-Karp, NP-hard graph problems, a summary of graph algorithms
terms:
- **Bipartite graph:** a graph whose vertices split into two sides with every edge between the sides.
- **Strongly connected component (SCC):** a maximal set of vertices in a directed graph that can all reach each other.
- **Bridge:** an edge whose removal disconnects the graph.
- **Articulation point (cut vertex):** a vertex whose removal disconnects the graph.
- **Low-link value:** the earliest discovery time a DFS subtree can reach with one back edge.
- **Eulerian path:** a path that uses every edge exactly once.
- **Maximum flow:** the most that can be sent from a source to a sink through edges with capacities.
- **Minimum cut:** the cheapest set of edges whose removal separates source from sink; equals the maximum flow.
- **NP-hard:** a problem with no known polynomial-time algorithm, such as the travelling salesman problem.
mistakes:
- Checking only the component that contains vertex 0 when the graph is disconnected.
- Treating the parent edge as a cycle in an undirected graph.
- Using `low[v] >= disc[u]` (the articulation-point test) to find bridges.
- Searching for a fast exact algorithm for an NP-hard problem instead of using small-n methods.

glance:
- Bipartite check | BFS two-colouring; a same-colour edge means an odd cycle | O(V + E) | O(V)
- Undirected cycle check | DFS ignoring the parent edge, or union-find | O(V + E) | O(V)
- Strongly connected components | Kosaraju: finishing order, then DFS on reversed edges | O(V + E) | O(V + E)
- Bridges / articulation points | Tarjan: low[v] > disc[u] / low[v] ≥ disc[u] | O(V + E) | O(V)
- Eulerian path | Hierholzer: walk unused edges, add vertices when stuck | O(E) | O(E)
- Maximum flow | Edmonds-Karp: BFS augmenting paths with reverse capacities | O(V · E²) | O(V²) with a matrix
- Travelling salesman (exact) | bitmask DP over subsets | O(2ⁿ · n²) | O(2ⁿ · n)

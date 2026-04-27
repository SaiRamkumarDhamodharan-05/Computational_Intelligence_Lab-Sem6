import heapq

class Graph:
    def __init__(self):
        self.graph = {}
        self.heuristic = {}

    def add_Node(self, node, h):
        self.graph[node] = []
        self.heuristic[node] = h

    def delete_Node(self, node):
        if node in self.graph:
            # Remove the node and its heuristic
            self.graph.pop(node)
            self.heuristic.pop(node)
            # Remove all edges pointing to this node from other nodes
            for other_node in self.graph:
                self.graph[other_node] = [edge for edge in self.graph[other_node] if edge[0] != node]
            print(f"Node {node} deleted.")
        else:
            print("Node not found.")

    def add_Edge(self, a, b, cost):
        if a in self.graph and b in self.graph:
            self.graph[a].append((b, cost))
            self.graph[b].append((a, cost))
        else:
            print("One or both nodes do not exist.")

    def delete_Edge(self, a, b):
        if a in self.graph and b in self.graph:
            # Filter out the specific edge in both directions (undirected)
            self.graph[a] = [edge for edge in self.graph[a] if edge[0] != b]
            self.graph[b] = [edge for edge in self.graph[b] if edge[0] != a]
            print(f"Edge between {a} and {b} deleted.")
        else:
            print("Nodes not found.")

    def a_star(self, start, goal):
        if start not in self.graph or goal not in self.graph:
            print("Start or Goal node not found")
            return

        open_list = []
        path=[]
        path.append(start)
        heapq.heappush(open_list, (self.heuristic[start], start))

        g_cost = {start: 0}
        parent = {start: None}
        closed = set()

        while open_list:
            f, current = heapq.heappop(open_list)

            if current in closed:
                continue

            g = g_cost[current]

            print(f"\nCurrent Node: {current}")
            print(f"f({current}) = g({g}) + h({self.heuristic[current]}) = {f}")

            if current == goal:
                print("\n GOAL NODE REACHED WITH OPTIMAL COST")
                print(f"Optimal Cost = {g_cost[goal]}")
                return

            closed.add(current)

            print("\nNeighbours:")
            candidate_nodes = []

            for neighbour, cost in self.graph[current]:
                new_g = g_cost[current] + cost
                new_f = new_g + self.heuristic[neighbour]

                print(f"{neighbour} -> g={new_g}, h={self.heuristic[neighbour]}, f={new_f}")
                if neighbour not in g_cost or new_g < g_cost[neighbour]:
                    g_cost[neighbour] = new_g
                    parent[neighbour] = current
                    heapq.heappush(open_list, (new_f, neighbour))
                    candidate_nodes.append((new_f, neighbour))

            if candidate_nodes:
                chosen = min(candidate_nodes, key=lambda x: x[0])
                print(f"\nSelected Node for next expansion: {chosen[1]} (lowest f = {chosen[0]})")
                path.append(chosen[1])
            else:
                print("\nNo valid neighbour for expansion")
            print("->".join(path))
        print("\n FAILURE: Goal node not reachable")

    def display_Graph(self):
        print("\n--- Graph ---")
        if not self.graph:
            print("Graph is empty.")
        for node in self.graph:
            print(f"{node} (h={self.heuristic[node]}) -> {self.graph[node]}")


def main():
    g = Graph()
    n = int(input("Enter number of nodes: "))
    print("Enter node and heuristic value:")
    for _ in range(n):
        node, h = input().split()
        g.add_Node(node, int(h))

    e = int(input("Enter number of edges: "))
    print("Enter edges (node1 node2 cost):")
    for _ in range(e):
        a, b, c = input().split()
        g.add_Edge(a, b, int(c))
    while True:
        print("\n--- MENU ---")
        print("1. Add Node")
        print("2. Delete Node")
        print("3. Add Edge")
        print("4. Delete Edge")
        print("5. A* Search")
        print("6. Display Graph")
        print("7. Exit")

        ch = input("Enter choice: ")

        if ch == '1':
            node, h = input("Enter node name and heuristic: ").split()
            g.add_Node(node, int(h))

        elif ch == '2':
            node = input("Enter node to delete: ")
            g.delete_Node(node)

        elif ch == '3':
            a, b, c = input("Enter node1, node2 and cost: ").split()
            g.add_Edge(a, b, int(c))

        elif ch == '4':
            a, b = input("Enter the two nodes to remove edge between: ").split()
            g.delete_Edge(a, b)

        elif ch == '5':
            s = input("Enter start node: ")
            gnode = input("Enter goal node: ")
            g.a_star(s, gnode)

        elif ch == '6':
            g.display_Graph()

        elif ch == '7':
            break
        else:
            print("Invalid choice")

if __name__ == "__main__":
    main()
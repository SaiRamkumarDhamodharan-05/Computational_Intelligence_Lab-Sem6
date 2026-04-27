from collections import deque
import heapq

class Graph:
        def __init__(self):
                self.graph = {}

        def add_Node(self, node):
                if node not in self.graph:
                        self.graph[node] = []
                        print(f"Node {node} is added")
                else:
                        print(f"Node {node} already exists")

        def delete_Node(self, node):
                if node in self.graph:
                        del self.graph[node]
                        for i in self.graph:
                                self.graph[i] = [(n, c) for n, c in self.graph[i] if n != node]
                        print(f"Node {node} is deleted")
                else:
                        print(f"Node {node} don't exist")

        def add_Edge(self, a, b, cost):
                if a not in self.graph:
                        self.add_Node(a)
                if b not in self.graph:
                        self.add_Node(b)

                self.graph[a].append((b, cost))
                self.graph[b].append((a, cost))
                print("Edge successfully added with cost", cost)

        def delete_Edge(self, a, b):
                if a in self.graph and b in self.graph:
                        self.graph[a] = [(n, c) for n, c in self.graph[a] if n != b]
                        self.graph[b] = [(n, c) for n, c in self.graph[b] if n != a]
                        print(f"Edge between '{a}' and '{b}' is deleted.")
                else:
                        print("Error: One or both nodes not found.")

        def display_Graph(self):
                print("\n--- Graph ---")
                if not self.graph:
                        print("Graph is empty.")
                for node, neighbors in self.graph.items():
                        print(f"{node} -> {neighbors}")

        # -------- BFS --------
        def bfs(self, start, goal):
                fringe = deque([start])
                visited = set([start])
                search_path = []

                print("\nBFS Search:")
                while fringe:
                        print("Fringe:", list(fringe))
                        current = fringe.popleft()
                        search_path.append(current)
                        print("Currently at:", current)

                        if current in goal:
                                return search_path

                        for neighbor, _ in self.graph.get(current, []):
                                if neighbor not in visited:
                                        visited.add(neighbor)
                                        fringe.append(neighbor)
                return None

        # -------- DFS --------
        def dfs(self, start, goal):
                stack = [start]
                visited = set()
                search_path = []

                print("\nDFS Search:")
                while stack:
                        print("Fringe:", stack)
                        current = stack.pop()

                        if current not in visited:
                                visited.add(current)
                                search_path.append(current)
                                print("Currently at:", current)

                                if current in goal:
                                        return search_path

                                for neighbor, _ in reversed(self.graph.get(current, [])):
                                        if neighbor not in visited:
                                                stack.append(neighbor)
                return None

        # -------- UCS --------
        def ucs(self, start, goal):
                pq = []
                heapq.heappush(pq, (0, start, [start]))
                visited = set()

                print("\nUCS Search:")
                while pq:
                        cost, current, path = heapq.heappop(pq)
                        print("Fringe:", pq)
                        print("Currently at:", current, "Cost:", cost)

                        if current in goal:
                                return path, cost

                        if current not in visited:
                                visited.add(current)
                                for neighbor, edge_cost in self.graph.get(current, []):
                                        if neighbor not in visited:
                                                heapq.heappush(
                                                        pq,
                                                        (cost + edge_cost, neighbor, path + [neighbor])
                                                )
                return None, None


def main():
        g = Graph()

        n = int(input("Enter number of nodes: "))
        print("Enter nodes:")
        for _ in range(n):
                g.add_Node(input())

        e = int(input("Enter the number of edges: "))
        print("Enter edges (x y cost):")
        for _ in range(e):
                x, y, cost = input().split()
                g.add_Edge(x, y, int(cost))

        while True:
                print("\n=== MENU ===")
                print("1. Add Node")
                print("2. Delete Node")
                print("3. Add Edge")
                print("4. Delete Edge")
                print("5. BFS")
                print("6. DFS")
                print("7. UCS")
                print("8. Display Graph")
                print("9. Exit")

                choice = input("Enter the choice: ")

                if choice == '1':
                        g.add_Node(input("Enter node name: "))

                elif choice == '2':
                        g.delete_Node(input("Enter node to delete: "))

                elif choice == '3':
                        a = input("Enter source node: ")
                        b = input("Enter destination node: ")
                        cost = int(input("Enter edge cost: "))
                        g.add_Edge(a, b, cost)

                elif choice == '4':
                        a = input("Enter first node: ")
                        b = input("Enter second node: ")
                        g.delete_Edge(a, b)

                elif choice == '5':
                        start = input("Enter start node: ")
                        k = int(input("Enter number of goals: "))
                        goals = [input() for _ in range(k)]
                        path = g.bfs(start, goals)
                        if path:
                                print("Path:", " -> ".join(path))
                        else:
                                print("Search Failed")

                elif choice == '6':
                        start = input("Enter start node: ")
                        k = int(input("Enter number of goals: "))
                        goals = [input() for _ in range(k)]
                        path = g.dfs(start, goals)
                        if path:
                                print("Path:", " -> ".join(path))
                        else:
                                print("Search Failed")

                elif choice == '7':
                        start = input("Enter start node: ")
                        k = int(input("Enter number of goals: "))
                        goals = [input() for _ in range(k)]
                        path, cost = g.ucs(start, goals)
                        if path:
                                print("Path:", " -> ".join(path))
                                print("Total Cost:", cost)
                        else:
                                print("Search Failed")

                elif choice == '8':
                        g.display_Graph()

                elif choice == '9':
                        print("Exit.")
                        break

                else:
                        print("Invalid choice")


if __name__ == "__main__":
        main()
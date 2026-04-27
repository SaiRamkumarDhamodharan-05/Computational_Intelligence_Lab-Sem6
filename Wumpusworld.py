import sys
import re

class WumpusWorld:
    def __init__(self, size):
        self.size = size
        self.pits = set()
        self.wumpus = None
        self.wumpus_alive = True
        self.gold = None

        # Agent
        self.agent_pos = (1, 1)
        self.arrow_available = True
        self.score = 0
        self.last_percept = None

        # Initialize world with manual input
        self.init_world_manual()

    def get_location_input(self, prompt):
        """Parses input and ensures it is within grid bounds."""
        while True:
            try:
                val = input(f"  Enter {prompt} as [r,c]: ").strip()
                match = re.findall(r'\d+', val)
                if len(match) == 2:
                    r, c = int(match[0]), int(match[1])
                    if 1 <= r <= self.size and 1 <= c <= self.size:
                        return (r, c)
                print(f"  !!! Invalid format or out of bounds (1-{self.size}). Try [1,1]")
            except ValueError:
                print("  !!! Please use the format [r,c]")

    def init_world_manual(self):
        print(f"\n[World Setup - Grid {self.size}x{self.size}]")
        occupied = {(1, 1)}
        notpos = { (1, 2), (2, 1)}# agent start is always reserved

        while True:
            pos = self.get_location_input("WUMPUS location")
            if pos not in occupied:
                self.wumpus = pos
                occupied.add(pos)
                break
            print("  !!! That cell is already occupied.")

        while True:
            pos = self.get_location_input("GOLD location")
            if pos not in occupied:
                self.gold = pos
                occupied.add(pos)
                break
            print("  !!! That cell is already occupied.")

        try:
            num_pits = int(input("\nHow many PITS do you want to place? "))
            for i in range(num_pits):
                while True:
                    p = self.get_location_input(f"PIT #{i+1}")
                    if p not in occupied:
                        self.pits.add(p)
                        occupied.add(p)
                        break
                    print("  !!! That cell is already occupied.")
        except:
            print("No pits added.")

    def neighbors(self, pos):
        r, c = pos
        moves = [(r-1, c), (r+1, c), (r, c-1), (r, c+1)]
        return [(nr, nc) for (nr, nc) in moves if 1 <= nr <= self.size and 1 <= nc <= self.size]

    def render_grid(self, reveal=False, title=None):
        p = self.percept()
        stench, breeze = p[0], p[1]
        adj = self.neighbors(self.agent_pos)

        W = 8  # inner width of each cell
        inner = self.size * W + (self.size - 1)  # total inner width
        H, V = "-", "|"  # ASCII characters for portability

        top    = "+" + (H*W+"+")*(self.size-1) + H*W + "+"
        mid    = "+" + (H*W+"+")*(self.size-1) + H*W + "+"
        bottom = "+" + (H*W+"+")*(self.size-1) + H*W + "+"
        # top row when a title banner sits above it
        top_link = "+" + (H*W+"+")*(self.size-1) + H*W + "+"

        if title:
            print("+" + H*inner + "+")
            print(V + title.center(inner) + V)
            print(top_link)
        else:
            print(top)

        for i in range(1, self.size + 1):
            coord_row   = V
            content_row = V
            for j in range(1, self.size + 1):
                curr = (i, j)
                coord_row += f"[{i},{j}]".center(W) + V

                if curr == self.agent_pos:
                    sym = "@"
                elif reveal:
                    sym = ("P" if curr in self.pits
                           else "W" if curr == self.wumpus and self.wumpus_alive
                           else "x" if curr == self.wumpus
                           else "G" if curr == self.gold
                           else ".")
                else:
                    h = ("P?" if breeze and curr in adj else "") + \
                        ("W?" if stench and curr in adj else "")
                    sym = h if h else "."

                content_row += sym.center(W) + V

            print(coord_row)
            print(content_row)
            print(mid if i < self.size else bottom)

    def print_status(self, p):
        arrow = "Available" if self.arrow_available else "Used"
        if p is None:
            percept_line = "  Percept: [Stench=None, Breeze=None, Glitter=None, Bump=None, Scream=None]"
        else:
            names  = ["Stench", "Breeze", "Glitter", "Bump", "Scream"]
            values = [str(bool(v)) for v in p]
            percept_line = "  Percept: [" + ", ".join(f"{n}={v}" for n, v in zip(names, values)) + "]"
        print(f"\n{percept_line}")
        print(f"")
        print(f"  Score   : {self.score}")
        print(f"  Arrow   : {arrow}")
        next_moves = "  ".join(f"[{r},{c}]" for r, c in self.neighbors(self.agent_pos))
        print(f"  Next pos: {next_moves}")
        print(f"")
        print(f"  {'--- Moves ---':<20}{'--- Actions ---'}")
        print(f"  {'W = Up':<20}{'G = Grab Gold'}")
        print(f"  {'S = Down':<20}{'F = Fire Arrow'}")
        print(f"  {'A = Left':<20}{'E = Exit'}")
        print(f"  {'D = Right':<20}")

    def percept(self, bump=False, scream=False):
        pos = self.agent_pos
        adj = self.neighbors(pos)
        breeze = any(n in self.pits for n in adj)
        stench = self.wumpus_alive and any(n == self.wumpus for n in adj)
        glitter = (pos == self.gold)
        return [stench, breeze, glitter, bump, scream]

    def move(self, dr, dc):
        self.score -= 1
        r, c = self.agent_pos
        new_pos = (r + dr, c + dc)

        if not (1 <= new_pos[0] <= self.size and 1 <= new_pos[1] <= self.size):
            print("!!! BUMP into wall !!!")
            return self.percept(bump=True)

        self.agent_pos = new_pos
        if new_pos in self.pits:
            self.score -= 1000
            self.render_grid(reveal=True, title=" FELL INTO A PIT - GAME OVER ")
            print(f"  Final Score: {self.score}")
            sys.exit()

        if new_pos == self.wumpus and self.wumpus_alive:
            self.score -= 1000
            self.render_grid(reveal=True, title=" EATEN BY THE WUMPUS - GAME OVER ")
            print(f"  Final Score: {self.score}")
            sys.exit()

        return self.percept()

    def shoot(self):
        if not self.arrow_available:
            print("No arrows left!")
            return self.percept()

        direction = input("Fire Direction (U=Up, D=Down, L=Left, R=Right): ").upper()
        dr, dc = 0, 0
        if direction == "U": dr = -1
        elif direction == "D": dr = 1
        elif direction == "L": dc = -1
        elif direction == "R": dc = 1
        else:
            print("Invalid direction.")
            return self.percept()

        self.arrow_available = False
        self.score -= 10
        r, c = self.agent_pos
        scream = False

        # Arrow travels the full row/column until it exits the grid
        nr, nc = r + dr, c + dc
        while 1 <= nr <= self.size and 1 <= nc <= self.size:
            if (nr, nc) == self.wumpus and self.wumpus_alive:
                self.wumpus_alive = False
                scream = True
                print("\n>> WUMPUS SCREAMS! You killed it!")
                break
            nr += dr
            nc += dc
        else:
            if not scream:
                print("\n>> Arrow missed!")

        return self.percept(scream=scream)

    def run(self):
        self.render_grid(reveal=True, title=" INITIAL WORLD REVEAL ")
        print()

        while True:
            self.render_grid()
            self.print_status(self.last_percept)
            self.last_percept = None
            choice = input("  > ").upper()

            if choice == "W": self.last_percept = self.move(-1, 0)
            elif choice == "S": self.last_percept = self.move(1, 0)
            elif choice == "A": self.last_percept = self.move(0, -1)
            elif choice == "D": self.last_percept = self.move(0, 1)
            elif choice == "G":
                if self.agent_pos == self.gold:
                    self.score += 1000
                    self.render_grid(reveal=True, title=" GOLD GRABBED  -  YOU WIN! ")
                    print(f"  Final Score: {self.score}")
                    sys.exit()
                else:
                    print("  No gold here.")
            elif choice == "F": self.last_percept = self.shoot()
            elif choice == "E": break

# Execution
try:
    size = int(input("Enter Grid Size (e.g., 4): ") or 4)
    game = WumpusWorld(size)
    game.run()
except KeyboardInterrupt:
    print("\nGame exited.")
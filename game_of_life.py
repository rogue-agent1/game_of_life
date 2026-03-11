#!/usr/bin/env python3
"""Conway's Game of Life — cellular automaton simulator."""
import sys, time, os, random

class Life:
    def __init__(self, width=40, height=20):
        self.w = width; self.h = height
        self.grid = [[False]*width for _ in range(height)]
        self.gen = 0
    def randomize(self, density=0.3):
        for y in range(self.h):
            for x in range(self.w):
                self.grid[y][x] = random.random() < density
    def set_pattern(self, pattern, ox=0, oy=0):
        for y, row in enumerate(pattern):
            for x, c in enumerate(row):
                if 0 <= oy+y < self.h and 0 <= ox+x < self.w:
                    self.grid[oy+y][ox+x] = c == '#'
    def neighbors(self, x, y):
        count = 0
        for dy in (-1, 0, 1):
            for dx in (-1, 0, 1):
                if dx == 0 and dy == 0: continue
                nx, ny = (x+dx) % self.w, (y+dy) % self.h
                if self.grid[ny][nx]: count += 1
        return count
    def step(self):
        new = [[False]*self.w for _ in range(self.h)]
        for y in range(self.h):
            for x in range(self.w):
                n = self.neighbors(x, y)
                if self.grid[y][x]:
                    new[y][x] = n in (2, 3)
                else:
                    new[y][x] = n == 3
        self.grid = new; self.gen += 1
    def population(self):
        return sum(sum(row) for row in self.grid)
    def render(self):
        lines = [f"Gen {self.gen} | Pop {self.population()}"]
        for row in self.grid:
            lines.append("".join("█" if c else "·" for c in row))
        return "\n".join(lines)

PATTERNS = {
    "glider": ["·#·", "··#", "###"],
    "blinker": ["###"],
    "toad": ["·###", "###·"],
    "beacon": ["##··", "#···", "···#", "··##"],
    "rpentomino": ["·##", "##·", "·#·"],
}

if __name__ == "__main__":
    life = Life(60, 25)
    pattern = sys.argv[1] if len(sys.argv) > 1 else "random"
    gens = int(sys.argv[2]) if len(sys.argv) > 2 else 50
    if pattern in PATTERNS:
        life.set_pattern(PATTERNS[pattern], life.w//2-1, life.h//2-1)
    else:
        life.randomize()
    for _ in range(gens):
        os.system("clear" if os.name != "nt" else "cls")
        print(life.render())
        life.step()
        time.sleep(0.1)

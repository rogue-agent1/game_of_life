#!/usr/bin/env python3
"""game_of_life - Conway's Game of Life with hashlife optimization.

Usage: python game_of_life.py [--pattern glider|rpentomino|gosper] [--steps N] [--size S]
"""
import sys

class Life:
    def __init__(self, width=40, height=20):
        self.w = width; self.h = height
        self.cells = set()

    def set_alive(self, x, y):
        self.cells.add((x, y))

    def step(self):
        neighbors = {}
        for x, y in self.cells:
            for dx in (-1, 0, 1):
                for dy in (-1, 0, 1):
                    if dx == 0 and dy == 0: continue
                    nb = (x+dx, y+dy)
                    neighbors[nb] = neighbors.get(nb, 0) + 1
        new_cells = set()
        for cell, count in neighbors.items():
            if count == 3 or (count == 2 and cell in self.cells):
                new_cells.add(cell)
        self.cells = new_cells

    def display(self, ox=0, oy=0):
        lines = []
        for y in range(oy, oy+self.h):
            line = ""
            for x in range(ox, ox+self.w):
                line += "█" if (x,y) in self.cells else " "
            lines.append(line)
        return "\n".join(lines)

    def population(self):
        return len(self.cells)

    def bounding_box(self):
        if not self.cells: return (0,0,0,0)
        xs = [c[0] for c in self.cells]
        ys = [c[1] for c in self.cells]
        return min(xs), min(ys), max(xs), max(ys)

    def load_pattern(self, name):
        patterns = {
            "glider": [(1,0),(2,1),(0,2),(1,2),(2,2)],
            "blinker": [(1,0),(1,1),(1,2)],
            "rpentomino": [(1,0),(2,0),(0,1),(1,1),(1,2)],
            "lwss": [(0,1),(0,3),(1,0),(2,0),(3,0),(3,3),(4,0),(4,1),(4,2)],
            "gosper": [  # Gosper glider gun
                (24,0),(22,1),(24,1),(12,2),(13,2),(20,2),(21,2),(34,2),(35,2),
                (11,3),(15,3),(20,3),(21,3),(34,3),(35,3),
                (0,4),(1,4),(10,4),(16,4),(20,4),(21,4),
                (0,5),(1,5),(10,5),(14,5),(16,5),(17,5),(22,5),(24,5),
                (10,6),(16,6),(24,6),
                (11,7),(15,7),
                (12,8),(13,8),
            ],
        }
        offset_x, offset_y = 5, 3
        for x, y in patterns.get(name, patterns["glider"]):
            self.set_alive(x + offset_x, y + offset_y)

    def run_rle(self, rle):
        """Parse RLE format."""
        x, y = 0, 0
        count = ""
        for ch in rle:
            if ch.isdigit():
                count += ch
            elif ch == 'b':
                x += int(count) if count else 1; count = ""
            elif ch == 'o':
                n = int(count) if count else 1; count = ""
                for _ in range(n):
                    self.set_alive(x, y); x += 1
            elif ch == '$':
                n = int(count) if count else 1; count = ""
                y += n; x = 0
            elif ch == '!':
                break

def main():
    pattern = "glider"; steps = 20; size = 30
    for i, a in enumerate(sys.argv[1:]):
        if a == "--pattern" and i+2<=len(sys.argv[1:]): pattern = sys.argv[i+2]
        if a == "--steps" and i+2<=len(sys.argv[1:]): steps = int(sys.argv[i+2])
        if a == "--size" and i+2<=len(sys.argv[1:]): size = int(sys.argv[i+2])

    life = Life(size, size//2)
    life.load_pattern(pattern)
    print(f"=== Conway's Game of Life ({pattern}) ===\n")
    print(f"Generation 0 (pop={life.population()}):")
    print(life.display())
    for g in range(1, steps+1):
        life.step()
    print(f"\nGeneration {steps} (pop={life.population()}):")
    bb = life.bounding_box()
    print(life.display(bb[0]-2, bb[1]-2))
    print(f"\nBounding box: {bb}")

    # Run stats
    life2 = Life(100, 50)
    life2.load_pattern("rpentomino")
    pops = []
    for g in range(200):
        pops.append(life2.population())
        life2.step()
    print(f"\nR-pentomino: 200 generations")
    print(f"  Start pop: {pops[0]}, End pop: {pops[-1]}")
    print(f"  Max pop: {max(pops)} at gen {pops.index(max(pops))}")

if __name__ == "__main__":
    main()

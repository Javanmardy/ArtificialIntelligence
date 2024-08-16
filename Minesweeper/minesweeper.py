import itertools
import random


class Minesweeper:

    def __init__(self, height=8, width=8, mines=8):

        self.height = height
        self.width = width
        self.mines = set()

        self.board = []
        for i in range(self.height):
            row = []
            for j in range(self.width):
                row.append(False)
            self.board.append(row)

        while len(self.mines) != mines:
            i = random.randrange(height)
            j = random.randrange(width)
            if not self.board[i][j]:
                self.mines.add((i, j))
                self.board[i][j] = True

        self.mines_found = set()

    def print(self):
        """
        Prints a text-based representation
        of where mines are located.
        """
        for i in range(self.height):
            print("--" * self.width + "-")
            for j in range(self.width):
                if self.board[i][j]:
                    print("|X", end="")
                else:
                    print("| ", end="")
            print("|")
        print("--" * self.width + "-")

    def is_mine(self, cell):
        i, j = cell
        return self.board[i][j]

    def nearby_mines(self, cell):
        count = 0
        for i in range(cell[0] - 1, cell[0] + 2):
            for j in range(cell[1] - 1, cell[1] + 2):
                if (i, j) == cell:
                    continue
                if 0 <= i < self.height and 0 <= j < self.width:
                    if self.board[i][j]:
                        count += 1

        return count

    def won(self):
        return self.mines_found == self.mines


class Sentence:

    def __init__(self, cells, count):
        self.cells = set(cells)
        self.count = count

    def __eq__(self, other):
        return self.cells == other.cells and self.count == other.count

    def __str__(self):
        return f"{self.cells} = {self.count}"

    def known_mines(self):
        if len(self.cells) == self.count:
            return set(self.cells)
        return set()

    def known_safes(self):
        if self.count == 0:
            return set(self.cells)
        return set()

    def mark_mine(self, cell):
        if cell in self.cells:
            self.cells.remove(cell)
            self.count -= 1

    def mark_safe(self, cell):
        if cell in self.cells:
            self.cells.remove(cell)


class MinesweeperAI:

    def __init__(self, height=8, width=8):

        self.height = height
        self.width = width

        self.moves_made = set()

        self.mines = set()
        self.safes = set()

        self.knowledge = []

    def mark_mine(self, cell):

        self.mines.add(cell)
        for sentence in self.knowledge:
            sentence.mark_mine(cell)

    def mark_safe(self, cell):

        self.safes.add(cell)
        for sentence in self.knowledge:
            sentence.mark_safe(cell)

    def add_knowledge(self, cell, count):

        self.moves_made.add(cell)

        self.mark_safe(cell)

        neighbors = set()
        i, j = cell
        for di in range(-1, 2):
            for dj in range(-1, 2):
                if di == 0 and dj == 0:
                    continue
                ni, nj = i + di, j + dj
                if 0 <= ni < self.height and 0 <= nj < self.width:
                    if (ni, nj) not in self.safes and (ni, nj) not in self.moves_made:
                        neighbors.add((ni, nj))
        if neighbors:
            new_sentence = Sentence(neighbors, count)
            self.knowledge.append(new_sentence)

        safes = set()
        mines = set()
        for sentence in self.knowledge:
            safes |= sentence.known_safes()
            mines |= sentence.known_mines()

        for safe in safes:
            self.mark_safe(safe)
        for mine in mines:
            self.mark_mine(mine)

        new_knowledge = []
        for sentence in self.knowledge:
            if sentence.cells:
                for other in self.knowledge:
                    if sentence != other and sentence.cells.issubset(other.cells):
                        inferred_sentence = Sentence(
                            other.cells - sentence.cells, other.count - sentence.count
                        )
                        if (
                            inferred_sentence not in self.knowledge
                            and inferred_sentence not in new_knowledge
                        ):
                            new_knowledge.append(inferred_sentence)
        self.knowledge.extend(new_knowledge)

    def make_safe_move(self):

        for safe in self.safes:
            if safe not in self.moves_made:
                return safe
        return None

    def make_random_move(self):

        choices = [
            (i, j)
            for i in range(self.height)
            for j in range(self.width)
            if (i, j) not in self.moves_made and (i, j) not in self.mines
        ]
        if choices:
            return random.choice(choices)
        return None

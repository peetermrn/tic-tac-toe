class Board:
    def __init__(self):
        self.board = [" " for _ in range(0,9)]  # 6 7 8
        self.player_to_move = "O"
        self.moves = [i for i in range(0, 9)]
        self.winner = ""
        self.bot = Bot()

    def make_move(self, i: int):
        if self.player_to_move == "O":
            self.board[i] = "O"
            self.player_to_move = "X"
        elif self.player_to_move == "X":
            self.board[i] = "X"
            self.player_to_move = "O"
        self.moves.remove(i)

    def is_over(self):
        """Return true if game is over, if not then false."""
        winning_combinations = [[0, 1, 2], [3, 4, 5], [6, 7, 8], [0, 3, 6], [1, 4, 7], [2, 5, 8], [0, 4, 8], [2, 4, 6]]
        for combination in winning_combinations:
            a, b, c = combination
            if self.board[a] == self.board[b] == self.board[c] != " ":
                self.winner = self.board[a]
                return True
        return len(self.moves) == 0

    def __repr__(self):
        res = "\n  board:       moves:\n\n"
        for i, e in enumerate(self.board):
            res += e + " | "
            if i in [2, 5, 8]:
                res = res[0:-2]
                if i == 2:
                    res += "   0 | 1 | 2"
                if i == 5:
                    res += "   3 | 4 | 5"
                if i == 8:
                    res += "   6 | 7 | 8"
                if i != 8:
                    res += "\n" + 9 * "-" + "    " + 9 * "-" + "\n"

        return res

    def play(self):
        beginner = input("who makes the first move, O(computer) or X(you)?")
        while beginner not in ["X", "O"]:
            print("error, answer again")
            beginner = input("who makes the first move, O(computer) or X(you)?")
        self.player_to_move = beginner
        print(self)
        while not self.is_over():
            if self.player_to_move == "X":
                n = (input(f"\nmake move ({self.player_to_move})"))
                while not n.isdigit() or not int(n) in self.moves:
                    print("not valid move, pick again")
                    n = (input(f"\nmake move ({self.player_to_move})"))
                n = int(n)
                self.make_move(n)
            else:
                self.make_move(self.bot.get_best_move(self))
            print(self)
            if self.is_over():
                print("GAME OVER")
                if self.winner:
                    print(f"winner is {self.winner}")
                break

    def copy(self):
        copy_board = Board()
        copy_board.moves = self.moves.copy()
        copy_board.player_to_move = self.player_to_move
        copy_board.board = self.board.copy()
        return copy_board


class Bot:
    def get_best_move(self, board: Board):
        """Player is X or O"""
        if len(board.moves) == 9:
            return 4
        moves = {}
        for m in board.moves:
            b = board.copy()
            b.make_move(m)
            a = self.minimax(b, 0, "O")
            moves[a] = m
        return moves[max(moves)]

    def minimax(self, board: Board, depth: int, player: str):
        if board.is_over():
            c = 0
            if board.winner == player:
                c = 5
            if board.winner == "X":
                c = -5
            return 9 - depth + c
        if board.player_to_move == player:
            max_pos = 0
            for move in board.moves:
                new_board = board.copy()
                new_board.make_move(move)
                pos = self.minimax(new_board, depth + 1, player)
                max_pos = max(max_pos, pos)
            return max_pos
        else:
            min_pos = 14
            for move in board.moves:
                new_board = board.copy()
                new_board.make_move(move)
                pos = self.minimax(new_board, depth + 1, player)
                min_pos = min(pos, min_pos)
            return min_pos


if __name__ == '__main__':
    board1 = Board()
    board1.play()

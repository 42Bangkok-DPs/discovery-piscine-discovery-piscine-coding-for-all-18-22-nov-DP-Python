class ChessPiece:
    def __init__(self, color, symbol):
        self.color = color
        self.symbol = symbol

    def is_valid_move(self, start, end, board):
        raise NotImplementedError("This method should be implemented in the subclass.")

    def get_attacks(self, position, board):
        raise NotImplementedError("This method should be implemented in the subclass.")


class Pawn(ChessPiece):
    def __init__(self, color):
        super().__init__(color, 'P')

    def is_valid_move(self, start, end, board):
        direction = 1 if self.color == 'black' else -1
        if start[1] == end[1]:  # Same column
            if (self.color == 'white' and start[0] == 6 and end[0] == 4) or \
               (self.color == 'black' and start[0] == 1 and end[0] == 3):
                if board[end[0]][end[1]] is None:
                    return True
            elif (end[0] == start[0] + direction) and board[end[0]][end[1]] is None:
                return True
        elif abs(start[1] - end[1]) == 1 and end[0] == start[0] + direction:
            target_piece = board[end[0]][end[1]]
            if target_piece and target_piece.color != self.color:
                return True
        return False

    def get_attacks(self, position, board):
        attacks = []
        direction = 1 if self.color == 'black' else -1
        row, col = position
        if 0 <= row + direction < 8:
            if col - 1 >= 0 and board[row + direction][col - 1] and board[row + direction][col - 1].color != self.color:
                attacks.append((row + direction, col - 1))
            if col + 1 < 8 and board[row + direction][col + 1] and board[row + direction][col + 1].color != self.color:
                attacks.append((row + direction, col + 1))
        return attacks


class Rook(ChessPiece):
    def __init__(self, color):
        super().__init__(color, 'R')

    def is_valid_move(self, start, end, board):
        if start[0] == end[0]:  # Horizontal move
            step = 1 if end[1] > start[1] else -1
            for col in range(start[1] + step, end[1], step):
                if board[start[0]][col] is not None:
                    return False
            return True
        elif start[1] == end[1]:  # Vertical move
            step = 1 if end[0] > start[0] else -1
            for row in range(start[0] + step, end[0], step):
                if board[row][start[1]] is not None:
                    return False
            return True
        return False

    def get_attacks(self, position, board):
        attacks = []
        row, col = position
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]  # Up, Down, Left, Right
        for dx, dy in directions:
            x, y = row + dx, col + dy
            while 0 <= x < 8 and 0 <= y < 8:
                if board[x][y]:
                    if board[x][y].color != self.color:
                        attacks.append((x, y))
                    break
                x += dx
                y += dy
        return attacks


class Knight(ChessPiece):
    def __init__(self, color):
        super().__init__(color, 'N')

    def is_valid_move(self, start, end, board):
        dx, dy = abs(start[0] - end[0]), abs(start[1] - end[1])
        if (dx == 2 and dy == 1) or (dx == 1 and dy == 2):
            return True
        return False

    def get_attacks(self, position, board):
        attacks = []
        row, col = position
        moves = [(-2, -1), (-1, -2), (1, -2), (2, -1), (2, 1), (1, 2), (-1, 2), (-2, 1)]
        for dx, dy in moves:
            x, y = row + dx, col + dy
            if 0 <= x < 8 and 0 <= y < 8:
                attacks.append((x, y))
        return attacks


class Bishop(ChessPiece):
    def __init__(self, color):
        super().__init__(color, 'B')

    def is_valid_move(self, start, end, board):
        if abs(start[0] - end[0]) == abs(start[1] - end[1]):  # Diagonal move
            dx = 1 if end[0] > start[0] else -1
            dy = 1 if end[1] > start[1] else -1
            x, y = start[0] + dx, start[1] + dy
            while x != end[0] and y != end[1]:
                if board[x][y] is not None:
                    return False
                x += dx
                y += dy
            return True
        return False

    def get_attacks(self, position, board):
        attacks = []
        row, col = position
        directions = [(-1, -1), (-1, 1), (1, -1), (1, 1)]  # Diagonals
        for dx, dy in directions:
            x, y = row + dx, col + dy
            while 0 <= x < 8 and 0 <= y < 8:
                if board[x][y]:
                    if board[x][y].color != self.color:
                        attacks.append((x, y))
                    break
                x += dx
                y += dy
        return attacks


class Queen(ChessPiece):
    def __init__(self, color):
        super().__init__(color, 'Q')

    def is_valid_move(self, start, end, board):
        return Rook(self.color).is_valid_move(start, end, board) or \
               Bishop(self.color).is_valid_move(start, end, board)

    def get_attacks(self, position, board):
        return Rook(self.color).get_attacks(position, board) + \
               Bishop(self.color).get_attacks(position, board)


class King(ChessPiece):
    def __init__(self, color):
        super().__init__(color, 'K')

    def is_valid_move(self, start, end, board):
        if abs(start[0] - end[0]) <= 1 and abs(start[1] - end[1]) <= 1:
            return True
        return False

    def get_attacks(self, position, board):
        attacks = []
        row, col = position
        for dx in [-1, 0, 1]:
            for dy in [-1, 0, 1]:
                x, y = row + dx, col + dy
                if 0 <= x < 8 and 0 <= y < 8 and (dx != 0 or dy != 0):
                    attacks.append((x, y))
        return attacks


class ChessBoard:
    def __init__(self):
        self.board = self.create_board()
        self.turn = 'white'  # White always goes first

    def create_board(self):
        board = [[None for _ in range(8)] for _ in range(8)]

        # Black pieces
        board[0][0] = Rook('black')
        board[0][1] = Knight('black')
        board[0][2] = Bishop('black')
        board[0][3] = Queen('black')
        board[0][4] = King('black')
        board[0][5] = Bishop('black')
        board[0][6] = Knight('black')
        board[0][7] = Rook('black')

        # Black pawns
        for i in range(8):
            board[1][i] = Pawn('black')

        # White pawns
        for i in range(8):
            board[6][i] = Pawn('white')

        # White pieces
        board[7][0] = Rook('white')
        board[7][1] = Knight('white')
        board[7][2] = Bishop('white')
        board[7][3] = Queen('white')
        board[7][4] = King('white')
        board[7][5] = Bishop('white')
        board[7][6] = Knight('white')
        board[7][7] = Rook('white')

        return board

    def display(self):
        for row in self.board:
            print(" ".join([piece.symbol if piece else '.' for piece in row]))

    def move_piece(self, start, end):
        piece = self.board[start[0]][start[1]]
        
        if piece is None:
            print("No piece at the starting position!")
            return False

        # Check if it's the correct player's turn
        if piece.color != self.turn:
            print(f"It's {self.turn}'s turn! Please wait for your turn.")
            return False

        # Check if the move is valid for the piece
        if piece.is_valid_move(start, end, self.board):
            target_piece = self.board[end[0]][end[1]]
            if target_piece and target_piece.color == piece.color:
                print("You cannot capture your own piece!")
                return False

            # Capture piece if there is one
            if target_piece:
                print(f"Captured {target_piece.symbol} at {end}")

            # Move the piece
            self.board[end[0]][end[1]] = piece
            self.board[start[0]][start[1]] = None
            print("Move successful!")

            # Switch turn after a successful move
            self.turn = 'black' if self.turn == 'white' else 'white'
            return True
        else:
            print("Invalid move!")
            return False

    def is_in_check(self, color):
        king_position = None
        for row in range(8):
            for col in range(8):
                piece = self.board[row][col]
                if piece and piece.color == color and isinstance(piece, King):
                    king_position = (row, col)
                    break
        if not king_position:
            return False

        for row in range(8):
            for col in range(8):
                piece = self.board[row][col]
                if piece and piece.color != color:
                    if king_position in piece.get_attacks((row, col), self.board):
                        return True
        return False

    def is_checkmate(self, color):
        if not self.is_in_check(color):
            return False

        # Try all possible moves for the color to see if they can escape check
        for row in range(8):
            for col in range(8):
                piece = self.board[row][col]
                if piece and piece.color == color:
                    for end in range(8):
                        for c in range(8):
                            if self.move_piece((row, col), (end, c)):
                                if not self.is_in_check(color):
                                    return False
        return True


def main():
    game_board = ChessBoard()
    game_board.display()

    while True:
        try:
            print(f"\nIt's {game_board.turn}'s turn.")
            start = input("Enter start position (row,col): ")
            start = tuple(map(int, start.split(',')))
            end = input("Enter end position (row,col): ")
            end = tuple(map(int, end.split(',')))

            if game_board.move_piece(start, end):
                game_board.display()

                if game_board.is_checkmate('white'):
                    print("White is checkmated! Black wins!")
                    break
                elif game_board.is_checkmate('black'):
                    print("Black is checkmated! White wins!")
                    break
        except ValueError:
            print("Invalid input. Please enter valid row and column indices.")
        except IndexError:
            print("Out of bounds. Please enter coordinates between 0 and 7.")


if __name__ == "__main__":
    main()
 
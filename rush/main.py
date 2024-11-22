def checkmate(board):
    # Parse the board into a 2D list
    board = board.strip().split('\n')
    size = len(board)

    # Locate the King
    king_pos = None
    for i in range(size):
        for j in range(size):
            if board[i][j] == 'K':
                king_pos = (i, j)
                break
        if king_pos:
            break

    if not king_pos:
        print("Error: No King found on the board.")
        return

    # Movement patterns for each piece
    directions = {
        'P': [(-1, -1), (-1, 1)],  # Pawn captures diagonally
        'B': [(-1, -1), (-1, 1), (1, -1), (1, 1)],  # Bishop moves diagonally
        'R': [(-1, 0), (1, 0), (0, -1), (0, 1)],  # Rook moves vertically/horizontally
        'Q': [(-1, -1), (-1, 1), (1, -1), (1, 1), (-1, 0), (1, 0), (0, -1), (0, 1)],  # Queen combines Bishop & Rook
    }

    # Check for each piece type
    for i in range(size):
        for j in range(size):
            piece = board[i][j]
            if piece in directions:
                for direction in directions[piece]:
                    x, y = i, j
                    while 0 <= x < size and 0 <= y < size:
                        x += direction[0]
                        y += direction[1]
                        if not (0 <= x < size and 0 <= y < size):
                            break
                        if (x, y) == king_pos:
                            print("Success")
                            return
                        if board[x][y] != '.':  # Stop if any piece is in the way
                            break

    print("Fail")


def main():
    # Example boards to test
    boards = [
        """\
R...
.K..
..P.
....\
""",  # King in check by Rook

        """\
....
.K..
.P..
....\
""",  # King is safe

        """\
....
..B.
....
.K..\
""",  # King in check by Bishop

        """\
....Q
......
......
...K..\
""",  # King in check by Queen

        """\
..
.K\
""",  # King is safe on a small board

        """\
........
...B....
........
........
....K...
........
...P....
........\
""",  # King in check by Bishop
    ]

    # test board each one
    for idx, board in enumerate(boards, 1):
        print(f"Board {idx}:")
        checkmate(board)
        print()


if __name__ == "__main__":
    main()

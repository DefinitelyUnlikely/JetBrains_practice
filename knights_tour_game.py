def knights_tour():

    def create_matrix():
        matrix = [[f"{'_' * cell_size}"] * columns for i in range(rows)]
        return matrix

    def valid_input():
        try:
            return int(x) > 0 and int(y) > 0
        except ValueError:
            return False

    while True:
        try:
            x, y = input("Enter your board dimensions: ").split()
            if valid_input():
                break
            print("Invalid dimensions!")
        except ValueError:
            print("Invalid dimensions!")
    while True:
        try:
            k_col, k_row = \
                input("Enter the knight's starting position: ").split()
            if valid_input() \
                    and (int(x) >= int(k_col) and int(y) >= int(k_row)):
                break
            print("Invalid dimensions!")
        except ValueError:
            print("Invalid dimensions!")

    # make into ints, reduce by 1 (so that they correspond to indices)
    k_col, k_row = int(k_col) - 1, int(k_row) - 1

    columns, rows = int(x), int(y)
    cell_size = len(str(columns * rows))

    # Create the matrix representing the board.
    board_matrix = create_matrix()

    def valid_moves(col, row):
        move_row = [2, 1, -1, -2, -2, -1, 1, 2]
        move_col = [1, 2, 2, 1, -1, -2, -2, -1]
        moves = []
        for i in range(8):
            if 0 <= col + move_col[i] < columns\
                    and 0 <= row + move_row[i] < rows\
                    and "_" in\
                    board_matrix[row + move_row[i]][col + move_col[i]]:
                moves.append((col + move_col[i], row + move_row[i]))
        return moves

    def print_board(matrix, col=0, row=0, player=True):
        board_copy = [inner_list[:] for inner_list in matrix]
        # marking the next moves possible and the count of their possible moves.
        if player:
            for move in valid_moves(col, row):
                further = valid_moves(move[0], move[1])
                board_copy[move[1]][move[0]] = f"{str(len(further)).rjust(cell_size, ' ')}"
        print(" " * len(str(rows)) + "-" * (columns * (cell_size + 1) + 3))
        for i in range(rows, 0, -1):
            print(str(i).rjust(len(str(rows))) + "| " + " ".join(
                board_copy[i - 1]) + " |")
        print(" " * len(str(rows)) + "-" * (columns * (cell_size + 1) + 3))
        print(
            ' ' * (cell_size + 1) + " ".join([f"{str(i).rjust(cell_size, ' ')}"
                                              for i in range(1, columns + 1)]))

    def knight_tour_player(column, row):
        pos_c, pos_r = column, row
        board_matrix[pos_r][pos_c] = f"{'X'.rjust(cell_size)}"
        count = 1

        if not knight_tour_computer(pos_c, pos_r):
            print("No solution exists!", end="")
            return

        while True:
            possible = valid_moves(pos_c, pos_r)
            if not possible:
                if count == (columns * rows):
                    print("What a great tour! Congratulations!")
                    break
                else:
                    print("No more possible moves!", end="")
                    print(f"Your knight visited {count} squares!")
                    break
            print_board(board_matrix, pos_c, pos_r)
            print()
            while True:
                try:
                    next_x, next_y = input("Enter your next move: ").split()
                    if valid_input():
                        if (int(next_x) - 1, int(next_y) - 1) in possible:
                            board_matrix[pos_r][pos_c] = f"{'*'.rjust(cell_size)}"
                            pos_c, pos_r = int(next_x) - 1, int(next_y) - 1
                            board_matrix[pos_r][pos_c] = f"{'X'.rjust(cell_size)}"
                            count += 1
                            break
                        else:
                            print("Invalid move!", end="")
                except ValueError:
                    print("Invalid move!", end="")

    def knight_tour_computer(knight_c, knight_r):
        # Create the board, n rows by m columns
        chess_board = [[0 for i in range(columns)] for j in range(rows)]
        # Place the knight at the starting position.
        chess_board[knight_r][knight_c] = 1

        def valid_moves_computer(col, row):
            move_row = [2, 1, -1, -2, -2, -1, 1, 2]
            move_col = [1, 2, 2, 1, -1, -2, -2, -1]
            moves = []
            for i in range(8):
                if 0 <= col + move_col[i] < columns \
                        and 0 <= row + move_row[i] < rows \
                        and chess_board[row + move_row[i]][col + move_col[i]] == 0:
                    moves.append((col + move_col[i], row + move_row[i]))

            return moves

        def solve(pos_c, pos_r, counter=2):

            # I need to come up with a base case that returns True if all
            # squares have been visited.
            if counter > rows * columns:
                return True

            possible = valid_moves_computer(pos_c, pos_r)
            moves = []
            for move in possible:
                further = valid_moves_computer(move[0], move[1])
                moves.append((len(further), move[0], move[1]))

            for i in sorted(moves):
                chess_board[i[2]][i[1]] = counter
                if solve(i[1], i[2], counter + 1):
                    return True
                chess_board[i[2]][i[1]] = 0

            return False

        if solve(knight_c, knight_r):
            chess_board = [[str(item).rjust(cell_size, " ") for item in column] for column in chess_board]
            return chess_board
        else:
            print("No solution exists!")

    while True:
        yn = input("Do you want to try the puzzle? (y/n): ")
        if yn == "y":
            knight_tour_player(k_col, k_row)
            break
        if yn == "n":
            solution = knight_tour_computer(k_col, k_row)
            if solution:
                print("Here's the solution!")
                print_board(solution, player=False)
            break
        print('Invalid option', end="")


if __name__ == "__main__":
    knights_tour()

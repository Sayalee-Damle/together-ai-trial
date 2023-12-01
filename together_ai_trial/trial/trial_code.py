def solve_sudoku(board):
    # Initialize the row and column sets
    rows = set()
    cols = set()
    boxes = set()
    
    # Loop through the board and solve each row, column, and box
    for i in range(9):
        row = board[i]
        for j in range(9):
            col = board[j]
            if row == 0 and col == 0:
                continue
            elif row == 0:
                rows.add(j)
            elif col == 0:
                cols.add(i)
            else:
                boxes.add((i, j))
    
    # Check if the board has been solved
    if len(rows) == 9 and len(cols) == 9 and len(boxes) == 9:
        return True
    else:
        return False
    
# Test the solver
board = [
    [0, 1, 2, 0, 0, 0],
    [0, 9, 8, 0, 0, 0],
    [0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0]
]
print(solve_sudoku(board))



# Returns all the possible locations of a block of given length in a set space
# Example:
#   block = 2, space = 4
#   return : [["B", "B", " ", " "], [" ", "B", "B", " "], [" ", " ", "B", "B"]]
#
def draw_block(block, space):
    space = space
    block_len = block

    lines = []

    for offset in range(space-block_len+1):
        lines.append([" " for _ in range(offset)]+["B" for _ in range(block_len)])

    return lines


# Returns the common line from a list of lines
# Example:
#   lines = [["B","B"," "," "], ["B"," "," ","B"]]
#   return : ["B", " ", "X", " "]
#
def get_common_line(lines):
    line_len = lines[0].__len__()
    common_line = [" " for _ in range(line_len)]
    for j in range(line_len):
        common_block = True
        common_empty = True
        for i in range(lines.__len__()):
            if lines[i][j] != "B":
                common_block = False
            if lines[i][j] != " ":
                common_empty = False
        if common_block:
            common_line[j] = "B"
        if common_empty:
            common_line[j] = "X"

    return common_line


# Returns the minimum length needed to fit the given blocks in a line
def get_min_space(blocks):
    return sum(blocks)+blocks.__len__()


# Returns all the possible arrangements of blocks in a line of given length
# Example:
#   lines = [1,2], line_len = 5
#   return : [["B", " ", "B", "B", " "], ["B", " ", " ", "B", "B"], [" ", "B", " ", "B", "B"]]
#
def populate_line(blocks, line_len):
    aggregate_lines = draw_block(blocks[0], line_len-get_min_space(blocks[1:]))
    for block_i in range(1,blocks.__len__()):
        new_lines = []
        for line in aggregate_lines:
            additions = draw_block(blocks[block_i], line_len-get_min_space(blocks[block_i+1:])-line.__len__()-1)
            possibilities = [line + [" "] + addition for addition in additions]
            new_lines += possibilities
        aggregate_lines = new_lines
    out = []
    for a in aggregate_lines:
        out.append(a + [" " for _ in range(line_len-a.__len__())])
    return out


# Filters the possible arrangements given according to a constraint
# Example:
#   possibilities = [["B", " ", "B", "B", " "], ["B", " ", " ", "B", "B"], [" ", "B", " ", "B", "B"]]
#   constraint = ["B", "X", " ", " ", " "]
#   return : [["B", " ", "B", "B", " "], ["B", " ", " ", "B", "B"]]
#
def constrain(possibilities, constraint):
    block_constraints = []
    empty_contraints = []
    for i in range(constraint.__len__()):
        element = constraint[i]
        if element == "X":
            empty_contraints.append(i)
        elif element == "B":
            block_constraints.append(i)
    new_lines = []
    for p in possibilities:
        fits_blocks = True
        for i in block_constraints:
            if p[i] != "B":
                fits_blocks = False
                break
        if not fits_blocks:
            continue
        fits_empties = True
        for i in empty_contraints:
            if p[i] == "B":
                fits_empties = False
                break
        if not fits_empties:
            continue
        new_lines.append(p)
    return new_lines


# Splits number string into array
def str_to_arr(num_str):
    groups = num_str.split(",")
    ls = []
    for g in groups:
        nums = g.split(" ")
        num_list = []
        for n in nums:
            num_list.append(int(n))
        ls.append(num_list)
    return ls


# Representation of Nonogram Board
class Board:

    # Initialises Board with given length and rows and columns
    def __init__(self, length, rows, columns):
        self.length = length
        self.rows = rows
        self.columns = columns
        self.board = [[" " for j in range(self.length)] for i in range(self.length)]

    # Solves nonogram and prints it out, show_process toggles a print-out of each run
    def solve(self, show_process):
        completed = False
        for run_count in range(50):
            completed = True

            for row_index in range(self.length):
                row_blocks = self.rows[row_index]
                constrained_rows = constrain(populate_line(row_blocks, self.length), self.get_row(row_index))
                if constrained_rows.__len__() != 0:
                    new_row = get_common_line(constrained_rows)
                    if new_row.__contains__(" "):
                        completed = False
                    self.set_row(row_index, new_row)

            if show_process:
                print("Run %i down rows" % (run_count+1))
                self.display_board()

            if completed:
                print("Took " + str(run_count) + " repetitions to complete")
                break

            for col_index in range(self.length):
                col_blocks = self.columns[col_index]
                constrained_col = constrain(populate_line(col_blocks, self.length), self.get_column(col_index))
                if constrained_col.__len__() != 0:
                    new_col = get_common_line(constrained_col)
                    if new_col.__contains__(" "):
                        completed = False
                    self.set_column(col_index, new_col)

            if show_process:
                print("Run %i across columns" % (run_count+1))
                self.display_board()

            if completed:
                print("Took " + str(run_count) + " repetitions to complete")
                break

        if not show_process:
            self.display_board()

    def display_board(self):
        for row_index in range(self.board.__len__()):
            row = self.board[row_index]
            out = ""
            for e in row:
                if e == "X":
                    out += "|."
                else:
                    out += "|"+e
            print(out+"|")

    def set_row(self, index, row):
        self.board[index] = row

    def set_column(self, index, column):
        for i in range(self.length):
            self.board[i][index] = column[i]

    def get_row(self, index):
        return self.board[index]

    def get_column(self, index):
        column = []
        for i in range(self.length):
            column.append(self.board[i][index])
        return column


from nonogram import Board

# Open textfile and separate out row and column numbers
f = open("data.txt", "r")
lines = f.readlines()
buffer = []
row_blocks = []
for line in lines:
    if line == "columns\n" or line == "rows\n":
        row_blocks = buffer
        buffer = []
    else:
        comp = line.split(",")
        blocks = []
        for c in comp:
            blocks.append(int(c))
        buffer.append(blocks)
col_blocks = buffer

b = Board(len(lines), row_blocks, col_blocks)

b.solve(False)

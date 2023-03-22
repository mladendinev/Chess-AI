# Chess-AI

# GUI

PyQt6

# Workflow:

1. Download chess database, preferably with games played by high ranked chess players.
2. Parse the game boards
3. Encode the information from the board
4. Configure an appropriate Neural Network
5. Train the NN model
6. Use a value function returning the best possible move in the current state of the game.

# Goals:

### Implement min-max with alpha-beta pruning

### Design a sample NN, train and validate the model

### Play against a computer or AI bot, rendering


# Notes
The position of the piece on the board is represented in binary format

Board is represented as - 8x8 - 64 bits

=====WHITE=====
Pawn - 1
Knight - 2
Bishop - 3
Rook - 4
Queen - 5
King - 6

=====BLACK=====
Pawn - 9
Knight - 10
Bishop - 11
Rook - 12
Queen - 13
King - 14

All the white pieces have their left most bit as 0 - (0001), (0010), (0011), (0100), (0101), (0110)
All black pieces have their left most bit as 1 - (1001), (1010), (1011), (1100), (1101), (1110)

The other three bits indicate the piece type independent of the color.

The left most bit identifies the color of the piece - if 1 then black, else white. "&" is the AND bitwise operator - 1&1 == true(1) 0&1 == false (0)

===== AI and Neural networks

np.zeros((5,8,8), np.unint8) -> 5 matrices each 8x8 representing 5 different neurons for each field on the board

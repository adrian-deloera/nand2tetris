// Nand2Tetris Palindrome Code

@0
M=1 // Set answer bit to the neutral value

(START)
@begCur
M=0
@strCur //Set the string cursor equal to 0
M=0


(INPUTLOOP)
@128  //jumps to compute when enter is pressed
D=A
@KBD
D=D-M
@COMPUTE
D;JEQ

@KBD  //calls the increment cursor when non-enter key is pressed
D=M
@INCREMENTCURSOR
D;JNE

@INPUTLOOP
0;JMP

(INCREMENTCURSOR) //increments the cursor by 1
@strCur
D=M+1
M=D
A=D+A
M=-1

@INPUTLOOP
0;JMP

(COMPUTE) // checks whether or not it is a Palindrome
@0
M=0

(END) // end loop for testing
@END
0;JMP


// Nand2Tetris Palindrome Code
// Adrian DeLoera  113372061

@0
M=1 // Set answer bit to the neutral value

@19
D=A
@begCur
M=D

@endCur
M=0

@18
D=A
@strCur 
M=D

(INPUTLOOP)
@128  //jumps to compute when enter is pressed
D=A
@KBD
D=D-M
@COMPUTE
D;JEQ

@KBD
D=M
@ADDCHAR //calls the character adder when non-enter key is pressed
D;JNE
@INPUTLOOP
0;JMP

(ADDCHAR) //increments the cursor by 1 and writes the keyboard input to memory
@strCur
M=M+1
A=M
M=D
@WAITRELEASE
0;JMP

(WAITRELEASE) //Waits for the key to be released before continuing to avoid zeros being placed between values
@KBD
D=M
@INPUTLOOP
D;JEQ
@WAITRELEASE
0;JMP

(COMPUTE) // checks whether or not it is a Palindrome
@strCur
D=M
@endCur
M=D
A=D
D=M
@begCur
A=M
D=D-M

@FAIL
D;JNE

@endCur
M=M-1
@begCur
M=M+1
@CHECKCURSORS
D;JEQ

(CHECKCURSORS) // checks position of cursors during computation
@endCur
D=M
@begCur
D=D-M
@PASS
D;JLE
@COMPUTE
D;JNE

(FAIL) //sets answer value to false, and returns to the input loop.
@0
M=0
@WAITRELEASE
0;JMP

(PASS)
@0
M=-1
@WAITRELEASE
0;JMP

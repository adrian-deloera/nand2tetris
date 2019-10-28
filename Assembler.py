import os,sys


Destination = {
    "null": "000",
    "M": "001",
    "D": "010",
    "A": "100",
    "MD": "011",
    "AM": "101",
    "AD": "110",
    "AMD": "111"
    }


jump = {
    "null": "000",
    "JGT": "001",
    "JEQ": "010",
    "JGE": "011",
    "JLT": "100",
    "JNE": "101",
    "JLE": "110",
    "JMP": "111"
    }


functions = {
    "0": "0101010", 
    "1": "0111111",
    "-1": "0111010",
    "D": "0001100",
    "A": "0110000",
    "!D": "0001101",
    "!A": "0110001",
    "-D": "0001111",
    "-A": "0110011",
    "D+1": "0011111",
    "A+1": "0110111",
    "D-1": "0001110",
    "A-1": "0110010",
    "D+A": "0000010",
    "D-A": "0010011",
    "A-D": "0000111",
    "D&A": "0000000",
    "D|A": "0010101",
    "M": "1110000",
    "!M": "1110001",
    "-M": "1110011",
    "M+1": "1110111",
    "M-1": "1110010",
    "D+M": "1000010",
    "D-M": "1010011",
    "M-D": "1000111",
    "D&M": "1000000",
    "D|M": "1010101"
    }


tablesymb = {
    "SP": 0,
    "LCL": 1,
    "ARG": 2,
    "THIS": 3,
    "THAT": 4,
    "SCREEN": 16384,
    "KBD": 24576,
    }

for i in range(0,16):
     label = "R" + str(i) 
     tablesymb[label] = i

cursor = 16
root = sys.argv[1]

def removeExtras(line):
        bit =line[0]
        if char == "\n" or char == "/":
            return ""
        elif char == " ":
            return removeExtras(line[1:])

def nullJumpFields(line):
        line = line[:-1]
        if not "=" in line:
          line = "null=" + line
        if not ";" in line:
            line = line + ";null"
        return line

def addVar(label):
        global cursor
        table[label] = cursor
        cursor += 1
        return table[label]

def transA(line):
        if line[1].isalpha():
            label=line[1:-1]
            aVal = tablesymb.get(label, -1)
            if aVal == -1:
                aVal = addVar(label)
        else:
            aVal =int(line[1:])
        bVal = bin(aVal)[2:].zfill(16)
        return bVal

def transC(line):
    line = removeExtras(line)
    temp = line.split("=")
    dCode = Destination.get(temp[0], "destFail")
    temp = temp[1].split(";")
    cCode = comp.get(temp[0], "compFail")
    jCode = jump.get(temp[1], "jumpFail")
    return cCode, dCode, jCode

def translate(line):
    if line[0] == "@":
        return transA(line)
    else:
        codes = transC(line)
        return "111" + codes[0] + codes[1] + codes[2]

def passA():
    infile = open(root + ".asm")
    outfile = open(root + ".tmp", "w")

    lineNum = 0
    for line in infile:
        stLine = line.strip(line)
        if stLine != "":
            if stLine[0] == "(":
                label = stLine[1:-1]
                tablesymb[label] = lineNum
                stLine = ""
            else:
                lineNum += 1
                outfile.write(stLine + "\n")

    infile.close()
    outfile.close()


def Assemble():
    infile = open(root + ".tmp")
    outfile = open(root + ".hack", "w")

    for line in infile:
        trLine = translate(line)
        outfile.write(trLine + "\n")

    infile.close()
    outfile.close()
    os.remove(root + ".tmp")



 # Now to run the actual program
passA()
Assemble()
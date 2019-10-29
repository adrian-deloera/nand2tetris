import sys, os

comp = {
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


dest = {
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

table = {
    "R0": 0,
    "R1": 1,
    "R2": 2,
    "R3": 3,
    "R4": 4,
    "R5": 5,
    "R6": 6,
    "R7": 7,
    "R8": 8,
    "R9": 9,
    "R10": 10,
    "R11": 11,
    "R12": 12,
    "R13": 13,
    "R14": 14,
    "R15": 15,
    "R16": 16,
    
    "SCREEN": 16384,
    "KBD": 24576,
    "SP": 0,
    "LCL": 1,
    "ARG": 2,
    "THIS": 3,
    "THAT": 4,
    }

for i in range(0,16):
  label = "R" + str(i)
  table[label] = i


nextVarStorage = 16    # memory cursor for variable storage
root = str(input())     # file that is inputted by the user
lastSlash = 0

try:
   lastSlash = root.rindex("/")
except:
  pass

rootStrLength = len(root)
rootStripped = root[lastSlash:rootStrLength].strip(".asm") # file name without the extenstion

def fillGaps(line):
  line = line[:-1]
  if not "=" in line:
    line = "null=" + line
  if not ";" in line:
    line = line + ";null"
  return line

def cleanLines(line):
  char = line[0]
  if char == "\n" or char == "/":
    return ""
  elif char == " ":
    return cleanLines(line[1:])
  else:
    return char + cleanLines(line[1:])


def handleVariables(label):
  nextVarStorage += 1
  table[label] = nextVarStorage
  return table[label]

def aBits(line):
  if line[1].isalpha():
    label = line[1:-1]
    aValue = table.get(label, -1)
    if aValue == -1:
      aValue = handleVariables(label)
  else:
    aValue = int(line[1:])
  bValue = bin(aValue)[2:].zfill(16)
  return bValue
 
def cBits(line):
  line = fillGaps(line)
  temp = line.split("=")
  destCode = dest.get(temp[0], "destFAIL")
  temp = temp[1].split(";")
  compCode = comp.get(temp[0], "compFAIL")
  jumpCode = jump.get(temp[1], "jumpFAIL")
  return compCode, destCode, jumpCode

def distinguishInstructionType(line):
  if line[0] == "@":
    return aBits(line)
  else:
    codes = cBits(line)
    return "111" + codes[0] + codes[1] + codes[2]

def handleJumpsAndClean():
  infile = open(root)
  outfile = open(rootStripped + ".tmp", "w")

  lineNumber = 0
  for line in infile:
    sline = cleanLines(line)
    if sline != "":
      if sline[0] == "(":
        label = sline[1:-1]
        table[label] = lineNumber
        sline = ""
      else:
        lineNumber += 1
        outfile.write(sline + "\n")

  infile.close()
  outfile.close()

def makeHackFile():
  infile = open(rootStripped + ".tmp")
  outfile = open(rootStripped + ".hack", "w")

  for line in infile:
    tline = distinguishInstructionType(line)
    outfile.write(tline + "\n")

  infile.close()
  outfile.close()
  os.remove(rootStripped + ".tmp")


# Actually run the dang thing
handleJumpsAndClean()
makeHackFile()
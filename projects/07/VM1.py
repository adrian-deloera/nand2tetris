import os, sys

class Translator:
  def __init__(self, dest):
    self.root = dest[:-4].split('/')[-1]
    self.outputFile = open(dest, "w")
    self.nextLabel = 0

  def setFileName(self, source):
    self.fileName = source[:-3]

  def writeArithmetic(self, command):
    trans = ""
    if command == "add":
      trans += "@SP\n" # pop into D
      trans += "AM=M-1\n"
      trans += "D=M\n" 
      trans += "@SP\n" # pop into M
      trans += "AM=M-1\n" 
      trans += "M=D+M\n" # push onto M
      trans += "@SP\n"
      trans += "M=M+1\n" 
    elif command == "sub":
      trans += "@SP\n" # pop into D
      trans += "AM=M-1\n"
      trans += "D=M\n" 
      trans += "@SP\n" # pop into M
      trans += "AM=M-1\n" 
      trans += "M=M-D\n" # push onto M
      trans += "@SP\n"
      trans += "M=M+1\n" 
    elif command == "neg":
      trans += "@SP\n" # put value in M
      trans += "A=M-1\n" 
      trans += "M=-M\n" # negate
    elif command == "not":
      trans += "@SP\n" # put value in M
      trans += "A=M-1\n" 
      trans += "M=!M\n" # negate
    elif command == "or":
      trans += "@SP\n" # pop into D
      trans += "AM=M-1\n"
      trans += "D=M\n" 
      trans += "@SP\n" # put value in M
      trans += "A=M-1\n"
      trans += "M=D|M\n" # put result in stack
    elif command == "and":
      trans += "@SP\n" # pop into D
      trans += "AM=M-1\n"
      trans += "D=M\n" 
      trans += "@SP\n" # get into M
      trans += "A=M-1\n"
      trans += "M=D&M\n" # put result in stack
    elif command == "eq":
      label = str(self.nextLabel)
      self.nextLabel += 1
      trans += "@SP\n" # pop into D
      trans += "AM=M-1\n"
      trans += "D=M\n" 
      trans += "@SP\n" # get in M
      trans += "A=M-1\n"
      trans += "D=M-D\n" # D = older value - newer
      trans += "M=-1\n" # put true on stack
      trans += "@eqTrue" + label + "\n" # and jump to end 
      trans += "D;JEQ\n"
      trans += "@SP\n" # set to false otherwise
      trans += "A=M-1\n"
      trans += "M=0\n" 
      trans += "(eqTrue" + label + ")\n"
    elif command == "gt":
      label = str(self.nextLabel)
      self.nextLabel += 1
      trans += "@SP\n" # pop into D
      trans += "AM=M-1\n"
      trans += "D=M\n" 
      trans += "@SP\n" # put value in M
      trans += "A=M-1\n"
      trans += "D=M-D\n" # D = older value - newer
      trans += "M=-1\n" # tentatively put true on stack
      trans += "@gtTrue" + label + "\n" # and jump to end 
      trans += "D;JGT\n"
      trans += "@SP\n" # set to false otherwise
      trans += "A=M-1\n"
      trans += "M=0\n" 
      trans += "(gtTrue" + label + ")\n"
    elif command == "lt":
      label = str(self.nextLabel)
      self.nextLabel += 1
      trans += "@SP\n" # pop into D
      trans += "AM=M-1\n"
      trans += "D=M\n" 
      trans += "@SP\n" # put value in M
      trans += "A=M-1\n"
      trans += "D=M-D\n" # D = older value - newer
      trans += "M=-1\n" # tentatively put true on stack
      trans += "@ltTrue" + label + "\n" # and jump to end
      trans += "D;JLT\n"
      trans += "@SP\n" # set to false otherwise
      trans += "A=M-1\n"
      trans += "M=0\n" 
      trans += "(ltTrue" + label + ")\n"
    else:
      trans = command + " not implemented yet\n"
    self.outputFile.write("// " + command + "\n" + trans)

  def writePushPop(self, command, segment, index):
    trans = ""
    if command == "push":
      trans += "// push " + segment + index + "\n"
      if segment == "constant":
        trans += "@" + index + "\n" # load index into A
        trans += "D=A\n" # move it to D
        trans += "@SP\n" # put 0 in A (M[0] contains stack pointer)
        trans += "A=M\n" # get stack pointer
        trans += "M=D\n" # put D in stack
        trans += "@SP\n" # load stack pointer address into A
        trans += "M=M+1\n" # increment stack pointer
      elif segment == "static":
        trans += "@" + self.root + "." + index + "\n"
        trans += "D=M\n"
        trans += "@SP\n" 
        trans += "A=M\n" 
        trans += "M=D\n"
        trans += "@SP\n"
        trans += "M=M+1\n"
      elif segment == "this":
        trans += "@" + index + "\n" # put value in D
        trans += "D=A\n"
        trans += "@THIS\n"
        trans += "A=M+D\n" 
        trans += "D=M\n"
        trans += "@SP\n" # put it in stack
        trans += "A=M\n"
        trans += "M=D\n"
        trans += "@SP\n" # increment stack pointer
        trans += "M=M+1\n"
      elif segment == "that":
        trans += "@" + index + "\n" # get value into D
        trans += "D=A\n"
        trans += "@THAT\n"
        trans += "A=M+D\n" 
        trans += "D=M\n"
        trans += "@SP\n" # put it in the stack
        trans += "A=M\n"
        trans += "M=D\n"
        trans += "@SP\n" # increment stack pointer
        trans += "M=M+1\n"
      elif segment == "argument":
        trans += "@" + index + "\n" # put value in D
        trans += "D=A\n"
        trans += "@ARG\n"
        trans += "A=M+D\n" 
        trans += "D=M\n"
        trans += "@SP\n" # put it in the stack
        trans += "A=M\n"
        trans += "M=D\n"
        trans += "@SP\n" # increment stack pointer
        trans += "M=M+1\n"
      elif segment == "local":
        trans += "@" + index + "\n" # put value into D
        trans += "D=A\n"
        trans += "@LCL\n"
        trans += "A=M+D\n" 
        trans += "D=M\n"
        trans += "@SP\n" # put it in the stack
        trans += "A=M\n"
        trans += "M=D\n"
        trans += "@SP\n" # increment stack pointer
        trans += "M=M+1\n"
      elif segment == "temp":
        trans += "@" + index + "\n" # put value into D
        trans += "D=A\n"
        trans += "@5\n"
        trans += "A=A+D\n" 
        trans += "D=M\n"
        trans += "@SP\n" # put it in the stack
        trans += "A=M\n"
        trans += "M=D\n"
        trans += "@SP\n" # increment stack pointer
        trans += "M=M+1\n"
      elif segment == "pointer":
        trans += "@" + index + "\n" # get value into D
        trans += "D=A\n"
        trans += "@3\n"
        trans += "A=A+D\n" 
        trans += "D=M\n"
        trans += "@SP\n" # put it in the stack
        trans += "A=M\n"
        trans += "M=D\n"
        trans += "@SP\n" # increment stack pointer
        trans += "M=M+1\n"
      else:
        trans += segment + "Can't push\n"
    elif command == "pop":
      trans += "// pop " + segment + index + "\n"
      if segment == "static":
        trans += "@SP\n" # pop in D
        trans += "AM=M-1\n"
        trans += "D=M\n"
        trans += "@" + self.root + "." + index + "\n"
        trans += "M=D\n"
      elif segment == "this":
        trans += "@" + index + "\n" # put address in R13
        trans += "D=A\n"
        trans += "@THIS\n"
        trans += "D=M+D\n" 
        trans += "@R13\n"
        trans += "M=D\n"
        trans += "@SP\n" # pop in D
        trans += "AM=M-1\n"
        trans += "D=M\n"
        trans += "@R13\n" # address in A 
        trans += "A=M\n"
        trans += "M=D\n"
      elif segment == "that":
        trans += "@" + index + "\n" # get address into R13
        trans += "D=A\n"
        trans += "@THAT\n"
        trans += "D=M+D\n" 
        trans += "@R13\n"
        trans += "M=D\n"
        trans += "@SP\n" # pop in D
        trans += "AM=M-1\n"
        trans += "D=M\n"
        trans += "@R13\n" # address in A 
        trans += "A=M\n"
        trans += "M=D\n"
      elif segment == "argument":
        trans += "@" + index + "\n" # get address into R13
        trans += "D=A\n"
        trans += "@ARG\n"
        trans += "D=M+D\n" 
        trans += "@R13\n"
        trans += "M=D\n"
        trans += "@SP\n" # pop in D
        trans += "AM=M-1\n"
        trans += "D=M\n"
        trans += "@R13\n" # address in A
        trans += "A=M\n"
        trans += "M=D\n"
      elif segment == "local":
        trans += "@" + index + "\n" # putet address into R13
        trans += "D=A\n"
        trans += "@LCL\n"
        trans += "D=M+D\n" 
        trans += "@R13\n"
        trans += "M=D\n"
        trans += "@SP\n" # pop in D
        trans += "AM=M-1\n"
        trans += "D=M\n"
        trans += "@R13\n" # address in A
        trans += "A=M\n"
        trans += "M=D\n"
      elif segment == "pointer":
        trans += "@" + index + "\n" # pet address in R13
        trans += "D=A\n"
        trans += "@3\n"
        trans += "D=A+D\n" 
        trans += "@R13\n"
        trans += "M=D\n"
        trans += "@SP\n" # pop in D
        trans += "AM=M-1\n"
        trans += "D=M\n"
        trans += "@R13\n" # address in A 
        trans += "A=M\n"
        trans += "M=D\n"
      elif segment == "temp":
        trans += "@" + index + "\n" # put address into R13
        trans += "D=A\n"
        trans += "@5\n"
        trans += "D=A+D\n" 
        trans += "@R13\n"
        trans += "M=D\n"
        trans += "@SP\n" # pop into D
        trans += "AM=M-1\n"
        trans += "D=M\n"
        trans += "@R13\n" # address in A
        trans += "A=M\n"
        trans += "M=D\n"
      else:
        trans += segment + "Can't pop\n"
    self.outputFile.write(trans)

  def writeError(self):
    self.outputFile.write("Not a Command\n")


class ParseLines:
  def __init__(self, source):
    self.infile = open(source)
    self.command = ["nada"]
    self.advanceReachedEOF = False

    self.cType = {
        "sub" : "math",
        "add" : "math",
        "neg" : "math",
        "eq"  : "math",
        "gt"  : "math",
        "lt"  : "math",
        "and" : "math",
        "or"  : "math",
        "not" : "math",
        "push" : "push",
        "pop"  : "pop",
        "EOF"  : "EOF",
        }

  def hasMoreCommands(self):
    position = self.infile.tell()
    self.advance()
    self.infile.seek(position)
    return not self.advanceReachedEOF

  def advance(self):
    thisLine = self.infile.readline()
    if thisLine == '':
      self.advanceReachedEOF = True
    else:
      splitLine = thisLine.split("/")[0].strip()
      if splitLine == '':
        self.advance()
      else:
        self.command = splitLine.split()

  def commandType(self):
    return self.cType.get(self.command[0], "invalid cType")

  def arg1(self):
    return self.command[1]

  def arg2(self):
    return self.command[2]

    
def main():
  root = str(input())
  rootname = root.strip(".vm")
  parse = ParseLines(root)
  writer = Translator(rootname + ".asm")
  
  while parse.hasMoreCommands():
    parse.advance()
    cType = parse.commandType()
    if cType == "push" or cType == "pop":
      writer.writePushPop(cType, parse.arg1(), parse.arg2())
    elif cType == "math":
      writer.writeArithmetic(parse.command[0])
    else:
      writer.writeError()

if __name__ == "__main__":
  main()

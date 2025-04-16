import math


class ChronospatialComputer:

    def __init__(self, fileName: str):
        with open(fileName, 'r') as f:
            lines = f.readlines()
            register_a = int(lines[0].split(": ")[1].strip())
            register_b = int(lines[1].split(": ")[1].strip())
            register_c = int(lines[2].split(": ")[1].strip())
            program = lines[4].split(": ")[1].split(",")
            program = list(map(int,program))
            print()

        self.reg_a = register_a
        self.reg_b = register_b
        self.reg_c = register_c
        self.program = program
        self.out = []
        self.instruction_pointer = 0
    
    def _combo(self,combo_op):
        combo_dict = {
            0:0,
            1:1,
            2:2,
            3:3,
            4:self.reg_a,
            5:self.reg_b,
            6:self.reg_c
        }
        return combo_dict[combo_op]

    def _adv(self):
        if(self.instruction_pointer + 1 >= len(self.program)):
            return False
        combo_op = self.program[self.instruction_pointer + 1]
        if(combo_op != 7):
            combo_out = self._combo(combo_op)
        else:
            print("Invalid program")
            return False
        self.reg_a = math.trunc(self.reg_a/pow(2,combo_out))
        self.instruction_pointer += 2

    def _bxl(self):
        if(self.instruction_pointer + 1 >= len(self.program)):
            return False
        literal_op = self.program[self.instruction_pointer + 1]
        self.reg_b ^= literal_op
        self.instruction_pointer += 2

    def _bst(self):
        if(self.instruction_pointer + 1 >= len(self.program)):
            return False
        combo_op = self.program[self.instruction_pointer + 1]
        if(combo_op != 7):
            combo_out = self._combo(combo_op)
        else:
            print("Invalid program")
            return False
        self.reg_b = combo_out % 8
        self.instruction_pointer += 2
    
    def _jnz(self):
        if(self.reg_a > 0):
            if(self.instruction_pointer + 1 >= len(self.program)):
                return False
            literal_op = self.program[self.instruction_pointer + 1]
            self.instruction_pointer = literal_op
        else:
            self.instruction_pointer += 2
    
    def _bxc(self):
        self.reg_b = self.reg_b ^ self.reg_c
        self.instruction_pointer += 2
        
    def _out(self):
        if(self.instruction_pointer + 1 >= len(self.program)):
            return False
        combo_op = self.program[self.instruction_pointer + 1]
        if(combo_op != 7):
            combo_out = self._combo(combo_op)
        else:
            print("Invalid program")
            return False      
        self.out = self.out + [combo_out % 8]
        self.instruction_pointer += 2
        
    def _bdv(self):
        if(self.instruction_pointer + 1 >= len(self.program)):
            return False
        combo_op = self.program[self.instruction_pointer + 1]
        if(combo_op != 7):
            combo_out = self._combo(combo_op)
        else:
            print("Invalid program")
            return False        
        self.reg_b = math.trunc(self.reg_a/pow(2,combo_out))
        self.instruction_pointer += 2
    
    def _cdv(self):
        if(self.instruction_pointer + 1 >= len(self.program)):
            return False
        combo_op = self.program[self.instruction_pointer + 1]
        if(combo_op != 7):
            combo_out = self._combo(combo_op)
        else:
            print("Invalid program")
            return False       
        self.reg_c = math.trunc(self.reg_a/pow(2,combo_out))
        self.instruction_pointer += 2

    def run_program(self):
        
        while(self.instruction_pointer < len(self.program)):
            operand = self.program[self.instruction_pointer]
            match operand:
                case 0:
                    if(self._adv() != None):
                        break
                case 1:
                    if(self._bxl() != None):
                        break                    
                case 2:
                    if(self._bst() != None):
                        break
                case 3:
                    if(self._jnz() != None):
                        break
                case 4:
                    if(self._bxc() != None):
                        break
                case 5:
                    if(self._out() != None):
                        break
                case 6:
                    if(self._bdv() != None):
                        break
                case 7:
                    if(self._cdv() != None):
                        break
        print("Output:")
        print(",".join(list(map(str,self.out))))
        print(f"Registar A :{self.reg_a}")
        print(f"Registar B :{self.reg_b}")
        print(f"Registar C :{self.reg_c}")

if __name__ == "__main__":
    fileName = "input1.csv"
    computer = ChronospatialComputer(fileName)
    computer.run_program()
    
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
        operand = self.program[self.instruction_pointer + 1]
        operand = self._combo(operand)
        self.reg_a = self.reg_a >> operand
        

    def _bxl(self):
        operand = self.program[self.instruction_pointer + 1]
        self.reg_b ^= operand

    def _bst(self):
        operand = self.program[self.instruction_pointer + 1]
        operand = self._combo(operand)
        self.reg_b = operand & 7
    
    def _jnz(self):
        if(self.reg_a > 0):            
            operand = self.program[self.instruction_pointer + 1]
            self.instruction_pointer = operand - 2        
    
    def _bxc(self):
        self.reg_b ^= self.reg_c
        
    def _out(self):
        operand = self.program[self.instruction_pointer + 1]
        operand = self._combo(operand)        
        return operand & 7
        
    def _bdv(self):
        operand = self.program[self.instruction_pointer + 1]
        operand = self._combo(operand)
        self.reg_b = self.reg_a >> operand
    
    def _cdv(self):
        operand = self.program[self.instruction_pointer + 1]
        operand = self._combo(operand)
        self.reg_c = self.reg_a >> operand

    def run_program(self, reg_a = None):
        
        if(reg_a != None):
            self.reg_a = reg_a
            self.reg_b = 0
            self.reg_c = 0
        while(self.instruction_pointer < len(self.program)):
            operand = self.program[self.instruction_pointer]
            match operand:
                case 0:
                    self._adv()
                case 1:
                    self._bxl()
                case 2:
                    self._bst()
                case 3:
                    self._jnz()                    
                case 4:
                    self._bxc()
                case 5:
                    return self._out()
                case 6:
                    self._bdv()            
                case 7:
                    self._cdv()
            
            self.instruction_pointer += 2
        
        # print(",".join(list(map(str,self.out))))
            
    def match_program(self, match_idx, curr_a):
        if (match_idx < 0):
            # found the resulting reg_a value
            print(curr_a)
            return True
        for test_val in range(8):
            new_a = curr_a << 3 | test_val
            self.reg_a = new_a
            self.instruction_pointer = 0
            # self.out = []
            res = self.run_program(reg_a=new_a)
            if(res == self.program[match_idx]):
                if(self.match_program(match_idx - 1, curr_a << 3 | test_val)):
                    return True                
        return False

if __name__ == "__main__":
    fileName = "input1.csv"
    computer = ChronospatialComputer(fileName)
    computer.match_program(len(computer.program) - 1, 0)
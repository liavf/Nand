
from Parser import Parser
from SymbolTable import SymbolTable
from Code import Code

class HackAssembler:
    def __init__(self, input_file, output_file):
        self.parser = Parser(input_file)
        self.symbol_table = SymbolTable()
        self.code = Code()
        self.output = output_file
        self.full_text = ""
    
    def first_pass(self):
        command_num = -1
        while self.parser.has_more_commands():
            self.parser.advance()

            if self.parser.command_type() != "L_COMMAND":
                command_num += 1

            else:
                symbol = self.parser.symbol()
                addr = command_num + 1
                self.symbol_table.add_entry(symbol, addr)
        self.parser.lines_read = -1
            
       
    def second_pass(self):
        while self.parser.has_more_commands():
            self.parser.advance()

            if self.parser.command_type() == "A_COMMAND":
                instruction = self.assemble_A()
                self.full_text += instruction + "\n"
  
            elif self.parser.command_type() == "C_COMMAND":
                instruction = self.assemble_C()
                self.full_text += instruction + "\n"
        self.output.write(self.full_text)
            
    
    def assemble_A(self):
        symbol = self.parser.symbol()
        if not symbol.isnumeric():
            if not self.symbol_table.contains(symbol):
                loc = self.symbol_table.counter
                self.symbol_table.counter += 1
                self.symbol_table.add_entry(symbol, loc)
            addr = self.symbol_table.get_address(symbol) 
            instruction = "0" + addr
        else:
            instruction = bin(int(symbol)).replace("0b", "").zfill(16)  
        
        return instruction
    
    def assemble_C(self):
        instruction = "1"
        comp = self.parser.comp()
        instruction += self.code.comp(comp)
        dest = self.parser.dest()
        instruction += self.code.dest(dest)
        jump = self.parser.jump()
        instruction += self.code.jump(jump)
        return instruction
        
        
"""
This file is part of nand2tetris, as taught in The Hebrew University, and
was written by Aviv Yaish. It is an extension to the specifications given
[here](https://www.nand2tetris.org) (Shimon Schocken and Noam Nisan, 2017),
as allowed by the Creative Common Attribution-NonCommercial-ShareAlike 3.0
Unported [License](https://creativecommons.org/licenses/by-nc-sa/3.0/).
"""


class SymbolTable:
    """
    A symbol table that keeps a correspondence between symbolic labels and 
    numeric addresses.
    """

    def __init__(self) -> None:
        """Creates a new symbol table initialized with all the predefined symbols
        and their pre-allocated RAM addresses, according to section 6.2.3 of the
        book.
        """
        # Your code goes here!
        self.table =  {'SP': '000000000000000',
            'LCL': '000000000000001',
            'ARG': '000000000000010',
           'THIS': '000000000000011',
           'THAT': '000000000000100',
             'R0': '000000000000000',
             'R1': '000000000000001',
             'R2': '000000000000010',
             'R3': '000000000000011',
             'R4': '000000000000100',
             'R5': '000000000000101',
             'R6': '000000000000110',
             'R7': '000000000000111',
             'R8': '000000000001000',
             'R9': '000000000001001',
            'R10': '000000000001010',
            'R11': '000000000001011',
            'R12': '000000000001100',
            'R13': '000000000001101',
            'R14': '000000000001110',
            'R15': '000000000001111',
         'SCREEN': '100000000000000',
            'KBD': '110000000000000', }
        self.counter = 16

    def add_entry(self, symbol: str, address: int) -> None:
        """Adds the pair (symbol, address) to the table.

        Args:
            symbol (str): the symbol to add.
            address (int): the address corresponding to the symbol.
        """
        # Your code goes here!
        if not self.contains(symbol):
            self.table[symbol] = bin(int(address)).replace("0b", "").zfill(15)
            
            

    def contains(self, symbol: str) -> bool:
        """Does the symbol table contain the given symbol?

        Args:
            symbol (str): a symbol.

        Returns:
            bool: True if the symbol is contained, False otherwise.
        """
        # Your code goes here!
        return symbol in self.table

    def get_address(self, symbol: str) -> str:
        """Returns the address associated with the symbol.

        Args:
            symbol (str): a symbol.

        Returns:
            int: the address associated with the symbol.
        """
        # Your code goes here!
        return self.table[symbol]

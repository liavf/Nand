"""
This file is part of nand2tetris, as taught in The Hebrew University, and
was written by Aviv Yaish. It is an extension to the specifications given
[here](https://www.nand2tetris.org) (Shimon Schocken and Noam Nisan, 2017),
as allowed by the Creative Common Attribution-NonCommercial-ShareAlike 3.0
Unported [License](https://creativecommons.org/licenses/by-nc-sa/3.0/).
"""
import typing


class Parser:
    """Encapsulates access to the input code. Reads an assembly program
    by reading each command line-by-line, parses the current command,
    and provides convenient access to the commands components (fields
    and symbols). In addition, removes all white space and comments.
    """

    def __init__(self, input_file: typing.TextIO) -> None:
        """Opens the input file and gets ready to parse it.

        Args:
            input_file (typing.TextIO): input file.
        """
        # Your code goes here!
        # A good place to start is to read all the lines of the input:
        # input_lines = input_file.read().splitlines()
        self.input_lines = []
        input_lines = input_file.read().splitlines()
        for line in input_lines:
            if line and not line.startswith("//"):
                self.input_lines.append(line.replace(" ", "").split("//")[0])
        self.num_lines = len(self.input_lines)
        self.lines_read = -1
        self.curr_command = self.input_lines[self.lines_read]

    def has_more_commands(self) -> bool:
        """Are there more commands in the input?

        Returns:
            bool: True if there are more commands, False otherwise.
        """
        # Your code goes here!
        if self.lines_read + 1 < self.num_lines:
            return True
        else:
            return False

    def advance(self) -> None:
        """Reads the next command from the input and makes it the current command.
        Should be called only if has_more_commands() is true.
        """
        # Your code goes here!
        self.lines_read += 1

    def command_type(self) -> str:
        """
        Returns:
            str: the type of the current command:
            "A_COMMAND" for @Xxx where Xxx is either a symbol or a decimal number
            "C_COMMAND" for dest=comp;jump
            "L_COMMAND" (actually, pseudo-command) for (Xxx) where Xxx is a symbol
        """
        # Your code goes here!
        command = self.input_lines[self.lines_read]
        if command.startswith("@"):
            return "A_COMMAND"
        elif command.startswith("("):
            return "L_COMMAND"
        else:
            return "C_COMMAND"

    def symbol(self) -> str:
        """
        Returns:
            str: the symbol or decimal Xxx of the current command @Xxx or
            (Xxx). Should be called only when command_type() is "A_COMMAND" or 
            "L_COMMAND".
        """
        # Your code goes here!
        command = self.input_lines[self.lines_read]
        if self.command_type() == "A_COMMAND":
            return command.replace("@", "")
        if self.command_type() == "L_COMMAND":
            return command.replace("(", "").replace(")","")

    def dest(self) -> str:
        """
        Returns:
            str: the dest mnemonic in the current C-command. Should be called 
            only when commandType() is "C_COMMAND".
        """
        # Your code goes here!
        command = self.input_lines[self.lines_read]
        if "=" in command:
            return command.split("=")[0] 
        else:
            return "NULL"

    def comp(self) -> str:
        """
        Returns:
            str: the comp mnemonic in the current C-command. Should be called 
            only when commandType() is "C_COMMAND".
        """
        # Your code goes here!
        command = self.input_lines[self.lines_read]
        if "=" in command:
            command = command.split("=")[1]
        if ";" in command:
            command = command.split(";")[0]
        if command:
            return command
        else:
            return "NULL"
            

    def jump(self) -> str:
        """
        Returns:
            str: the jump mnemonic in the current C-command. Should be called 
            only when commandType() is "C_COMMAND".
        """
        # Your code goes here!
        command = self.input_lines[self.lines_read]
        if ";" in command:
            return command.split(";")[1] 
        else:
            return "NULL"

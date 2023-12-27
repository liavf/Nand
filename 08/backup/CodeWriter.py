"""
This file is part of nand2tetris, as taught in The Hebrew University, and
was written by Aviv Yaish. It is an extension to the specifications given
[here](https://www.nand2tetris.org) (Shimon Schocken and Noam Nisan, 2017),
as allowed by the Creative Common Attribution-NonCommercial-ShareAlike 3.0
Unported [License](https://creativecommons.org/licenses/by-nc-sa/3.0/).
"""
import typing


class CodeWriter:
    """Translates VM commands into Hack assembly code."""

    def __init__(self, output_stream: typing.TextIO) -> None:
        """Initializes the CodeWriter.

        Args:
            output_stream (typing.TextIO): output stream.
        """
        # Your code goes here!
        # Note that you can write to output_stream like so:
        # output_stream.write("Hello world! \n")
        self.output = output_stream
        self.jmp_num = 0
        self.filename = None
        self.curr_function = "null"
        self.call_count = 0

    def set_file_name(self, filename: str) -> None:
        """Informs the code writer that the translation of a new VM file is 
        started.

        Args:
            filename (str): The name of the VM file.
        """
        # Your code goes here!
        # This function is useful when translating code that handles the
        # static segment. For example, in order to prevent collisions between two
        # .vm files which push/pop to the static segment, one can use the current
        # file's name in the assembly variable's name and thus differentiate between
        # static variables belonging to different files.
        # To avoid problems with Linux/Windows/MacOS differences with regards
        # to filenames and paths, you are advised to parse the filename in
        # the function "translate_file" in Main.py using python's os library,
        # For example, using code similar to:
        # input_filename, input_extension = os.path.splitext(os.path.basename(input_file.name))
        self.filename = filename

    def write_arithmetic(self, command: str) -> None:
        """Writes assembly code that is the translation of the given 
        arithmetic command. For the commands eq, lt, gt, you should correctly
        compare between all numbers our computer supports, and we define the
        value "true" to be -1, and "false" to be 0.

        Args:
            command (str): an arithmetic command.
        """
        # Your code goes here!
        text = "// {}\n".format(command)
        basic_template = \
"""@SP
AM=M-1
D=M
A=A-1
"""
        jump_template = \
"""@SP
AM=M-1
D=M
A=A-1
D=M-D
@FALSE{jmp_num}
D;{jmp_condition}
@SP
A=M-1
M={true_val}
@CONT{jmp_num}
0;JMP
(FALSE{jmp_num})
@SP
A=M-1
M={false_val}
(CONT{jmp_num})
"""
        ar_dict = {"add": "M=M+D\n",
                "sub": "M=M-D\n",
                "neg": "@SP\nA=M-1\nM=-M\n",
                "eq": "JNE",
                "gt": "JLE",
                "lt": "JGE",
                "and": "M=M&D\n",
                "or": "M=M|D\n",
                "not": "@SP\nA=M-1\nM=!M\n",
        }
        if command in ("not", "neg"):
            text += ar_dict[command]
        elif command in ("add", "sub", "and", "or"):
            text += basic_template + ar_dict[command]
        else:
            text += jump_template.format(jmp_num=self.jmp_num, true_val=-1, false_val=0, jmp_condition=ar_dict[command])
            self.jmp_num += 1
        self.output.write(text)
        

    def write_push_pop(self, command: str, segment: str, index: int) -> None:
        """Writes assembly code that is the translation of the given 
        command, where command is either C_PUSH or C_POP.

        Args:
            command (str): "C_PUSH" or "C_POP".
            segment (str): the memory segment to operate on.
            index (int): the index in the memory segment.
        """
        # Your code goes here!
        # Note: each reference to "static i" appearing in the file Xxx.vm should
        # be translated to the assembly symbol "Xxx.i". In the subsequent
        # assembly process, the Hack assembler will allocate these symbolic
        # variables to the RAM, starting at address 16.
        constant_push = \
"""@{}
D=A
@SP
A=M
M=D
@SP
M=M+1
""".format(index)
        this_that_dict = {'0': "THIS",
                          '1': "THAT"}
        static_pop = \
"""@SP
AM=M-1
D=M
@{}.{}
M=D
""".format(self.filename, index)
        static_push = \
"""@{}.{}
D=M
@SP
A=M
M=D
@SP
M=M+1
""".format(self.filename, index)
        static_dict = {"C_PUSH": static_push, "C_POP": static_pop}
        seg_dict = {"local": "LCL",
                    "argument": "ARG",
                    "this": "THIS",
                    "that": "THAT",
                    # "pointer": this_that_dict[index],
                    "temp": "R5",
                    # "static": str(16+index)
                    }
        text = "// " + command + " " + segment + " " + str(index) + "\n" 
        if segment == "constant":
            text += constant_push
        elif segment == "static":
            text += static_dict[command]
        elif segment == "pointer":
            if command == "C_PUSH":
                text += \
"""@{}
D=M
@SP
A=M
M=D
@SP
M=M+1
""".format(this_that_dict[index])
            else:
                text += \
"""@SP
AM=M-1
D=M
@{}
M=D
""".format(this_that_dict[index])
        else:
            if command == "C_PUSH":
                text += self.write_push(seg_dict[segment], index)
            if command == "C_POP":
                text += self.write_pop(seg_dict[segment], index)
        self.output.write(text)


    def write_push(self, segment, index):
        """Writes assembly code that is the translation of the given 
        command, where command is C_PUSH

        Args:
            segment (str): the memory segment to operate on.
            index (int): the index in the memory segment.
        """
        if segment == "R5":
            line = "D=A"
        else:
            line = "D=M"
        push_template = \
"""@{}
{}
@{}
A=D+A
D=M
@SP
A=M
M=D
@SP
M=M+1
""".format(segment, line, index)
        return push_template
    
    def write_pop(self, segment, index):
        """Writes assembly code that is the translation of the given 
        command, where command is C_POP

        Args:
            segment (str): the memory segment to operate on.
            index (int): the index in the memory segment.
        """
        if segment == "R5":
            line = "D=A"
        else:
            line = "D=M"
        pop_template = \
"""@{}
{}
@{}
D=D+A
@R13
M=D
@SP
AM=M-1
D=M
@R13
A=M
M=D
""".format(segment, line, index)
        return pop_template

    def write_label(self, label: str) -> None:
        """Writes assembly code that affects the label command. 
        Let "Xxx.foo" be a function within the file Xxx.vm. The handling of
        each "label bar" command within "Xxx.foo" generates and injects the symbol
        "Xxx.foo$bar" into the assembly code stream.
        When translating "goto bar" and "if-goto bar" commands within "foo",
        the label "Xxx.foo$bar" must be used instead of "bar".

        Args:
            label (str): the label to write.
        """
        # This is irrelevant for project 7,
        # you will implement this in project 8!
        text = f"//label {label}\n({self.curr_function}${label})\n"
        self.output.write(text)
    
    def write_goto(self, label: str) -> None:
        """Writes assembly code that affects the goto command.

        Args:
            label (str): the label to go to.
        """
        # This is irrelevant for project 7,
        # you will implement this in project 8!
        text = f"//goto {label}\n@{self.curr_function}${label}\n0;JMP\n"
        self.output.write(text)
    
    def write_if(self, label: str) -> None:
        """Writes assembly code that affects the if-goto command. 

        Args:
            label (str): the label to go to.
        """
        # This is irrelevant for project 7,
        # you will implement this in project 8!
        text = (f"//if-goto {label}\n"
            "@SP\n"
            "AM=M-1\n"
            "D=M\n"
            f"@{self.curr_function}${label}\n"
            "D;JNE\n"
        )
        self.output.write(text)
    
    def write_function(self, function_name: str, n_vars: int) -> None:
        """Writes assembly code that affects the function command. 
        The handling of each "function Xxx.foo" command within the file Xxx.vm
        generates and injects a symbol "Xxx.foo" into the assembly code stream,
        that labels the entry-point to the function's code.
        In the subsequent assembly process, the assembler translates this 
        symbol into the physical address where the function code starts.

        Args:
            function_name (str): the name of the function.
            n_vars (int): the number of local variables of the function.
        """
        # This is irrelevant for project 7,
        # you will implement this in project 8!
        # The pseudo-code of "function function_name n_vars" is:
        # (function_name)       // injects a function entry label into the code
        # repeat n_vars times:  // n_vars = number of local variables
        #   push constant 0     // initializes the local variables to 0
        self.curr_function = function_name
        text = "//function {} {}\n".format(function_name, n_vars)
        text += "({})\n".format(function_name)
        self.output.write(text)
        for i in range(int(n_vars)):
            self.write_push_pop("C_PUSH", "constant", "0")

    def write_call(self, function_name: str, n_args: int) -> None:
        """Writes assembly code that affects the call command. 
        Let "Xxx.foo" be a function within the file Xxx.vm.
        The handling of each "call" command within Xxx.foo's code generates and
        injects a symbol "Xxx.foo$ret.i" into the assembly code stream, where
        "i" is a running integer (one such symbol is generated for each "call"
        command within "Xxx.foo").
        This symbol is used to mark the return address within the caller's 
        code. In the subsequent assembly process, the assembler translates this
        symbol into the physical memory address of the command immediately
        following the "call" command.

        Args:
            function_name (str): the name of the function to call.
            n_args (int): the number of arguments of the function.
        """
        # This is irrelevant for project 7,
        # you will implement this in project 8!
        # The pseudo-code of "call function_name n_args" is:
        # push return_address   // generates a label and pushes it to the stack
        self.output.write("//call {} {}\n".format(function_name, n_args))
        call_num = self.call_count
        self.call_count += 1
        ret_addr = "{}$ret.{}".format(function_name, str(call_num))

        self.write_push_pop("C_PUSH", "constant", ret_addr)
        # push LCL              // saves LCL of the caller
        template = \
"""@{}
D=M
@SP
A=M
M=D
@SP
M=M+1
"""
        text = ""
        for seg in ["LCL", "ARG", "THIS", "THAT"]:
            text += template.format(seg)
#         self.write_push_pop("C_PUSH", "local", 0)
#         self.write_push_pop("C_PUSH", "argument", 0)
#         self.write_push_pop("C_PUSH", "this", 0)
#         self.write_push_pop("C_PUSH", "that", 0)
        # push ARG              // saves ARG of the caller
        # push THIS             // saves THIS of the caller
        # push THAT             // saves THAT of the caller
        # ARG = SP-5-n_args     // repositions ARG
        text += \
"""@SP
D=M
@{num}
D=D-A
@ARG
M=D
""".format(num=str(int(n_args)+5))
        # LCL = SP              // repositions LCL
        text += \
"""@SP
D=M
@LCL
M=D
"""
        # goto function_name    // transfers control to the callee
        text += \
"""@{}
0;JMP
""".format(function_name)
        # (return_address)      // injects the return address label into the code
        text += "({})\n".format(ret_addr)
        self.output.write(text)
    
    def write_return(self) -> None:
        """Writes assembly code that affects the return command."""
        # This is irrelevant for project 7,
        # you will implement this in project 8!
        frame = "@{}.frame".format(self.curr_function)
        ret_add = "@{}.ret".format(self.curr_function)
        # The pseudo-code of "return" is:
        # frame = LCL                   // frame is a temporary variable
        # return_address = *(frame-5)   // puts the return address in a temp var
        text = \
"""//return
@LCL
D=M
{frame}
M=D
@5
A=D-A
D=M
{ret_add}
M=D
""".format(frame=frame, ret_add=ret_add)
        self.output.write(text)
        # *ARG = pop()                  // repositions the return value for the caller
        self.output.write(self.write_pop("ARG", 0))
        # SP = ARG + 1                  // repositions SP for the caller
        text = \
"""@ARG
D=M+1
@SP
M=D
"""
        # self.output.write(text)
        # THAT = *(frame-1)             // restores THAT for the caller
        # THIS = *(frame-2)             // restores THIS for the caller
        # ARG = *(frame-3)              // restores ARG for the caller
        # LCL = *(frame-4)              // restores LCL for the caller
        template = \
"""@{index}
D=A
{frame}
A=M-D
D=M
@{seg}
M=D
"""
        frame_dict = {1:"THAT", 2:"THIS", 3:"ARG", 4:"LCL"}
        for i in range(1,5):
            text += template.format(index=str(i), frame=frame, seg=frame_dict[i])
        # goto return_address           // go to the return address
        text += ret_add + "\n" +\
        "A=M\n" + \
        "0;JMP\n"
        self.output.write(text)

    def write_init(self):
        """

        """
        text = "//init\n@256\nD=A\n@SP\nM=D\n"
        self.output.write(text)
        self.write_call("Sys.init", 0)



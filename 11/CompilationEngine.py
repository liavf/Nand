"""
This file is part of nand2tetris, as taught in The Hebrew University, and
was written by Aviv Yaish. It is an extension to the specifications given
[here](https://www.nand2tetris.org) (Shimon Schocken and Noam Nisan, 2017),
as allowed by the Creative Common Attribution-NonCommercial-ShareAlike 3.0
Unported [License](https://creativecommons.org/licenses/by-nc-sa/3.0/).
"""
import typing
from VMWriter import VMWriter
from SymbolTable import SymbolTable
from JackTokenizer import JackTokenizer

arithmetic_dict_binary = {'+': 'add',
                     '-': 'sub',
                     '*': 'call Math.multiply 2',
                     '/': 'call Math.divide 2',
                     '&amp;': 'and',
                     '|': 'or',
                     '&lt;': 'lt',
                     '&gt;': 'gt',
                     '=': 'eq'}

arithmetic_dict_unary = {'-': 'neg',
                         '~': 'not',
                         '^': 'shiftleft',
                         '#': 'shiftright'}

variable_dict = {'static': 'static',
                    'field': 'this',
                    'var': 'local',
                    'arg': 'argument'}


class CompilationEngine:
    """Gets input from a JackTokenizer and emits its parsed structure into an
    output stream.
    """

    def __init__(self, input_stream, output_stream) -> None:
        """
        Creates a new compilation engine with the given input and output. The
        next routine called must be compileClass()
        :param input_stream: The input stream.
        :param output_stream: The output stream.
        """
        # Your code goes here!
        # Note that you can write to output_stream like so:
        # output_stream.write("Hello world! \n")
        self.tokenizer = JackTokenizer(input_stream)
        self.writer = VMWriter(output_stream)
        self.symbol_table = SymbolTable()
        self.class_name = None
        self.while_label_num = 0
        self.if_label_num = 0

    def compile_class(self) -> None:
        """Compiles a complete class."""
        # Your code goes here!
        self.tokenizer.advance()
        self.tokenizer.advance()
        self.class_name = self.tokenizer.identifier()
        self.tokenizer.advance()
        self.tokenizer.advance()
        while self.tokenizer.token_type() == "keyword" and self.tokenizer.keyword() in ["static", "field"]:
            self.compile_class_var_dec()
        while self.tokenizer.token_type() == "keyword" and self.tokenizer.keyword() in ["constructor", "function", "method"]:
            self.compile_subroutine()

    def compile_class_var_dec(self) -> None:
        """Compiles a static declaration or a field declaration."""
        # Your code goes here!
        var_kind = self.tokenizer.keyword()
        self.tokenizer.advance()
        # if self.tokenizer.token_type() == "keyword":
        #     # self.output.write("<keyword> {} </keyword>\n".format(self.tokenizer.keyword()))
        var_type = self.tokenizer.keyword()
        # else:
        #     self.output.write("<identifier> {} </identifier>\n".format(self.tokenizer.identifier()))
        self.tokenizer.advance()
        # self.output.write("<identifier> {} </identifier>\n".format(self.tokenizer.identifier()))
        var_name = self.tokenizer.identifier()
        self.symbol_table.define(var_name, var_type, var_kind)
        self.tokenizer.advance()
        while self.tokenizer.token_type() == "symbol" and self.tokenizer.symbol() == ",": 
            # self.output.write("<symbol> {} </symbol>\n".format(self.tokenizer.symbol()))
            self.tokenizer.advance()
            # self.output.write("<identifier> {} </identifier>\n".format(self.tokenizer.identifier()))
            var_name = self.tokenizer.identifier()
            self.symbol_table.define(var_name, var_type, var_kind)
            self.tokenizer.advance()
        # self.output.write("<symbol> {} </symbol>\n".format(self.tokenizer.symbol()))
        self.tokenizer.advance()
        # self.output.write("</classVarDec>\n")

    def compile_subroutine(self) -> None:
        """
        Compiles a complete method, function, or constructor.
        You can assume that classes with constructors have at least one field,
        you will understand why this is necessary in project 11.
        """
        # Your code goes here!
        # self.output.write("<subroutineDec>\n")
        # self.output.write("<keyword> {} </keyword>\n".format(self.tokenizer.keyword()))
        subroutine_type = self.tokenizer.keyword()
        self.symbol_table.start_subroutine()
        self.tokenizer.advance()
        return_type = self.tokenizer.keyword()
        self.tokenizer.advance()
        subroutine_name = self.tokenizer.identifier()
        if subroutine_type == "method":
            self.symbol_table.define("this", self.class_name, "arg")
        # self.output.write("<identifier> {} </identifier>\n".format(self.tokenizer.identifier()))
        self.tokenizer.advance()
        # self.output.write("<symbol> {} </symbol>\n".format(self.tokenizer.symbol()))
        self.tokenizer.advance()
        params = self.compile_parameter_list()
        # self.output.write("<symbol> {} </symbol>\n".format(self.tokenizer.symbol()))
        self.tokenizer.advance()
        # self.output.write("<subroutineBody>\n")
        # self.output.write("<symbol> {} </symbol>\n".format(self.tokenizer.symbol()))
        self.tokenizer.advance()
        while self.tokenizer.token_type() == "keyword" and self.tokenizer.keyword() == "var":
            self.compile_var_dec()
        n_locals = self.symbol_table.var_count("var")
        self.writer.write_function(self.class_name + "." + subroutine_name, n_locals)

        if subroutine_type == "constructor":
            self.writer.write_push("constant", self.symbol_table.var_count("field"))
            self.writer.write_call("Memory.alloc", 1)
            self.writer.write_pop("pointer", 0)

        elif subroutine_type == 'method':
            self.writer.write_push('argument', 0)
            self.writer.write_pop('pointer', 0)
        # print("liav")
        self.compile_statements()
        # self.output.write("<symbol> {} </symbol>\n".format(self.tokenizer.symbol()))
        self.tokenizer.advance()

    def compile_parameter_list(self) -> None:
        """Compiles a (possibly empty) parameter list, not including the 
        enclosing "()".
        """
        # Your code goes here!
        # self.output.write("<parameterList>\n")
        params = 0
        if self.tokenizer.token_type() == "symbol" and self.tokenizer.symbol() == ")":
            # self.output.write("</parameterList>\n")
            return params
        # if self.tokenizer.token_type() == "keyword":
        #     self.output.write("<keyword> {} </keyword>\n".format(self.tokenizer.keyword()))
        # else:
        #     self.output.write("<identifier> {} </identifier>\n".format(self.tokenizer.identifier()))
        var_type = self.tokenizer.keyword()
        self.tokenizer.advance()
        # self.output.write("<identifier> {} </identifier>\n".format(self.tokenizer.identifier()))
        var_name = self.tokenizer.identifier()
        self.tokenizer.advance()
        self.symbol_table.define(var_name, var_type, "arg")
        params += 1
        while self.tokenizer.token_type() == "symbol" and self.tokenizer.symbol() == ",":
            # self.output.write("<symbol> {} </symbol>\n".format(self.tokenizer.symbol()))
            self.tokenizer.advance()
            # if self.tokenizer.token_type() == "keyword":
                # self.output.write("<keyword> {} </keyword>\n".format(self.tokenizer.keyword()))
            var_type = self.tokenizer.keyword()
            # else:
                # self.output.write("<identifier> {} </identifier>\n".format(self.tokenizer.identifier()))
            # var_name = self.tokenizer.identifier()
                # self.symbol_table.define(var_name, var_type, "arg")
                # print(var_name, var_type)
            self.tokenizer.advance()
            # self.output.write("<identifier> {} </identifier>\n".format(self.tokenizer.identifier()))
            var_name = self.tokenizer.identifier()
            self.symbol_table.define(var_name, var_type, "arg")
            params += 1
            self.tokenizer.advance()
        # self.output.write("</parameterList>\n")
        return params


    def compile_var_dec(self) -> None:
        """Compiles a var declaration."""
        # Your code goes here!
        # self.output.write("<varDec>\n")
        # self.output.write("<keyword> {} </keyword>\n".format(self.tokenizer.keyword()))
        var_kind = self.tokenizer.keyword()
        self.tokenizer.advance()
        # if self.tokenizer.token_type() == "keyword":
        #     self.output.write("<keyword> {} </keyword>\n".format(self.tokenizer.keyword()))
        # else:
        #     self.output.write("<identifier> {} </identifier>\n".format(self.tokenizer.identifier()))
        var_type = self.tokenizer.keyword()
        self.tokenizer.advance()
        # self.output.write("<identifier> {} </identifier>\n".format(self.tokenizer.identifier()))
        var_name = self.tokenizer.identifier()
        self.symbol_table.define(var_name, var_type, var_kind)
        self.tokenizer.advance()
        while self.tokenizer.token_type() == "symbol" and self.tokenizer.symbol() == ",":
            # self.output.write("<symbol> {} </symbol>\n".format(self.tokenizer.symbol()))
            self.tokenizer.advance()
            # self.output.write("<identifier> {} </identifier>\n".format(self.tokenizer.identifier()))
            var_name = self.tokenizer.identifier()
            self.symbol_table.define(var_name, var_type, var_kind)
            self.tokenizer.advance()
        # self.output.write("<symbol> {} </symbol>\n".format(self.tokenizer.symbol()))
        self.tokenizer.advance()
        # self.output.write("</varDec>\n")

    def compile_statements(self) -> None:
        """Compiles a sequence of statements, not including the enclosing 
        "{}".
        """
        # Your code goes here!
        # self.output.write("<statements>\n")
        while self.tokenizer.token_type() == "keyword" and self.tokenizer.keyword() in ["let", "if", "while", "do", "return"]:
            if self.tokenizer.keyword() == "let":
                self.compile_let()
            elif self.tokenizer.keyword() == "if":
                self.compile_if()
            elif self.tokenizer.keyword() == "while":
                self.compile_while()
            elif self.tokenizer.keyword() == "do":
                self.compile_do()
            elif self.tokenizer.keyword() == "return":
                self.compile_return()
        # self.output.write("</statements>\n")


    def compile_do(self) -> None:
        """Compiles a do statement."""
        # Your code goes here!
        # self.output.write("<doStatement>\n")
        # self.output.write("<keyword> {} </keyword>\n".format(self.tokenizer.keyword()))
        self.tokenizer.advance()
        self.compile_term()
        # self.output.write("<identifier> {} </identifier>\n".format(self.tokenizer.identifier()))
        # first = self.tokenizer.identifier()
        # self.tokenizer.advance()
        # exp_num = 0
        # func_name = first
        # if self.tokenizer.token_type() == "symbol" and self.tokenizer.symbol() == ".":
        #     # self.output.write("<symbol> {} </symbol>\n".format(self.tokenizer.symbol()))
        #     self.tokenizer.advance()
        #     # self.output.write("<identifier> {} </identifier>\n".format(self.tokenizer.identifier()))
        #     second = self.tokenizer.identifier()
        #     type_first = self.symbol_table.type_of(first)
        #     if type_first != None:
        #         kind = self.symbol_table.kind_of(first)
        #         index = self.symbol_table.index_of(first)
        #         self.writer.write_push(variable_dict[kind], index)
        #         exp_num += 1
        #         func_name = type_first + "." + second
        #     else:
        #         func_name += "." + second
        #     self.tokenizer.advance()
        # elif self.tokenizer.token_type() == "symbol" and self.tokenizer.symbol() == "(":
        #     self.writer.write_push("pointer", 0)
        #     func_name = self.class_name + "." + first
        #     exp_num += 1
        # # self.output.write("<symbol> {} </symbol>\n".format(self.tokenizer.symbol()))
        # self.tokenizer.advance()
        # exp_num += self.compile_expression_list()
        # self.writer.write_call(func_name, exp_num)
        # # self.output.write("<symbol> {} </symbol>\n".format(self.tokenizer.symbol()))
        # self.tokenizer.advance()
        # self.output.write("<symbol> {} </symbol>\n".format(self.tokenizer.symbol()))
        self.writer.write_pop("temp", 0)
        self.tokenizer.advance()
        # self.output.write("</doStatement>\n")


    def compile_let(self) -> None:
        """Compiles a let statement."""
        # Your code goes here!
        # self.output.write("<letStatement>\n")
        # self.output.write("<keyword> {} </keyword>\n".format(self.tokenizer.keyword()))
        self.tokenizer.advance()
        # self.output.write("<identifier> {} </identifier>\n".format(self.tokenizer.identifier()))
        first = self.tokenizer.identifier()
        kind = self.symbol_table.kind_of(first)
        index = self.symbol_table.index_of(first)
        self.tokenizer.advance()
        array = False
        if self.tokenizer.token_type() == "symbol" and self.tokenizer.symbol() == "[":
            array = True
            # self.output.write("<symbol> {} </symbol>\n".format(self.tokenizer.symbol()))
            self.tokenizer.advance()
            self.compile_expression()
            self.writer.write_push(variable_dict[kind], index)
            # self.output.write("<symbol> {} </symbol>\n".format(self.tokenizer.symbol()))
            self.writer.write_arithmetic('add')
            self.tokenizer.advance()
        # self.output.write("<symbol> {} </symbol>\n".format(self.tokenizer.symbol()))
        self.tokenizer.advance()
        self.compile_expression()
        if array:
            self.writer.write_pop("temp", 0)
            self.writer.write_pop("pointer", 1)
            self.writer.write_push("temp", 0)
            self.writer.write_pop("that", 0)
        else:
            # print(first, kind, index)
            self.writer.write_pop(variable_dict[kind], index)
        # self.output.write("<symbol> {} </symbol>\n".format(self.tokenizer.symbol()))
        self.tokenizer.advance()
        # self.output.write("</letStatement>\n")


    def compile_while(self) -> None:
        """Compiles a while statement."""
        # Your code goes here!
        # self.output.write("<whileStatement>\n")
        # self.output.write("<keyword> {} </keyword>\n".format(self.tokenizer.keyword()))
        label_num = self.while_label_num
        while_label = "WHILE_EXP" + str(label_num)
        end_label = "WHILE_END" + str(label_num)
        self.while_label_num += 1
        self.writer.write_label(while_label)
        self.tokenizer.advance()
        # self.output.write("<symbol> {} </symbol>\n".format(self.tokenizer.symbol()))
        self.tokenizer.advance()
        self.compile_expression()
        self.writer.write_arithmetic('not')
        self.writer.write_if(end_label)
        # self.output.write("<symbol> {} </symbol>\n".format(self.tokenizer.symbol()))
        self.tokenizer.advance()
        # self.output.write("<symbol> {} </symbol>\n".format(self.tokenizer.symbol()))
        self.tokenizer.advance()
        self.compile_statements()
        self.writer.write_goto(while_label)
        # self.output.write("<symbol> {} </symbol>\n".format(self.tokenizer.symbol()))
        
        self.writer.write_label(end_label)
        self.tokenizer.advance()
        # self.output.write("</whileStatement>\n")


    def compile_return(self) -> None:
        """Compiles a return statement."""
        # Your code goes here!
        # self.output.write("<returnStatement>\n")
        # self.output.write("<keyword> {} </keyword>\n".format(self.tokenizer.keyword()))
        self.tokenizer.advance()
        # print(self.tokenizer.token_type(), self.tokenizer.symbol())
        if self.tokenizer.token_type() != "symbol" or self.tokenizer.symbol() != ";":
            self.compile_expression()
        else:
            self.writer.write_push("constant", 0)
        # self.output.write("<symbol> {} </symbol>\n".format(self.tokenizer.symbol()))
        self.writer.write_return()
        self.tokenizer.advance()
        # self.output.write("</returnStatement>\n")
        

    def compile_if(self) -> None:
        """Compiles a if statement, possibly with a trailing else clause."""
        # Your code goes here!
        # self.output.write("<ifStatement>\n")
        # self.output.write("<keyword> {} </keyword>\n".format(self.tokenizer.keyword()))
        label_num = self.if_label_num
        # true_label = "IF_TRUE" + str(label_num)
        # false_label = "IF_FALSE" + str(label_num)
        # end_label = "IF_END" + str(label_num)
        false_label = "IF_FALSE" + str(label_num)
        end_label = "IF_END" + str(label_num)
        self.if_label_num += 1
        self.tokenizer.advance()
        # self.output.write("<symbol> {} </symbol>\n".format(self.tokenizer.symbol()))
        self.tokenizer.advance()
        self.compile_expression()
        # self.writer.write_arithmetic('neg')
        # self.output.write("<symbol> {} </symbol>\n".format(self.tokenizer.symbol()))
        self.tokenizer.advance()
        # self.output.write("<symbol> {} </symbol>\n".format(self.tokenizer.symbol()))
        self.tokenizer.advance()
        self.writer.write_arithmetic('not')
        self.writer.write_if(false_label)
        self.compile_statements()
        self.writer.write_goto(end_label)
        self.writer.write_label(false_label)
        # self.output.write("<symbol> {} </symbol>\n".format(self.tokenizer.symbol()))
        self.tokenizer.advance()
        if self.tokenizer.token_type() == "keyword" and self.tokenizer.keyword() == "else":
            # self.output.write("<keyword> {} </keyword>\n".format(self.tokenizer.keyword()))
            # self.writer.write_label(false_label)
            self.tokenizer.advance()
            # self.output.write("<symbol> {} </symbol>\n".format(self.tokenizer.symbol()))
            self.tokenizer.advance()
            self.compile_statements()
            # self.output.write("<symbol> {} </symbol>\n".format(self.tokenizer.symbol()))
            self.tokenizer.advance()
        self.writer.write_label(end_label)
        # self.output.write("</ifStatement>\n")


    def compile_expression(self) -> None:
        """Compiles an expression."""
        # Your code goes here!
        # self.output.write("<expression>\n")
        self.compile_term()
        while self.tokenizer.token_type() == "symbol" and self.tokenizer.symbol() in ["+", "-", "*", "/", "&amp;", "|", "&gt;", "&lt;", "="]:
            action = self.tokenizer.symbol()
            # self.output.write("<symbol> {} </symbol>\n".format(self.tokenizer.symbol()))
            self.tokenizer.advance()
            self.compile_term()
            self.writer.write_arithmetic(arithmetic_dict_binary[action])
        # self.output.write("</expression>\n")

    def compile_term(self) -> None:
        """Compiles a term. 
        This routine is faced with a slight difficulty when
        trying to decide between some of the alternative parsing rules.
        Specifically, if the current token is an identifier, the routing must
        distinguish between a variable, an array entry, and a subroutine call.
        A single look-ahead token, which may be one of "[", "(", or "." suffices
        to distinguish between the three possibilities. Any other token is not
        part of this term and should not be advanced over.
        """
        # Your code goes here!
        # self.output.write("<term>\n")
        # self.tokenizer.advance()
        if self.tokenizer.token_type() == "int_const":
            # self.output.write("<integerConstant> {} </integerConstant>\n".format(self.tokenizer.int_val()))        
            self.writer.write_push("constant", self.tokenizer.int_val())
            self.tokenizer.advance()
        elif self.tokenizer.token_type() == "string_const":
            # self.output.write("<stringConstant> {} </stringConstant>\n".format(self.tokenizer.string_val()))
            self.writer.write_str(self.tokenizer.string_val())
            self.tokenizer.advance()
        elif self.tokenizer.token_type() == "keyword":
            # self.output.write("<keyword> {} </keyword>\n".format(self.tokenizer.keyword()))
            value = self.tokenizer.keyword()
            if value == "true":
                self.writer.write_push("constant", 0)
                self.writer.write_arithmetic("not")
            elif value == "false":
                self.writer.write_push("constant", 0)
            elif value == "null":
                self.writer.write_push("constant", 0)
            elif value == "this":
                self.writer.write_push("pointer", 0)
            self.tokenizer.advance()
        elif self.tokenizer.token_type() == "symbol": 
            if self.tokenizer.symbol() in ["-", "~", "^", "#"]:
                symbol = self.tokenizer.symbol()
                # self.output.write("<symbol> {} </symbol>\n".format(self.tokenizer.symbol()))
                self.tokenizer.advance()
                self.compile_term()
                self.writer.write_arithmetic(arithmetic_dict_unary[symbol])
            elif self.tokenizer.symbol() == "(":
                # self.output.write("<symbol> {} </symbol>\n".format(self.tokenizer.symbol()))
                self.tokenizer.advance()
                self.compile_expression()
                # self.output.write("<symbol> {} </symbol>\n".format(self.tokenizer.symbol()))
                self.tokenizer.advance()
            else:
                # self.output.write("<symbol> {} </symbol>\n".format(self.tokenizer.symbol()))
                self.tokenizer.advance()
                self.compile_term()
                # self.output.write("<symbol> {} </symbol>\n".format(self.tokenizer.symbol()))
                self.tokenizer.advance()
        elif self.tokenizer.token_type() == "identifier": 
            # self.output.write("<identifier> {} </identifier>\n".format(self.tokenizer.identifier()))
            first_variable = self.tokenizer.identifier()
            self.tokenizer.advance()
            kind = self.symbol_table.kind_of(first_variable)
            index = self.symbol_table.index_of(first_variable)
            type = self.symbol_table.type_of(first_variable)
            if self.tokenizer.token_type() == "symbol" and self.tokenizer.symbol() == "[":
                # self.output.write("<symbol> {} </symbol>\n".format(self.tokenizer.symbol()))
                self.tokenizer.advance()
                self.compile_expression()
                self.writer.write_push(variable_dict[kind], index)
                self.writer.write_arithmetic('add')
                self.writer.write_pop('pointer', 1)
                self.writer.write_push('that', 0)
                # self.output.write("<symbol> {} </symbol>\n".format(self.tokenizer.symbol()))
                self.tokenizer.advance()
            elif self.tokenizer.token_type() == "symbol" and self.tokenizer.symbol() == ".":
                # self.output.write("<symbol> {} </symbol>\n".format(self.tokenizer.symbol()))
                self.tokenizer.advance()
                # self.output.write("<identifier> {} </identifier>\n".format(self.tokenizer.identifier()))
                second_variable = self.tokenizer.identifier()
                self.tokenizer.advance()
                # self.output.write("<symbol> {} </symbol>\n".format(self.tokenizer.symbol()))
                self.tokenizer.advance()
                exp_num = 0
                if type != None:
                    self.writer.write_push(variable_dict[kind], index)
                    exp_num += 1
                exp_num += self.compile_expression_list()
                if type != None:
                    self.writer.write_call(type + "." + second_variable, exp_num)
                else:
                    self.writer.write_call(first_variable + "." + second_variable, exp_num)
                # self.output.write("<symbol> {} </symbol>\n".format(self.tokenizer.symbol()))
                self.tokenizer.advance()
            elif self.tokenizer.token_type() == "symbol" and self.tokenizer.symbol() == "(":
                # self.output.write("<symbol> {} </symbol>\n".format(self.tokenizer.symbol()))
                self.tokenizer.advance()
                self.writer.write_push("pointer", 0)
                exp_num = self.compile_expression_list()
                # self.output.write("<symbol> {} </symbol>\n".format(self.tokenizer.symbol()))
                
                self.writer.write_call(self.class_name + "." + first_variable, exp_num+1)
                # self.writer.write_call(first_variable, exp_num)
                self.tokenizer.advance()
            else:
                self.writer.write_push(variable_dict[kind], index)

        # self.output.write("</term>\n")



    def compile_expression_list(self) -> int:
        """Compiles a (possibly empty) comma-separated list of expressions."""
        # Your code goes here!
        # self.output.write("<expressionList>\n")
        exp_num = 0
        if self.tokenizer.token_type() != "symbol" or self.tokenizer.symbol() != ")":
            self.compile_expression()
            exp_num += 1
            while self.tokenizer.token_type() == "symbol" and self.tokenizer.symbol() == ",":
                # self.output.write("<symbol> {} </symbol>\n".format(self.tokenizer.symbol()))
                self.tokenizer.advance()
                self.compile_expression()
                exp_num += 1
        # self.output.write("</expressionList>\n")
        return exp_num

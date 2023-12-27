"""
This file is part of nand2tetris, as taught in The Hebrew University, and
was written by Aviv Yaish. It is an extension to the specifications given
[here](https://www.nand2tetris.org) (Shimon Schocken and Noam Nisan, 2017),
as allowed by the Creative Common Attribution-NonCommercial-ShareAlike 3.0
Unported [License](https://creativecommons.org/licenses/by-nc-sa/3.0/).
"""
import typing


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
        self.tokenizer = input_stream
        self.output = output_stream
        # self.compile_class()

    def compile_class(self) -> None:
        """Compiles a complete class."""
        # Your code goes here!
        self.output.write("<class>\n")
        self.tokenizer.advance()
        self.output.write("<keyword> {} </keyword>\n".format(self.tokenizer.keyword()))
        self.tokenizer.advance()
        self.output.write("<identifier> {} </identifier>\n".format(self.tokenizer.identifier()))
        self.tokenizer.advance()
        self.output.write("<symbol> {} </symbol>\n".format(self.tokenizer.symbol()))
        self.tokenizer.advance()
        while self.tokenizer.token_type() == "keyword" and self.tokenizer.keyword() in ["static", "field"]:
            self.compile_class_var_dec()
        while self.tokenizer.token_type() == "keyword" and self.tokenizer.keyword() in ["constructor", "function", "method"]:
            self.compile_subroutine()
        self.output.write("<symbol> {} </symbol>\n".format(self.tokenizer.symbol()))
        self.output.write("</class>\n")

    def compile_class_var_dec(self) -> None:
        """Compiles a static declaration or a field declaration."""
        # Your code goes here!
        self.output.write("<classVarDec>\n")
        self.output.write("<keyword> {} </keyword>\n".format(self.tokenizer.keyword()))
        self.tokenizer.advance()
        if self.tokenizer.token_type() == "keyword":
            self.output.write("<keyword> {} </keyword>\n".format(self.tokenizer.keyword()))
        else:
            self.output.write("<identifier> {} </identifier>\n".format(self.tokenizer.identifier()))
        self.tokenizer.advance()
        self.output.write("<identifier> {} </identifier>\n".format(self.tokenizer.identifier()))
        self.tokenizer.advance()
        while self.tokenizer.token_type() == "symbol" and self.tokenizer.symbol() == ",": 
            self.output.write("<symbol> {} </symbol>\n".format(self.tokenizer.symbol()))
            self.tokenizer.advance()
            self.output.write("<identifier> {} </identifier>\n".format(self.tokenizer.identifier()))
            self.tokenizer.advance()
        self.output.write("<symbol> {} </symbol>\n".format(self.tokenizer.symbol()))
        self.tokenizer.advance()
        self.output.write("</classVarDec>\n")

    def compile_subroutine(self) -> None:
        """
        Compiles a complete method, function, or constructor.
        You can assume that classes with constructors have at least one field,
        you will understand why this is necessary in project 11.
        """
        # Your code goes here!
        self.output.write("<subroutineDec>\n")
        self.output.write("<keyword> {} </keyword>\n".format(self.tokenizer.keyword()))
        self.tokenizer.advance()
        if self.tokenizer.token_type() == "keyword":
            self.output.write("<keyword> {} </keyword>\n".format(self.tokenizer.keyword()))
        else:
            self.output.write("<identifier> {} </identifier>\n".format(self.tokenizer.identifier()))
        self.tokenizer.advance()
        self.output.write("<identifier> {} </identifier>\n".format(self.tokenizer.identifier()))
        self.tokenizer.advance()
        self.output.write("<symbol> {} </symbol>\n".format(self.tokenizer.symbol()))
        self.tokenizer.advance()
        self.compile_parameter_list()
        self.output.write("<symbol> {} </symbol>\n".format(self.tokenizer.symbol()))
        self.tokenizer.advance()
        self.output.write("<subroutineBody>\n")
        self.output.write("<symbol> {} </symbol>\n".format(self.tokenizer.symbol()))
        self.tokenizer.advance()
        while self.tokenizer.token_type() == "keyword" and self.tokenizer.keyword() == "var":
            self.compile_var_dec()
        self.compile_statements()
        self.output.write("<symbol> {} </symbol>\n".format(self.tokenizer.symbol()))
        self.tokenizer.advance()
        self.output.write("</subroutineBody>\n")
        self.output.write("</subroutineDec>\n")

    def compile_parameter_list(self) -> None:
        """Compiles a (possibly empty) parameter list, not including the 
        enclosing "()".
        """
        # Your code goes here!
        self.output.write("<parameterList>\n")
        if self.tokenizer.token_type() == "symbol" and self.tokenizer.symbol() == ")":
            self.output.write("</parameterList>\n")
            return
        if self.tokenizer.token_type() == "keyword":
            self.output.write("<keyword> {} </keyword>\n".format(self.tokenizer.keyword()))
        else:
            self.output.write("<identifier> {} </identifier>\n".format(self.tokenizer.identifier()))
        self.tokenizer.advance()
        self.output.write("<identifier> {} </identifier>\n".format(self.tokenizer.identifier()))
        self.tokenizer.advance()
        while self.tokenizer.token_type() == "symbol" and self.tokenizer.symbol() == ",":
            self.output.write("<symbol> {} </symbol>\n".format(self.tokenizer.symbol()))
            self.tokenizer.advance()
            if self.tokenizer.token_type() == "keyword":
                self.output.write("<keyword> {} </keyword>\n".format(self.tokenizer.keyword()))
            else:
                self.output.write("<identifier> {} </identifier>\n".format(self.tokenizer.identifier()))
            self.tokenizer.advance()
            self.output.write("<identifier> {} </identifier>\n".format(self.tokenizer.identifier()))
            self.tokenizer.advance()
        self.output.write("</parameterList>\n")


    def compile_var_dec(self) -> None:
        """Compiles a var declaration."""
        # Your code goes here!
        self.output.write("<varDec>\n")
        self.output.write("<keyword> {} </keyword>\n".format(self.tokenizer.keyword()))
        self.tokenizer.advance()
        if self.tokenizer.token_type() == "keyword":
            self.output.write("<keyword> {} </keyword>\n".format(self.tokenizer.keyword()))
        else:
            self.output.write("<identifier> {} </identifier>\n".format(self.tokenizer.identifier()))
        self.tokenizer.advance()
        self.output.write("<identifier> {} </identifier>\n".format(self.tokenizer.identifier()))
        self.tokenizer.advance()
        while self.tokenizer.token_type() == "symbol" and self.tokenizer.symbol() == ",":
            self.output.write("<symbol> {} </symbol>\n".format(self.tokenizer.symbol()))
            self.tokenizer.advance()
            self.output.write("<identifier> {} </identifier>\n".format(self.tokenizer.identifier()))
            self.tokenizer.advance()
        self.output.write("<symbol> {} </symbol>\n".format(self.tokenizer.symbol()))
        self.tokenizer.advance()
        self.output.write("</varDec>\n")

    def compile_statements(self) -> None:
        """Compiles a sequence of statements, not including the enclosing 
        "{}".
        """
        # Your code goes here!
        self.output.write("<statements>\n")
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
        self.output.write("</statements>\n")


    def compile_do(self) -> None:
        """Compiles a do statement."""
        # Your code goes here!
        self.output.write("<doStatement>\n")
        self.output.write("<keyword> {} </keyword>\n".format(self.tokenizer.keyword()))
        self.tokenizer.advance()
        self.output.write("<identifier> {} </identifier>\n".format(self.tokenizer.identifier()))
        self.tokenizer.advance()
        if self.tokenizer.token_type() == "symbol" and self.tokenizer.symbol() == ".":
            self.output.write("<symbol> {} </symbol>\n".format(self.tokenizer.symbol()))
            self.tokenizer.advance()
            self.output.write("<identifier> {} </identifier>\n".format(self.tokenizer.identifier()))
            self.tokenizer.advance()
        self.output.write("<symbol> {} </symbol>\n".format(self.tokenizer.symbol()))
        self.tokenizer.advance()
        self.compile_expression_list()
        self.output.write("<symbol> {} </symbol>\n".format(self.tokenizer.symbol()))
        self.tokenizer.advance()
        self.output.write("<symbol> {} </symbol>\n".format(self.tokenizer.symbol()))
        self.tokenizer.advance()
        self.output.write("</doStatement>\n")


    def compile_let(self) -> None:
        """Compiles a let statement."""
        # Your code goes here!
        self.output.write("<letStatement>\n")
        self.output.write("<keyword> {} </keyword>\n".format(self.tokenizer.keyword()))
        self.tokenizer.advance()
        self.output.write("<identifier> {} </identifier>\n".format(self.tokenizer.identifier()))
        self.tokenizer.advance()
        if self.tokenizer.token_type() == "symbol" and self.tokenizer.symbol() == "[":
            self.output.write("<symbol> {} </symbol>\n".format(self.tokenizer.symbol()))
            self.tokenizer.advance()
            self.compile_expression()
            self.output.write("<symbol> {} </symbol>\n".format(self.tokenizer.symbol()))
            self.tokenizer.advance()
        self.output.write("<symbol> {} </symbol>\n".format(self.tokenizer.symbol()))
        self.tokenizer.advance()
        self.compile_expression()
        self.output.write("<symbol> {} </symbol>\n".format(self.tokenizer.symbol()))
        self.tokenizer.advance()
        self.output.write("</letStatement>\n")


    def compile_while(self) -> None:
        """Compiles a while statement."""
        # Your code goes here!
        self.output.write("<whileStatement>\n")
        self.output.write("<keyword> {} </keyword>\n".format(self.tokenizer.keyword()))
        self.tokenizer.advance()
        self.output.write("<symbol> {} </symbol>\n".format(self.tokenizer.symbol()))
        self.tokenizer.advance()
        self.compile_expression()
        self.output.write("<symbol> {} </symbol>\n".format(self.tokenizer.symbol()))
        self.tokenizer.advance()
        self.output.write("<symbol> {} </symbol>\n".format(self.tokenizer.symbol()))
        self.tokenizer.advance()
        self.compile_statements()
        self.output.write("<symbol> {} </symbol>\n".format(self.tokenizer.symbol()))
        self.tokenizer.advance()
        self.output.write("</whileStatement>\n")


    def compile_return(self) -> None:
        """Compiles a return statement."""
        # Your code goes here!
        self.output.write("<returnStatement>\n")
        self.output.write("<keyword> {} </keyword>\n".format(self.tokenizer.keyword()))
        self.tokenizer.advance()
        if self.tokenizer.token_type() != "symbol" or self.tokenizer.symbol() != ";":
            self.compile_expression()
        self.output.write("<symbol> {} </symbol>\n".format(self.tokenizer.symbol()))
        self.tokenizer.advance()
        self.output.write("</returnStatement>\n")

    def compile_if(self) -> None:
        """Compiles a if statement, possibly with a trailing else clause."""
        # Your code goes here!
        self.output.write("<ifStatement>\n")
        self.output.write("<keyword> {} </keyword>\n".format(self.tokenizer.keyword()))
        self.tokenizer.advance()
        self.output.write("<symbol> {} </symbol>\n".format(self.tokenizer.symbol()))
        self.tokenizer.advance()
        self.compile_expression()
        self.output.write("<symbol> {} </symbol>\n".format(self.tokenizer.symbol()))
        self.tokenizer.advance()
        self.output.write("<symbol> {} </symbol>\n".format(self.tokenizer.symbol()))
        self.tokenizer.advance()
        self.compile_statements()
        self.output.write("<symbol> {} </symbol>\n".format(self.tokenizer.symbol()))
        self.tokenizer.advance()
        if self.tokenizer.token_type() == "keyword" and self.tokenizer.keyword() == "else":
            self.output.write("<keyword> {} </keyword>\n".format(self.tokenizer.keyword()))
            self.tokenizer.advance()
            self.output.write("<symbol> {} </symbol>\n".format(self.tokenizer.symbol()))
            self.tokenizer.advance()
            self.compile_statements()
            self.output.write("<symbol> {} </symbol>\n".format(self.tokenizer.symbol()))
            self.tokenizer.advance()
        self.output.write("</ifStatement>\n")


    def compile_expression(self) -> None:
        """Compiles an expression."""
        # Your code goes here!
        self.output.write("<expression>\n")
        self.compile_term()
        while self.tokenizer.token_type() == "symbol" and self.tokenizer.symbol() in ["+", "-", "*", "/", "&amp;", "|", "&gt;", "&lt;", "="]:
            self.output.write("<symbol> {} </symbol>\n".format(self.tokenizer.symbol()))
            self.tokenizer.advance()
            self.compile_term()
        self.output.write("</expression>\n")

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
        self.output.write("<term>\n")
        # self.tokenizer.advance()
        if self.tokenizer.token_type() == "int_const":
            self.output.write("<integerConstant> {} </integerConstant>\n".format(self.tokenizer.int_val()))        
            self.tokenizer.advance()
        elif self.tokenizer.token_type() == "string_const":
            self.output.write("<stringConstant> {} </stringConstant>\n".format(self.tokenizer.string_val()))
            self.tokenizer.advance()
        elif self.tokenizer.token_type() == "keyword":
            self.output.write("<keyword> {} </keyword>\n".format(self.tokenizer.keyword()))
            self.tokenizer.advance()
        elif self.tokenizer.token_type() == "symbol": 
            if self.tokenizer.symbol() in ["-", "~", "^", "#"]:
                self.output.write("<symbol> {} </symbol>\n".format(self.tokenizer.symbol()))
                self.tokenizer.advance()
                self.compile_term()
            elif self.tokenizer.symbol() == "(":
                self.output.write("<symbol> {} </symbol>\n".format(self.tokenizer.symbol()))
                self.tokenizer.advance()
                self.compile_expression()
                self.output.write("<symbol> {} </symbol>\n".format(self.tokenizer.symbol()))
                self.tokenizer.advance()
            else:
                self.output.write("<symbol> {} </symbol>\n".format(self.tokenizer.symbol()))
                self.tokenizer.advance()
                self.compile_term()
                self.output.write("<symbol> {} </symbol>\n".format(self.tokenizer.symbol()))
                self.tokenizer.advance()
        elif self.tokenizer.token_type() == "identifier": 
            self.output.write("<identifier> {} </identifier>\n".format(self.tokenizer.identifier()))
            self.tokenizer.advance()
            if self.tokenizer.token_type() == "symbol" and self.tokenizer.symbol() == "[":
                self.output.write("<symbol> {} </symbol>\n".format(self.tokenizer.symbol()))
                self.tokenizer.advance()
                self.compile_expression()
                self.output.write("<symbol> {} </symbol>\n".format(self.tokenizer.symbol()))
                self.tokenizer.advance()
            elif self.tokenizer.token_type() == "symbol" and self.tokenizer.symbol() == "(":
                self.output.write("<symbol> {} </symbol>\n".format(self.tokenizer.symbol()))
                self.tokenizer.advance()
                self.compile_expression_list()
                self.output.write("<symbol> {} </symbol>\n".format(self.tokenizer.symbol()))
                self.tokenizer.advance()
            elif self.tokenizer.token_type() == "symbol" and self.tokenizer.symbol() == ".":
                self.output.write("<symbol> {} </symbol>\n".format(self.tokenizer.symbol()))
                self.tokenizer.advance()
                self.output.write("<identifier> {} </identifier>\n".format(self.tokenizer.identifier()))
                self.tokenizer.advance()
                self.output.write("<symbol> {} </symbol>\n".format(self.tokenizer.symbol()))
                self.tokenizer.advance()
                self.compile_expression_list()
                self.output.write("<symbol> {} </symbol>\n".format(self.tokenizer.symbol()))
                self.tokenizer.advance()

        
        self.output.write("</term>\n")



    def compile_expression_list(self) -> None:
        """Compiles a (possibly empty) comma-separated list of expressions."""
        # Your code goes here!
        self.output.write("<expressionList>\n")
        if self.tokenizer.token_type() != "symbol" or self.tokenizer.symbol() != ")":
            self.compile_expression()
            while self.tokenizer.token_type() == "symbol" and self.tokenizer.symbol() == ",":
                self.output.write("<symbol> {} </symbol>\n".format(self.tokenizer.symbol()))
                self.tokenizer.advance()
                self.compile_expression()
        self.output.write("</expressionList>\n")

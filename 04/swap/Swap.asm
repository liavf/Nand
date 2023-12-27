// This file is part of nand2tetris, as taught in The Hebrew University, and
// was written by Aviv Yaish. It is an extension to the specifications given
// [here](https://www.nand2tetris.org) (Shimon Schocken and Noam Nisan, 2017),
// as allowed by the Creative Common Attribution-NonCommercial-ShareAlike 3.0
// Unported [License](https://creativecommons.org/licenses/by-nc-sa/3.0/).

// The program should swap between the max. and min. elements of an array.
// Assumptions:
// - The array's start address is stored in R14, and R15 contains its length
// - Each array value x is between -16384 < x < 16384
// - The address in R14 is at least >= 2048
// - R14 + R15 <= 16383
//
// Requirements:
// - Changing R14, R15 is not allowed.

// Put your code here.

	@i 
	M = 0
	@temp 
	M = 0
	@R14 
	D = M
	@max_addr
	M = D
	@min_addr
	M = D

(LOOP)
	// start at R14
	// while i < R15
	// compare max to value inside cell
	// if cell is greater (cell - max >0) , save max and max_addr
	// same for min
	// while i < R15
	@i
	D = M 
	@R15
	D = D - M 
	@END 
	D;JGE
	//get curr address
	@i 
	D = M
	@R14
	A = M + D
	D = A 
	// save curr address in temp
	@temp
	M = D
	A = D
	D = M
	@max_addr
	A = M
	D = D - M 
	@UPDATE_MAX
	D;JGT 
	@temp
	A = M
	D = M
	@min_addr
	A = M
	D = D - M 
	@UPDATE_MIN
	D;JLT
	// i++
	@i
	M = M + 1
	@LOOP 
	0;JMP

(UPDATE_MAX)
	@temp
	D = M
	@max_addr
	M = D
	A = D
	D = M
	@min_addr
	A = M
	D = D - M 
	@UPDATE_MIN
	D;JLT
	@i
	M = M + 1
	@LOOP
	0;JMP

(UPDATE_MIN)
	@temp
	D = M
	@max_addr
	M = D
	@i
	M = M + 1
	@LOOP
	0;JMP	

(END)
	@min_addr
	A = M
	D = M 
	@temp 
	M = D
	@max_addr
	A = M
	D = M
	@min_addr
	A = M
	M = D
	@temp 
	D = M 
	@max_addr
	A = M 
	M = D
	@FINAL 
	0;JMP

(FINAL)
	@FINAL
	0;JMP
	
	
	
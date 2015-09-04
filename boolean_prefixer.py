# Boolean prefixer, turns infixed boolean statements into prefixed. Also computes any operation 
# involving constants T and F. 

import sys
import csv

class BooleanPrefixer:
	""" 
	Class BooleanPrefixer. 
	Initializes with no argument or single argument, the filename of the input. 
	
	As long as file has been read at least once, one can call parse() on the most recent input. 
	"""
	
	# Establishes operator precedence. The higher the better. Class constant.
	OPERATOR_PRECEDENCE = { "(" : 3, ")" : 3, "!" : 2 , "&" : 1, "|" : 0 }
		
	def __init__(self, filename = None):
		""" 
		Initializes BoolealPrefixer class. If a filename is already provided, tokenizes the input.
		""" 
		if (filename):
			self.readTokens(filename)
		else:
			self.tokens = None
		
	def parse(self, filename = None):
		""" 
		Converts infixed boolean statements to prefixed ones. 
		Allows for the input of a filename 
		if user wishes to overwrite existing tokens or simply haven't read in any inputs previously.
		
		The basic algorithm works as follows: 
			Using two stacks, we'll walk through every single token in linear fashion. 
			For each token, we first check if it's not an operator. If it's not, put it in outputStack. 		
			If it's an operator, we can't immediately process it, because we don't know what the next operator is.
			But we can figure out if the previous operator, which we've put in the operatorStack, is processable. 
			If the previous operator(s) is processable, then we process them. Otherwise, put the current operator 
			on the operatorStack. 
			Once we reach the end of out token stream, we can then go back to our stacks and combine everything 
			into one statement (the number of operators left on the stack now should be fairly small as well.)
			
		We only run through the token stream once, so the runtime efficiency should be on the order of O(N). 
		"""
		if (filename):
			self.readTokens(filename)
			
		if (self.tokens):
			# 2 stacks, one only holds operators, and the other a variety of token and token combinations
			operatorStack = []
			outputStack = []
			
			# Iterate through all the tokens. 
			for token in self.tokens:
				if token in self.OPERATOR_PRECEDENCE.keys(): # token is an operator
					if not operatorStack :
						# no operator queued, just put the current one in there. 
						operatorStack.append(token)

					elif token == ")":
						# Process everything up till the last '('
						# What we do is first discard the ')', and then process everything until you run into '('
						while (operatorStack[-1] != "("):
							self.processLastExpr(operatorStack, outputStack)
						#removes the "("
						operatorStack.pop() 
						
					elif operatorStack[-1] == "(":
						# same thing as no operator existing previously
						operatorStack.append(token)
					
					elif self.OPERATOR_PRECEDENCE[token] > self.OPERATOR_PRECEDENCE[operatorStack[-1]]:
						# if current operator takes precedence over the last one in the stack, 
						# just put this in the output stack.
						operatorStack.append(token)
					
					elif token == "!" and operatorStack[-1] == "!":
						# edge case, where there is consecutive !'s. 
						# Simply hold onto those until you see a new operator
						operatorStack.append(token)
						
					else:
						# Now that we've checked for our cases, we can process the queued up operators
						
						while (True):
							lastOperator = operatorStack[-1]
							if ( not operatorStack or lastOperator == "(" or self.OPERATOR_PRECEDENCE[token] > self.OPERATOR_PRECEDENCE[lastOperator]):
								# come here if:
								# 1. no operators left
								# 2. it's a '(', which is the same as no operator
								# 3. we've now processed all safe-to-process operators in the stack
								operatorStack.append(token)
								break
							else:
								self.processLastExpr(operatorStack, outputStack)
								if (not operatorStack):
									# We've finished processing so far...
									operatorStack.append(token)
									break					
				else:
					# it's a non-operator, so just queue it to the output stack and we'll take care of it later
					outputStack.append(token)
			
			# now that we've completed reading all tokens, time to process backward. 
			while (operatorStack): 
				self.processLastExpr(operatorStack, outputStack) 
			
			# we are done!
			return outputStack.pop()
		else:
			print("Yet to read file, either call this function with a filename or initialize with a filename.")
			exit(1)
	
	def processLastExpr(self, operatorStack, outputStack):
		""" 
		Given the the two stacks, process the top operator on operatorStack, 
		and adds the result back to outputStack.
		"""
		
		# pop the expressions we'll process
		operator = operatorStack.pop()
		arg2 = outputStack.pop()
		arg1 = None		
		
		if operator == "!":
			# if operator is !, return the opposite if arg2 is constant, or just append the expressions. 
			if (arg2 == "T"):
				outputStack.append("F")
			elif (arg2 == "F"):
				outputStack.append("T")
			else:
				outputStack.append("(" + operator + " " + arg2 + ")")
		else:
			# 2-argument operator case
			arg1 = outputStack.pop()
			if (arg1  == "T" or arg2 == "T"):
				if (operator == "&"):
					if (arg1 == "T"): 
						outputStack.append(arg2)
					else:
						outputStack.append(arg1)
				else:
					# in case of |, it will be true no matter what the other argument is if one is true. 
					outputStack.append("T")
			elif (arg1 == "F" or arg2 == "F"):
				if (operator == "&"):
					# in case of &, it will be false no matter what the other argument is if one is false.
					outputStack.append("F")
				else: 
					if (arg1 == "F"):
						outputStack.append(arg2)
					else:
						outputStack.append(arg1)
			else:
				# no constants, just append. 
				outputStack.append("(" + operator + " " + arg1 + " " + arg2 + ")")
			
			
	
	def readTokens(self, filename):
		""" 
		Warning: if called on a prefixer that already has tokens read in, this will overwrite 
		those original tokens. 
		
		Operates on the object itself, and takes in a filename to read the tokens from. 
		"""
			
		self.tokens = []
		try:
			with open(filename, 'rb') as input:
				lines = csv.reader(input, delimiter=' ')
				
				#Currently simply reads the last line - assuming there is only 1 line. 
				for line in lines:
					for token in line: 
						
						# chop off all front parens and append them. 
						while (token[0] == '(' ):
							self.tokens.append("(")
							token = token[1:]
						
						# chop off all close parens
						temp = []
						while (token[len(token)-1] == ')'):
							temp.append(")")
							token = token[:-1] # everything up till last element
						
						# append
						self.tokens.append(token)
						for cparens in temp:
							self.tokens.append(cparens)
	
		except:
			print "Unable to open file: " + filename
			exit(0)
			
def main():
	if (len(sys.argv) != 2):
		print("Invalid Usage. Use as python boolean_prefixer.py [filename]")
	else:
		# Reads in the file. 
		prefixer = BooleanPrefixer(sys.argv[1])
		print prefixer.parse()
		# print prefixer.tokens

if __name__ == "__main__":
    main()
 
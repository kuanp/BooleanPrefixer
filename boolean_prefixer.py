# Boolean prefixer, turns infixed boolean statements into prefixed. Also computes any operation 
# involving constants T and F. 

import sys
import csv

class BooleanPrefixer:
	# Establishes operator precedence. The higher the better. Class constant.
	OPERATOR_PRECEDENCE = { "!" : 2 , "&" : 1, "|" : 0 }
	
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
		Allows for the input of a filename if user wishes to overwrite existing tokens or 
		simply haven't read in any inputs.
		"""
		if (filename):
			self.readTokens(filename)
			
		if (self.tokens):
			# 2 stacks, one only holds operators, and the other a variety of token and token combinations
			operatorStack = []
			outputStack = []
			
			# Iterate through all the tokens. 
			for token in self.tokens:
				if token in self.OPERATOR_PRECEDENCE.keys(): 
					#token is an operator
					if not operatorStack:
						# no operator queued, just put the current one in there. 
						operatorStack.append(token)
						
					elif self.OPERATOR_PRECEDENCE[token] > self.OPERATOR_PRECEDENCE[operatorStack[-1]]:
						# if current operator takes precedence over the last one in the stack, 
						# just put this in the output stack.
						operatorStack.append(token)
						
					else:
						# current operator precedent is either same or less, 
						# which means we can comfortably process the past operators that were queued up. 
						
						while (True):
							#print operatorStack
							#print outputStack
							lastOperator = operatorStack[-1]
							if (self.OPERATOR_PRECEDENCE[token] > self.OPERATOR_PRECEDENCE[lastOperator]):
								# we've now processed all safe-to-process operators in the stack
								operatorStack.append(token)
								break
							else:
								self.processLastExpr(operatorStack, outputStack)
								if (not operatorStack):
									# We've finished processing so far...
									operatorStack.append(token)
									break					
				else:
					outputStack.append(token)
			
			# now that we've completed reading all tokens, time to process backward. 
			while (operatorStack): 
				#print operatorStack
				#print outputStack
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
				
				# Takes care of the parens. Currently simply reads the last line - 
				# assuming there is only 1 line. 
				for line in lines:
					for token in line: 
						if (token[0] == '(' ):
							self.tokens.append("(")
							self.tokens.append(token[1:])
							
						elif (token[len(token)-1] == ')'):
							self.tokens.append(token[:-1]) # everything up till last element
							self.tokens.append(")")
						else: 
							self.tokens.append(token)
	
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
		
		for token in prefixer.tokens:
			print ", \n".join(token)

if __name__ == "__main__":
    main()
 
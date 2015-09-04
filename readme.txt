This is a simple pre-fixer for infixed boolean expressions.

USAGE: python boolean_prefixer.py [FILENAME]

Sample input file is called input. Inputs must be valid boolean expressions
, with spaces between variables(T, F, a, b) and operators. It is not
required for you to leave space between parens.

In other words,
(a & b) | ! c
is a valid expression.

But,
( a&b ) | !C
is not.
# A simple expression evaluator 
- Supports multi-character names as variables
- Supports arithmetic operators +-*/^ and unary minus
- Supports bracketed expressions
 
Implements a Stack class using dque
Implements a Lexer class that performs tokenization
Postfix conversion is performed and the postfix expression is evaluated

Example usage
```
import evaluator

ex = evaluator.ExpressionProcessor({'a':10,'b':20, 'var':2})
result = ex.calculate('1+(2^3-4)+a-b')
print(f"Result:{result}")

``` 
from enum import Enum
import string
from collections import deque
import unittest

# An implementation of stack structure using deque
# List can also be used
class Stack(deque):
    def __init__(self):
        self.stack_top = -1
        super().__init__()

    def push(self, item):
        self.append(item)
        self.stack_top += 1
        return True

    def pop(self):
        try:
            item = super().pop()
            self.stack_top -= 1
            return item
        except Exception as e:
            return None

    def is_empty(self):
        return False if len(self) > 0 else True

    def top(self):
        return self[self.stack_top] if self.stack_top >= 0 else None
#
# Every token in an expression shall be represented as a token instance.
# A token can be an operator, a variable or a number(literal).
# An operator will have a precedence and associativity. A literal will have them as None
#
class Token:
    class Type(Enum):
        OPERATOR = 1
        VARIABLE = 2
        NUMBER = 3
        LPARENTHESIS = 4
        RPARENTHESIS = 5

    def __init__(self, token, type, precedence=None, associativity=None, optype=None):
        self.token = token
        self.type = type
        self.precedence = precedence
        self.associativity = associativity
        self.optype = optype

#
# Lexer class to perform tokenization of the expression
# The lex() method will convert a given expression into a list of Token objects
#   expression:- string containing expression
#   variables:- A dictionary where variables used in the expression are stored as keys and their values as values
#
class Lexer(list):
    operators = {
        '+': {"precendence":0, "associativity":"L", "optype": "binary"},
        '-': {"precendence":0, "associativity": "L", "optype": "binary"},
        '*': {"precendence":1, "associativity": "L", "optype": "binary"},
        '/': {"precendence":1, "associativity": "L", "optype": "binary"},
        '^': {"precendence":2, "associativity": "R", "optype": "binary"},
        'u-': {"precendence": 3, "associativity": "R", "optype": "unary"}
    }
    def __init__(self, expression, variables):
        self.expression = f"({expression})"
        self.variables = variables
        self.lex_pos = 0

    # Main method to call
    def lex(self):
        while self._next_token():
            pass

    def _next_token(self):
        if self.lex_pos >= len(self.expression):
            return False

        # Ignore white space(s)
        if self.expression[self.lex_pos] == ' ':
            self.lex_pos += 1
            return True

        # Find if the last token was an operator
        last_token_type = self[-1].type if len(self)>0 else None
        is_last_token_operator = False
        if last_token_type:
            is_last_token_operator = last_token_type == Token.Type.OPERATOR

        #print(f"last token was operator: {is_last_token_operator}")

        if self.expression[self.lex_pos] in self.operators.keys():
            operator = self.expression[self.lex_pos]
            if is_last_token_operator and operator == "-":
                operator = 'u-'

            op_attributes = self.operators[operator]
            self.append(Token(operator, Token.Type.OPERATOR,
                              op_attributes['precendence'],
                              op_attributes['associativity'],
                              op_attributes['optype']))
            self.lex_pos += 1
            return True
        elif self.expression[self.lex_pos] == "(":
            self.append(Token(self.expression[self.lex_pos], Token.Type.LPARENTHESIS, -1))
            self.lex_pos += 1
            return True
        elif self.expression[self.lex_pos] == ")":
            self.append(Token(self.expression[self.lex_pos], Token.Type.RPARENTHESIS, -1))
            self.lex_pos += 1
            return True
        elif self.expression[self.lex_pos].lower() in string.ascii_lowercase:
            var = self._get_variable_name()
            self.append (Token(var, Token.Type.VARIABLE, -1))
            return True
        elif self.expression[self.lex_pos] in string.digits:
            num = self._get_number()
            self.append (Token(num, Token.Type.NUMBER, -1))
            return True
        return False

    def _get_variable_name(self):
        var_chars = []
        while (self.lex_pos < len(self.expression)) and (self.expression[self.lex_pos].lower() in string.ascii_lowercase):
            var_chars.append(self.expression[self.lex_pos])
            self.lex_pos += 1
        return ''.join(var_chars)

    def _get_number(self):
        num_chars = []
        while (self.lex_pos < len(self.expression)) and (self.expression[self.lex_pos] in string.digits):
            num_chars.append(self.expression[self.lex_pos])
            self.lex_pos += 1
        return ''.join(num_chars)

    def __str__(self):
        return ' '.join([t.token for t in self])

#
# Convert the ouptut from Lexer(which is in Infix format), into a Postfix expression
#
class PostFix(list):
    def __init__(self):
        super().__init__()

    # Convert an infix list of tokens into postfix by looping through the infix token list.
    # 1. If the current token is a variable or a literal, add it to the postfix list
    # 2. If the current token is a RIGHTPARANTHESIS, repeatedly pop from stack until a LEFTPARANTHESIS is encounterd.
    #    Add those tokens to postfix list
    # 3. If the current token is an operator, repeatedly pop from stack until current operator's precedence is less than
    #    the precedence from the stack. Add those tokens to postfix list
    # 4. Once all tokens are exhausted, repeatedly pop all tokens from stack and append them to postfix list
    def to_postfix(self, tokens):
        stack = Stack()
        for token in tokens:
            if token.type in [token.Type.VARIABLE, token.Type.NUMBER]:
                self.append(token)
            elif token.type == Token.Type.LPARENTHESIS:
                stack.push(token)
            elif token.type == Token.Type.RPARENTHESIS:
                self.extend(self.pop_until_lparanthesis(stack))
            elif token.type == Token.Type.OPERATOR:
                self.extend(self.pop_until_higher_operator(stack, token))
                stack.push(token)

        while not stack.is_empty():
            self.append(stack.pop())

    # Repeatedly pop form the stack until a left paranthesis is encountered
    # return the popped list of tokens
    def pop_until_lparanthesis(self, stack):
        items = []
        if stack.is_empty():
            return items

        while (stack.top().token != '(') and (not stack.is_empty()):
            items.append(stack.pop())
        stack.pop()
        return items

    # Repeatedly pop form the stack as long as the current operator's precedence is lower than those obtained from tack
    # return the popped list of tokens
    def pop_until_higher_operator(self, stack, op_token):
        items = []
        if stack.is_empty():
            return items

        while (stack.top().precedence >= op_token.precedence) and (not stack.is_empty()):
            items.append(stack.pop())
        return items

    def __str__(self):
        return ' '.join([t.token for t in self])

"""
Evaluator class. 
Takes in a postfix expression (list of Tokens arranged in postfix order), along with a dictionary of variables
"""
class Evaluator:
    def __init__(self, postfix_list, variables):
        self.postfix_list = postfix_list
        self.variables = variables

    def get_variable_value(self, var_name):
        # Lookup a variable into the dictionary to fetch its value
        return self.variables.get(var_name, None)

    def evaluate(self):
        stack = Stack()
        result = 0

        for token in self.postfix_list:
            if token.type == Token.Type.NUMBER:
                stack.push(token.token)
            elif token.type == Token.Type.VARIABLE:
                if self.variables.get(token.token, None) is None:
                    raise Exception("Variable not defined")
                stack.push(self.variables.get(token.token, 0))
            elif token.type == Token.Type.OPERATOR and token.optype == 'binary':
                right_operand = stack.pop()
                left_operand = stack.pop()
                result = self.operate_binary(token, left_operand, right_operand)
                stack.push(result)
            elif token.type == Token.Type.OPERATOR and token.optype == 'unary':
                operand = stack.pop()
                result = self.operate_unary(token, operand)
                stack.push(result)
        return result

    """
    Implement all binary operators
    """
    def operate_binary(self, operator, lvalue, rvalue):
        if operator.token == '+':
            return int(lvalue) + int(rvalue)
        elif operator.token == '-':
            return int(lvalue) - int(rvalue)
        elif operator.token == '*':
            return int(lvalue) * int(rvalue)
        elif operator.token == '/':
            return int(lvalue) / int(rvalue)
        elif operator.token == '^':
            return pow(int(lvalue), int(rvalue))
        return 0

    """
    Implement all unary operators
    """
    def operate_unary(self, operator, operand):
        opvalue = operand.token

        if operator.token == 'u-':
            return int(opvalue) * -1

"""
The final class that encapsulates all lexer, postfix conversion and evaluation logic
"""
class ExpressionProcessor:
    def __init__(self, variables=None):
        self.variables = {} if variables is None else variables

    def calculate(self, expression):
        lx = Lexer(expression, self.variables)
        lx.lex()
        px = PostFix()
        px.to_postfix(lx)

        ex = Evaluator(px, self.variables)
        return ex.evaluate()


"""
Unit test cases
"""
class Evaluate(unittest.TestCase):
    def test(self):
        ex = ExpressionProcessor({'a':10,'b':20, 'var':2})

        # Test a happy path
        res1 = ex.calculate('1+(2^3-4)+a-b')
        self.assertEqual(-5, res1)
        print(f"res1:{res1}")

        # Expression with spaces
        res2 = ex.calculate('1 + 2')
        self.assertEqual(3, res2)
        print(f"res2:{res2}")

        # multi-character variables
        res3 = ex.calculate('var+b-a')
        self.assertEqual(12, res3)
        print(f"res2:{res3}")

# Run all tests
tst = Evaluate().test()
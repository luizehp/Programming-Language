import re
import sys

# --- Pré-processador ---


class PrePro:
    @staticmethod
    def filter(code: str) -> str:
        # remove comentários começando com '#' até o fim da linha
        code = re.sub(r'#.*', '', code)
        return code


# --- Token ---
class Token:
    def __init__(self, type: str, value):
        self.type = type
        self.value = value

    def __repr__(self):
        return f"Token({self.type}, {self.value})"


# --- Tokenização via regex ---
TOKEN_SPECIFICATION = [
    ("NEWLINE",    r"\n"),
    ("SKIP",       r"[ \t]+"),
    ("COMPONENT",  r"\b(?:resistor|capacitor|indutor)\b"),
    ("PROPERTY",   r"\b(?:tensao|corrente|resistência|valor)\b"),
    ("IF",         r"\bse\b"),
    ("THEN",       r"\bentao\b"),
    ("ELSE",       r"\bsenao\b"),
    ("END",        r"\bfim\b"),
    ("LOOP",       r"\bloop\b"),
    ("CYCLE",      r"\bciclos_clock\b"),
    ("EQ",         r"=="),
    ("ASSIGN",     r"="),
    ("PLUS",       r"\+"),
    ("MINUS",      r"-"),
    ("MULT",       r"\*"),
    ("DIV",        r"/"),
    ("GT",         r">"),
    ("LT",         r"<"),
    ("LPAREN",     r"\("),
    ("RPAREN",     r"\)"),
    ("COMMA",      r","),
    ("DOT",        r"\."),
    ("NUM_UNIT",   r"\d+(?:\.\d+)?(?:Ω|F|H|V|A)"),
    ("NUMBER",     r"\d+(?:\.\d+)?"),
    ("IDENTIFIER", r"[A-Za-z_][A-Za-z0-9_]*"),
]
_token_regex = re.compile(
    "|".join(f"(?P<{name}>{pattern})" for name, pattern in TOKEN_SPECIFICATION)
)


class Tokenizer:
    def __init__(self, code: str):
        self.tokens = list(self._generate_tokens(code))
        self.pos = 0
        self.current = self.tokens[0]

    def _generate_tokens(self, code: str):
        for mo in _token_regex.finditer(code):
            typ = mo.lastgroup
            val = mo.group(typ)
            if typ == "NEWLINE":
                yield Token("NEWLINE", "\n")
            elif typ == "SKIP":
                continue
            elif typ == "NUM_UNIT":
                m = re.match(r"(\d+(?:\.\d+)?)(Ω|F|H|V|A)", val)
                yield Token("NUM_UNIT", (m.group(1), m.group(2)))
            else:
                yield Token(typ, val)
        yield Token("EOF", "")

    def peek(self):
        return self.current

    def advance(self):
        self.pos += 1
        if self.pos < len(self.tokens):
            self.current = self.tokens[self.pos]
        else:
            self.current = Token("EOF", "")

    def expect(self, type_):
        if self.current.type == type_:
            val = self.current.value
            self.advance()
            return val
        raise Exception(f"Esperado {type_}, obteve {self.current.type}")

# --- Tabela de Símbolos ---


class SymbolTable:
    def __init__(self, parent=None):
        self.table = {}
        self.parent = parent

    def declare(self, name, data, type_):
        if name in self.table:
            raise Exception(f"'{name}' já declarado")
        self.table[name] = (data, type_)

    def get(self, name):
        if name in self.table:
            return self.table[name]
        if self.parent:
            return self.parent.get(name)
        raise Exception(f"'{name}' não declarado")

    def set(self, name, data):
        if name in self.table:
            _, t = self.table[name]
            self.table[name] = (data, t)
        elif self.parent:
            self.parent.set(name, data)
        else:
            raise Exception(f"'{name}' não declarado")


# --- Regras de unidades ---
UNIT_MULTIPLY = {
    ('Ω', 'F'): 's', ('F', 'Ω'): 's',   # RC time constant
    ('V', 'Ω'): 'A', ('Ω', 'V'): 'A'    # I = V/R or V = I·R
}
UNIT_DIVIDE = {
    ('V', 'Ω'): 'A',  # I = V/R
    ('Ω', 'F'): 'Ω/F'
}

# --- AST Nodes ---


class Node:
    def evaluate(self, st: SymbolTable):
        raise NotImplementedError()


class Program(Node):
    def __init__(self, statements): self.statements = statements

    def evaluate(self, st):
        for stmt in self.statements:
            stmt.evaluate(st)


class ComponentDecl(Node):
    def __init__(self, ctype, name, expr):
        self.ctype = ctype
        self.name = name
        self.expr = expr

    def evaluate(self, st):
        val, unit = self.expr.evaluate(st)
        st.declare(self.name, {"valor": (val, unit)}, self.ctype)


class Assignment(Node):
    def __init__(self, name, expr):
        self.name = name
        self.expr = expr

    def evaluate(self, st):
        val, unit = self.expr.evaluate(st)
        st.set(self.name, {"valor": (val, unit)})


class PropertyAssignment(Node):
    def __init__(self, name, prop, expr):
        self.name = name
        self.prop = prop
        self.expr = expr

    def evaluate(self, st):
        val, unit = self.expr.evaluate(st)
        comp, _ = st.get(self.name)
        comp[self.prop] = (val, unit)


class PropertyAccess(Node):
    def __init__(self, name, prop):
        self.name = name
        self.prop = prop

    def evaluate(self, st):
        comp, _ = st.get(self.name)
        return comp.get(self.prop)


class Number(Node):
    def __init__(self, val):
        self.val = float(val)

    def evaluate(self, st):
        return (self.val, None)


class NumberWithUnit(Node):
    def __init__(self, val, unit):
        self.val = float(val)
        self.unit = unit

    def evaluate(self, st):
        return (self.val, self.unit)


class Identifier(Node):
    def __init__(self, name):
        self.name = name

    def evaluate(self, st):
        data, _ = st.get(self.name)
        return data.get("valor")


class BinaryOp(Node):
    def __init__(self, left, op, right):
        self.left = left
        self.op = op
        self.right = right

    def evaluate(self, st):
        (lv, lu) = self.left.evaluate(st)
        (rv, ru) = self.right.evaluate(st)
        # Adição/Subtração
        if self.op in ('+', '-'):
            if lu != ru or lu is None:
                raise TypeError(
                    f"Incompatível para '{self.op}': [{lu}] vs [{ru}]")
            val = lv + rv if self.op == '+' else lv - rv
            return (val, lu)
        # Multiplicação
        if self.op == '*':
            if lu and ru:
                unit = UNIT_MULTIPLY.get((lu, ru), f"{lu}*{ru}")
            elif lu:
                unit = lu
            elif ru:
                unit = ru
            else:
                unit = None
            return (lv * rv, unit)
        # Divisão
        if self.op == '/':
            if lu and ru:
                unit = UNIT_DIVIDE.get((lu, ru), f"{lu}/{ru}")
            elif lu:
                unit = lu
            elif ru:
                unit = f"1/{ru}"
            else:
                unit = None
            return (lv / rv, unit)
        # Comparações
        if self.op in ('>', '<', '=='):
            if lu != ru:
                raise TypeError(
                    f"Incompatível para '{self.op}': [{lu}] vs [{ru}]")
            if self.op == '>':
                return (lv > rv, None)
            if self.op == '<':
                return (lv < rv, None)
            return (lv == rv, None)
        raise Exception(f"Operação inválida '{self.op}'")


class Conditional(Node):
    def __init__(self, cond, then_blk, else_blk=None):
        self.cond = cond
        self.then_blk = then_blk
        self.else_blk = else_blk

    def evaluate(self, st):
        cond_val, _ = self.cond.evaluate(st)
        if cond_val:
            self.then_blk.evaluate(st)
        elif self.else_blk:
            self.else_blk.evaluate(st)


class Loop(Node):
    def __init__(self, times, body):
        self.times = times
        self.body = body

    def evaluate(self, st):
        cnt, _ = self.times.evaluate(st)
        for _ in range(int(cnt)):
            self.body.evaluate(SymbolTable(st))


class Block(Node):
    def __init__(self, statements):
        self.statements = statements

    def evaluate(self, st):
        for stmt in self.statements:
            stmt.evaluate(st)

# --- Parser ---


class Parser:
    def __init__(self, tokenizer: Tokenizer):
        self.tok = tokenizer

    def parse(self):
        stmts = []
        while self.tok.peek().type != 'EOF':
            if self.tok.peek().type == 'NEWLINE':
                self.tok.advance()
                continue
            stmts.append(self.parse_statement())
        return Program(stmts)

    def parse_statement(self):
        tok = self.tok.peek()
        if tok.type == 'COMPONENT':
            ctype = self.tok.expect('COMPONENT')
            name = self.tok.expect('IDENTIFIER')
            self.tok.expect('ASSIGN')
            expr = self.parse_expression()
            return ComponentDecl(ctype, name, expr)

        if tok.type == 'IDENTIFIER':
            name = self.tok.expect('IDENTIFIER')
            if self.tok.peek().type == 'DOT':
                self.tok.advance()
                prop = self.tok.expect('PROPERTY')
                if self.tok.peek().type == 'ASSIGN':
                    self.tok.expect('ASSIGN')
                    expr = self.parse_expression()
                    return PropertyAssignment(name, prop, expr)
                return PropertyAccess(name, prop)
            self.tok.expect('ASSIGN')
            expr = self.parse_expression()
            return Assignment(name, expr)

        if tok.type == 'IF':
            self.tok.expect('IF')
            cond = self.parse_expression()
            self.tok.expect('THEN')
            then_blk = self.parse_block()
            else_blk = None
            if self.tok.peek().type == 'ELSE':
                self.tok.expect('ELSE')
                else_blk = self.parse_block()
            self.tok.expect('END')
            return Conditional(cond, then_blk, else_blk)

        if tok.type == 'LOOP':
            self.tok.expect('LOOP')
            times = self.parse_expression()
            self.tok.expect('CYCLE')
            body = self.parse_block()
            self.tok.expect('END')
            return Loop(times, body)

        raise Exception(f"Comando inválido: {tok.type}")

    def parse_block(self):
        stmts = []
        while self.tok.peek().type not in ('END', 'ELSE', 'EOF'):
            if self.tok.peek().type == 'NEWLINE':
                self.tok.advance()
                continue
            stmts.append(self.parse_statement())
        return Block(stmts)

    def parse_expression(self):
        node = self.parse_term()
        while self.tok.peek().type in ('GT', 'LT', 'EQ'):
            op = self.tok.peek().value
            self.tok.advance()
            right = self.parse_term()
            node = BinaryOp(node, op, right)
        return node

    def parse_term(self):
        node = self.parse_factor()
        while self.tok.peek().type in ('PLUS', 'MINUS', 'MULT', 'DIV'):
            op = self.tok.peek().value
            self.tok.advance()
            right = self.parse_factor()
            node = BinaryOp(node, op, right)
        return node

    def parse_factor(self):
        tok = self.tok.peek()
        if tok.type == 'NUMBER':
            val = self.tok.expect('NUMBER')
            return Number(val)
        if tok.type == 'NUM_UNIT':
            val, unit = self.tok.expect('NUM_UNIT')
            return NumberWithUnit(val, unit)
        if tok.type == 'IDENTIFIER':
            name = self.tok.expect('IDENTIFIER')
            if self.tok.peek().type == 'DOT':
                self.tok.advance()
                prop = self.tok.expect('PROPERTY')
                return PropertyAccess(name, prop)
            return Identifier(name)
        if tok.type == 'LPAREN':
            self.tok.expect('LPAREN')
            expr = self.parse_expression()
            self.tok.expect('RPAREN')
            return expr
        raise Exception(f"Fator inesperado: {tok.type}")

# --- Main ---


def main():
    if len(sys.argv) < 2:
        print("Uso: python main.py <arquivo.txt>")
        return
    code = PrePro.filter(open(sys.argv[1], 'r', encoding='utf-8').read())
    tokenizer = Tokenizer(code)
    parser = Parser(tokenizer)
    ast = parser.parse()
    st = SymbolTable()
    ast.evaluate(st)

    print("\n--- Estado final dos componentes ---")
    for name, (data, tipo) in st.table.items():
        print(f"{name} ({tipo}):")
        for prop, val in data.items():
            v, u = val if isinstance(val, tuple) else (val, None)
            if u:
                print(f"  {prop}: {v} {u}")
            else:
                print(f"  {prop}: {v}")


if __name__ == '__main__':
    main()

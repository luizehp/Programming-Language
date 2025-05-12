
Linguagem para modelar e controlar circuitos eletrônicos
bash ´´´


<program>       ::= { <statement> }

<statement>     ::= <declaration>
                  | <assignment>
                  | <conditional>
                  | <loop>
                  | <function_call>

<declaration>   ::= <component_type> <identifier> "=" <value>

<component_type>::= "resistor"
                  | "capacitor"
                  | "indutor"

<assignment>    ::= <identifier> "=" <expression>
                  | <identifier> "." <property> "=" <expression>

<property>      ::= "tensao"
                  | "corrente"
                  | "resistência"

<conditional>   ::= "se" <expression> <relop> <expression> "entao"
                      <block>
                   [ "senao" <block> ]
                   "fim"

<relop>         ::= ">" | "<" | ">=" | "<=" | "==" | "!="

<loop>          ::= "loop" <number> "ciclos_clock" <block> "fim"
                  | "enquanto" <expression> <relop> <expression> <block> "fim"

<block>         ::= <statement> { <statement> }

<function_call> ::= <identifier> "(" [ <argument_list> ] ")"

<argument_list> ::= <expression> { "," <expression> }

<expression>    ::= <term> { ( "+" | "-" ) <term> }
<term>          ::= <factor> { ( "*" | "/" ) <factor> }
<factor>        ::= <number> [ <unit> ]
                  | <identifier>
                  | "(" <expression> ")"

<value>         ::= <number> [ <unit> ]

<identifier>    ::= <letter> { <letter> | <digit> }
<number>        ::= <digit> { <digit> } [ "." <digit> { <digit> } ]

<unit>          ::= "Ω"    (* ohm *)
                  | "F"    (* farad *)
                  | "H"    (* henry *)
                  | "V"    (* volt *)
                  | "A"    (* ampere *)

<letter>        ::= "a" | … | "z" | "A" | … | "Z"
<digit>         ::= "0" | … | "9"
´´´
flex lexer.l
bison -d parser.y
gcc lex.yy.c parser.tab.c -o circuitflow
./circuitflow < seu_programa.cf

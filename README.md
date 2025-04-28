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

<property>      ::= "tensão"
                  | "corrente"
                  | "resistência"

<conditional>   ::= "se" <expression> <relop> <expression> "então"
                      <block>
                   [ "senão" <block> ]
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

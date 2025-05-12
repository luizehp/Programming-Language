%{
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

void yyerror(const char *s);
extern int yylex(void);

int yydebug = 1;
%}

// Define a estrutura no cabeçalho gerado
%code requires {
    typedef struct {
        double number;
        const char *unit;
    } Value;
}

%union {
    double number;
    char *identifier;
    Value value;
    const char *unit;
    const char *relop;
}


%token <number> NUMBER
%token <identifier> IDENTIFIER
%token RESISTOR CAPACITOR INDUTOR
%token SE ENTAO SENAO FIM LOOP CICLOS_CLOCK ENQUANTO
%token TENSAO CORRENTE RESISTENCIA
%token <unit> OMEGA FARAD HENRY VOLT AMPERE
%token <relop> GE LE EQ NE GT LT
%token ASSIGN DOT

%type <value> value
%type <unit> unit_opt
%type <identifier> component_type property
%type <relop> relop
%type <number> expression term factor

%left '+' '-'
%left '*' '/'

%start program
%%

program:
    /* vazio */
    | program statement
    ;

statement:
    declaration
    | assignment
    | conditional
    | loop
    | function_call
    ;

declaration:
    component_type IDENTIFIER ASSIGN value
    { printf("Declaração: %s = %.2f%s\n", $2, $4.number, $4.unit ? $4.unit : ""); }
    ;

component_type:
    RESISTOR { $$ = "resistor"; }
    | CAPACITOR { $$ = "capacitor"; }
    | INDUTOR { $$ = "indutor"; }
    ;

value:
    NUMBER unit_opt { $$.number = $1; $$.unit = $2; }
    ;

unit_opt:
    /* vazio */ { $$ = NULL; }
    | OMEGA { $$ = "Ω"; }
    | FARAD { $$ = "F"; }
    | HENRY { $$ = "H"; }
    | VOLT { $$ = "V"; }
    | AMPERE { $$ = "A"; }
    ;

assignment:
    IDENTIFIER ASSIGN expression
    { printf("Atribuição: %s = %.2f\n", $1, $3); }
    | IDENTIFIER DOT property ASSIGN expression
    { printf("Atribuição de propriedade: %s.%s = %.2f\n", $1, $3, $5); }
    ;

property:
    TENSAO { $$ = "tensao"; }
    | CORRENTE { $$ = "corrente"; }
    | RESISTENCIA { $$ = "resistência"; }
    ;

conditional:
    SE expression relop expression ENTAO block opt_senao FIM
    { printf("Condicional: %.2f %s %.2f\n", $2, $3, $4); }
    ;

opt_senao:
    /* vazio */
    | SENAO block
    ;

relop:
    GT { $$ = ">"; }
    | LT { $$ = "<"; }
    | GE { $$ = ">="; }
    | LE { $$ = "<="; }
    | EQ { $$ = "=="; }
    | NE { $$ = "!="; }
    ;

loop:
    LOOP NUMBER CICLOS_CLOCK block FIM
    { printf("Loop por %.0f ciclos\n", $2); }
    | ENQUANTO expression relop expression block FIM
    { printf("Loop enquanto: %.2f %s %.2f\n", $2, $3, $4); }
    ;

block:
    statement
    | block statement
    ;

function_call:
    IDENTIFIER '(' opt_arg_list ')'
    { printf("Chamada de função: %s\n", $1); }
    ;

opt_arg_list:
    /* vazio */
    | argument_list
    ;

argument_list:
    expression
    | argument_list ',' expression
    ;

expression:
    term { $$ = $1; }
    | expression '+' term { $$ = $1 + $3; }
    | expression '-' term { $$ = $1 - $3; }
    ;

term:
    factor { $$ = $1; }
    | term '*' factor { $$ = $1 * $3; }
    | term '/' factor { $$ = $1 / $3; }
    ;

factor:
    NUMBER unit_opt { $$ = $1; }
    | IDENTIFIER { $$ = 0; }
    | IDENTIFIER DOT property { $$ = 0; }
    | '(' expression ')' { $$ = $2; }
    ;

%%

void yyerror(const char *s) {
    fprintf(stderr, "Erro: %s\n", s);
}

int main() {
    yydebug = 1;  // Ativar debug
    yyparse();
    return 0;
}
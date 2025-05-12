
%{
#include <stdio.h>
#include <stdlib.h>
extern int yylex();
extern char *yytext;
void yyerror(const char *s){ fprintf(stderr,"Erro: %s em '%s'\n", s, yytext); }
%}

/* Tokens */
%token RESISTOR CAPACITOR INDUTOR
%token SE ENTAO SENAO FIM
%token LOOP CICLOS_CLOCK ENQUANTO
%token IDENTIFIER NUMBER UNIT
%token EQ NE GE LE

/* Precedência (se quiser) */
%left '+' '-'
%left '*' '/'

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
    component_type IDENTIFIER '=' NUMBER UNIT             { /* AST: criar componente */ }
  ;

component_type:
    RESISTOR
  | CAPACITOR
  | INDUTOR
  ;

assignment:
    IDENTIFIER '=' expression                             { /* AST: atribuição */ }
  | IDENTIFIER '.' IDENTIFIER '=' expression              { /* AST: prop.assignment */ }
  ;

conditional:
    SE expression relop expression ENTAO block_opt senopt FIM
                                                           { /* AST: if */ }
  ;

relop:
    '>' | '<' | GE | LE | EQ | NE
  ;

senopt:
    /* vazio */
  | SENAO block_opt
  ;

loop:
    LOOP NUMBER CICLOS_CLOCK block_opt FIM                { /* AST: fixed-count loop */ }
  | ENQUANTO expression relop expression block_opt FIM   { /* AST: while */ }
  ;

block_opt:
    statement
  | block_opt statement
  ;

function_call:
    IDENTIFIER '(' arg_list_opt ')'                       { /* AST: call */ }
  ;

arg_list_opt:
    /* vazio */
  | arg_list
  ;

arg_list:
    expression
  | arg_list ',' expression
  ;

expression:
    expression '+' expression     { /* AST: add */ }
  | expression '-' expression     { /* AST: sub */ }
  | expression '*' expression     { /* AST: mul */ }
  | expression '/' expression     { /* AST: div */ }
  | NUMBER                        { /* AST: literal */ }
  | IDENTIFIER                    { /* AST: var */ }
  | '(' expression ')'            { /* AST: grouped */ }
  ;

%%

int main(void) {
  return yyparse();
}

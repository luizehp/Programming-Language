%{
#include "analisador.tab.h"
#include <stdlib.h>
%}

%option noyywrap
%option 8bit

%%

"/"              { return '/'; }  // Novo token adicionado
"+"              { return '+'; }
"-"              { return '-'; }
"*"              { return '*'; }
"resistor"       { return RESISTOR; }
"capacitor"      { return CAPACITOR; }
"indutor"        { return INDUTOR; }
"se"             { return SE; }
"entao"          { return ENTAO; }
"senao"          { return SENAO; }
"fim"            { return FIM; }
"loop"           { return LOOP; }
"ciclos_clock"   { return CICLOS_CLOCK; }
"enquanto"       { return ENQUANTO; }
"tensao"         { return TENSAO; }
"corrente"       { return CORRENTE; }
"resistência"    { return RESISTENCIA; }
"Ω"              { yylval.unit = "Ω"; return OMEGA; }
"F"              { yylval.unit = "F"; return FARAD; }
"H"              { yylval.unit = "H"; return HENRY; }
"V"              { yylval.unit = "V"; return VOLT; }
"A"              { yylval.unit = "A"; return AMPERE; }
">="             { yylval.relop = ">="; return GE; }
"<="             { yylval.relop = "<="; return LE; }
"=="             { yylval.relop = "=="; return EQ; }
"!="             { yylval.relop = "!="; return NE; }
">"              { yylval.relop = ">"; return GT; }
"<"              { yylval.relop = "<"; return LT; }
"="              { return ASSIGN; }
"."              { return DOT; }
"("              { return '('; }
")"              { return ')'; }
","              { return ','; }
[0-9]+(\.[0-9]+)? { yylval.number = atof(yytext); return NUMBER; }
[a-zA-ZÁÉÍÓÚÂÊÎÔÛÀÈÌÒÙÇáéíóúâêîôûàèìòùç][a-zA-Z0-9_ÁÉÍÓÚÂÊÎÔÛÀÈÌÒÙÇáéíóúâêîôûàèìòùç]* { yylval.identifier = strdup(yytext); return IDENTIFIER; }
[ \t\n]+         { /* Ignorar espaços */ }
.                { fprintf(stderr, "Caractere inválido: %s\n", yytext); }

%%
%{
#include "parser.tab.h"
%}

%%

"resistor"         { return RESISTOR; }
"capacitor"        { return CAPACITOR; }
"indutor"          { return INDUTOR; }

"se"                { return SE; }
"então"             { return ENTAO; }
"senão"             { return SENAO; }
"fim"               { return FIM; }

"loop"              { return LOOP; }
"ciclos_clock"      { return CICLOS_CLOCK; }
"enquanto"          { return ENQUANTO; }

[0-9]+(\.[0-9]+)?   {
                      yylval.dval = atof(yytext);
                      return NUMBER;
                    }

"Ω"|"F"|"H"|"V"|"A"  {
                      yylval.sval = strdup(yytext);
                      return UNIT;
                    }

[a-zA-Z][a-zA-Z0-9_]* {
                      yylval.sval = strdup(yytext);
                      return IDENTIFIER;
                    }

"=="| "!=" | ">=" | "<="    { return *yytext=='=' ? EQ : *yytext=='!'? NE : *yytext=='>'? GE : LE; }
">"                         { return '>'; }
"<"                         { return '<'; }

"="                         { return '='; }
"."                         { return '.'; }
","                         { return ','; }
"("                         { return '('; }
")"                         { return ')'; }

[ \t\r\n]+                  { /* ignora espaços */ }
"//".*                      { /* ignora comentário */ }

.                           { /* qualquer outro caractere */ }

%%

int yywrap(void) { return 1; }

/* A Bison parser, made by GNU Bison 3.8.2.  */

/* Bison interface for Yacc-like parsers in C

   Copyright (C) 1984, 1989-1990, 2000-2015, 2018-2021 Free Software Foundation,
   Inc.

   This program is free software: you can redistribute it and/or modify
   it under the terms of the GNU General Public License as published by
   the Free Software Foundation, either version 3 of the License, or
   (at your option) any later version.

   This program is distributed in the hope that it will be useful,
   but WITHOUT ANY WARRANTY; without even the implied warranty of
   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
   GNU General Public License for more details.

   You should have received a copy of the GNU General Public License
   along with this program.  If not, see <https://www.gnu.org/licenses/>.  */

/* As a special exception, you may create a larger work that contains
   part or all of the Bison parser skeleton and distribute that work
   under terms of your choice, so long as that work isn't itself a
   parser generator using the skeleton or a modified version thereof
   as a parser skeleton.  Alternatively, if you modify or redistribute
   the parser skeleton itself, you may (at your option) remove this
   special exception, which will cause the skeleton and the resulting
   Bison output files to be licensed under the GNU General Public
   License without this special exception.

   This special exception was added by the Free Software Foundation in
   version 2.2 of Bison.  */

/* DO NOT RELY ON FEATURES THAT ARE NOT DOCUMENTED in the manual,
   especially those whose name start with YY_ or yy_.  They are
   private implementation details that can be changed or removed.  */

#ifndef YY_YY_ANALISADOR_TAB_H_INCLUDED
# define YY_YY_ANALISADOR_TAB_H_INCLUDED
/* Debug traces.  */
#ifndef YYDEBUG
# define YYDEBUG 0
#endif
#if YYDEBUG
extern int yydebug;
#endif
/* "%code requires" blocks.  */
#line 13 "analisador.y"

    typedef struct {
        double number;
        const char *unit;
    } Value;

#line 56 "analisador.tab.h"

/* Token kinds.  */
#ifndef YYTOKENTYPE
# define YYTOKENTYPE
  enum yytokentype
  {
    YYEMPTY = -2,
    YYEOF = 0,                     /* "end of file"  */
    YYerror = 256,                 /* error  */
    YYUNDEF = 257,                 /* "invalid token"  */
    NUMBER = 258,                  /* NUMBER  */
    IDENTIFIER = 259,              /* IDENTIFIER  */
    RESISTOR = 260,                /* RESISTOR  */
    CAPACITOR = 261,               /* CAPACITOR  */
    INDUTOR = 262,                 /* INDUTOR  */
    SE = 263,                      /* SE  */
    ENTAO = 264,                   /* ENTAO  */
    SENAO = 265,                   /* SENAO  */
    FIM = 266,                     /* FIM  */
    LOOP = 267,                    /* LOOP  */
    CICLOS_CLOCK = 268,            /* CICLOS_CLOCK  */
    ENQUANTO = 269,                /* ENQUANTO  */
    TENSAO = 270,                  /* TENSAO  */
    CORRENTE = 271,                /* CORRENTE  */
    RESISTENCIA = 272,             /* RESISTENCIA  */
    OMEGA = 273,                   /* OMEGA  */
    FARAD = 274,                   /* FARAD  */
    HENRY = 275,                   /* HENRY  */
    VOLT = 276,                    /* VOLT  */
    AMPERE = 277,                  /* AMPERE  */
    GE = 278,                      /* GE  */
    LE = 279,                      /* LE  */
    EQ = 280,                      /* EQ  */
    NE = 281,                      /* NE  */
    GT = 282,                      /* GT  */
    LT = 283,                      /* LT  */
    ASSIGN = 284,                  /* ASSIGN  */
    DOT = 285                      /* DOT  */
  };
  typedef enum yytokentype yytoken_kind_t;
#endif

/* Value type.  */
#if ! defined YYSTYPE && ! defined YYSTYPE_IS_DECLARED
union YYSTYPE
{
#line 20 "analisador.y"

    double number;
    char *identifier;
    Value value;
    const char *unit;
    const char *relop;

#line 111 "analisador.tab.h"

};
typedef union YYSTYPE YYSTYPE;
# define YYSTYPE_IS_TRIVIAL 1
# define YYSTYPE_IS_DECLARED 1
#endif


extern YYSTYPE yylval;


int yyparse (void);


#endif /* !YY_YY_ANALISADOR_TAB_H_INCLUDED  */

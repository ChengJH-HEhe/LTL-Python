// LTL formula grammar aligned with course benchmarks:
// - Propositions: lowercase identifiers (a, b, c, ...)
// - Temporal: G F X U (uppercase)
// - Boolean: /\  \/  ->  !
// - Parentheses: arbitrarily deep nesting via primary; optional redundant outer () are
//   stripped in parse_ltl_antlr before lexing so inputs like "(((a)))" match cleanly.
// Whitespace is ignored. Spacing is optional, e.g. "c U (!a)" and "cU(!a)" both work.
grammar LTL;

formula
    : untilExpr EOF
    ;

untilExpr
    : untilExpr U_OP implyExpr  # UntilChain
    | implyExpr                 # UntilSingle
    ;

// Right-associative: a -> b -> c === a -> (b -> c)
implyExpr
    : orExpr IMP implyExpr      # ImplyRec
    | orExpr                    # ImplyAtom
    ;

orExpr
    : orExpr OR andExpr         # OrChain
    | andExpr                   # OrAtom
    ;

andExpr
    : andExpr AND unaryExpr     # AndChain
    | unaryExpr                 # AndAtom
    ;

unaryExpr
    : NOT unaryExpr             # Not
    | G_MOD unaryExpr           # Globally
    | F_MOD unaryExpr           # Finally
    | X_MOD unaryExpr           # Next
    | primary                   # UnaryPass
    ;

primary
    : LPAREN untilExpr RPAREN   # Parens
    | ID                        # Prop
    ;

// Lexer
U_OP   : 'U' ;
G_MOD  : 'G' ;
F_MOD  : 'F' ;
X_MOD  : 'X' ;
NOT    : '!' ;

AND    : '/\\' ;
OR     : '\\/' ;
IMP    : '->' ;

LPAREN : '(' ;
RPAREN : ')' ;

ID     : [a-z] [a-z0-9_]* ;

WS     : [ \t\r\n]+ -> skip ;

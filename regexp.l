%{
#include "regexp.tab.h"
#include <stdio.h>
#include <stdlib.h>
%}

%%
"E"         { return EPSILON; }
[abc]       { 
                /* On utilise var_charactere défini dans le %union de regexp.y */
                yylval.var_charactere = yytext[0]; 
                return VARIABLE; 
            }
"*"         { return ETOILE; }
"+"         { return PLUS; }
"."         { return POINT; }
"("         { return PAR_O; }
")"         { return PAR_F; }

[ \t\n]     { ; } /* Ignorer les espaces et retours à la ligne */

.           { 
                printf("Caractère inconnu : %s\n", yytext); 
            }
%%
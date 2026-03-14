/* Etape 1 : Définition générales */

%{
#include <stdio.h>
#include <stdlib.h>

int compteur_automate = 0; 
FILE *fichier;
int res0, res1 ; 

int yylex();
void yyerror(const char *s);
%}  

%union {
    char var_charactere ; 
    int var_indice  ; 
}

/* Etape 2 : Définition des tokens */ 
%token <var_charactere> VARIABLE
%token EPSILON ETOILE PLUS POINT PAR_O PAR_F  

/* Liaison entre la grammaire et l'union */
%type <var_indice> expression 

/* Etape 3 : Priorité des opérations */ 
%left PLUS 
%left POINT
%right ETOILE

%% 

/* Etape 4 : Règles de grammaires */ 
input: expression expression {
    res0 = $1 ;
    res1 = $2 ;
} ;

expression : 
    VARIABLE { 
        fprintf(fichier, "a%d = automate(\"%c\")\n", compteur_automate, $1);
        $$ = compteur_automate;
        compteur_automate++;
    }
    | EPSILON {
        fprintf (fichier, "a%d = automate(\"E\")\n", compteur_automate) ;
        $$ = compteur_automate;
        compteur_automate++;
    }
    | expression ETOILE {
        fprintf(fichier, "a%d = etoile(a%d)\n", compteur_automate, $1) ;
        $$ = compteur_automate; 
        compteur_automate++;
    }
    | expression PLUS expression {
        fprintf( fichier, "a%d = union(a%d, a%d)\n", compteur_automate, $1, $3) ;
        $$ = compteur_automate;
        compteur_automate++ ;
    }
    | expression POINT expression {
        fprintf(fichier, "a%d = concatenation(a%d, a%d)\n", compteur_automate, $1, $3);
        $$ = compteur_automate;
        compteur_automate++ ;
    }
    | PAR_O expression PAR_F {
        $$ = $2;
    }
;

%%

/* Etape 5 : Création du main.py */
int main() {
    // Sous-étape 1 :  On indique à Lex/Yacc de lire test.1 au lieu du clavier
    extern FILE *yyin; 
    yyin = fopen("test.1", "r");
    
    if (yyin == NULL) {
        fprintf(stderr, "Erreur : Impossible d'ouvrir le fichier test.1\n");
        return 1;
    }

    // Sous-étape 2 : ouvrir le fichier de sortie
    fichier = fopen("main.py", "w");
    if (fichier == NULL) return 1;

    fprintf(fichier, "from automate import *\n\n");
    
    // Sous étape 3 : Analyse
    yyparse(); 

    // Sous-étape 4 : Remplissage du fichier Python
    fprintf(fichier, "res0 = tout_faire(a%d)\n", res0);
    fprintf(fichier, "res1 = tout_faire(a%d)\n", res1);
    fprintf(fichier, "\nif egal(res0, res1):\n");
    fprintf(fichier, "    print(\"EGAL\")\n");
    fprintf(fichier, "else:\n");
    fprintf(fichier, "    print(\"NON EGAL\")\n");
    fclose(fichier);
    fclose(yyin);
    printf("\nLe fichier main.py bien été crée à partir de test.1\n");
    return 0;
}
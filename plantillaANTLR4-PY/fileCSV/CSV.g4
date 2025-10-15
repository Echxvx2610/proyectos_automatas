grammar CSV;

// Regla principal - archivo CSV completo
csvFile: row (('\r'? '\n' row)* '\r'? '\n')? EOF;
/*
row → La primera fila es obligatoria (por ejemplo un csv vacio no es valido )
(...)?  → El ? hace que todo el grupo sea opcional
('\r'? '\n' row)* → El * permite cero o mas repeticione de:
'\r'? → Retorno de carro opcional
'\n' → Salto de linea obligatorio
row → Otra fila
'\r'? '\n' → Newline final opcional (permite que el archivo termine con o sin salto de linea)
EOF → End Of File (garantiza que se procese todo el archivo)
 */

// Regla para una fila
row: field (',' field)*;
/*
field → Primer campo obligatorio (una fila vacia tendria un campo vacio)
(',' field)* → El * permite cero o mas campos adicionales

por ejemplo:
cristian
cristian,oscar
,
 */
// Regla para un campo individual
field
    : TEXT           # TextField
    | STRING         # QuotedField
    |                # EmptyField
    ;

// Reglas del lexer
TEXT: ~[,\n\r"]+; // cualquier cosa excepto coma, newline o comilla
STRING: '"' ('""' | ~'"')* '"'; // texto entre comillas, "" para comilla literal
WS: [ \t]+ -> skip; // ignorar espacios en blanco
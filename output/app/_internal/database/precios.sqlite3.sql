BEGIN TRANSACTION;
CREATE TABLE IF NOT EXISTS "cupones" (
	"ID"	INTEGER NOT NULL,
	"Artículo"	TEXT,
	"Nombre"	TEXT,
	"Física disponíble"	INTEGER,
	"Almacen"	INTEGER,
	"Clase"	TEXT,
	"Marca"	TEXT,
	"Matriz"	TEXT,
	"Tipo de Producto"	TEXT,
	"Precio anterior"	INTEGER,
	"Precio actual"	INTEGER,
	PRIMARY KEY("ID" AUTOINCREMENT)
);
COMMIT;

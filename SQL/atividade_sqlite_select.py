import sqlite3

DB_PATH = "loja_select.db"


def criar_banco(conn: sqlite3.Connection) -> None:
    cursor = conn.cursor()

    cursor.execute("DROP TABLE IF EXISTS venda")
    cursor.execute("DROP TABLE IF EXISTS produto")
    cursor.execute("DROP TABLE IF EXISTS cliente")

    cursor.execute(
        """
        CREATE TABLE cliente (
            id_cliente INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            cidade TEXT NOT NULL
        )
        """
    )

    cursor.execute(
        """
        CREATE TABLE produto (
            id_produto INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            preco REAL NOT NULL,
            estoque INTEGER NOT NULL
        )
        """
    )

    cursor.execute(
        """
        CREATE TABLE venda (
            id_venda INTEGER PRIMARY KEY AUTOINCREMENT,
            id_cliente INTEGER NOT NULL,
            valor REAL NOT NULL,
            data_venda TEXT NOT NULL,
            FOREIGN KEY (id_cliente) REFERENCES cliente(id_cliente)
        )
        """
    )

    clientes = [
        ("Ana Silva", "Macapá"),
        ("Bruno Costa", "Santana"),
        ("Carlos Almeida", "Macapá"),
        ("Mariana Souza", "Belém"),
        ("João Silva", "Santana"),
        ("Fernanda Lima", "Macapá"),
        ("Amanda Rocha", "Belém"),
        ("Pedro Martins", "Oiapoque"),
        ("Lucas Ferreira", "Macapá"),
        ("Aline Santos", "Santana"),
    ]
    cursor.executemany(
        """
        INSERT INTO cliente (nome, cidade)
        VALUES (?, ?)
        """,
        clientes,
    )

    produtos = [
        ("Notebook Dell", 3500.00, 8),
        ("Mouse Gamer", 120.00, 25),
        ("Teclado Mecânico", 280.00, 15),
        ("Monitor 24 Polegadas", 900.00, 6),
        ("Cabo HDMI", 35.00, 50),
        ("Headset Bluetooth", 180.00, 12),
        ("Mousepad Grande", 45.00, 30),
        ("Memória RAM 8GB", 250.00, 10),
        ("SSD 480GB", 320.00, 4),
        ("Webcam Full HD", 210.00, 7),
        ("Microfone USB", 450.00, 3),
        ("Carregador Universal", 85.00, 18),
    ]
    cursor.executemany(
        """
        INSERT INTO produto (nome, preco, estoque)
        VALUES (?, ?, ?)
        """,
        produtos,
    )

    vendas = [
        (1, 3500.00, "2026-05-01"),
        (2, 120.00, "2026-05-02"),
        (3, 900.00, "2026-05-03"),
        (1, 280.00, "2026-05-04"),
        (5, 35.00, "2026-05-05"),
        (6, 180.00, "2026-05-06"),
        (7, 320.00, "2026-05-07"),
        (8, 450.00, "2026-05-08"),
    ]
    cursor.executemany(
        """
        INSERT INTO venda (id_cliente, valor, data_venda)
        VALUES (?, ?, ?)
        """,
        vendas,
    )

    conn.commit()


def executar_consultas(conn: sqlite3.Connection) -> None:
    cursor = conn.cursor()

    city_escolhida = "Macapá"

    consultas: list[tuple[str, str]] = [
        ("1) Todos os clientes", "SELECT * FROM cliente"),
        ("2) Todos os produtos", "SELECT * FROM produto"),
        ("3) Nome e preço (produtos)", "SELECT nome, preco FROM produto"),
        ("4) Produtos com preço > 100", "SELECT * FROM produto WHERE preco > 100"),
        ("5) Produtos com preço < 500", "SELECT * FROM produto WHERE preco < 500"),
        (
            "6) Clientes da cidade específica (ex.: Macapá)",
            "SELECT * FROM cliente WHERE cidade = ?",
        ),
        ("7) Produtos com estoque > 10", "SELECT * FROM produto WHERE estoque > 10"),
        (
            "8) Produtos com preço > 100 e estoque > 5",
            "SELECT * FROM produto WHERE preco > 100 AND estoque > 5",
        ),
        (
            "9) Produtos com preço < 50 OU estoque > 20",
            "SELECT * FROM produto WHERE preco < 50 OR estoque > 20",
        ),
        ("10) Clientes cujo nome começa com 'A'", "SELECT * FROM cliente WHERE nome LIKE 'A%'"),
        ("11) Produtos que contenham 'note' no nome", "SELECT * FROM produto WHERE LOWER(nome) LIKE '%note%'"),
        ("12) Produtos com preço entre 100 e 500", "SELECT * FROM produto WHERE preco BETWEEN 100 AND 500"),
        ("13) Produtos ordenados por preço crescente", "SELECT * FROM produto ORDER BY preco ASC"),
        ("14) Produtos ordenados por preço decrescente", "SELECT * FROM produto ORDER BY preco DESC"),
        ("15) Clientes ordenados por nome", "SELECT * FROM cliente ORDER BY nome ASC"),
        (
            "16) Produtos ordenados por preço desc e nome asc",
            "SELECT * FROM produto ORDER BY preco DESC, nome ASC",
        ),
    ]

    for titulo, sql in consultas:
        print("\n" + "=" * 80)
        print(titulo)
        print("-" * 80)

        if "WHERE cidade = ?" in sql:
            cursor.execute(sql, (city_escolhida,))
        else:
            cursor.execute(sql)

        colunas = [desc[0] for desc in cursor.description] if cursor.description else []
        linhas = cursor.fetchall()

        if not linhas:
            print("(nenhum registro)")
            continue

        if colunas:
            print(" | ".join(colunas))
            print("-" * 80)

        for linha in linhas:
            print(" | ".join(str(v) for v in linha))


def main() -> None:
    conn = sqlite3.connect(DB_PATH)
    try:
        criar_banco(conn)
        executar_consultas(conn)
        print("\nBanco de dados criado e consultas executadas com sucesso!")
        print(f"Arquivo gerado: {DB_PATH}")
    finally:
        conn.close()


if __name__ == "__main__":
    main()

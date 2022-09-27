# código muito simplificado para criar um banco de dados de exemplo.
import sqlite3

# abre uma conexão
con = sqlite3.connect('banco.db')

# pega um cursor, que é o objeto que irá executar as transações
cur = con.cursor()

# cria tabela produtos
cur.execute('''
    CREATE TABLE IF NOT EXISTS produtos (
        id_produto integer, nome text, descricao text,
        primary key(id_produto)
    )
''')

# cria tabela anotações
cur.execute('''
    CREATE TABLE IF NOT EXISTS anotacoes (
        id_anotacao integer, data text, preco text,
        primary key(id_anotacao)
    )
''')

cur.execute('''
    CREATE TABLE IF NOT EXISTS anotacoes_para_produtos (
        id_produto integer not null, id_anotacao integer not null,
        primary key (id_produto, id_anotacao),
        foreign key (id_produto) references produtos(id_produto),
        foreign key (id_anotacao) references anotacoes(id_anotacao)
    );
''')


# insere dados
# cur.execute('''
#     INSERT INTO exemplo(id, x, y, semestre) VALUES
#     (0, 0, 1, 'primeiro semestre'),
#     (1, 1, 0, 'primeiro semestre'),
#     (2, 2, 0, 'primeiro semestre'),
#     (3, 3, 0, 'primeiro semestre'),
#     (4, 4, 0, 'primeiro semestre'),
#     (5, 0, 0, 'segundo semestre'),
#     (6, 1, 1, 'segundo semestre'),
#     (7, 2, 0, 'segundo semestre'),
#     (8, 3, 0, 'segundo semestre'),
#     (9, 4, 0, 'segundo semestre');
# ''')

# salva modificações
con.commit()

# fecha conexão com o banco
con.close()
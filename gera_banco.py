# código muito simplificado para criar um banco de dados de exemplo.
import sqlite3
import os


def main():
    database_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'banco.db')

    if os.path.exists(database_path):
        os.remove(database_path)

    # abre uma conexão com o banco e fecha automaticamente no fim do bloco with
    with sqlite3.connect(database_path) as con:
        # pega um cursor, que é o objeto que irá executar as transações
        cur = con.cursor()

        # cria tabela produtos
        cur.execute('''
            CREATE TABLE IF NOT EXISTS produtos (
                id_produto integer, 
                nome text,
                primary key(id_produto)
            )
        ''')

        # cria tabela anotações
        cur.execute('''
            CREATE TABLE IF NOT EXISTS anotacoes (
                id_anotacao integer, 
                date_annotation text, 
                preco text,
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

        # não precisa mais fechar a conexão, já que estamos abrindo o banco com with
        # fecha conexão com o banco
        # con.close()

if __name__ == '__main__':
    main()

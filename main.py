from selenium import webdriver
import os
import time
import sqlite3
from datetime import datetime as dt


def main():
    if os.name == 'nt':  # se o sistema operacional for windows
        path = './geckodriver.exe'  # o executável é .exe
    else:  # se o sistema operacional for linux ou mac
        path = './geckodriver'  # o executável não tem extensão

    # usar with garante que o método driver.close() será chamado,
    # mesmo que uma exceção ocorra no meio do código
    # isso evita que, quando fazemos testes e o programa dá erro,
    # fique uma instância do firefox aberta
    with webdriver.Firefox(executable_path=path) as driver:
        # abre uma instância do firefox na página dada
        driver.get('https://www.canecaria.com.br/')
        time.sleep(4)  # dorme uns 10 segundos, para dar tempo de ver a página
        xpath_1 = '/html/body/div/div/div[3]/div/main/div/div/div/div[2]/div/div/div/section[1]/div[2]/div/div[3]/div/div/div[1]/h1/a'
        elements = driver.find_elements_by_xpath(xpath_1)
        print('existem %d elementos da classe %s' % (len(elements), xpath_1))

        database_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'banco.db')
        # abre uma conexão
        with sqlite3.connect(database_path) as con:
            cur = con.cursor()

            # pega a string da data de hoje
            today = dt.now().strftime('%Y-%m-%d-%H-%M-%S')

            # pega o último id da tabela produtos
            try:
                last_product_id = int(cur.execute('SELECT MAX(id_produto) from produtos').fetchone()[0]) + 1
            except:
                last_product_id = 0

            # pega o último id da tabela anotacoes
            try:
                last_annotation_id = int(cur.execute('SELECT MAX(id_anotacao) from anotacoes').fetchone()[0]) + 1
            except:
                last_annotation_id = 0

            # para cada produto que foi capturado pelo selenium
            for element in elements:
                # pega o nome do produto pelo site
                nome = element.text

                # tenta achar o id do produto que tem o nome do site
                # fetchone = retorna uma tupla; fetchall = retorna uma lista de tuplas
                # cada tupla é uma linha da tabela. a tupla tem tantas posições quanto
                # seletores que foram passados para a cláusula SELECT
                # se apenas um item foi selecionado, é uma tupla de 1 posição
                res = cur.execute('SELECT id_produto FROM produtos WHERE nome=\'{0}\''.format(nome)).fetchone()
                if res is None:  # não achou nada no banco; o produto não existe lá ainda
                    # insere no banco o produto
                    cur.execute(
                        'INSERT INTO produtos(id_produto, nome) VALUES ({0}, \'{1}\')'.format(last_product_id, nome)
                    )
                    id_produto = last_product_id
                    last_product_id += 1
                else:
                    # atribui o id recuperado a variável id_produto
                    id_produto = res[0]

                # TODO descobrir como colocar o preço é com vocês =D
                cur.execute(
                    'INSERT INTO anotacoes(id_anotacao, date_annotation, preco) VALUES ({0}, \'{1}\', \'{2}\')'.format(
                        last_annotation_id, today, 'R$ 0,00')
                )

                cur.execute(
                    'INSERT INTO anotacoes_para_produtos(id_produto, id_anotacao) VALUES ({0}, {1})'.format(
                        id_produto, last_annotation_id
                    )
                )
                last_annotation_id += 1

            con.commit()


if __name__ == '__main__':
    main()

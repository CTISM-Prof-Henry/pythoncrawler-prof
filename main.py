from selenium import webdriver
import os
import time
import sqlite3


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

        # abre uma conexão
        con = sqlite3.connect('banco.db')
        # pega um cursor, que é o objeto que irá executar as transações
        cur = con.cursor()

        # pega o ultimo id da tabela produtos
        try:
            last_id = int(cur.execute('SELECT MAX(id_produto) from produtos').fetchone()[0]) + 1;
        except:
            last_id = 0


        for element in elements:
            cur.execute(
                'INSERT INTO produtos(id_produto, nome) VALUES ({0}, \'{1}\')'.format(last_id, element.text)
            )
            last_id += 1

        con.commit()
        # fecha conexão com o banco
        con.close()


if __name__ == '__main__':
    main()

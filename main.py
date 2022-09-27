from selenium import webdriver
import os
import time


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

        for element in elements:
            print(element.text)

        # # pega apenas o primeiro <p> da página
        # element = driver.find_element_by_tag_name("p")
        # print(element.text)  # imprime o texto do primeiro paraǵrafo
        # # pega todos os <p> da página
        # elements = driver.find_elements_by_tag_name("p")
        # for some in elements:
        #     print(some.text)
        #
        # # pega todos os <p> da página
        # elements = driver.find_elements_by_class_name("strait")
        # for some in elements:
        #     print(some.text)
        # element = driver.find_element_by_id("lista")
        # elements = driver.find_elements_by_xpath('/html/body/ul/li')
        # for some in elements:
        #     print(some.text)


if __name__ == '__main__':
    main()

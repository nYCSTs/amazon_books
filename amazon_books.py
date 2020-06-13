import requests
from bs4 import BeautifulSoup

# REFERENCIA: https://medium.com/@tusharseth93/scraping-the-web-a-fast-and-simple-way-to-scrape-amazon-b3d6d74d649f
# VERSAO 1.5

proxies = {
	'http':'142.93.57.37:80',
	'http':'107.191.41.188:8080',
	'http':'104.45.11.234:3128',
	'http':'163.172.189.32:8811',
	'http':'136.244.116.130:8080',
	'http':'161.35.70.249:8080',
	'http':'149.28.49.67:8080',
	'http':'138.201.106.88:8080',
	'http':'165.227.87.203:3128',
	'http':'173.212.202.65:80',
}

headers = {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64;     x64; rv:66.0) Gecko/20100101 Firefox/66.0", "Accept-Encoding":"gzip, deflate",     "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8", "DNT":"1","Connection":"close", "Upgrade-Insecure-Requests":"1"}

def get_connection(code):
	if (len(code) == 10):
		r = requests.get('https://www.amazon.com.br/gp/offer-listing/' + code + '/condition=new/ref=olp_f_primeEligible?f_freeShipping=true', headers=headers, proxies=proxies)
	else:
		r = requests.get(code, headers=headers, proxies=proxies)
	
	content = r.content
	soup = BeautifulSoup(content, features="lxml")
	r.close()

	return soup

def get_price(soup):
	return str(soup.findAll('span', {'class':'a-offscreen'}))[-16:-8]

def get_name(soup):
	return str(soup.findAll('title', {'dir':'ltr'}))[50:-9]

def url_fixer(url):
	index = url.find('dp')
	return 'https://www.amazon.com.br/' + url[index:index + 13]
	
VERSION = 1.5
link_list = []
codes = []
qnt_items = 5


print(VERSION)
while True:
	opc = int(input('\n\t1) Checar por disponibilidade.\n\t2) Adicionar novo link\n\t3) Remover link\n\t4) Pesquisar por nome\n\t5) Mostrar toda lista\n\t6) Limpar lista\n\t7) Configurações\n\t8) Fechar\n>> '))

	#checar por disponibilidade 
	if (opc == 1):
		try:
			open('links.txt', mode = 'r')
		except:
			print("Arquivo 'links.txt' nao existe. Para criar acesse primeiramente a opção 2) ou 4)")
		else:
			with open("links.txt", mode = 'r') as file:
				link_list = file.readlines()
			codes = [link.strip()[-10:] for link in link_list]
			link_list = [link.strip() for link in link_list]
			
			if (len(codes) >= 1):
				for index, code in enumerate(codes):
					soup = get_connection(code)
					spacement = '.' * (50 - len(get_name(soup)))

					if 'não há ofertas de produto dentro destas condições' in soup.text:
						print(get_name(soup) + spacement + ' - SEM ESTOQUE. \t\n(LINK: ' + link_list[index] + ')\n')
					else:
						print(get_name(soup) + spacement + ' - EM ESTOQUE. PREÇO: ' + get_price(soup) + '\t\n(LINK: ' + link_list[index] + ')\n')

			else:
				print('A lista de links esta vazia.\n')
		
	#adicionar novo link
	elif (opc == 2):
		while (opc):
			url = input('Insira uma url: ')
			if url[-1] == '/':
				url = url[:-1]
			if len(url) != 40:
				url = url_fixer(url)
			with open("links.txt", mode = 'a+') as file:
				file.write(url + '\n')
				print('Link adicionado com sucesso.')
			opc = int(input('Continuar adicionando?\n\t1 - Sim\n\t0 - Não\n> '))
			#CASO SEJA UM VALOR DIFERENTE DE 1 E 0

	#remover link
	elif (opc == 3):
		try:
			open('links.txt', mode = 'r')
		except:
			print("Arquivo 'links.txt' nao existe. Para criar acesse primeiramente a opção 2) ou 4)")
		else:
			with open("links.txt", "r") as file:
				d = file.readlines()
				d = [link.strip() for link in d]
				file.seek(0)
				if (len(d) >= 1):	
					for line_no in range(0, len(d)):
						soup = get_connection(d[line_no][-10:])
						print(str(line_no + 1) + ') ' + get_name(soup) + ' (LINK: ' + d[line_no] + ')')
					lineRem = int(input('\nLinha a ser removida (para voltar insira 0): '))
					if (lineRem > len(d) and lineRem != 0):
						print(f'Valor invalido. Tente valores entre 1 e {len(d)}')
					elif (lineRem > 0):
						with open("links.txt", 'w') as file:
							for line in d:
								if line.strip("\n") != d[lineRem - 1]:
									file.write(line + '\n')
				else:
					print('Nao ha links')

	#pesquisar por nome
	elif (opc == 4):
		while True:
			search = input('Busca: ')
			url = 'https://www.amazon.com.br/s?k=' + search.lower()
			links = []
			names = []
			aux = 0 
			flag = 1

			while True:
				soup = get_connection(url)
				for d in soup.findAll('div', attrs={'class':'sg-col-4-of-12 sg-col-8-of-16 sg-col-16-of-24 sg-col-12-of-20 sg-col-24-of-32 sg-col sg-col-28-of-36 sg-col-20-of-28'}):
					names.append(str(d.find('span', attrs={'class':'a-size-medium a-color-base a-text-normal'}))[66:-7])
					index = str(d.find('a', attrs={'class':'a-link-normal a-text-normal'})).find('dp')
					links.append('https://www.amazon.com.br/' + str(d.find('a', attrs={'class':'a-link-normal a-text-normal'}))[index:index + 13])
					aux += 1
					if (aux == qnt_items):
						flag = 0
						break
				if (flag == 0):
					break

			for index, item in enumerate(names):
				print(f'{index + 1}) {item}')

			while True:
				num = int(input('\nItem a ser adicionado (0 > nova busca; -1 > voltar): '))
				if (num > 0 and num <= qnt_items):
					with open('links.txt', mode = 'a+') as file:
						file.write(links[num - 1] + '\n')
					break
				elif (num > qnt_items or num < -1):
					print(f'Valor inserido invalido (entre 1 e {qnt_items}), tente novamente.')
				elif (num == 0 or num == -1):
					break
			if (num != 0):
				break

	#mostrar toda lista
	elif (opc == 5):
		try:
			open('links.txt', mode = 'r')
		except:
			print("Arquivo 'links.txt' nao existe. Para criar acesse primeiramente a opção 2) ou 4)")
		else:
			with open("links.txt", mode = 'r') as file:
				link_list = file.readlines()
			codes = [link.strip()[-10:] for link in link_list]
			for code in codes:
				if (len(get_price(get_connection(code))) > 0):
					print(f'{get_name(get_connection(code))} - {get_price(get_connection(code))}')
				else:
					print(f'{get_name(get_connection(code))}')

	#limpar lista
	elif (opc == 6):
		with open('links.txt', mode = 'w') as file:
			file.write('')
		print('A lista foi limpa')

	#configuracoes
	elif(opc == 7):
		qnt_items = int(input("Quantidade de items a ser procurada em '4) Pesquisar por nome': "))

	#fechar
	elif (opc == 8):
		break



#1.0 - basico x
#1.1 - aceitar possiveis formatos de links x
#1.2 - remover links x
#1.3 - mostrar preco x
#1.4 - pesquisar por nome x 
#1.41 - fixes
#1.5 - menu de configuracao, fechar e toda lista
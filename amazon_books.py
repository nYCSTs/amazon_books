
import requests
from bs4 import BeautifulSoup

# REFERENCIA: https://medium.com/@tusharseth93/scraping-the-web-a-fast-and-simple-way-to-scrape-amazon-b3d6d74d649f
# VERSAO 1.4

proxies = {
	'http':'http://142.93.57.37:80',
	'http':'107.191.41.188:8080',
	'http':'104.45.11.234:3128',
	'http':'163.172.189.32:8811',
	'http':'136.244.116.130:8080',
	'http':'161.35.70.249:8080',
	'http':'149.28.49.67:8080',
	'http':'138.201.106.88:8080',
	'http':'165.227.87.203:3128',
	'http':'173.212.202.65:80',
	'http':'134.209.29.120:8080',
	'http':'108.61.164.163:8080',
	'http':'109.69.75.5:46347',
	'http':'109.248.60.53:8081',
	'http':'108.61.166.237:8080',
	'http':'104.244.77.254:8080',
	'http':'104.244.75.26:8080',
	'http':'151.80.199.89:3128',
	'http':'136.244.116.130:8080',
	'http':'161.35.70.249:8080',
	'http':'169.51.52.227:3128',
	'http':'138.201.106.88:8080',
	'http':'176.98.95.105:60342',
	'http':'136.244.70.47:8080',
	'http':'188.10.135.155:3128',
	'http':'185.142.212.152:3128',
	'http':'188.166.53.57:8080',
	'http':'185.130.105.119:808',
	'http':'185.199.84.161:53281',
	'http':'185.130.105.119:65022',
	'http':'185.130.105.119:65102',
	'http':'185.137.232.95:80',
	'http':'49.12.75.192:3128',
	'http':'5.172.188.92:8080',
}

headers = {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64;     x64; rv:66.0) Gecko/20100101 Firefox/66.0", "Accept-Encoding":"gzip, deflate",     "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8", "DNT":"1","Connection":"close", "Upgrade-Insecure-Requests":"1"}

link_list = []
codes = []

class Teste:
	VERSION = 1.4
	def __init__(self):
		pass

def info(code):
	r = requests.get('https://www.amazon.com.br/gp/offer-listing/' + code + '/condition=new/ref=olp_f_primeEligible?f_freeShipping=true', headers=headers, proxies=proxies)
	content = r.content
	soup = BeautifulSoup(content, features="lxml")

	price = str(soup.findAll('span', {'class':'a-offscreen'}))
	name = str(soup.findAll('title', {'dir':'ltr'}))

	return [r, name[50:-9], price[-16:-8]]

inst = Teste
print(inst.VERSION)
opc = int(input('\t1) Checar por disponibilidade.\n\t2) Adicionar novo link\n\t3) Remover link\n\t4) Pesquisar por nome (em desenvolvimento)\n\t5) Limpar lista\n\t6) Debugger\n>> '))
if (opc == 1):
	with open("links.txt", mode = 'r') as file:
		link_list = file.readlines()
	codes = [link.strip()[-10:] for link in link_list]
	link_list = [link.strip() for link in link_list]
	for index, code in enumerate(codes):
		title = info(code)
		x = '.' * (50 - len(title[1]))

		if 'não há ofertas de produto dentro destas condições' in title[0].text:
			print(title[1] + x + ' - SEM ESTOQUE. (LINK: ' + link_list[index] + ')')
		else:
			print(title[1] + x + ' - EM ESTOQUE. PREÇO: ' + title[2] + ' (LINK: ' + link_list[index] + ')')

		print('-------------')
		
	title[0].close()
	
elif (opc == 2):
	while (True):
		link = input('Insira uma url: ')
		if link[-1] == '/':
			link = link[:-1]
		elif len(link) != 40:
			index = link.find('dp')
			link = 'https://www.amazon.com.br/' + link[index:index + 13]
		with open("links.txt", mode = 'a') as file:
			file.write(link + '\n')
			print('Link adicionado.')
		while (opc):
			opc = int(input('Continuar adicionando?\n\t1 - Sim\n\t0 - Não\n> '))
			if (opc == 1):
				break
			elif (opc != 1 and opc != 0):
				print('Entrada invalida, tente novamente.\n')
		if (not opc):
			break

elif (opc == 3):
	with open("links.txt", "r") as file:
		d = file.readlines()
		d = [link.strip() for link in d]
		file.seek(0)
		if (len(d) >= 1):	
			for line_no in range(0, len(d)):
				print(str(line_no + 1) + ') ' + info(d[line_no][-10:])[1] + ' (LINK: ' + d[line_no] + ')')
			lineRem = int(input('\nLinha a ser removida: '))
		else:
			print('Nao ha links')
	with open("links.txt", 'w') as file:
		for line in d:
			if line.strip("\n") != d[lineRem - 1]:
				file.write(line + '\n')

elif (opc == 4):
	search = input('Busca: ')
	url = 'https://www.amazon.com.br/s?k=' + search.lower()
	aux = 0
	links = []
	names = []

	r = requests.get(url, headers=headers, proxies=proxies)
	content = r.content
	soup = BeautifulSoup(content, features="lxml")

	print(soup)

	for d in soup.findAll('div', attrs={'class':'sg-col-4-of-12 sg-col-8-of-16 sg-col-16-of-24 sg-col-12-of-20 sg-col-24-of-32 sg-col sg-col-28-of-36 sg-col-20-of-28'}):
		names.append(str(d.find('span', attrs={'class':'a-size-medium a-color-base a-text-normal'}))[66:-7])
		index = str(d.find('a', attrs={'class':'a-link-normal a-text-normal'})).find('dp')
		links.append('https://www.amazon.com.br/' + str(d.find('a', attrs={'class':'a-link-normal a-text-normal'}))[index:index + 13])
		if (aux == 5):
			break
		aux += 1
	
	aux = 1
	for item in names:
		print(aux)
		print(item)
		aux += 1

	num = int(input('Insira qual numero a ser adicionado: '))

	with open('links.txt', mode = 'a') as file:
		file.write(links[num - 1] + '\n')

	r.close()
	
elif (opc == 5):
	with open('links.txt', mode = 'w') as file:
		file.write('')

elif (opc == 6):
	r = requests.get('https://www.amazon.com.br', headers=headers, proxies=proxies)
	content = r.content
	soup = BeautifulSoup(content, features="lxml")


#1.0 - basico x
#1.1 - aceitar possiveis formatos de links x
#1.2 - remover links x
#1.3 - mostrar preco x
#1.4 - pesquisar por nome x 
#1.41 - testes usando classe

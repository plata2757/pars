from bs4 import BeautifulSoup


import requests as req
import fake_useragent


user = fake_useragent.UserAgent().random
header = {'user-agent': user}


def get_page(tabak):
	url = f'https://site.com/collection/{tabak}?order=price'
	response = req.get(url,headers=header)
	#print(response.status_code)
	soup = BeautifulSoup(response.text,'html.parser')

	product_cards = soup.find_all('div',class_='product-card-inner')#.text.strip(' \n\t')
	
	find_cards = []

	for card in product_cards:
		try:
			find_cards.append({
						'title': card.find('a',class_='product-link').text.strip(' \n\t'),
						'cost': card.find('div',class_='price in-card').text.strip(' \n\t')
				})
		except:
			find_cards.append({
						'title': card.find('a',class_='product-link').text.strip(' \n\t'),
						'cost': card.find('p',class_='product_current_price').text.strip(' \n\t')
				})
	return get_all_pages(find_cards,url)


def get_all_pages(find_cards,url):
	number_page = 2
	lst = find_cards

	
	while 1:
		response = req.get(url+f'&page={number_page}',headers=header)
		number_page += 1


		soup = BeautifulSoup(response.text,'html.parser')

		notice = soup.find('div',class_='products-list is-collection row')

		if notice.text.strip(' \n\t') == 'В данном разделе пока нет товаров. Мы работаем над этим.':
			return find_cards
			break
		else:
			product_cards = soup.find_all('div',class_='product-card-inner')#.text.strip(' \n\t')
			

			for card in product_cards:
				try:
					lst.append({
								'title': card.find('a',class_='product-link').text.strip(' \n\t'),
								'cost': card.find('div',class_='price in-card').text.strip(' \n\t')
						})
				except:
					lst.append({
								'title': card.find('a',class_='product-link').text.strip(' \n\t'),
								'cost': card.find('p',class_='product_current_price').text.strip(' \n\t')
						})
	
	return lst


			




def main():
	list_tab =['tabak-1','tabak-2','tabak-3','tabak-...']
	tabaks = []

	for i in list_tab:
		tabaks.append(get_page(i))

	for item in tabaks:
		print(item)

	for c in tabaks:
		with open('ls.txt','a') as fls:
			fls.writelines('\n')
		for sl in c:
			with open('ls.txt','a') as file:
				file.writelines(sl['title']+'\n'+sl['cost']+'\n')



if __name__ == '__main__':
	main()
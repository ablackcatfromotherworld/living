from ast import main
import requests
import parsel 

class GetCategory:
    def __init__(self):
        self.url = "https://www.olhosnatv.com.br/p/blog-page.html"
        self.response = requests.get(self.url)

    def get_category(self):
        return self.response.text
    
    def get_category_list(self):
        category_list = parsel.Selector(self.get_category()).xpath('//div[@class="post-body entry-content float-container"]/p//a/@href').getall()
        return category_list

if __name__ == "__main__":
    get_category = GetCategory()
    category_list = get_category.get_category_list()
    print(category_list)

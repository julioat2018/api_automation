# from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.http import require_http_methods
from selenium import webdriver


# Create your views here.
def index(request):
    return HttpResponse("Hello, world. You're at the api index.")


@require_http_methods(["POST"])
def auto_submit(request):
    name = request.POST.get('name')
    surname = request.POST.get('surname')
    password = request.POST.get('password')
    email = request.POST.get('email')
    phone = request.POST.get('phone')
    site_id = request.POST.get('site_id')

    url = 'https://energia.tariffe-speciali.it/fv_optima_settembre2018/'
    options = webdriver.ChromeOptions()
    # options.add_argument('--headless')
    br = webdriver.Chrome(options=options, executable_path=settings.DIR_PATH + 'browser/chromedriver')
    br.set_page_load_timeout(40)

    # options = webdriver.FirefoxOptions()
    # options.add_argument('--headless')
    # browser = webdriver.Firefox(options=options, executable_path=settings.DIR_PATH + 'browser/geckodriver')

    if site_id == 'energia':
        print("energia")
        br.find_element_by_xpath('//*[@id="nome"]').send_keys(name)
        br.find_element_by_xpath('//*[@id="cognome"]').send_keys(surname)
        br.find_element_by_xpath('//*[@id="telefono"]').send_keys(phone)
        br.find_element_by_xpath('//*[@id="form-cliente"]/div/div[5]/div/input').click()
        pass
    elif site_id == 'telefonia':
        print("telefonia")
        pass

    return HttpResponse("Hello, world. You're at the api auto_submit.")



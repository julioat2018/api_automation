# from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views.decorators.http import require_http_methods
from django.conf import settings
import re

from selenium import webdriver
from selenium.common.exceptions import TimeoutException, ElementClickInterceptedException
# from seleniumwire import webdriver

import time


def index(request):
    return HttpResponse("Hello, world. You're at the api index.")


@require_http_methods(["POST"])
def auto_submit(request):
    name = request.POST.get('name', '')
    surname = request.POST.get('surname', '')
    password = request.POST.get('password', '')
    email = request.POST.get('email', '')
    phone = request.POST.get('phone', '')
    site_id = request.POST.get('site_id', '')

    is_run = False

    for port in range(2301, 2311):
        print("port ==============> ", port)
        options = webdriver.ChromeOptions()
        options.add_argument('--headless')
        proxy = '163.172.70.236:' + str(port)
        options.add_argument('--proxy-server=socks5://' + proxy)
        options.add_argument("--no-sandbox")
        br = webdriver.Chrome(options=options, executable_path=settings.BASE_DIR + settings.DIR_PATH + 'chromedriver')
        br.maximize_window()
        br.set_page_load_timeout(100)

        # options = webdriver.FirefoxOptions()
        # options.add_argument('--headless')
        # proxy = '163.172.70.236:' + str(port)
        # options.add_argument('--proxy-server=socks5://' + proxy)
        # options.add_argument("--no-sandbox")
        # br = webdriver.Firefox(options=options, executable_path=settings.BASE_DIR + settings.DIR_PATH + 'geckodriver')

        # try:
        #     br.get('https://www.rainsbrook.co.uk/cgi-bin/proxytest.pl')
        #     result = br.find_element_by_xpath("//body").text
        #     if 'Requested from:' not in result:
        #         br.close()
        #         continue
        #     print(result)
        # except Exception as e:
        #     print(e)
        #     br.close()
        #     continue

        is_run = True
        try:
            if site_id == 'energia':
                url = 'https://energia.tariffe-speciali.it/fv_optima_settembre2018/'
                br.get(url)

                br.find_element_by_xpath('//*[@id="nome"]').send_keys(name)
                br.find_element_by_xpath('//*[@id="cognome"]').send_keys(surname)
                br.find_element_by_xpath('//*[@id="telefono"]').send_keys(phone)
                time.sleep(5)
                br.find_element_by_xpath('//input[@type="submit"]').click()
                br.close()
            elif site_id == 'telefonia':
                url = 'https://telefonia.tariffe-speciali.it/diamond_fibra/conferma.php'
                br.get(url)

                br.find_element_by_xpath('//*[@id="nome"]').send_keys(name)
                br.find_element_by_xpath('//*[@id="cognome"]').send_keys(surname)
                br.find_element_by_xpath('//*[@id="telefono"]').send_keys(phone)
                # br.find_element_by_xpath('//*[@id="form-cliente"]/div/div[5]/div/input').click()
                br.close()
            else:
                return JsonResponse({'result': 'Bad request'})
        except TimeoutException as e:
            print(e)
            br.close()
            return JsonResponse({'result': 'TimeoutException'})
        except ElementClickInterceptedException as e:
            print(e)
            br.close()
            return JsonResponse({'result': 'ElementClickInterceptedException'})

        break

    if is_run:
        return JsonResponse({'result': 'Success'})
    else:
        return JsonResponse({'result': 'Proxy error'})



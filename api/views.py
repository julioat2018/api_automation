# from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views.decorators.http import require_http_methods
from django.conf import settings

# from selenium import webdriver
from seleniumwire import webdriver

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
        # options.add_argument('--proxy-server=socks5://' + proxy)
        # options.add_argument("--proxy-auto-detect")

        seleniumwire_options = {
            'proxy': {
                'http': '163.172.70.236:' + str(port),
                'https': '163.172.70.236:' + str(port)
            }
        }
        br = webdriver.Chrome(seleniumwire_options=seleniumwire_options, options=options)

        # br = webdriver.Chrome(options=options, executable_path=settings.BASE_DIR + settings.DIR_PATH + 'chromedriver')
        br.set_page_load_timeout(40)

        # options = webdriver.FirefoxOptions()
        # options.add_argument('--headless')
        # br = webdriver.Chrome(options=options, executable_path=settings.BASE_DIR + settings.DIR_PATH + 'geckodriver')

        try:
            response = br.get('https://www.rainsbrook.co.uk/cgi-bin/proxytest.pl')
            response_status = response.status_code
            print(response_status)
        except Exception as e:
            print(e)
            br.close()
            continue

        is_run = True
        try:
            if site_id == 'energia':
                url = 'https://energia.tariffe-speciali.it/fv_optima_settembre2018/'
                br.get(url)
                time.sleep(1)

                br.find_element_by_xpath('//*[@id="nome"]').send_keys(name)
                br.find_element_by_xpath('//*[@id="cognome"]').send_keys(surname)
                br.find_element_by_xpath('//*[@id="telefono"]').send_keys(phone)
                br.find_element_by_xpath('//*[@id="form-cliente"]/div/div[5]/div/input').click()
                br.close()
                time.sleep(10)
            elif site_id == 'telefonia':
                url = 'https://telefonia.tariffe-speciali.it/diamond_fibra/conferma.php'
                br.get(url)
                time.sleep(1)

                br.find_element_by_xpath('//*[@id="nome"]').send_keys(name)
                br.find_element_by_xpath('//*[@id="cognome"]').send_keys(surname)
                br.find_element_by_xpath('//*[@id="telefono"]').send_keys(phone)
                # br.find_element_by_xpath('//*[@id="form-cliente"]/div/div[5]/div/input').click()
                br.close()
                time.sleep(10)
            else:
                return JsonResponse({'result': 'Bad request'})
        except Exception as e:
            print(e)
            br.close()
            return JsonResponse({'result': 'Fail'})

        break

    if is_run:
        return JsonResponse({'result': 'Success'})
    else:
        return JsonResponse({'result': 'Proxy error'})



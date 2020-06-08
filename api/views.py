# from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views.decorators.http import require_http_methods
from django.conf import settings
import re

from selenium import webdriver
from selenium.common.exceptions import TimeoutException, ElementClickInterceptedException
# from seleniumwire import webdriver

import time
import requests


def index(request):
    return HttpResponse("Hello, world. You're at the api index.")


def check_proxy(host, ports):
    for i in range(ports[0],ports[1]):
        try:
            r = requests.get("https://www.rainsbrook.co.uk/cgi-bin/proxytest.pl",
                         proxies=dict(http="socks5://{}:{}".format(host,i),
                                      https="socks5://{}:{}".format(host,i)))
        except requests.exceptions.ConnectionError as e:
            continue
        if r.status_code == 200:
            port = str(i)
            proxy_ip= re.findall(re.compile("Requested from:.*"), r.text)[0]
            return port, proxy_ip
    return None, None


@require_http_methods(["POST"])
def auto_submit(request):
    name = request.POST.get('name', '')
    surname = request.POST.get('surname', '')
    password = request.POST.get('password', '')
    email = request.POST.get('email', '')
    phone = request.POST.get('phone', '')
    site_id = request.POST.get('site_id', '')

    is_run = False
    counter = 0
    for port in range(2301, 2311):
        print("port ==============> ", port)
        options = webdriver.ChromeOptions()
        options.add_argument('--headless')
        proxy = '163.172.70.236:' + str(port)
        options.add_argument('--proxy-server=socks5://' + proxy)
        options.add_argument("--no-sandbox")
        options.add_argument("--start-maximized")
        options.add_argument("--window-size=1920,1080")
        br = webdriver.Chrome(options=options, executable_path=settings.BASE_DIR + settings.DIR_PATH + 'chromedriver')
        # br.maximize_window()
        br.set_page_load_timeout(100)

        # options = webdriver.FirefoxOptions()
        # options.add_argument('--headless')
        # proxy = '163.172.70.236:' + str(port)
        # options.add_argument('--proxy-server=socks5://' + proxy)
        # options.add_argument("--no-sandbox")
        # br = webdriver.Firefox(options=options, executable_path=settings.BASE_DIR + settings.DIR_PATH + 'geckodriver')

        try:
            # br.get('https://www.rainsbrook.co.uk/cgi-bin/proxytest.pl')
            # result = br.find_element_by_xpath("//body").text
            # if 'Requested from:' not in result:
            #     counter += 1
            #     br.close()
            #     continue

            # try:
            #     r = requests.get("https://www.rainsbrook.co.uk/cgi-bin/proxytest.pl",
            #                      proxies=dict(http="socks5://{}:{}".format('163.172.70.236', port),
            #                                   https="socks5://{}:{}".format('163.172.70.236', port)))
            #
            #     if r.status_code == 200:
            #         proxy_ip = re.findall(re.compile("Requested from:.*"), r.text)[0]
            #         print(proxy_ip)
            #         if proxy_ip == '163.172.70.236':
            #             br.close()
            #             continue
            #     else:
            #         br.close()
            #         continue
            # except requests.exceptions.ConnectionError as e:
            #     print(e)
            #     br.close()
            #     continue
            pass
        except Exception as e:
            print(e)
            counter += 1
            br.close()
            continue

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

    if counter == 0:
        return JsonResponse({'result': 'Success'})
    elif counter == 10:
        return JsonResponse({'result': 'Proxy error'})
    else:
        return JsonResponse({'result': 'Success with timeout'})

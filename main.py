import requests
from time import sleep
from lxml.html import fromstring
import http_proxies
import socks_proxies
import keyboard
import sys

#proxy = proxies.Proxies('socks')
#print(proxy.scrape('https://www.google.com/'))

def get_num_input(minimum,maximum,question):
    user_input = input(question)
    while True:
        if user_input.isnumeric():
            number = int(user_input)
            if number >= minimum and number <= maximum:
                return number
            else:
                error = 'Your input needs to be between ' + str(minimum) + ' and ' + str(maximum) + ' (inclusive). Please try again: '
        else:
            error = 'Please input a number between ' + str(minimum) + ' and ' + str(maximum) + ' (inclusive). Please try again: '
        user_input = input(error)

def run():
    proxy_types = [
        'http',
        'https',
        'socks4'
    ]

    #output is the console output taken from proxy_types and adjusted for formatting
    output = []
    for temp in proxy_types:
        output.append(temp)

    #calculate longest length
    longest_length = 0
    for word in output:
        if len(word) > longest_length:
            longest_length = len(word)

    #add spaces on left and right
    for x in range(0,len(output)):

        left_indent = 4
        right_indent = longest_length - len(output[x]) + 4

        spaces_add_left = ''
        spaces_add_right = ''
        for i in range(0,left_indent):
            spaces_add_left = spaces_add_left + ' '
        for z in range(0,right_indent):
            spaces_add_right = spaces_add_right + ' '
        output[x] = '[' + str(x+1) + ']' + spaces_add_left + output[x] + spaces_add_right + '|'
        
        
    for option in output:
        print(option)


    proxy_type_int = get_num_input(1,len(output)+1,'Please choose a proxy type: ')
    proxy_type = proxy_types[proxy_type_int-1]



    print('')
    print('[1]   Generate Proxies    |')
    print('[2]   Delete Proxies      |')
    action_int = get_num_input(1,2,'Which would you like to do: ')
    action = ''
    if action_int == 1:
        action = 'generate'
    if action_int == 2:
        action = 'delete'

    if action == 'generate':
        times_int = get_num_input(0,9999999999999,'How Many Proxies Would You Like To Generate (enter 0 for infinite): ')
        if int(times_int) == 0:
            times_int = 99999999999999999999999999999999999999999999999999999999


        if proxy_type == 'http' or proxy_type == 'https':
            proxy = http_proxies.Http_proxies()
            # Make each request using a randomly selected proxy
            for i in range(times_int):
                try:
                    r = proxy.scrape('https://www.google.com/')
                except:
                    proxy = http_proxies.Http_proxies()
        if proxy_type == 'socks4':
            proxy = socks_proxies.Socks_proxies()
            # Make each request using a randomly selected proxy
            for i in range(times_int):
                try:
                    r = proxy.scrape('https://www.google.com/')
                except:
                    proxy = socks_proxies.Socks_proxies()
    if action == 'delete':
        try:
            f = open(proxy_type + '.txt','w')
            f.write('')
            f.close()
        except:
            print('There is no file for "' + proxy_type + '.txt"')


while keyboard.is_pressed('ctrl+q') == False:
    run()
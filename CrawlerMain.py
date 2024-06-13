import requests as rq
from bs4 import BeautifulSoup
import re
import time
import random
from fake_useragent import UserAgent
import os
from datetime import datetime
import pyfiglet
from termcolor import colored
import webbrowser # This was imported for test reasons earlier in code during develpoment. You can use this if you want or remove this line idc.

script_directory = os.path.dirname(os.path.abspath(__file__))

user_agents = UserAgent()

proxy_list_url = 'https://www.us-proxy.org/'
response = rq.get(proxy_list_url)
proxy_data = response.text

proxies = proxy_data.strip().split('\n')

title = colored(pyfiglet.figlet_format("Scam search"), color="blue")

class Main():
    print(title)
    result_tag = pyfiglet.figlet_format("RESULTS")
    
    urls = ['https://scammer.info/tag/telephone-number', 'https://scammer.info/tag/toll-free-number', 'https://scammer.info/tag/impersonators', 'https://scammer.info/tag/refund-scam', 'https://scammer.info/tag/phishing', 'https://scammer.info/tag/paypal']
    seen_numbers = set()
    seen_links = set()
    
    agent = {'User-Agent': user_agents.random}
    proxy = {'http': random.choice(proxies)}
    
    results_folder = os.path.join(script_directory, "Results")
    if not os.path.exists(results_folder):
        os.makedirs(results_folder)

    #current_date = datetime.now().strftime("%Y-%m-%d")
    FileNameIn = input("File output name? Do NOT include .txt: ")
    file_name = os.path.join(results_folder, f"{FileNameIn}.txt")
    
    start_time = time.time()
    
    ColoredOptions = colored("""
            \nOptions:
            1) Get numbers only
            2) Get all results
            """, color="yellow")
    print(ColoredOptions)
    result = input("\n> ")
    
    with open(file_name, "w", encoding="utf-8") as output_file:
        output_file.write(result_tag)
        output_file.write(f"\nFake User Agent: {agent['User-Agent']}\n")
        output_file.write(f"Proxy: {proxy['http']}\n\n")

        for url in urls:

            try:
                response = rq.get(url, headers=agent, proxies=proxy)
                response.raise_for_status()

                soup = BeautifulSoup(response.text, 'html.parser')
                target_class = "title raw-link raw-topic-link"
                target_links = soup.find_all('a', class_=target_class)
                
                if result == "1":
                    try:
                        for link in target_links:
                            link_text = link.text
                            href = link['href']

                            phone_numbers = re.findall(r'\b\d{3}[-.\s]?\d{3}[-.\s]?\d{4}\b', link_text)

                            for number in phone_numbers:
                                if number not in seen_numbers:
                                    formatted_output = f"Number: {number}, Link: {href}"
                                    output_file.write(formatted_output + "\n")
                                    seen_numbers.add(number)
                    except:
                        exit("An erorr occured, exiting.")
                elif result == "2":
                    try:
                        for link in target_links:
                            if link not in seen_links:
                                link_text = link.text
                                href = link['href']
                        
                                output_file.write(f"Result: {link_text}, link: {href}\n")
                                seen_links.add(link)
                    except:
                        exit("An error has occured. Exiting.")
                    else:
                        print("Invalid option.. exiting.")
                    
                        
            except Exception as e:
                print(f"Error accessing URL {url}: {e}")

    print("\nFinished in %s seconds. Output stored in /Results." % (time.time() - start_time))
    input("Press any key to exit...")

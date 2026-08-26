import requests
from colorama import Fore 

URL1  = "https://dahier.dynv6.net"  # Intentionally missing scheme (http:// or https://)  
URL0  = ["www.bernhard-david.de","http://bernhard-david.de","https://bernhard-david.de","dummy "]  # Correct URL with scheme

for url in URL0:
    try:
        r = requests.get(url)
        print (Fore.GREEN + "Request", url, " successful:")
        print(r.status_code)
        print (r.text)

    except:
        print (Fore.RED + "Request", url, "failed")
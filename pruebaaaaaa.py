import nmap

nm = nmap.PortScanner()
result = nm.scan('127.0.0.1', '22-443')
print(result)
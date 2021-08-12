import argparse
import os

parser = argparse.ArgumentParser(description='Basic Scanner for CTF')
parser.add_argument('host', help='directory to start')
args = parser.parse_args()
ip = args.host

PURPLE = '\033[95m'
CYAN = '\033[96m'
DARKCYAN = '\033[36m'
BLUE = '\033[94m'
GREEN = '\033[92m'
YELLOW = '\033[93m'
RED = '\033[91m'
END = '\033[0m'


def menu_decorator(color_args):
	def function_wrapper(func):
		def draw_outlines(*args):
			print_colored_line(color_args['color'])
			print_colored_string(color_args['color'], f"\t{color_args['text']}")
			print_colored_line(color_args['color'])
			func(*args)
			print_colored_line(color_args['color'])
			print()
		return draw_outlines
	return function_wrapper

def main():
	print_colored_line(GREEN)
	print_colored_string(GREEN, f"Scanning {ip}")

	nmap_scan(ip)
	gobuster_scan(ip)

# execute nmap scan
@menu_decorator({"color": YELLOW, "text": "Gobuster Scan" })
def nmap_scan(ip):
	os.system(f"nmap -A {ip}")

# execute gobuster scan
@menu_decorator({"color": CYAN, "text": "Agressiv NMAP SCAN" })
def gobuster_scan(ip):
	os.system(f"gobuster dir -u {ip} -w /usr/share/wordlists/dirb/common.txt -s '200-300' -e" )

def print_colored_line(color):
	print(color + "---------------------------------------------------------------------------------" + '\033[0m')

def print_colored_string(color, string):
	print(color + string + '\033[0m')

if __name__ == '__main__':
	main()
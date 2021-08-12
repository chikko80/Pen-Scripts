import argparse
import os

parser = argparse.ArgumentParser(description='Basic Scanner for CTF')
parser.add_argument('host', help='directory to start')
args = parser.parse_args()
ip = args.host

def main():
	print("Scanning " + ip)

	# execute nmap scan
	os.system("nmap -A " + ip)

	# execute gobuster scan
	os.system("gobuster dir -u " + ip + " -w /usr/share/wordlists/dirb/common.txt -s '200-300' -e")


if __name__ == '__main__':
	main()
#! /usr/bin/python3

import warnings
warnings.simplefilter("ignore", UserWarning)

import argparse
import os
import requests
from Wappalyzer import Wappalyzer, WebPage
import re

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
	comment_scan(ip)
	wappalyzer_scan(ip)

# nmap scan
@menu_decorator({"color": CYAN, "text": "Agressiv NMAP SCAN" })
def nmap_scan(ip):
	os.system(f"nmap -A {ip}")

# gobuster scan
@menu_decorator({"color": YELLOW, "text": "Gobuster Scan" })
def gobuster_scan(ip):
	os.system(f"gobuster dir -u {ip} -w /usr/share/wordlists/dirb/common.txt" )

# comment scan
@menu_decorator({"color": GREEN, "text": "Comments Scan" })
def comment_scan(ip):
	response = requests.get(f"http://{ip}/")
	comments = re.findall(r'(\/\*[\w\'\s\r\n\*]*\*\/)|(\/\/[\w\s\']*)|(\<![\-\-\s\w\>\/]*\>)', response.text)

	filtered = list(set([comment for tuplee in comments for comment in tuplee if comment]))
	for comment in filtered:
		print(comment)

# wappalyzer scan
@menu_decorator({"color": PURPLE, "text": "Wappalyzer Scan" })
def wappalyzer_scan(ip):
	webpage = WebPage.new_from_url(f"http://{ip}/")
	wappalyzer = Wappalyzer.latest()
	parse_wappalyzer_result(wappalyzer.analyze_with_versions_and_categories(webpage))

def parse_wappalyzer_result(result):
	print(f"{'Name':<20} {'Category':<20} {'Name':20}")
	print()
	for key,inner_dict in result.items():
		key = str(key)
		versions = str(inner_dict['versions'])
		categories = str(inner_dict['categories'])
		print(f"{key:<20} {versions:<20} {categories:20}")

def print_colored_line(color):
	print(color + "---------------------------------------------------------------------------------" + '\033[0m')

def print_colored_string(color, string):
	print(color + string + '\033[0m')

if __name__ == '__main__':
	main()
import os
# Tips for manual discovery:
# Discover more seed domains by looking up who has registered their domain with the target via reverse whois 
# Can be done manually with whoxy.com (typically look at Company Name) (medium-fidelity data)
# DOMLink does this automatically, but requires api key from WhoXY

# Discover seed/subdomains with ad analytics tracker codes. You can see which analytics codes the main target has, then see which domains share that code
# Can be discovered manually in builtwith.com > Relationship Profile
# python3 /opt/Bug-Bounty-Toolz/getrelationship.py

# Google copyright text, TOS text, privacy policy text to find potential seeds/subdomains

# Google: site:twitch.tv -www.twitch.tv -watch.twitch.tv

# s3 bucket discovery?

dir_base = '~/Documents/Bounty\ Targets/Quora/'
root_domain = 'quora.com'
dir_subdomain_raw = dir_base + 'subdomain_raw.txt'
dir_subdomain_web = dir_base + 'subdomain_web.txt'
dir_dork_wordlist = ' '
#api_key_slack = os.environ.get('SLACK_TOKEN')
api_key_shodan = ''
api_key_github = ''

# Simply concatentate the results of a given tool to the overall list of raw subdomains
def subdomain_concat_results(concat_file):
	os.system('cat ' + concat_file + ' >> ' + dir_subdomain_raw)

# Subdomain enumeration with Linked and JS discovery
# You can perform Linked Discovery manually via Burp Suite Pro
# Other tools to consider: GoSpider, Subdomainizer - Looks for subdomains by analyzing Javascript (Burp extension, uses JS to find endpoints)
def subdomain_linked_js():
	output_subscraper = dir_base + 'subscraper_results.txt'
	# os.system('hakrawler -url ' + root_domain + ' -depth 10 -subs')
	os.system('subscraper ' + root_domain + ' -o ' + output_subscraper) # lvl 1 enum (default): show all enumerated subdomains (fastest) #takeover needs pipe
	subdomain_concat_results(output_subscraper)

# Scrape domain information from all sorts of projects that expose databases of URLs or domains.
def subdomain_scraping():
	output_amass = dir_base + 'amass_results.txt'
	output_subfinder = dir_base + 'subfinder_results.txt'
	print('Scraping various sources for subdomains...')
	os.system('amass enum -d ' + root_domain + ' -o ' + output_amass + ' -timeout 60' ) # Timeout in an hour
	os.system('subfinder -d ' + root_domain  + ' -o ' + output_subfinder)
	subdomain_concat_results(output_amass)
	subdomain_concat_results(output_subfinder)

# Attempt subdomain discovery by brute forcing
# Other tools to consider: shuffleDNS, massdns
def subdomain_brute_forcing():
	os.system('amass enum -brute -d ' + root_domain + '-src') # all.txt available on Haddix's github

# Look for subdomains by dorking various sites/resources
def subdomain_dork():
	print("https://github.com/search?o=desc&q=%22officedepot.com%22+key&s=indexed&type=Code")
	# github-subdomains.py
	# shosubgo # Search Shodan
	# Discover BitBucket
	# scrape cloud ranges w/ Sam Erb

# Check for permutations of a known subdomain 
def subdomain_permutation_scanning():
	print('altnds')

# After subdomains are discovered, check to see if they're running a web service on ports 80 or 443
def subdomain_web_service_enumeration():
	print('Checking for web services on enumerated subdomains...')
	os.system('cat ' + dir_subdomain_raw + ' | httprobe >> ' + dir_subdomain_web) # httpx is a possible alternative

# After subdomains are discovered, check to see if they're running non-web services
def subdomain_port_enumeration():
	print('hello')
	#masscan -p1-p65535 -iL $ipFile --max-rate 1800 -oG $output
	#dnmasscan # wrapper for masscan which allows the use of domains as inputs
	#nmap # Feed output of dnmasscan to nmap
	# brutespray # Brute force services which require authentication. Requires -oG format as input

# Check for subdomains which have the same favicon as the root domain
def subdomain_favicon_analysis():
	print('FavFreak')

# Screenshotting
def subdomain_screenshotting():
	print('EyeWitness') # Aquatone, HTTPScreenshot are alternatives. Provide httprobe output as input

def main():
	subdomain_scraping()
	subdomain_web_service_enumeration()
	print('Done!')

if __name__ == "__main__":
    main()


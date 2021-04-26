import os
import pdb

# Tips for manual discovery:
# Discover more seed domains by looking up who has registered their domain with the target via reverse whois 
# Can be done manually with whoxy.com (typically look at Company Name) (medium-fidelity data)
# DOMLink does this automatically, but requires api key from WhoXY

# Discover seed/subdomains with ad analytics tracker codes. You can see which analytics codes the main target has, then see which domains share that code
# Can be discovered manually in builtwith.com > Relationship Profile
# python3 /opt/Bug-Bounty-Toolz/getrelationship.py

# Google copyright text, TOS text, privacy policy text to find potential seeds/subdomains

# Google: site:twitch.tv -www.twitch.tv -watch.twitch.tv

# TODO: turn dir_base into a list for multiple in-scope assets
dir_base = '~/Documents/Bounty\ Targets/BlockFi/'
root_domain = 'blockfi.com'
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
	# os.system('hakrawler -url ' + root_domain + ' -depth 10 -subs')
	print('Performing Linked and JS discovery...')
	output_subscraper = dir_base + 'subscraper_results.txt'
	output_subdomainizer = dir_base + 'subdomainizer_results.txt'
	output_subdomainizer_ext = dir_base + 'subdomainizer_results_ext.txt'
	dir_subdomainizer = '/opt/SubDomainizer/' # path to script needs to be here due to import error when relying on $PATH
	os.system('touch ' + output_subscraper)
	os.system('subscraper ' + root_domain + ' -o ' + output_subscraper) # lvl 1 enum (default): show all enumerated subdomains (fastest). Brutes by default
	# Discovers subdomains/secrets from JS files. Also finds s3 buckets, cloudfront urls, subdomain/cloud takeovers
	os.system('python3 ' + dir_subdomainizer  + 'SubDomainizer.py -u ' + root_domain  + ' -o ' + output_subdomainizer + ' >> ' + output_subdomainizer_ext)
	subdomain_concat_results(output_subscraper)
	subdomain_concat_results(output_subdomainizer)

# Scrape domain information from all sorts of projects that expose databases of URLs or domains.
def subdomain_scraping():
	print('Scraping various sources for subdomains...')
	output_amass = dir_base + 'amass_results.txt'
	output_subfinder = dir_base + 'subfinder_results.txt'
	os.system('amass enum -d ' + root_domain + ' -o ' + output_amass + ' -timeout 60' ) # Timeout in an hour
	os.system('subfinder -d ' + root_domain  + ' -o ' + output_subfinder)
	subdomain_concat_results(output_amass)
	subdomain_concat_results(output_subfinder)

# Attempt subdomain discovery by brute forcing
# Other tools to consider: shuffleDNS, massdns
def subdomain_brute_forcing():
	print('Brute forcing subdomains...')
	output_amass_brute = dir_base + 'amass_brute_results.txt'
	brute_wordlist = dir_base + '../subdomain_brute_wordlist.txt' # subdomain brute forcing wordlist will be in parent Bounty directory
	os.system('amass enum -brute -d ' + root_domain + ' -w ' + brute_wordlist + ' -o ' + output_amass_brute)

# Look for subdomains by dorking various sites/resources
def subdomain_dork():
	print("https://github.com/search?o=desc&q=%22officedepot.com%22+key&s=indexed&type=Code")
	# github-subdomains.py
	# shosubgo # Search Shodan
	# Discover BitBucket
	# scrape cloud ranges w/ Sam Erb

# Check for permutations of a known subdomain. Wordlist provided by dsngen repo
def subdomain_permutation_scanning():
	os.system('altdns -i subdomain_raw.txt -o altdns_output.txt -w ~/BugBountyAutomation/subdomain_brute_wordlist.txt -r -s results_output.txt')

# After subdomains are discovered, check to see if they're running a web service on ports 80 or 443
def subdomain_web_service_enumeration():
	print('Checking for web services on enumerated subdomains...')
	os.system('cat ' + dir_subdomain_raw + ' | httprobe >> ' + dir_subdomain_web) # httpx is a possible alternative

# After subdomains are discovered, check to see if they're running non-web services
def subdomain_port_enumeration():
	output_dnmasscan_dns = dir_base + 'dnmasscan_dns_output.log'
	output_dnmasscan_log = dir_base + 'dnmasscan_log_output.log'
	output_nmap = dir_base + 'dnmasscan_output'
	print('Banner grabbing raw domains...')
    # sudo dnmasscan subdomain_raw.txt dns.log -oG masscan_results --top-ports 1000 --rate 1000 
    # cat masscan_results | awk '{print $4}' > masscan_ips.txt
	os.system('dnmasscan ' + dir_subdomain_raw + ' ' + output_dnmasscan_dns + ' --rate=10000 -oG ' + output_dnmasscan_log) # masscan wrapper: subdomain->IPs
	# os.system('nmap -sS -iL ' + output_dnmasscan_log + ' -oA ' + output_nmap) # Feed output of dnmasscan to nmap. Should we use -sC -sV
	# brutespray # Brute force services which require authentication. Requires -oG format as input

# Check for subdomains which have the same favicon as the root domain
def subdomain_favicon_analysis():
	print('FavFreak')

# Web Page Screenshotting
def subdomain_screenshotting():
	output_aquatone = dir_base + 'aquatone_results.txt'
	print('Screenshotting web pages...')
	os.system('cat ' + dir_subdomain_web + ' | aquatone >> ' + output_aquatone) # 

#TODO: Use sort -u to sort and de-dupe results
def main():
	os.system('touch ' + dir_subdomain_raw)
	subdomain_linked_js() 
	subdomain_scraping()
	subdomain_brute_forcing()
	# subdomain_permutation_scanning() # not done yet
	subdomain_web_service_enumeration()
	subdomain_screenshotting()
	print('Done!')

if __name__ == "__main__":
    main()


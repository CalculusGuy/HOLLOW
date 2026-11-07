import argparse
import sys
try:
    from colorama import init, Fore
    init(autoreset=True)
except ImportError:
    sys.exit("Please install requirements: pip install requests colorama")

from core.fingerprint import detect_waf, attempt_bypass
from core.bypass import suggest_bypass

def main():
    parser = argparse.ArgumentParser(description="Hollow - WAF Fingerprinting & Bypass Profiler")
    parser.add_argument("-t", "--target", required=True, help="Target URL (e.g., https://example.com)")
    parser.add_argument("--evade", action="store_true", help="Automatically attempt WAF bypass headers")
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
        print(f"{Fore.GREEN}[+] No obvious WAF detected via headers.")

    if result["blocked"]:
        print(f"{Fore.RED}[!] Attack payload was BLOCKED (Status: {result['attack_status']})")
    else:
        print(f"{Fore.GREEN}[+] Attack payload passed through (Status: {result['attack_status']})")

    # --- NEW EVASION LOGIC ---
    if args.evade:
        print(f"\n{Fore.CYAN}[*] --evade flag detected. Attempting header bypasses...")
        bypasses = attempt_bypass(target, result["headers"])
        if bypasses:
            print(f"{Fore.GREEN}[+] SUCCESS! The following headers bypassed the WAF:")
            for b in bypasses:
                print(f"    {Fore.MAGENTA}->{Fore.WHITE} {b}")
        else:
            print(f"{Fore.RED}[-] No header bypasses worked on this target.")
    # -------------------------

    print(f"\n{Fore.CYAN}[*] Suggested Bypass Strategies:")
    strategies = suggest_bypass(result["waf_detected"], result["blocked"])
    for strat in strategies:
        print(f"    {Fore.MAGENTA}->{Fore.WHITE} {strat}")

if __name__ == "__main__":
    main()

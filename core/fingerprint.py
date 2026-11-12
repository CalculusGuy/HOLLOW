import requests
import json

def detect_waf(url):
    # We keep headers as a fallback, but rely on behavior now.
    waf_signatures = {
        "cloudflare": ["cloudflare", "cf-ray"],
        "akamai": ["akamai", "akamaighost"],
        "aws": ["awselb", "x-amz-cf-id"],
        "sucuri": ["x-sucuri-id", "sucuri"],
        "f5": ["big-ip", "f5"],
        "imperva": ["incapsula", "x-iinfo"]
    }

    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
    payload = "<script>alert(1)</script>' OR 1=1 --"
    target_url = f"{url}?test={payload}"

    try:
        baseline = requests.get(url, headers=headers, timeout=5)
        attack = requests.get(target_url, headers=headers, timeout=5)
        
        detected_waf = "Unknown / Generic WAF"
        blocked = False

        # 1. Behavioral Detection (Status Codes)
        if attack.status_code in [403, 406, 429]:
            blocked = True
        elif attack.status_code == 200:
            # If the attack succeeded, there might be no WAF, or it's a very bad one.
            blocked = False

        # 2. Header Detection (Refine the WAF name)
        for waf_name, signatures in waf_signatures.items():
            for sig in signatures:
                for header_key, header_val in baseline.headers.items():
                    if sig in header_key.lower() or sig in header_val.lower():
                        detected_waf = waf_name
                        break

        # 3. Body Detection (Look for specific block page strings)
        attack_body = attack.text.lower()
        if "cloudflare" in attack_body and "attention required" in attack_body:
            detected_waf = "cloudflare"
            blocked = True
        elif "access denied" in attack_body and "incapsula" in attack_body:
            detected_waf = "imperva"
            blocked = True
        elif "request blocked" in attack_body and "akamai" in attack_body:
            detected_waf = "akamai"
            blocked = True

        return {
            "waf_detected": detected_waf if blocked or detected_waf != "Unknown / Generic WAF" else None,
            "blocked": blocked,
            "baseline_status": baseline.status_code,
            "attack_status": attack.status_code,
            "headers": dict(baseline.headers)
        }
    except requests.exceptions.RequestException as e:
        return {"error": str(e)}

def find_origin_ip(domain):
    domain = domain.replace("www.", "")
    print(f"[*] Searching for subdomains via HackerTarget for root domain: {domain}...")
    
    try:
        # HackerTarget free API for host search
        url = f"https://api.hackertarget.com/hostsearch/?q={domain}"
        response = requests.get(url, timeout=10)
        
        if response.status_code == 200:
            data = response.text
            if "error" in data.lower() or "no records" in data.lower():
                print(f"[-] HackerTarget returned no records.")
                return []
                
            subdomains = set()
            for line in data.split("\n"):
                if line:
                    sub = line.split(",")[0].strip().lower()
                    if sub and "*" not in sub:
                        subdomains.add(sub)
            
            print(f"[+] Found {len(subdomains)} unique subdomains.")
            return list(subdomains)[:10] # Return the first 10
        else:
            print(f"[-] HackerTarget returned status code {response.status_code}")
    except Exception as e:
        print(f"[-] Error finding origin IPs: {e}")
        
    return []

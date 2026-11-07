import requests

def detect_waf(url):
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
        detected_waf = None

        for waf_name, signatures in waf_signatures.items():
            for sig in signatures:
                for header_key, header_val in baseline.headers.items():
                    if sig in header_key.lower() or sig in header_val.lower():
                        detected_waf = waf_name
                        break

        blocked = False
        if attack.status_code in [403, 406, 429] and baseline.status_code == 200:
            blocked = True
            if not detected_waf:
                detected_waf = "Unknown / Generic WAF"

        return {
            "waf_detected": detected_waf,
            "blocked": blocked,
            "baseline_status": baseline.status_code,
            "attack_status": attack.status_code,
            "headers": dict(baseline.headers)
        }
    except requests.exceptions.RequestException as e:
        return {"error": str(e)}

def attempt_bypass(url, baseline_headers):
    bypass_headers = [
        {"X-Forwarded-For": "127.0.0.1"},
        {"X-Originating-IP": "127.0.0.1"},
        {"X-Remote-IP": "127.0.0.1"},
        {"X-Client-IP": "127.0.0.1"},
        {"X-Host": "127.0.0.1"},
        {"X-Forwarded-Host": "127.0.0.1"}
    ]
    
    payload = "<script>alert(1)</script>' OR 1=1 --"
    target_url = f"{url}?test={payload}"
    
    successful_bypasses = []
    
    for header in bypass_headers:
        # Merge default headers with the bypass header
        headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
        headers.update(header)
        
        try:
            response = requests.get(target_url, headers=headers, timeout=5)
            # If the status is 200, the bypass worked
            if response.status_code == 200:
                successful_bypasses.append(list(header.keys())[0])
        except requests.exceptions.RequestException:
            pass
            
    return successful_bypasses

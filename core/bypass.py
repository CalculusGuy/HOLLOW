def suggest_bypass(waf_name, blocked):
    if not blocked and not waf_name:
        return ["[+] No WAF detected or payload was not blocked. Try standard injection."]

    strategies = []
    
    if waf_name == "cloudflare":
        strategies.append("Cloudflare detected: Try finding the origin IP via DNS history (SecurityTrails/Censys).")
        strategies.append("Look for SSRF to bypass the WAF internally.")
        strategies.append("Try case-switching or encoding payloads (e.g., %00, unicode).")
        
    elif waf_name == "aws":
        strategies.append("AWS WAF detected: Try changing payload size, or use chunked transfer encoding.")
        
    elif waf_name == "imperva":
        strategies.append("Imperva detected: Try using inline comments (/**/) in SQLi payloads.")
        strategies.append("Check if the WAF blocks based on specific parameter names (e.g., 'union').")
        
    elif blocked:
        strategies.append(f"{waf_name} detected: Payload triggered a block. Try obfuscation (Hex, URL encoding, Base64).")
        strategies.append("Try using alternative HTTP methods (POST instead of GET).")

    if not strategies:
        strategies.append("WAF detected but no specific bypass known. Fuzz the payload encoding.")
        
    return strategies

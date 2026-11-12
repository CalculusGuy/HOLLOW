import urllib.parse

def suggest_bypass(waf_name, blocked):
    if not blocked and not waf_name:
        return ["[+] No WAF detected or payload was not blocked. Try standard injection."]

    strategies = []
    
    if waf_name == "cloudflare":
        strategies.append("Cloudflare detected: Try finding the origin IP via DNS history (SecurityTrails/Censys).")
        strategies.append("Look for SSRF to bypass the WAF internally.")
        
    elif waf_name == "aws":
        strategies.append("AWS WAF detected: Try changing payload size, or use chunked transfer encoding.")
        
    elif waf_name == "imperva":
        strategies.append("Imperva detected: Try using inline comments (/**/) in SQLi payloads.")
        
    if blocked:
        strategies.append("Payload triggered a block. Hollow will now attempt automated mutations.")
        
    if not strategies:
        strategies.append("WAF detected. Attempting generic obfuscation bypasses.")
        
    return strategies

def generate_mutations(payload):
    """Generates different mutations of the payload to test bypasses."""
    mutations = {}
    
    # 1. URL Encoding
    mutations["URL Encoded"] = urllib.parse.quote(payload)
    
    # 2. Hex Encoding
    mutations["Hex Encoded"] = "".join([f"\\x{ord(c):02x}" for c in payload])
    
    # 3. Case Switching (for HTML tags)
    mutations["Case Switched"] = "".join([c.upper() if i % 2 == 0 else c.lower() for i, c in enumerate(payload)])
    
    # 4. Inline Comments (Breaks SQLi signatures)
    mutations["Inline Comments"] = payload.replace(" ", "/**/")
    
    return mutations

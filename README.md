 <div align="center">

# ⚔️ HOLLOW v2

### WAF Fingerprinting & Bypass Profiler

**Red Team Reconnaissance · Behavioral Fingerprinting · Evasion Intelligence**

[![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![Red Teaming](https://img.shields.io/badge/Red-Teaming-DC2626?style=for-the-badge)](https://github.com/CalculusGuy/Hollow)
[![License](https://img.shields.io/badge/License-MIT-F59E0B?style=for-the-badge)](LICENSE)

**Created by [Nilanjan Chowdhury](https://github.com/CalculusGuy)**

</div>

---

## 🎯 What is HOLLOW?

**HOLLOW** is a lightweight, Python-based Red Team reconnaissance tool designed to identify Web Application Firewalls (WAFs) protecting web applications and evaluate their responses to controlled attack simulations.

Instead of blindly firing exploits, HOLLOW maps the defense first.

It sends baseline requests followed by controlled test payloads to analyze blocking behavior, fingerprint WAFs through HTTP headers and response bodies, and generate tailored evasion intelligence.

**The objective is simple: Understand the defense before testing the attack surface.**

---

## 🚀 Features

- **Behavioral WAF Fingerprinting:** Identifies major WAFs (Cloudflare, AWS WAF, Akamai, Sucuri, F5, Imperva) by analyzing HTTP headers and actual block pages.
- **Block Detection:** Sends controlled XSS and SQLi payloads to analyze HTTP responses (403/406) and identify filtering behavior.
- **Payload Mutator (`--mutate`):** Generates and tests payload variations when the original payload is blocked, including URL encoding, hexadecimal encoding, case switching, and inline comments.
- **Origin IP Hunter:** When Cloudflare is detected, queries the HackerTarget API for subdomain intelligence to help identify potentially exposed origin infrastructure.
- **Evasion Testing (`--evade`):** Tests alternative HTTP request headers (e.g., `X-Forwarded-For`) to evaluate header-based trust configurations.
- **Colorized CLI:** Clean, readable terminal output for real-time reconnaissance.

---

## 🏗️ Architecture

```text
HOLLOW/
│
├── main.py                 # CLI entry point
├── requirements.txt        # Project dependencies
│
└── core/
    ├── __init__.py
    ├── fingerprint.py      # WAF detection, behavioral analysis & API recon
    └── bypass.py            # Evasion testing, mutations & strategy recommendations
```

---

## ⚙️ Installation

### 1. Clone the repository

```bash
git clone https://github.com/CalculusGuy/Hollow.git
cd Hollow
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

---

## 💻 Usage

### 1. Basic WAF Fingerprinting

```bash
python main.py -t https://example.com
```

### 2. WAF Fingerprinting + Payload Mutations

```bash
python main.py -t https://example.com --mutate
```

### 3. Evasion Testing

```bash
python main.py -t https://example.com --evade
```

### 4. Combined Testing

```bash
python main.py -t https://example.com --mutate --evade
```

---

## 📊 Example Output

```text
[*] Scanning target: https://www.digitalocean.com

[*] Probing for WAF signatures...

[+] WAF Detected: CLOUDFLARE

[!] Attack payload was BLOCKED (Status: 403)

[*] --mutate flag detected. Generating payload mutations...

    [-] URL Encoded failed. Status: 403
    [-] Hex Encoded failed. Status: 403
    [-] Case Switched failed. Status: 403
    [-] Inline Comments failed. Status: 403

[*] Cloudflare detected. Attempting to find Origin IPs...

[*] Searching for subdomains via HackerTarget API...

[+] Found 50 unique subdomains.

    [+] Potential bypass subdomains found:
        -> api.digitalocean.com
        -> clienteng-nyc3.digitalocean.com
        -> accounts.mcp.digitalocean.com
        ...

[*] Suggested Bypass Strategies:

    -> Cloudflare detected: Try finding the origin IP via DNS history.
    -> Payload triggered a block. Hollow attempted automated mutations.
```

---

## 🧠 Supported WAFs & Intelligence

| WAF | Detection Indicators | Testing Intelligence |
|:---|:---|:---|
| **Cloudflare** | `cf-ray`, `cloudflare` headers, "Attention Required" block page | Origin infrastructure discovery, encoding analysis |
| **AWS WAF** | AWS-related headers and response signatures | Request normalization analysis, chunked encoding |
| **F5 BIG-IP** | `big-ip`, `f5` headers | Encoding and method-handling analysis |
| **Imperva** | `incapsula`, `x-iinfo` headers, "Access Denied" block page | SQLi filtering and inline comment normalization |
| **Akamai** | `akamai`, `akamaighost` headers, "Request Blocked" page | Obfuscation and case normalization |
| **Sucuri** | `x-sucuri-id`, `sucuri` headers | Header handling and filtering analysis |

> **Note:** WAF identification is heuristic-based. Header signatures, block pages, and response behavior are indicators, not definitive proof of a particular WAF.

---

## ⚠️ Responsible Use

HOLLOW is developed for **authorized security testing and educational research only.**

Use this tool exclusively against:

- Systems you own.
- Systems for which you have explicit written authorization.
- Bug bounty targets, strictly within their published scope and rules.

Do not use HOLLOW to attack unauthorized third-party systems or violate applicable laws.

The author assumes no responsibility for misuse.

---

## 👨‍💻 Author

**Nilanjan Chowdhury**

*Offensive Security Researcher · AI/LLM Red Teaming*

- **GitHub:** [@CalculusGuy](https://github.com/CalculusGuy)
- **LinkedIn:** [Nilanjan Chowdhury](https://linkedin.com/in/nilanjan-chowdhury-a36787359/)
- **Medium:** [@nilanjan.calculus](https://medium.com/@nilanjan.calculus)

---

## 📜 License

This project is licensed under the **MIT License**. See the [LICENSE](LICENSE) file for details.

---

<div align="center">

### ⚔️ HOLLOW v2

**Map the defense. Bypass the wall.**

⭐ If HOLLOW is useful, consider starring the repository.

</div>

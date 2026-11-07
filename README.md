 <div align="center">

# ⚔️ HOLLOW

### WAF Fingerprinting & Bypass Profiler

**Red Team Reconnaissance · WAF Detection · Evasion Intelligence**

[![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![Red Teaming](https://img.shields.io/badge/Red-Teaming-DC2626?style=for-the-badge)](https://github.com/CalculusGuy/Hollow)
[![License](https://img.shields.io/badge/License-MIT-F59E0B?style=for-the-badge)](LICENSE)

**Created by [Nilanjan Chowdhury](https://github.com/CalculusGuy)**

</div>

---

## 🎯 What is HOLLOW?

**HOLLOW** is a lightweight, Python-based Red Team reconnaissance tool designed to identify Web Application Firewalls (WAFs) protecting web applications and evaluate their response to controlled attack simulations.

Instead of blindly firing exploits, HOLLOW maps the defense first.

It sends baseline requests followed by controlled malicious test payloads to identify potential WAF presence, analyze blocking behavior, and generate tailored evasion intelligence based on the detected technology.

The objective is simple: **Understand the defense before testing the attack surface.**

---

## 🚀 Features

- **WAF Fingerprinting:** Identifies major WAF technologies, including Cloudflare, AWS WAF, Akamai, Sucuri, F5, and Imperva using HTTP headers and response signatures.
- **Block Detection:** Uses controlled XSS and SQLi test payloads to analyze HTTP responses and identify potential filtering behavior.
- **Evasion Testing (`--evade`):** Tests alternative HTTP request headers, including `X-Forwarded-For` and `X-Originating-IP`, to evaluate header-based trust configurations.
- **Bypass Intelligence:** Generates WAF-specific testing recommendations based on fingerprinting results.
- **Colorized CLI:** Provides clean, readable terminal output for real-time reconnaissance.

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
    ├── fingerprint.py      # WAF detection and response analysis
    └── bypass.py           # Evasion testing and strategy recommendations
```

---

## ⚙️ Installation

**1. Clone the repository**

```bash
git clone https://github.com/CalculusGuy/Hollow.git
cd Hollow
```

**2. Install dependencies**

```bash
pip install -r requirements.txt
```

---

## 💻 Usage

### 1. Basic WAF Fingerprinting

```bash
python main.py -t https://example.com
```

### 2. WAF Fingerprinting + Evasion Testing

```bash
python main.py -t https://example.com --evade
```

---

## 📊 Example Output

```text
[*] Scanning target: https://example.com

[*] Probing for WAF signatures...

[+] WAF Detected: CLOUDFLARE

[!] Attack payload was BLOCKED (Status: 403)

[*] --evade flag detected.
[*] Attempting header-based evasion tests...

[-] No tested header variations bypassed the filtering.

[*] Suggested Testing Strategies:

    -> Investigate origin exposure and DNS history.
    -> Evaluate internal trust boundaries and SSRF exposure.
    -> Test encoding and normalization inconsistencies.
    -> Review WAF rules and application-level validation.
```

---

## 🧠 Supported WAFs

| WAF | Detection Indicators | Testing Intelligence |
|:---|:---|:---|
| **Cloudflare** | `cf-ray`, `cloudflare` headers | Origin exposure, encoding analysis |
| **AWS WAF** | AWS-related headers and response signatures | Request normalization analysis |
| **F5 BIG-IP** | `big-ip`, `f5` headers | Encoding and method-handling analysis |
| **Imperva** | `incapsula`, `x-iinfo` headers | SQLi filtering and normalization |
| **Akamai** | `akamai`, `akamaighost` headers | Obfuscation and case normalization |
| **Sucuri** | `x-sucuri-id`, `sucuri` headers | Header handling and filtering analysis |

*Note: WAF identification is heuristic-based. Header signatures and response behavior are indicators, not definitive proof of a particular WAF.*

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

Offensive Security Researcher · AI/LLM Red Teaming

- **GitHub:** [@CalculusGuy](https://github.com/CalculusGuy)
- **LinkedIn:** [Nilanjan Chowdhury](https://linkedin.com/in/nilanjan-chowdhury-a36787359/)
- **Medium:** [@nilanjan.calculus](https://medium.com/@nilanjan.calculus)

---

## 📜 License

This project is licensed under the **MIT License**. See the [LICENSE](LICENSE) file for details.

---

<div align="center">

### ⚔️ HOLLOW

**Map the defense. Bypass the wall.**

⭐ If HOLLOW is useful, consider starring the repository.

</div>

# Halal Browser

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Security: Privacy-First](https://img.shields.io/badge/Security-Privacy--Hardened-emerald.svg)]()
[![Platform: Desktop](https://img.shields.io/badge/Platform-Cross--Platform-important.svg)]()

> **Halal Browser** is a privacy-focused desktop web browser engineered to provide a clean, fast, and security-hardened browsing experience with built-in ad-blocking, anti-tracking, DNS-over-HTTPS, and customizable content filters.

---

## 🛡 Security & Privacy Core

- **Tracker & Telemetry Shield**: Blocks third-party telemetry, behavioral tracking scripts, and fingerprinters at the network layer.
- **DNS-over-HTTPS (DoH)**: Built-in encrypted DNS routing to prevent ISP-level DNS snooping and tampering.
- **Zero-Log Architecture**: No remote history syncing or telemetry transmission. All browser configuration data remains strictly local.
- **Customizable Filter Engine**: Supports custom blocklists and rules compatible with standard AdBlock / uBlock formats.

---

## 🚀 Building & Running from Source

### Prerequisites
- Node.js 18+ / Rust Toolchain (depending on active runtime build target)
- Git

### Installation & Launch
```bash
# Clone the repository
git clone https://github.com/ahmedfawzyjr/halal-browser.git
cd halal-browser

# Install dependencies
npm install

# Run in development mode
npm run dev
```

---

## 📄 License

Licensed under the [MIT License](LICENSE).

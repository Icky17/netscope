# NetScope

A powerful network scanner and port analyzer built with Python.

![Feature Image](.github/assets/example.png)

## 🌟 Key Features

- Network scanning using CIDR notation
- Parallel port scanning for improved speed
- Common service detection
- Automatic report generation in JSON format
- Configurable port scan ranges
- User-friendly command-line interface

## 📋 Prerequisites

- Python 3.8 or higher
- pip (Python Package Installer)

## ⚙️ Installation

1. Clone the repository:
```bash
git clone https://github.com/icky17/netscope.git
cd netscope
```

2. Install required packages:
```bash
pip install -r requirements.txt
```

## 🚀 Usage

### Basic Scan
Perform a basic scan of your local network:
```bash
python netscope.py 192.168.1.0/24
```

### Advanced Options
Scan all ports (1-1024) and save results to a custom file:
```bash
python netscope.py 192.168.1.0/24 --all-ports -o custom_results.json
```

### Parameters
- `target`: Target network in CIDR notation (e.g., 192.168.1.0/24)
- `--output, -o`: Output file for results (JSON format)
- `--all-ports, -a`: Scan all ports (1-1024) instead of just common ports

## 📊 Output Format

Results are saved in JSON format and include:
- Host IP address
- Open ports
- Detected services
- Scan timestamp

## ⚠️ Security Notes

- Only use this tool on networks you have permission to scan
- Comply with local laws and regulations regarding network scanning
- The tool might be flagged by security systems as potentially suspicious

## 📝 License

This project is licensed under the MIT License - see [LICENSE](LICENSE) for details.

## 🤝 Contributing

Contributions are welcome! Please read [CONTRIBUTING.md](CONTRIBUTING.md) for details on the process.

## 👨‍💻 Author

👤 **Jairo Morales**

- Github: [@Icky17](https://github.com/Icky17)
- Linkedin: [@Jairo Morales Pérez](https://www.linkedin.com/in/jairo-morales-p%C3%A9rez-67949b216/)
- Website: https://jairomorales.ch/
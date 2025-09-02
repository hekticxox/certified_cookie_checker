# 🍪 Certified Cookie Checker

A production-ready, modular cookie verification system with intelligent error handling and self-healing capabilities.

## 📁 Repository Structure

```
├── src/                    # Production source code
│   ├── verified_cookie_checker_hooked.py  # Main verification engine
│   ├── run_hooked_system.py              # System orchestrator  
│   ├── patch_system.py                   # Modular patch loader
│   ├── patches/                          # Extensible patches directory
│   ├── setup_production.py               # Environment setup
│   ├── system_monitor.py                 # Runtime monitoring
│   └── deploy_production.py              # Deployment automation
├── personal/               # Personal working files (not pushed to git)
│   ├── cookies/           # Your cookie files
│   ├── logs/             # Generated logs and reports
│   ├── screenshots/      # Screenshot outputs
│   └── state/           # Runtime state files
├── docs/                  # Documentation
│   └── README_HOOKED_SYSTEM.md           # Detailed system documentation
├── examples/              # Usage examples and templates
│   ├── sample_cookies.txt                # Cookie format example
│   └── config_example.py                 # Configuration template
├── requirements.txt       # Python dependencies
├── setup.py              # Package setup
└── deploy.bat            # Windows deployment script
```

## 🚀 Quick Start

### 1. Install Dependencies
```bash
pip install -r requirements.txt
python src/setup_production.py
```

### 2. Add Your Cookies
```bash
# Copy your cookie files to personal/cookies/
cp your_cookies.txt personal/cookies/

# Or use the sample format
cp examples/sample_cookies.txt personal/cookies/my_cookies.txt
```

### 3. Run Verification
```bash
python src/run_hooked_system.py --cookies personal/cookies/my_cookies.txt --headless
```

## 🛠️ Features

- **🔧 Modular Architecture**: Extensible patch system for custom behaviors
- **🎯 Smart Error Handling**: Auto-repair and intelligent retry mechanisms  
- **📊 Comprehensive Logging**: Detailed reports and progress tracking
- **🔒 Privacy First**: Personal files stay in `personal/` (never pushed to git)
- **⚡ Performance Optimized**: Aggressive timeouts and resource management
- **📸 Visual Debugging**: Screenshot capture for failed verifications
- **🚨 Self-Healing**: Automatic recovery from common browser issues

## 📖 Documentation

- [Detailed System Guide](docs/README_HOOKED_SYSTEM.md) - Complete feature documentation
- [Examples](examples/) - Sample configurations and cookie formats
- [Source Code](src/) - Production-ready verification engine

## 🔐 Privacy & Security

- All personal data stays in `personal/` directory
- Cookie files, logs, and screenshots are never pushed to git
- Clean separation between production code and working files
- Example files provided for safe testing

## 🤝 Contributing

1. Production code goes in `src/`
2. Personal files stay in `personal/` 
3. Documentation in `docs/`
4. Examples and templates in `examples/`

## 📄 License

This project is ready for production use and beta testing.

# Revit AI Assistant - pyRevit Extension

A powerful pyRevit extension that integrates AI assistance directly into Revit 2024+. Get instant help with the Revit API, generate Python scripts, and execute code without leaving Revit.

## ✨ Features

- 🤖 **AI-Powered Code Generation** - Generate working Revit API scripts using Claude or Gemini
- 📚 **Comprehensive API Documentation** - Built-in Revit API documentation lookup
- ⚡ **Direct Code Execution** - Run generated scripts directly in Revit
- 🔄 **Dual AI Support** - Choose between Claude 3.5 Sonnet or Gemini Pro
- 🎯 **Smart Context Matching** - Automatically finds relevant documentation for your queries
- 🛡️ **Safe Execution** - Automatic transaction handling and error management

## 🚀 Quick Start

### Prerequisites
- **Revit 2024 or newer**
- **pyRevit 4.8+** ([Download here](https://github.com/eirannejad/pyRevit/releases))
- **API Key** (Claude or Gemini)

### Installation

1. **Download the Extension**
   ```bash
   # Option 1: Direct download
   # Download ZIP from GitHub and extract
   
   # Option 2: Git clone
   git clone https://github.com/YOUR_USERNAME/rvt-function-call.git
   ```

2. **Install pyRevit** (if not already installed)
   - Download from [pyRevit Releases](https://github.com/eirannejad/pyRevit/releases)
   - Run installer as Administrator
   - Restart Revit

3. **Add Extension to pyRevit**
   - Open Revit
   - Go to **pyRevit** tab → **pyRevit** button → **Settings**
   - In **Custom Extension Directories**, click **Add Folder**
   - Select the folder containing `RvtFunctionCall.extension`
   - Click **Save Settings** and reload pyRevit

4. **Configure API Keys**
   - Navigate to: `RvtFunctionCall.extension/`
   - Copy `config_template.json` to `config.json`
   - Edit `config.json` with your API keys:
   ```json
   {
     "default_model": "claude",
     "claude_api_key": "sk-ant-api03-YOUR-ACTUAL-KEY-HERE",
     "gemini_api_key": "AIzaSy-YOUR-ACTUAL-KEY-HERE",
     "max_docs": 5
   }
   ```

5. **Test the Installation**
   - Look for **RvtFunctionCall** tab in Revit
   - Click **Assistant** button
   - Try: "Create a simple wall script"

## 🎯 Usage Examples

### Basic Queries
- "How do I get all walls in the current document?"
- "What are the properties of the Document class?"
- "Show me how to create a new level"

### Script Generation
- "Write a script to create a 10-foot wall"
- "Generate code to rename all sheets with a prefix"
- "Create a script to export all views to PDF"

### API Help
- "How do I use FilteredElementCollector?"
- "What parameters does a Wall element have?"
- "How do I start a transaction in Revit?"

## 🔧 Configuration

### API Keys

#### Claude API Key
1. Visit [Anthropic Console](https://console.anthropic.com/)
2. Create account or sign in
3. Generate API key
4. Add to `config.json`

#### Gemini API Key
1. Visit [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Create API key
3. Add to `config.json`

### Settings
- `default_model`: "claude" or "gemini"
- `max_docs`: Number of documentation sections to include (1-10)

## 🏗️ Project Structure

```
RvtFunctionCall.extension/
├── RvtFunctionCall.tab/           # Revit ribbon tab
│   ├── AI.panel/                  # AI tools panel
│   │   ├── Assistant.pushbutton/  # Main assistant button
│   │   │   ├── script.py          # Main script
│   │   │   └── ui.xaml            # User interface
│   │   └── bundle.yaml            # Panel config
│   └── bundle.yaml                # Tab config
├── lib/                           # Core libraries
│   ├── utils/                     # Utility modules
│   │   ├── ai_client.py           # AI API integration
│   │   ├── config.py              # Configuration management
│   │   └── docs_lookup.py         # Documentation lookup
│   └── revit_api_docs/            # API documentation
│       ├── Document.txt           # Document class docs
│       ├── Element.txt            # Element class docs
│       └── [30+ other classes]    # Complete API coverage
├── config_template.json           # Configuration template
└── README.md                      # This file
```

## 🔍 Troubleshooting

### Extension Not Appearing
- ✅ Verify pyRevit is installed and working
- ✅ Check extension path in pyRevit settings
- ✅ Reload pyRevit or restart Revit

### API Errors
- ✅ Verify API keys are correct in `config.json`
- ✅ Check internet connection
- ✅ Ensure API account has sufficient credits

### Code Execution Errors
- ✅ Make sure you have an active Revit document
- ✅ Check generated code for syntax errors
- ✅ Review the confirmation dialog before execution

### "Invalid Syntax" Errors
- ✅ Check for `**revit**` vs `__revit__` formatting
- ✅ Manually edit code if needed before execution

## 🛠️ Development

### Adding New Documentation
1. Add `.txt` files to `lib/revit_api_docs/`
2. Follow the existing format with properties and methods
3. Restart the extension

### Customizing AI Prompts
- Edit prompts in `lib/utils/ai_client.py`
- Modify the documentation lookup in `lib/utils/docs_lookup.py`

## 📋 System Requirements

- **Operating System**: Windows 10/11
- **Revit Version**: 2024, 2025
- **pyRevit Version**: 4.8 or newer
- **Python**: 3.7+ (included with pyRevit)
- **Internet**: Required for AI API calls

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🆘 Support

- **Issues**: [GitHub Issues](https://github.com/YOUR_USERNAME/rvt-function-call/issues)  
- **Discussions**: [GitHub Discussions](https://github.com/YOUR_USERNAME/rvt-function-call/discussions)
- **Documentation**: Check the `lib/revit_api_docs/` folder for API reference

## 🔄 Updates

### Latest Version Features
- ✅ Claude 3.5 Sonnet (Latest) support
- ✅ Improved code extraction and validation
- ✅ Better error handling and user feedback
- ✅ Automatic transaction management
- ✅ Code preview before execution

---

**Made with ❤️ for the Revit community**

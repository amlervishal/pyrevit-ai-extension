# Revit AI Assistant - pyRevit Extension

🤖 **Get AI-powered help with Revit API coding directly inside Revit!**

This extension adds an AI assistant to your Revit that can answer questions about the Revit API and generate Python scripts for you. Just ask in plain English and get working code!

## ✨ What It Does

- **Ask Questions**: "How do I select all walls on Level 1?"
- **Generate Scripts**: "Create a script to copy furniture to multiple floors"
- **Get Code Examples**: Uses 18+ proven examples to create better code
- **Run Code Instantly**: Execute generated scripts directly in Revit

## 🔧 Installation

### Step 1: Install pyRevit
1. **Download pyRevit** from: https://github.com/eirannejad/pyRevit/releases
2. **Run the installer** as Administrator
3. **Restart Revit** after installation

### Step 2: Add This Extension
1. **Download this extension** (green "Code" button → "Download ZIP")
2. **Extract the ZIP file** to a folder on your computer
3. **Open Revit** and go to the **pyRevit** tab
4. **Click the pyRevit button** → **Settings**
5. **Find "Custom Extension Directories"**
6. **Click "Add Folder"** and select the folder containing `RvtFunctionCall.extension`
7. **Click "Save Settings"** and **reload pyRevit**

### Step 3: Get an AI API Key
You need either Claude or Gemini (or both):

#### For Claude (Recommended):
1. Go to: https://console.anthropic.com/
2. Create an account or sign in
3. Generate an API key
4. Copy the key (starts with `sk-ant-api03-...`)

#### For Gemini:
1. Go to: https://makersuite.google.com/app/apikey
2. Create an API key
3. Copy the key (starts with `AIzaSy...`)

### Step 4: Configure the Extension
1. **Navigate to** the extension folder: `RvtFunctionCall.extension/`
2. **Copy** `config_template.json` and **rename it** to `config.json`
3. **Open** `config.json` in any text editor
4. **Paste your API key** in the appropriate field:
   ```json
   {
     "default_model": "claude",
     "claude_api_key": "sk-ant-api03-YOUR-ACTUAL-KEY-HERE",
     "gemini_api_key": "AIzaSy-YOUR-ACTUAL-KEY-HERE",
     "max_docs": 5
   }
   ```
5. **Save the file**

## 🚀 How to Use

1. **Open Revit** with a project
2. **Look for the "RvtFunctionCall" tab** in your ribbon
3. **Click "Assistant"** to open the AI helper
4. **Type your question** or request, like:
   - "Select all doors on Level 1"
   - "Copy selected furniture to Level 2"
   - "Create a 10-foot tall wall"
   - "Update all room numbers"
5. **Click "Ask"** to get your answer
6. **Click "Execute"** to run the generated code in Revit

## 💡 Example Questions to Try

- "How do I get all walls in the document?"
- "Select all chairs on the ground floor"
- "Move selected elements 5 feet to the right"
- "Copy furniture to multiple levels"
- "Create dimensions between selected walls"
- "Update parameter values for doors"
- "Import a CAD file with options"
- "Analyze areas in the project and export to JSON"
- "Calculate room areas by level"

## ⚠️ Important Notes

- **Keep your API key safe** - don't share it with others
- **The extension needs internet** to contact the AI services
- **Always review generated code** before running it
- **Start with simple requests** to get familiar with the system
- **Run Revit as Administrator** if you get SSL certificate errors
- **Windows 10/11 recommended** for best SSL compatibility

## 🆘 Troubleshooting

### Extension doesn't appear in Revit:
- Make sure pyRevit is properly installed and loaded
- Check that the extension folder path is correct in pyRevit settings
- Try reloading pyRevit or restarting Revit

### "API key not set" error:
- Make sure you created `config.json` (not `config_template.json`)
- Check that your API key is correctly pasted
- Ensure no extra spaces in the API key

### "No internet connection" errors:
- Check your internet connection
- Verify your API key is valid and has credits
- Try the other AI model (Claude vs Gemini)
- **Run Revit as Administrator** if you get SSL/certificate errors
- **Windows firewall** might be blocking the connection

### Code execution errors:
- Make sure you have an active Revit document open
- Review the generated code for any obvious issues
- Try simpler requests first to test the system
- **Some AI-generated examples may need manual fixes** - report issues on GitHub

## 🔗 Helpful Links

- **pyRevit Download**: https://github.com/eirannejad/pyRevit/releases
- **Claude API**: https://console.anthropic.com/
- **Gemini API**: https://makersuite.google.com/app/apikey
- **pyRevit Documentation**: https://pyrevit.readthedocs.io/

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

**Made for the Revit community** ❤️

*Need help? Create an issue on GitHub or check the troubleshooting section above.*

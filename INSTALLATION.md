# Revit AI Assistant Installation Guide

## 📥 Download & Installation

### Method 1: Direct GitHub Download (Recommended)

1. **Download the Extension**
   - Go to: https://github.com/YOUR_USERNAME/rvt-function-call
   - Click the green **"Code"** button
   - Select **"Download ZIP"**
   - Extract the ZIP file to: `C:\RevitExtensions\` (or any preferred folder)

2. **Install pyRevit** (if not already installed)
   - Download from: https://github.com/eirannejad/pyRevit/releases
   - Run `pyRevit_X.X.XX.XXXXX_signed.exe` as Administrator
   - Restart Revit after installation

3. **Add Extension to pyRevit**
   - Open Revit 2024/2025
   - Go to **pyRevit** tab in the ribbon
   - Click **pyRevit** button (leftmost) → **Settings**
   - In **Custom Extension Directories** section:
     - Click **Add Folder**
     - Navigate to your extracted folder
     - Select the folder that contains `RvtFunctionCall.extension`
     - Click **OK**
   - Click **Save Settings**
   - Click **Reload pyRevit**

4. **Configure API Keys**
   - Navigate to: `[Your Path]\RvtFunctionCall.extension\`
   - **Copy** `config_template.json` → **Rename to** `config.json`
   - **Edit** `config.json` with a text editor:
   ```json
   {
     "default_model": "claude",
     "claude_api_key": "sk-ant-api03-[YOUR-ACTUAL-CLAUDE-KEY]",
     "gemini_api_key": "AIzaSy[YOUR-ACTUAL-GEMINI-KEY]",
     "max_docs": 5
   }
   ```
   - **Save** the file

5. **Test Installation**
   - Look for **RvtFunctionCall** tab in Revit ribbon
   - Click **Assistant** button
   - Test with: "How do I get all walls in the document?"

### Method 2: Git Clone (For Developers)

```bash
# Clone the repository
git clone https://github.com/YOUR_USERNAME/rvt-function-call.git

# Navigate to the directory
cd rvt-function-call

# Follow steps 2-5 from Method 1
```

## 🔑 Getting API Keys

### Claude API Key (Anthropic)
1. Visit: https://console.anthropic.com/
2. Create account or sign in
3. Go to **API Keys** section
4. Click **Create Key**
5. Copy the key (starts with `sk-ant-api03-`)
6. Paste into `config.json`

### Gemini API Key (Google)
1. Visit: https://makersuite.google.com/app/apikey
2. Sign in with Google account
3. Click **Create API Key**
4. Copy the key (starts with `AIzaSy`)
5. Paste into `config.json`

## ✅ Verification Checklist

- [ ] pyRevit 4.8+ installed
- [ ] RvtFunctionCall tab appears in Revit
- [ ] Assistant button is visible
- [ ] config.json file created with valid API keys
- [ ] Test query returns a response
- [ ] Code execution works (try simple scripts first)

## 🚨 Common Issues & Solutions

### "Extension not appearing"
- ✅ Check pyRevit installation
- ✅ Verify extension folder path in pyRevit settings
- ✅ Reload pyRevit or restart Revit

### "Error executing script: invalid syntax"
- ✅ Check for `**revit**` in code - should be `__revit__`
- ✅ Manually edit the generated code if needed
- ✅ Use the code preview dialog

### "API key not set"
- ✅ Ensure `config.json` exists (not `config_template.json`)
- ✅ Check API key format and validity
- ✅ Verify no extra spaces in the config file

### "Out of memory" icon error
- ✅ Delete `icon.png` file from the button folder
- ✅ pyRevit will use text instead of icon

## 🔄 Updates

To update the extension:
1. Download the latest version from GitHub
2. Replace the old `RvtFunctionCall.extension` folder
3. Keep your existing `config.json` file
4. Reload pyRevit

## 📞 Support

If you encounter issues:
1. Check this installation guide
2. Review the main README.md
3. Create an issue on GitHub with:
   - Revit version
   - pyRevit version
   - Error messages (if any)
   - Steps you followed

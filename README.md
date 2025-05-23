# Revit Function Call AI Assistant

A pyRevit extension that provides AI-assisted Python code generation and Revit API help through function calls to Claude or Gemini.

## Features

- Ask questions about the Revit API
- Generate Python scripts for automating Revit tasks
- Execute generated code directly within Revit
- Choose between Claude or Gemini AI models
- Comprehensive Revit API documentation lookup

## Prerequisites

- Revit 2024 or newer
- pyRevit 4.8 or newer
- Claude API key or Gemini API key (or both)

## Quick Install

1. Download or clone this repository
2. Install pyRevit if not already installed
3. Add this extension to pyRevit
4. Configure your API keys
5. Start using the AI assistant in Revit!

## Detailed Installation

See [Installation Guide](#installation) below for complete steps.

## Usage

1. In Revit, go to the **RvtFunctionCall** tab
2. Click on the **Assistant** button in the AI panel
3. Enter your question or request for a Python script
4. Select the AI model to use (Claude or Gemini)
5. Click **Ask** to get a response
6. If code is generated, click **Execute Code** to run it directly in Revit

### Example Queries

- "How do I get all walls in the current view?"
- "Write a script to create a new level at elevation 10"
- "Generate a script to rename all sheets with a prefix"
- "What are the properties of the Document class?"
- "How do I modify wall parameters?"

## Installation

### Step 1: Install pyRevit

1. Download pyRevit from: https://github.com/eirannejad/pyRevit/releases
2. Run the installer and follow the instructions
3. Restart Revit to load pyRevit

### Step 2: Install This Extension

#### Option A: Direct Download
1. Download this repository as a ZIP file
2. Extract to a folder on your computer
3. Follow Step 3 below

#### Option B: Git Clone
```bash
git clone https://github.com/YOUR_USERNAME/rvt-function-call.git
```

### Step 3: Add Extension to pyRevit

1. Open Revit
2. Go to the **pyRevit** tab
3. Click on the **pyRevit** button (leftmost icon)
4. Select **Settings**
5. In the **Custom Extension Directories** section, click **Add Folder**
6. Browse to and select the folder containing `RvtFunctionCall.extension`
7. Click **Save Settings** and reload pyRevit

### Step 4: Configure API Keys

1. Navigate to the extension folder: `RvtFunctionCall.extension/`
2. Open `config.json` in a text editor
3. Add your API keys:
   ```json
   {
     "default_model": "claude",
     "claude_api_key": "your-actual-claude-api-key-here",
     "gemini_api_key": "your-actual-gemini-api-key-here",
     "max_docs": 5
   }
   ```
4. Save the file

### Step 5: Test the Extension

1. Restart Revit or reload pyRevit
2. Look for the **RvtFunctionCall** tab in Revit
3. Click the **Assistant** button
4. Try a test query like: "How do I get all walls in the document?"

## API Keys

### Getting a Claude API Key
1. Go to https://console.anthropic.com/
2. Create an account or sign in
3. Navigate to API Keys section
4. Create a new API key
5. Copy the key to your config.json

### Getting a Gemini API Key
1. Go to https://makersuite.google.com/app/apikey
2. Create a new API key
3. Copy the key to your config.json

## Project Structure

```
RvtFunctionCall.extension/
├── RvtFunctionCall.tab/             # Revit tab
│   ├── AI.panel/                    # Panel in the tab
│   │   ├── Assistant.pushbutton/    # Main button
│   │   │   ├── icon.png             # Button icon
│   │   │   ├── script.py            # Main script
│   │   │   └── ui.xaml              # UI definition
│   │   └── bundle.yaml              # Panel configuration
│   └── bundle.yaml                  # Tab configuration
├── lib/                             # Libraries directory
│   ├── utils/                       # Utility functions
│   │   ├── ai_client.py             # AI API client
│   │   ├── config.py                # Configuration manager
│   │   └── docs_lookup.py           # Documentation functions
│   └── revit_api_docs/              # Revit API documentation
└── config.json                      # Configuration file
```

## Troubleshooting

### Extension Not Appearing
- Check that pyRevit is properly installed
- Verify the extension folder is added to pyRevit settings
- Try reloading pyRevit or restarting Revit

### API Errors
- Verify your API keys are correct in config.json
- Check your internet connection
- Ensure your API account has sufficient credits

### Code Execution Errors
- Make sure you have an active Revit document
- Check that the generated code is valid Python
- Some operations may require specific Revit contexts

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License.

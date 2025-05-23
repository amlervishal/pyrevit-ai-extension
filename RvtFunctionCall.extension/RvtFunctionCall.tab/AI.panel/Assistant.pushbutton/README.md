# Revit AI Assistant

This tool provides a user interface to interact with AI models (Claude or Gemini) for help with Revit API questions and script generation.

## Features

- Ask questions about Revit API
- Generate Python scripts to automate Revit tasks
- Execute generated code directly in Revit
- Choose between Claude and Gemini AI models

## Configuration

You'll need to provide API keys in the config.json file (created after first run) in the extension root directory.

## How it Works

1. The tool extracts keywords from your query
2. It searches for relevant Revit API documentation in the docs directory
3. The documentation and your query are sent to the selected AI model
4. The AI generates a response based on the provided context
5. If code is generated, you can execute it directly in Revit

## Tips

- Be specific in your queries for better results
- Mention specific Revit API classes or methods if you know them
- For script generation, clearly describe what you want to achieve

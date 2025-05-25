# AI Assistant Button - Troubleshooting Guide

## Files in this directory:

### Main Files:
- **script.py** - Main robust script with comprehensive error handling and fallbacks
- **ui.xaml** - User interface definition
- **icon.png** - Button icon (32x32 PNG)

### Fallback/Test Files:
- **script_simple_test.py** - Simple test script to verify extension loading
- **test_simple.py** - Basic diagnostic script

## Troubleshooting Steps:

### If ribbon doesn't appear at all:
1. Check that `icon.png` exists (not .svg, not .bak)
2. Verify all bundle.yaml files exist
3. Check PyRevit Console for errors
4. Restart Revit completely

### If button appears but doesn't work:
1. **Test with simple script first:**
   ```bash
   # Rename files to test
   mv script.py script_main.py
   mv script_simple_test.py script.py
   # Restart Revit and test
   ```

2. **Check configuration:**
   - Update API keys in `../../config.json`
   - Verify `lib/utils/` modules exist

3. **Check PyRevit Console for detailed errors**

### If UI fails to load:
1. Check that `ui.xaml` is valid
2. Verify all referenced UI elements exist
3. Try the simple fallback script

## Current Status:
- ✅ Icon: icon.png exists
- ✅ Structure: All files in correct locations  
- ✅ Fallbacks: Comprehensive error handling added
- ✅ Config: Enhanced configuration with debug options

## Script Features:
The main script now includes:
- Robust import handling with multiple fallback methods
- UI error handling that prevents crashes
- Configuration loading with defaults
- Status reporting and diagnostics
- Graceful degradation when components aren't available

## Testing Approach:
1. Try main script first
2. If issues, use simple test script to verify basic loading
3. Check console output for specific error messages
4. Fix issues step by step
5. Return to main script when components work

The extension should now load reliably even with missing components!

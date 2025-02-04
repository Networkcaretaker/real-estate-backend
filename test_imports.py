# Create a new file called test_imports.py at the root level
import os
import sys

# Print current directory
print("Current directory:", os.getcwd())

# Print Python path
print("\nPython path:")
for path in sys.path:
    print(path)

# Try to read the file content directly
try:
    with open("app/routes/webhook.py", "rb") as f:
        content = f.read()
        print("\nFile content (first 100 bytes):", content[:100])
except Exception as e:
    print("\nError reading file:", str(e))
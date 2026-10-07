import os
import shutil

items = ['model', 'engine', 'data', 'assets', 'pages', 'app.py', 'ui.py']
target = 'legacy_streamlit'
os.makedirs(target, exist_ok=True)

for item in items:
    if os.path.exists(item):
        shutil.move(item, os.path.join(target, item))

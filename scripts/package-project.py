#!/usr/bin/env python3
# EduPulse CRM - Project Packaging & Zip Archive Utility
# Creates a standalone, clean zip distribution of the codebase.

import os
import sys
import shutil
import zipfile
from pathlib import Path

def create_zip():
    base_dir = Path(__file__).resolve().parent.parent
    zip_filename = base_dir / "EduPulse-Education-CRM.zip"

    exclude_dirs = {'.git', 'node_modules', '__pycache__', '.pytest_cache', 'dist', 'build'}
    exclude_files = {'EduPulse-Education-CRM.zip', '.DS_Store', 'Thumbs.db'}

    print(f"Creating project zip archive: {zip_filename.name} ...")
    
    with zipfile.ZipFile(zip_filename, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(base_dir):
            dirs[:] = [d for d in dirs if d not in exclude_dirs and not d.startswith('.')]
            for file in files:
                if file in exclude_files or file.endswith('.pyc'):
                    continue
                file_path = Path(root) / file
                arcname = file_path.relative_to(base_dir)
                zipf.write(file_path, arcname)

    size_mb = os.path.getsize(zip_filename) / (1024 * 1024)
    print(f"[SUCCESS] Zip package created successfully: {zip_filename} ({size_mb:.2f} MB)")

if __name__ == '__main__':
    create_zip()

#!/usr/bin/env python3
"""
EduPulse CRM - Codebase Lines of Code (LOC) Measurement Tool
Counts production lines of code, excluding external libraries, .git, binary files, and tests.
"""

import os
import sys
import json
from pathlib import Path

EXCLUDED_DIRS = {
    '.git', 'node_modules', '__pycache__', '.pytest_cache', 
    'dist', 'build', 'coverage', '.vscode', '.idea'
}

SUPPORTED_EXTENSIONS = {
    '.js': 'JavaScript',
    '.ts': 'TypeScript',
    '.html': 'HTML',
    '.css': 'CSS',
    '.py': 'Python',
    '.sql': 'SQL',
    '.json': 'JSON Configuration',
    '.md': 'Markdown Documentation',
    '.sh': 'Shell Script',
    '.bat': 'Batch Script'
}

def count_file_lines(filepath):
    """Count total, blank, comment, and code lines in a file."""
    total_lines = 0
    blank_lines = 0
    comment_lines = 0
    code_lines = 0
    
    ext = os.path.splitext(filepath)[1].lower()
    
    try:
        with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
            for line in f:
                total_lines += 1
                stripped = line.strip()
                if not stripped:
                    blank_lines += 1
                elif ext in ['.js', '.ts', '.css', '.sql'] and (stripped.startswith('//') or stripped.startswith('/*') or stripped.startswith('*')):
                    comment_lines += 1
                elif ext in ['.py', '.sh'] and stripped.startswith('#'):
                    comment_lines += 1
                elif ext in ['.html'] and (stripped.startswith('<!--') or stripped.endswith('-->')):
                    comment_lines += 1
                else:
                    code_lines += 1
    except Exception as e:
        pass
        
    return {
        'total': total_lines,
        'blank': blank_lines,
        'comment': comment_lines,
        'code': code_lines
    }

def scan_project(root_dir):
    """Scan all files in the project root."""
    stats_by_lang = {}
    stats_by_dir = {}
    total_stats = {'total': 0, 'blank': 0, 'comment': 0, 'code': 0, 'files': 0}
    prod_stats = {'total': 0, 'blank': 0, 'comment': 0, 'code': 0, 'files': 0}
    
    for dirpath, dirnames, filenames in os.walk(root_dir):
        dirnames[:] = [d for d in dirnames if d not in EXCLUDED_DIRS and not d.startswith('.')]
        
        rel_dir = os.path.relpath(dirpath, root_dir)
        top_dir = rel_dir.split(os.sep)[0] if rel_dir != '.' else 'root'
        is_test_dir = top_dir == 'tests' or 'test' in rel_dir.lower()
        
        if top_dir not in stats_by_dir:
            stats_by_dir[top_dir] = {'total': 0, 'blank': 0, 'comment': 0, 'code': 0, 'files': 0}
            
        for filename in filenames:
            ext = os.path.splitext(filename)[1].lower()
            if ext in SUPPORTED_EXTENSIONS:
                filepath = os.path.join(dirpath, filename)
                res = count_file_lines(filepath)
                lang = SUPPORTED_EXTENSIONS[ext]
                
                if lang not in stats_by_lang:
                    stats_by_lang[lang] = {'total': 0, 'blank': 0, 'comment': 0, 'code': 0, 'files': 0}
                    
                for k in ['total', 'blank', 'comment', 'code']:
                    stats_by_lang[lang][k] += res[k]
                    stats_by_dir[top_dir][k] += res[k]
                    total_stats[k] += res[k]
                    if not is_test_dir:
                        prod_stats[k] += res[k]
                    
                stats_by_lang[lang]['files'] += 1
                stats_by_dir[top_dir]['files'] += 1
                total_stats['files'] += 1
                if not is_test_dir:
                    prod_stats['files'] += 1

    return stats_by_lang, stats_by_dir, total_stats, prod_stats

def main():
    root = os.path.abspath(os.path.dirname(__file__))
    print("=" * 78)
    print("           EDUPULSE EDUCATION CRM - CODEBASE METRICS SCANNER           ")
    print("=" * 78)
    print(f"Scanning directory: {root}\n")
    
    stats_by_lang, stats_by_dir, total_stats, prod_stats = scan_project(root)
    
    print(f"{'Language':<22} | {'Files':<8} | {'Lines':<10} | {'Blank':<8} | {'Comment':<8} | {'Code (LOC)':<10}")
    print("-" * 78)
    for lang, s in sorted(stats_by_lang.items(), key=lambda x: x[1]['total'], reverse=True):
        print(f"{lang:<22} | {s['files']:<8} | {s['total']:<10} | {s['blank']:<8} | {s['comment']:<8} | {s['code']:<10}")
    
    print("-" * 78)
    print(f"{'TOTALS':<22} | {total_stats['files']:<8} | {total_stats['total']:<10} | {total_stats['blank']:<8} | {total_stats['comment']:<8} | {total_stats['code']:<10}")
    print("=" * 78)
    
    print("\nBreakdown by Top-Level Directory:")
    print("-" * 78)
    print(f"{'Directory':<22} | {'Files':<8} | {'Total Lines':<12} | {'Code Lines (LOC)':<16}")
    print("-" * 78)
    for d, s in sorted(stats_by_dir.items(), key=lambda x: x[1]['total'], reverse=True):
        print(f"{d:<22} | {s['files']:<8} | {s['total']:<12} | {s['code']:<16}")
    print("=" * 78)
    
    target_loc = 50000
    print(f"\n[TRAINPLEX PRODUCTION METRICS (TESTS EXCLUDED)]")
    print(f"  Production Source Files: {prod_stats['files']:,}")
    print(f"  Production Code (LOC):   {prod_stats['code']:,} lines (Target: >= {target_loc:,})")
    print(f"  Total Workspace Lines:   {total_stats['total']:,} lines")
    
    if prod_stats['code'] >= target_loc:
        print(f"\n[SUCCESS] Project passes TrainPlex production LOC criteria: {prod_stats['code']:,} >= {target_loc:,} LOC")
    else:
        print(f"\n[WARNING] Project has {prod_stats['code']:,} prod LOC (Target: {target_loc:,})")

if __name__ == '__main__':
    main()

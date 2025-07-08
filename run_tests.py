#!/usr/bin/env python3
"""
Test runner script for YT Leechr
"""

import sys
import os
import subprocess
from pathlib import Path

def main():
    """Run tests with appropriate configuration"""
    
    # Add src to Python path
    src_path = Path(__file__).parent / 'src'
    sys.path.insert(0, str(src_path))
    
    # Set environment variables for testing
    os.environ['QT_QPA_PLATFORM'] = 'offscreen'  # Run tests without display
    
    # Run pytest with our configuration
    test_args = [
        'python', '-m', 'pytest',
        '-v',  # Verbose output
        '--tb=short',  # Short traceback format
        'tests/',  # Test directory
    ]
    
    # Add coverage if available
    try:
        import coverage
        test_args.extend([
            '--cov=src',
            '--cov-report=term-missing',
            '--cov-report=html:htmlcov'
        ])
        print("Running tests with coverage...")
    except ImportError:
        print("Running tests without coverage (install pytest-cov for coverage)")
    
    # Add any additional arguments passed to this script
    test_args.extend(sys.argv[1:])
    
    print(f"Executing: {' '.join(test_args)}")
    
    # Run the tests
    result = subprocess.run(test_args)
    return result.returncode

if __name__ == '__main__':
    sys.exit(main())
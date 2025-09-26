#!/usr/bin/env python3
"""
Memory usage test for ML-KEM calculator.
Used by GitHub Actions CI to monitor performance.
"""

import resource
import mlkem_prime_roots

def main():
    """Test memory usage of ML-KEM calculator."""
    # Get memory usage before
    usage_before = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
    
    # Run the main calculator
    mlkem_prime_roots.main()
    
    # Get memory usage after
    usage_after = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss

    # On Linux, ru_maxrss is in KB
    memory_used = usage_after - usage_before
    print(f'Memory used: {memory_used} KB')

    # Check memory usage is reasonable (< 100MB)
    if memory_used > 100 * 1024:
        print('Warning: High memory usage detected')
        return False
    else:
        print('✓ Memory usage is acceptable')
        return True

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)
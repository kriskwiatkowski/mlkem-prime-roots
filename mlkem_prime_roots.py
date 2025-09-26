#!/usr/bin/env python3
"""
ML-KEM Prime Roots Calculator

This script calculates the prime roots used by ML-KEM (Module-Lattice-Based Key 
Encapsulation Mechanism) for Number Theoretic Transform (NTT) operations.

ML-KEM uses:
- Prime modulus q = 3329
- Primitive root ζ = 17 (a primitive 256th root of unity modulo q)
- Various powers of the primitive root for NTT operations
"""

import math
from typing import List, Tuple


def mod_exp(base: int, exp: int, mod: int) -> int:
    """Fast modular exponentiation using binary method."""
    result = 1
    base = base % mod
    while exp > 0:
        if exp % 2 == 1:
            result = (result * base) % mod
        exp = exp >> 1
        base = (base * base) % mod
    return result


def is_primitive_root(g: int, p: int, factors: List[int]) -> bool:
    """
    Check if g is a primitive root modulo p.
    factors should contain all prime factors of p-1.
    """
    for factor in factors:
        if mod_exp(g, (p - 1) // factor, p) == 1:
            return False
    return True


def find_primitive_roots(p: int, count: int = 10) -> List[int]:
    """Find primitive roots modulo p."""
    if p <= 1:
        return []
    
    # Find prime factors of p-1
    phi = p - 1
    factors = []
    n = phi
    for i in range(2, int(math.sqrt(n)) + 1):
        if n % i == 0:
            factors.append(i)
            while n % i == 0:
                n //= i
    if n > 1:
        factors.append(n)
    
    roots = []
    for g in range(2, p):
        if len(roots) >= count:
            break
        if is_primitive_root(g, p, factors):
            roots.append(g)
    
    return roots


def find_nth_roots_of_unity(n: int, q: int) -> List[int]:
    """
    Find all primitive nth roots of unity modulo q.
    For ML-KEM, we need 256th roots of unity.
    """
    roots = []
    
    # Check if nth roots of unity exist
    if (q - 1) % n != 0:
        print(f"Warning: {n}th roots of unity don't exist modulo {q}")
        return roots
    
    # Find primitive roots modulo q
    primitive_roots = find_primitive_roots(q, 50)
    
    for g in primitive_roots:
        # Calculate g^((q-1)/n) mod q
        root = mod_exp(g, (q - 1) // n, q)
        if root not in roots:
            roots.append(root)
            # We typically only need one primitive nth root
            break
    
    return roots


def generate_ntt_roots(zeta: int, n: int, q: int) -> Tuple[List[int], List[int]]:
    """
    Generate NTT roots and their bit-reversed order.
    zeta: primitive nth root of unity
    n: transform size (256 for ML-KEM)
    q: prime modulus
    """
    # Forward NTT roots: zeta^i for i = 0, 1, ..., n-1
    forward_roots = []
    for i in range(n):
        root = mod_exp(zeta, i, q)
        forward_roots.append(root)
    
    # Inverse NTT roots: zeta^(-i) for i = 0, 1, ..., n-1
    zeta_inv = mod_exp(zeta, q - 2, q)  # Fermat's little theorem for modular inverse
    inverse_roots = []
    for i in range(n):
        root = mod_exp(zeta_inv, i, q)
        inverse_roots.append(root)
    
    return forward_roots, inverse_roots


def bit_reverse(num: int, bits: int) -> int:
    """Reverse the bits of a number."""
    result = 0
    for _ in range(bits):
        result = (result << 1) | (num & 1)
        num >>= 1
    return result


def generate_bit_reversed_roots(roots: List[int]) -> List[int]:
    """Generate bit-reversed order of roots for NTT."""
    n = len(roots)
    bits = int(math.log2(n))
    
    bit_reversed = [0] * n
    for i in range(n):
        j = bit_reverse(i, bits)
        bit_reversed[j] = roots[i]
    
    return bit_reversed


def main():
    """Main function to calculate ML-KEM prime roots."""
    
    # ML-KEM parameters
    Q = 3329  # Prime modulus
    N = 256   # Polynomial degree / NTT size
    
    print("=" * 60)
    print("ML-KEM Prime Roots Calculator")
    print("=" * 60)
    print(f"Prime modulus (q): {Q}")
    print(f"Polynomial degree (n): {N}")
    print()
    
    # Verify that Q is prime
    def is_prime(n):
        if n < 2:
            return False
        for i in range(2, int(math.sqrt(n)) + 1):
            if n % i == 0:
                return False
        return True
    
    print(f"Is q = {Q} prime? {is_prime(Q)}")
    print()
    
    # Find primitive roots modulo Q
    print("Finding primitive roots modulo q...")
    primitive_roots = find_primitive_roots(Q, 10)
    print(f"First 10 primitive roots modulo {Q}:")
    for i, root in enumerate(primitive_roots):
        print(f"  g_{i+1} = {root}")
    print()
    
    # Find 256th roots of unity
    print(f"Finding primitive {N}th roots of unity...")
    nth_roots = find_nth_roots_of_unity(N, Q)
    print(f"Primitive {N}th roots of unity modulo {Q}:")
    for i, root in enumerate(nth_roots):
        print(f"  ζ_{i+1} = {root}")
    print()
    
    # ML-KEM specifically uses ζ = 17 as the primitive 256th root of unity
    ZETA = 17
    print(f"ML-KEM uses ζ = {ZETA} as the primitive {N}th root of unity")
    
    # Verify that 17 is indeed a primitive 256th root of unity modulo 3329
    zeta_256 = mod_exp(ZETA, N, Q)
    print(f"Verification: ζ^{N} ≡ {zeta_256} (mod {Q}) - {'✓ Correct' if zeta_256 == 1 else '✗ Incorrect'}")
    
    # Check if it's primitive (order should be exactly 256)
    order = 1
    power = ZETA
    while power != 1:
        power = (power * ZETA) % Q
        order += 1
        if order > N:  # Safety check
            break
    print(f"Order of ζ = {ZETA}: {order} - {'✓ Primitive' if order == N else '✗ Not primitive'}")
    print()
    
    # Generate NTT roots
    print("Generating NTT roots...")
    forward_roots, inverse_roots = generate_ntt_roots(ZETA, N, Q)
    
    # Display first few roots
    print("First 16 forward NTT roots (ζ^i mod q):")
    for i in range(16):
        print(f"  ζ^{i:2d} = {forward_roots[i]:4d}")
    print("  ...")
    print()
    
    print("First 16 inverse NTT roots (ζ^(-i) mod q):")
    for i in range(16):
        print(f"  ζ^{-i:2d} = {inverse_roots[i]:4d}")
    print("  ...")
    print()
    
    # Generate twiddle factors for ML-KEM NTT (bit-reversed order)
    print("Generating bit-reversed twiddle factors for NTT...")
    
    # ML-KEM uses specific twiddle factors
    # For level 7 down to level 1 of the NTT butterfly operations
    twiddle_factors = []
    
    for level in range(7, 0, -1):  # levels 7 down to 1
        step = 2 ** level
        for i in range(0, N, 2 * step):
            j = i + step
            # Twiddle factor is ζ^(bit_reverse(j, 8))
            br_j = bit_reverse(j // 2, 7)
            twiddle = mod_exp(ZETA, br_j, Q)
            twiddle_factors.append(twiddle)
    
    print(f"Generated {len(twiddle_factors)} twiddle factors")
    print("First 16 twiddle factors:")
    for i in range(min(16, len(twiddle_factors))):
        print(f"  w_{i:2d} = {twiddle_factors[i]:4d}")
    print("  ...")
    print()
    
    # Save results to file
    print("Saving results to 'mlkem_roots_output.txt'...")
    try:
        with open('mlkem_roots_output.txt', 'w') as f:
            f.write("ML-KEM Prime Roots and NTT Parameters\n")
            f.write("=" * 40 + "\n\n")
            f.write(f"Prime modulus (q): {Q}\n")
            f.write(f"Polynomial degree (n): {N}\n")
            f.write(f"Primitive root (ζ): {ZETA}\n\n")
            
            f.write("Forward NTT roots (ζ^i mod q):\n")
            for i in range(N):
                f.write(f"zeta_powers[{i:3d}] = {forward_roots[i]:4d}\n")
            
            f.write("\nInverse NTT roots (ζ^(-i) mod q):\n")
            for i in range(N):
                f.write(f"zeta_inv_powers[{i:3d}] = {inverse_roots[i]:4d}\n")
            
            f.write(f"\nTwiddle factors for NTT ({len(twiddle_factors)} total):\n")
            for i, tw in enumerate(twiddle_factors):
                f.write(f"twiddle[{i:3d}] = {tw:4d}\n")
        
        print("✓ Results saved successfully!")
    except Exception as e:
        print(f"Error saving file: {e}")
        return 1  # Return error code for testing
    
    print()
    print("Summary:")
    print(f"- Prime modulus: {Q}")
    print(f"- Primitive {N}th root of unity: {ZETA}")
    print(f"- Generated {N} forward NTT roots")
    print(f"- Generated {N} inverse NTT roots")
    print(f"- Generated {len(twiddle_factors)} twiddle factors")
    
    return 0  # Return success code


if __name__ == "__main__":
    exit(main())
#!/usr/bin/env python3
"""
Mathematical validation script for ML-KEM constants.
Used by GitHub Actions CI to verify correctness.
"""

import mlkem_prime_roots

def main():
    """Validate ML-KEM mathematical properties."""
    # Verify key ML-KEM properties
    Q = 3329
    N = 256  
    ZETA = 17

    # Test that q is prime
    def is_prime(n):
        if n < 2: 
            return False
        for i in range(2, int(n**0.5) + 1):
            if n % i == 0: 
                return False
        return True

    assert is_prime(Q), f"{Q} is not prime"
    print("✓ Q = 3329 is prime")

    # Test that 256 divides q-1
    assert (Q - 1) % N == 0, f"{N} does not divide {Q-1}"
    print("✓ 256 divides (q-1)")

    # Test that 17 is a primitive 256th root of unity
    zeta_n = mlkem_prime_roots.mod_exp(ZETA, N, Q)
    assert zeta_n == 1, f"17^256 mod 3329 = {zeta_n}, not 1"
    print("✓ 17^256 ≡ 1 (mod 3329)")

    # Test that 17 has order exactly 256
    order = 1
    power = ZETA
    while power != 1 and order <= N:
        power = (power * ZETA) % Q
        order += 1
    assert order == N, f"Order of 17 is {order}, not {N}"
    print("✓ Order of 17 is exactly 256")

    print("All mathematical properties verified!")
    return True

if __name__ == "__main__":
    main()
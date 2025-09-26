# ML-KEM Prime Roots Calculator

A Python script that calculates the prime roots used by ML-KEM (Module-Lattice-Based Key Encapsulation Mechanism) for Number Theoretic Transform (NTT) operations.

![CI Status](https://github.com/kriskwiatkowski/mlkem-prime-roots/actions/workflows/ci.yml/badge.svg)

## Overview

ML-KEM is a post-quantum cryptographic algorithm that relies on Number Theoretic Transforms (NTT) for efficient polynomial operations. This script calculates and verifies the mathematical constants used in ML-KEM implementations.

### Key ML-KEM Parameters

- **Prime modulus (q)**: 3329
- **Polynomial degree (n)**: 256  
- **Primitive root (ζ)**: 17 (a primitive 256th root of unity modulo 3329)

## Features

- ✅ Verifies that q = 3329 is prime
- ✅ Finds primitive roots modulo q
- ✅ Calculates 256th roots of unity
- ✅ Generates all 256 forward NTT roots (ζ^i mod q)
- ✅ Generates all 256 inverse NTT roots (ζ^(-i) mod q)  
- ✅ Computes 127 twiddle factors for NTT operations
- ✅ Validates mathematical properties
- ✅ Outputs results to file for reference

## Usage

```bash
# Run the calculator
python mlkem_prime_roots.py

# Run tests
python -m pytest test_mlkem_prime_roots.py -v
```

## Output

The script generates:
1. Console output showing calculations and verifications
2. `mlkem_roots_output.txt` - Complete list of all roots and twiddle factors

Example output:
```
============================================================
ML-KEM Prime Roots Calculator
============================================================
Prime modulus (q): 3329
Polynomial degree (n): 256

Is q = 3329 prime? True

ML-KEM uses ζ = 17 as the primitive 256th root of unity
Verification: ζ^256 ≡ 1 (mod 3329) - ✓ Correct
Order of ζ = 17: 256 - ✓ Primitive

Summary:
- Prime modulus: 3329
- Primitive 256th root of unity: 17
- Generated 256 forward NTT roots
- Generated 256 inverse NTT roots
- Generated 127 twiddle factors
```

## Mathematical Background

ML-KEM uses Number Theoretic Transforms for efficient polynomial multiplication in the ring **Z_q[X]/(X^n + 1)**. The key requirements are:

1. **q ≡ 1 (mod 2n)** - Ensures 2nth roots of unity exist
2. **ζ^n ≡ -1 (mod q)** - For primitive 2nth root of unity
3. **ζ has order exactly 2n** - For primitive property

For ML-KEM:
- q = 3329 ≡ 1 (mod 512) ✓
- n = 256, so we need 256th roots of unity
- ζ = 17 has order 256 modulo 3329 ✓

## Testing

The project includes comprehensive tests covering:

- ✅ Modular arithmetic correctness
- ✅ Primitive root verification  
- ✅ Mathematical property validation
- ✅ Edge case handling
- ✅ Performance benchmarks
- ✅ Security scanning

### Continuous Integration

GitHub Actions automatically:
- Tests against Python 3.8-3.12
- Runs daily regression tests
- Performs security scans with Bandit
- Validates mathematical properties
- Checks performance metrics

## Requirements

- Python 3.8 or later
- No external dependencies (uses only standard library)

## Contributing

1. Fork the repository
2. Create a feature branch
3. Add tests for new functionality
4. Ensure all tests pass
5. Submit a pull request

## License

This project is released under the MIT License.

## References

- [ML-KEM Draft Standard](https://csrc.nist.gov/Projects/post-quantum-cryptography/post-quantum-cryptography-standardization/Module-Lattice-Based-Key-Encapsulation-Mechanism-Standard)
- [CRYSTALS-Kyber](https://pq-crystals.org/kyber/)
- Number Theoretic Transform algorithms

---

**Note**: This calculator is for educational and reference purposes. For production ML-KEM implementations, use officially validated cryptographic libraries.
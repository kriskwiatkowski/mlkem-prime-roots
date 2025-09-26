#!/usr/bin/env python3
"""
Test suite for ML-KEM Prime Roots Calculator

This module contains unit tests to verify the correctness of the ML-KEM
prime roots calculations and ensure the mathematical properties are maintained.
"""

import unittest
import os
import sys
from unittest.mock import patch
from io import StringIO

# Import the main module
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import mlkem_prime_roots


class TestMLKEMPrimeRoots(unittest.TestCase):
    """Test cases for ML-KEM prime roots calculations."""
    
    def setUp(self):
        """Set up test constants."""
        self.Q = 3329  # ML-KEM prime modulus
        self.N = 256   # Polynomial degree
        self.ZETA = 17 # ML-KEM primitive root
    
    def test_mod_exp(self):
        """Test modular exponentiation function."""
        # Test basic cases
        self.assertEqual(mlkem_prime_roots.mod_exp(2, 3, 7), 1)  # 2^3 mod 7 = 8 mod 7 = 1
        self.assertEqual(mlkem_prime_roots.mod_exp(3, 2, 5), 4)  # 3^2 mod 5 = 9 mod 5 = 4
        self.assertEqual(mlkem_prime_roots.mod_exp(5, 0, 13), 1) # 5^0 mod 13 = 1
        
        # Test with ML-KEM parameters
        self.assertEqual(mlkem_prime_roots.mod_exp(self.ZETA, self.N, self.Q), 1)
        
    def test_primitive_root_verification(self):
        """Test that ζ = 17 is a primitive 256th root of unity mod 3329."""
        # Verify ζ^256 ≡ 1 (mod 3329)
        result = mlkem_prime_roots.mod_exp(self.ZETA, self.N, self.Q)
        self.assertEqual(result, 1, "17^256 should be 1 mod 3329")
        
        # Verify that 17 has order exactly 256
        order = 1
        power = self.ZETA
        while power != 1 and order <= self.N:
            power = (power * self.ZETA) % self.Q
            order += 1
        
        self.assertEqual(order, self.N, f"Order of 17 should be {self.N}")
    
    def test_find_primitive_roots(self):
        """Test finding primitive roots modulo q."""
        roots = mlkem_prime_roots.find_primitive_roots(self.Q, 5)
        
        # Should find at least some roots
        self.assertGreater(len(roots), 0, "Should find at least one primitive root")
        self.assertLessEqual(len(roots), 5, "Should not exceed requested count")
        
        # All roots should be in valid range
        for root in roots:
            self.assertGreater(root, 1, "Primitive root should be > 1")
            self.assertLess(root, self.Q, f"Primitive root should be < {self.Q}")
    
    def test_nth_roots_of_unity(self):
        """Test finding 256th roots of unity."""
        roots = mlkem_prime_roots.find_nth_roots_of_unity(self.N, self.Q)
        
        # Should find at least one root
        self.assertGreater(len(roots), 0, "Should find at least one 256th root of unity")
        
        # Each root should satisfy root^256 ≡ 1 (mod 3329)
        for root in roots:
            result = mlkem_prime_roots.mod_exp(root, self.N, self.Q)
            self.assertEqual(result, 1, f"Root {root}^{self.N} should be 1 mod {self.Q}")
    
    def test_generate_ntt_roots(self):
        """Test NTT roots generation."""
        forward_roots, inverse_roots = mlkem_prime_roots.generate_ntt_roots(
            self.ZETA, self.N, self.Q
        )
        
        # Check lengths
        self.assertEqual(len(forward_roots), self.N, f"Should have {self.N} forward roots")
        self.assertEqual(len(inverse_roots), self.N, f"Should have {self.N} inverse roots")
        
        # Check first element (should be 1)
        self.assertEqual(forward_roots[0], 1, "First forward root should be 1")
        self.assertEqual(inverse_roots[0], 1, "First inverse root should be 1")
        
        # Check second element
        self.assertEqual(forward_roots[1], self.ZETA, f"Second forward root should be {self.ZETA}")
        
        # Verify inverse property: forward[i] * inverse[i] ≡ 1 (mod q) for i > 0
        for i in range(1, min(10, self.N)):  # Test first 10 for efficiency
            product = (forward_roots[i] * inverse_roots[i]) % self.Q
            self.assertEqual(product, 1, f"forward[{i}] * inverse[{i}] should be 1 mod {self.Q}")
    
    def test_bit_reverse(self):
        """Test bit reversal function."""
        # Test known cases
        self.assertEqual(mlkem_prime_roots.bit_reverse(0, 3), 0)  # 000 -> 000
        self.assertEqual(mlkem_prime_roots.bit_reverse(1, 3), 4)  # 001 -> 100
        self.assertEqual(mlkem_prime_roots.bit_reverse(2, 3), 2)  # 010 -> 010
        self.assertEqual(mlkem_prime_roots.bit_reverse(3, 3), 6)  # 011 -> 110
        self.assertEqual(mlkem_prime_roots.bit_reverse(4, 3), 1)  # 100 -> 001
        
        # Test that double bit reverse gives original
        for i in range(8):
            original = i
            reversed_once = mlkem_prime_roots.bit_reverse(original, 3)
            reversed_twice = mlkem_prime_roots.bit_reverse(reversed_once, 3)
            self.assertEqual(reversed_twice, original, 
                           f"Double bit reverse of {original} should give {original}")
    
    def test_mathematical_properties(self):
        """Test mathematical properties of ML-KEM parameters."""
        # Test that 3329 is prime
        def is_prime(n):
            if n < 2:
                return False
            for i in range(2, int(n**0.5) + 1):
                if n % i == 0:
                    return False
            return True
        
        self.assertTrue(is_prime(self.Q), f"{self.Q} should be prime")
        
        # Test that 256 divides q-1 (necessary for 256th roots of unity)
        self.assertEqual((self.Q - 1) % self.N, 0, 
                        f"{self.N} should divide {self.Q}-1 = {self.Q-1}")
    
    def test_main_function_execution(self):
        """Test that the main function runs without errors."""
        # Capture stdout to avoid cluttering test output
        with patch('sys.stdout', new=StringIO()) as fake_out:
            # Test main function returns 0 (success)
            result = mlkem_prime_roots.main()
            self.assertEqual(result, 0, "Main function should return 0 for success")
            
        # Check that output file was created
        self.assertTrue(os.path.exists('mlkem_roots_output.txt'), 
                       "Output file should be created")
        
        # Check output file has reasonable size
        if os.path.exists('mlkem_roots_output.txt'):
            file_size = os.path.getsize('mlkem_roots_output.txt')
            self.assertGreater(file_size, 1000, "Output file should be substantial")
            
        # Clean up
        if os.path.exists('mlkem_roots_output.txt'):
            os.remove('mlkem_roots_output.txt')
    
    def test_edge_cases(self):
        """Test edge cases and error conditions."""
        # Test primitive roots for small numbers
        roots = mlkem_prime_roots.find_primitive_roots(1, 5)
        self.assertEqual(len(roots), 0, "Should find no primitive roots for p=1")
        
        roots = mlkem_prime_roots.find_primitive_roots(2, 5)
        self.assertEqual(len(roots), 0, "Should find no primitive roots for p=2")
        
        # Test nth roots when they don't exist
        with patch('sys.stdout', new=StringIO()):
            roots = mlkem_prime_roots.find_nth_roots_of_unity(100, 7)  # 100 doesn't divide 6
            self.assertEqual(len(roots), 0, "Should find no 100th roots of unity mod 7")


class TestMLKEMConstants(unittest.TestCase):
    """Test ML-KEM specific constants and relationships."""
    
    def test_mlkem_constants(self):
        """Test that ML-KEM constants satisfy required properties."""
        Q = 3329
        N = 256
        ZETA = 17
        
        # Test that n divides (q-1) - required for nth roots of unity
        self.assertEqual((Q - 1) % N, 0, f"{N} should divide {Q-1}")
        
        # Test that zeta^n ≡ 1 (mod q) for primitive nth root
        zeta_n = mlkem_prime_roots.mod_exp(ZETA, N, Q)
        self.assertEqual(zeta_n, 1, f"ζ^{N} should be 1 mod {Q} (primitive {N}th root)")
        
        # Test that zeta^(n/2) ≢ 1 (mod q) to ensure it's primitive
        zeta_n_half = mlkem_prime_roots.mod_exp(ZETA, N // 2, Q)
        self.assertNotEqual(zeta_n_half, 1, f"ζ^{N//2} should not be 1 mod {Q}")
        
        # Test that q is odd (required for NTT)
        self.assertEqual(Q % 2, 1, f"{Q} should be odd")


if __name__ == '__main__':
    # Run the tests
    unittest.main(verbosity=2)
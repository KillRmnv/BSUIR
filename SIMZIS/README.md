# SIMZIS Laboratory Works

This repository contains laboratory works completed for the SIMZIS (Information Security) course. Each lab focuses on different aspects of cryptography and information security.

## Laboratory Work 1: Password Generator and Brute Force Analysis

**File:** `1/SIMZIS1.cpp`

This lab implements:
- Password generator using Cyrillic alphabet and digits (76 characters total)
- Frequency distribution visualization of generated passwords
- Brute force attack time estimation for three scenarios:
  - Server environment
  - Local machine
  - Ideal conditions
- Output of theoretical cracking time in seconds, minutes, hours, and days

## Laboratory Work 2: Table Transposition Cipher

**File:** `2/SIMZIS2.cpp`

This lab implements:
- Table transposition cipher for encryption and decryption
- Input of plaintext, table dimensions (length and width)
- Encryption by reading table columns sequentially
- Decryption by trying all possible table dimensions that match ciphertext length
- Padding with random bytes and asterisks for incomplete blocks

## Laboratory Work 4: Diffie-Hellman Key Exchange

**File:** `4/SIMZIS4.cpp`

This lab implements:
- Diffie-Hellman key exchange protocol
- Primitive root calculation modulo a prime number
- Shared secret computation between two parties (Alice and Bob)
- Verification that both parties compute the same shared secret

## Laboratory Work 5: RSA Cryptosystem with Digital Signatures

**File:** `5/SIMZIS5.py`

This lab implements:
- RSA encryption and decryption system
- Digital signature creation and verification
- Prime number generation using sympy library
- Public exponent selection from Fermat numbers (3, 5, 17, 257, 65537)
- Text-to-number conversion using bit shifting and ASCII values
- Key generation, encryption/decryption, and signing/verification functions

## Laboratory Work 6: Network Firewall Technology

**File:** `lw6.docx` (report)

This lab involved:
- Studying network firewall technology
- Creating two virtual machines with Windows 10
- Configuring policies for data reception, exchange, and sharing of common resources

## Laboratory Work 7: OpenSSL Cryptographic Library

**File:** `lw7.docx` (report)

This lab involved:
- Installing OpenSSL on a virtual machine or Windows 7/8/10
- Exploring the library's capabilities (using the "?" command)
- Testing the speed of various encryption algorithms
- Creating cryptographic keys
- Performing encryption and decryption of arbitrary files using:
  * Various symmetric algorithms
  * Various asymmetric algorithms
- Hashing various files using different algorithms (including md5 and sha1)
- Creating a self-signed X509 certificate
- Studying the certificate's components and their purpose
- Report contents:
  * Performance testing results
  * Encryption times (comparative evaluation of DES and AES, AES and RSA)
  * Obtained hash values
  * Certificate with component descriptions

## Laboratory Work 8: Network Traffic Analysis with Snort

**File:** `lw8.docx` (report)

This lab involved:
- Starting a virtual machine on the main computer and changing the computer name to a unique one
- Installing Snort
- Running Snort in sniffer or logging mode with various detail levels
- Accessing the local network (executing ping, launching browser or explorer, saving a file to the host machine)
- Stopping Snort and determining which IP ports and addresses were accessed
- Using \windows\system32\etc\service to identify used system services
- Viewing the contents of intercepted packets
- Using additional literature to decipher the output header contents
- Report contents:
  * Examples of packets
  * List of detected protocols and services

## Common Features

All laboratory works include:
- Source code implementation in C++ (except Lab 5 which uses Python)
- Detailed reports in OpenDocument format (.odt)
- Visual Studio Code workspace configurations (.vscode)
- Build directories where applicable

## Requirements

- C++ compiler (for Labs 1, 2, 4)
- Python 3.x with sympy library (for Lab 5)
- UTF-8 locale support for proper Cyrillic character handling

## Notes

The works demonstrate practical implementation of cryptographic algorithms and protocols, focusing on understanding their mechanics, strengths, and limitations through hands-on coding exercises.
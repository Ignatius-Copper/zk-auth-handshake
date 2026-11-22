# zk-auth-handshake

A minimal, zero-dependency Python client-server implementation of a **Zero-Knowledge Proof (ZKP)** authentication handshake based on the **Fiat–Shamir identification protocol**.

## ⚠️ Disclaimer
**For educational and demonstration purposes only.** This project uses small prime numbers (10⁵ to 10⁶) to keep calculations fast and readable, and it has not been audited for security. **Do not use this code in production environments.**

## Overview
This repository demonstrates how a client (**Prover**) can prove knowledge of a secret vector \(S = (s_1, \dots, s_t)\) to a server (**Verifier**) over a TCP socket without ever transmitting S over the network. Once the handshake succeeds, the connection transitions into an interactive messaging session.

## Cryptographic Protocol Flow

```text
Client (Prover)                                      Server (Verifier)

      |                                                      |
      |  1. Request parameters (get_params)                  |
      | ---------------------------------------------------> |
      |  2. Send modulus n = p * q and rounds t              |
      | <--------------------------------------------------- |
      |                                                      |
      |  [Generates coprime secrets s_i, gcd(s_i, n) = 1]    |
      |  [Computes public key v_i = s_i^2 mod n]             |
      |                                                      |
      |  3. Register username & public vector V (registrate) |
      | ---------------------------------------------------> |
      |  4. Registration status ("Ok")                       |
      | <--------------------------------------------------- |
      |                                                      |
      |  [Picks random r_i, computes x_i = r_i^2 mod n]      |
      |  5. Send commitments X (auth_init)                   |
      | ---------------------------------------------------> |
      |  6. Send random binary challenge E in {0, 1}^t       |
      | <--------------------------------------------------- |
      |                                                      |
      |  [Computes y_i = r_i * s_i^(e_i) mod n]              |
      |  7. Send responses Y (auth_responce)                 |
      | ---------------------------------------------------> |
      |                                  [Verifies for all i:|
      |                                   y_i^2 == x_i * v_i^(e_i) mod n]

      |  8. Verification result (status: True/False)         |
      | <--------------------------------------------------- |
      |                                                      |
      |  9. Authenticated interactive chat / commands        |
      | <==================================================> |
```

### Step-by-Step Breakdown
1. **Parameter Setup (`get_params`):** The server generates two distinct prime numbers $p, q \in [10^5, 10^6]$, computes the public modulus $n = p \cdot q$, and picks a random number of rounds $t \in [4, 20]$.
2. **Key Generation & Registration (`registrate`):** The client generates $t$ secret integers $s_i \in [2, n-1]$ coprime to $n$ ($\gcd(s_i, n) = 1$) and computes the public verification vector $v_i \equiv s_i^2 \pmod n$. Only the username and $V$ are sent to the server.
3. **Commitment (`auth_init`):** For each round, the client chooses a random nonce $r_i \in [1, n-1]$ and sends the commitment $x_i \equiv r_i^2 \pmod n$ to the server.
4. **Challenge:** The server generates a cryptographically secure random bit vector $E = (e_1, \dots, e_t) \in \{0, 1\}^t$ and sends it to the client.
5. **Response & Verification (`auth_responce`):**
   - If $e_i = 0$, the client sends $y_i \equiv r_i \pmod n$.
   - If $e_i = 1$, the client sends $y_i \equiv r_i \cdot s_i \pmod n$.
   - The server accepts the proof only if $y_i^2 \equiv x_i \cdot v_i^{e_i} \pmod n$ holds for all $t$ rounds.

## Project Structure
- `server.py` — Multi-threaded TCP server acting as the **Verifier**. Handles parameter distribution, user registration, round verification, and post-auth messaging.
- `client.py` — Interactive TCP client acting as the **Prover**. Handles commitment generation, challenge responses, and the interactive terminal prompt.
- `utils.py` — Core math and serialization utilities: prime generation (`generat_numbers`), coprime secret generation (`proving`), and UTF-8 JSON encoding/decoding.

## Quick Start

### Requirements
- **Python 3.8+** (uses only built-in standard libraries: `socket`, `threading`, `secrets`, `json`, `sys`).

### 1. Start the Server
```bash
python server.py
```
By default, the server listens on `127.0.0.1:65432`.

### 2. Run the Client
Open a second terminal and run:
```bash
python client.py
```
Follow the prompt to enter a username. After the zero-knowledge handshake succeeds, you can send messages or test server commands (`/users`, `/all_rooms`, `/exit`).

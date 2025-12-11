# vArbitrum
This repository contains the smart contracts used to simulate the vArbitrum protocol’s challenge–response mechanism, along with Python scripts for constructing (off-chain) Merkle roots using AVM state hashes.

## Repository Structure
1. **Contracts_needed_ones/**
   
This folder contains all Solidity smart contracts used to simulate the vArbitrum dispute-resolution process.
It includes:
-  *Modified challenge contract (mChallenge.sol)*: extends Arbitrum’s original Challenge.sol to support challenger's result submission, hashed bisection values and updated single-step verification logic
-  *Other supporting contracts (from Arbitrum EthBridge)*:
   - ChallengeFactory.sol: creates challenge instances
   - ChallengeLib.sol: Merkle proof helpers
   - MerkleLib.sol: Merkle root generation
   - OneStepProofCommon.sol: executes a single disputed step
   - OneStepProof.sol: AVM-instruction → EVM-opcode translation 
   - ChallengeTester.sol: a lightweight test code replacing Arbitrum’s RollupUser.sol
- *Computation example* — Matrix Multiplication (*matrixmul.sol* - 10×10 matrix multiplication smart contract)
2. **Sample_Mroot_generation/**

This folder contains Python scripts executed off-chain by each manager to:
- parse AVM-like state files
- compute per-step state hashes
- construct the Merkle root using the state hashes
The file *Instruction.txt* provides step-by-step guidance on running the scripts.

## Simulation Environment
The proof-of-concept replicates the vArbitrum's challenge-response protocol in a local setup using:
- *Ganache* to simulate local Ethereum
- *Truffle / Remix* for compiling and deploying contracts
- *Web3.py* for Python-based manager scripts
(Note that only 8+ essential contracts from EthBridge are deployed (called rEthBridge) for this testing without deploying the full Arbitrum codebase.)

## How to use this repository
1. Compile contracts using Remix or Truffle
2. Deploy rEthBridge contracts to Ganache
3. Use the provided Python scripts to:
  - simulate manager execution
  - compute Merkle roots
  - submit results to the on-chain verifier
4. Use the following smart-contract function calls to test the full protocol:
  <img width="400" height="300" alt="contract_list" src="https://github.com/user-attachments/assets/0e2c8667-48f7-4044-ae95-3c762a2a0f52" />

## How the challenge-response works (high-level idea)
            ┌──────────────────────────────────────────┐
          │              Client (C)                  │
          │  Deploys program + initialization data   │
          └──────────────────────────────────────────┘
                             │
                             ▼
       ┌─────────────────────────────────────────────────────┐
       │               Managers S1 and S2                    │
       │  • Execute computation off-chain (in private EVM)   │
       │  • Generate state hashes (AVM-like) 
       |    + construct Merkle roots (R1, R2)                │
       └─────────────────────────────────────────────────────┘
                             │
               Submit R1 and R2 to rEthBridge
                             ▼
              ┌────────────────────────────────┐
              │        Verifier Contract       │
              │        (mChallenge.sol)        │
              └────────────────────────────────┘
                       /                 \
                (Roots match)        (Roots differ)
                     /                     \
                    ▼                       ▼
       ┌──────────────────┐     ┌─────────────────────────┐
       │ Accept Result ✔  │     │   Challenge Begins      │
       │                  │     │ initializeChallenge()   │
       └──────────────────┘     └─────────────────────────┘
                                           │
                                           ▼
             ┌─────────────────────────────────────────┐
             │             Bisection Phase             │
             │  • Asserter sends bisected hashes       │
             │  • Challenger selects disputed segment  │
             │  • Repeat until 1 instruction remains   │
             │     (bisectExecution())                 │
             └─────────────────────────────────────────┘
                                           │
                                           ▼
             ┌──────────────────────────────────────────┐
             │           Single-Step Proof              │
             │  • Asserter submits step data            │
             │    oneStepProveExecution()               │
             │  • Contract executes step                │
             │    via OneStepProofCommon.sol            │
             └──────────────────────────────────────────┘
                                           │
                                           ▼
                ┌──────────────────────────────────────┐
                │              Decision                │
                │  • If proof valid → Asserter wins    │
                │  • Else → Challenger wins            │
                │ completeChallenge()                  │
                └──────────────────────────────────────┘
                                           │
                                           ▼
              ┌─────────────────────────────────────────┐
              │        Final Result Returned            │
              └─────────────────────────────────────────┘


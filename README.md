# vArbitrum
This repository contains the smart contracts used to simulate the vArbitrum protocol's challenge-response process and Python scripts for constructing (off-chain) Merkle roots using AVM state hashes.

## Repository Structure
1. Contracts_needed_ones/
   
This folder contains all Solidity smart contracts used to simulate the vArbitrum dispute-resolution process.
Specifically, it includes:
-  *Modified challenge contract (mChallenge.sol)*: extends Arbitrum’s original Challenge.sol 
-  *Other supporting contracts (from Arbitrum EthBridge)*:
   - ChallengeFactory.sol: creates challenge instances
   - ChallengeLib.sol: Merkle root helpers, segment proof verification
   - MerkleLib.sol: Merkle root generation
   - OneStepProofCommon.sol: executes a single disputed step
   - OneStepProof.sol: AVM-instruction → EVM-opcode translation for correctness checking
   - ChallengeTester.sol: a lightweight test code replacing Arbitrum’s RollupUser.sol
- *Computation example* — Matrix Multiplication (matrixmul.sol - 10×10 matrix multiplication smart contract)
2. Sample_Mroot_generation/

This folder contains the Python scripts executed off-chain by each manager to compute AVM state hashes (from the state files) and construct the Merkle root.
Steps to test the codes are provided in the *Instruction.txt* file.

## Simulation Environment
The proof-of-concept replicates the Arbitrum dispute-resolution flow but in a lightweight local environment, using:
- *Ganache* to simulate Ethereum
- *Truffle / Remix* for compiling and deploying contracts
- *Web3.py* for Python-based manager scripts
(Note that only 8+ essential contracts from EthBridge are deployed (called rEthBridge) for this testing without the full Arbitrum codebase.)

## How to use this repository
1. Compile contracts using Remix or Truffle
2. Deploy rEthBridge contracts to Ganache
3. Use the provided Python scripts to:
  - simulate manager execution
  - compute Merkle roots
  - submit results to the on-chain verifier
4. Use the following function calls from smart contracts to test:
  <img width="400" height="300" alt="contract_list" src="https://github.com/user-attachments/assets/0e2c8667-48f7-4044-ae95-3c762a2a0f52" />

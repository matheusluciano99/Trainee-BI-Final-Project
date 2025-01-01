# Trainee-BI-Final-Project

## DAO Voting System

### Dependencies

1. **Foundry**

   Run in your terminal:

   curl -L https://foundry.paradigm.xyz | bash

   Then run:

   foundryup

2. **Python dependencies**

- Reflex
- web3
- python-dotenv

  To install these dependencies, run:

  pip install -r requirements.txt

  # Deploying the contract and running the app

  ## Setup environment variables

  ### Setup your .env:

  RPC_URL="SEPOLIA_RPC_URL"
  DAO_ADDRESS="DAO_ADDRESS"
  TOKEN_ADDRESS="TOKEN_ADDRESS"
  PRIVATE_KEY="YOUR_PRIVATE_KEY"
  ETHERSCAN_API_KEY="YOUR_ETHERSCAN_API"

  ### Run

  source .env

  ### Deploy

  forge script script/DeployMyDAO.s.sol:DeployMyDAO \
   --rpc-url $SEPOLIA_RPC_URL \
   --private-key $PRIVATE_KEY \
   --broadcast \
   --verify \
   --etherscan-api-key $ETHERSCAN_API_KEY

  ### Run the frontend

  reflex run

  ## The Contracts of this project were deployed at:

  ### TokenBCI: 0x5e7084b61127A19175d47205eBaD403F6620870b

  ### DAO: 0x74706a37DDfaa1D7890ae4182009A6f4eb7DFA2C

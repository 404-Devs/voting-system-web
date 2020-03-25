import json
from web3 import Web3

PRIVATE_KEY = "714e2ce5aeb6a1c1aa23d3267937e2de732f3fc1a7f229746a875d5720bbc819"
PUBLIC_KEY = "0x9d0be98b49BED438500F263e27595453Dc308380"
WEB3 = Web3(Web3.HTTPProvider("http://127.0.0.1:7545"))
abi = json.loads(open("Voting.json", "r").read())["abi"]
VOTING = WEB3.eth.contract(address="0x5ae0B80Eb23D5d4f3855d19A799D316A177f85F5", abi=abi)

def execute(tx_dict):
    signed_tx = WEB3.eth.account.sign_transaction(tx_dict, PRIVATE_KEY)
    result = WEB3.eth.sendRawTransaction(signed_tx.rawTransaction)
    receipt = WEB3.eth.getTransactionReceipt(result)
    return receipt

def add_election_to_bc(electionId, name, start_timestamp, end_timestamp):
    tx_dict = VOTING.functions.setElection(electionId, name, start_timestamp, end_timestamp).buildTransaction({'nonce': WEB3.eth.getTransactionCount(PUBLIC_KEY)})
    return execute(tx_dict)

def add_aspirant_to_bc(aspirantId, name):
    tx_dict = VOTING.functions.setAspirant(aspirantId, name).buildTransaction({'nonce': WEB3.eth.getTransactionCount(PUBLIC_KEY)})
    return execute(tx_dict)

def add_team_to_bc(electionId, teamId, name, chairmanId, secGenId, treasurerId):
    tx_dict = VOTING.functions.setAspirant(electionId, teamId, name, chairmanId, secGenId, treasurerId).buildTransaction({'nonce': WEB3.eth.getTransactionCount(PUBLIC_KEY)})
    return execute(tx_dict)

def add_voting_token_bc(electionId):
    tx_dict = VOTING.functions.setAspirant(electionId).buildTransaction({'nonce': WEB3.eth.getTransactionCount(PUBLIC_KEY)})
    return execute(tx_dict)

def end_election_bc(electionId):
    tx_dict = VOTING.functions.setAspirant(electionId).buildTransaction({'nonce': WEB3.eth.getTransactionCount(PUBLIC_KEY)})
    return execute(tx_dict)

def cast_bc(electionId, teamId, votingToken):
    tx_dict = VOTING.functions.setAspirant(electionId, teamId, votingToken).buildTransaction({'nonce': WEB3.eth.getTransactionCount(PUBLIC_KEY)})
    return execute(tx_dict)

def get_winner_bc(electionId):
    return VOTING.functions.get_winner(electionId).call()

def get_team_bc(electionId, teamId):
    return VOTING.functions.get_winner(electionId, teamId).call()

if __name__ == "__main__":
    print(add_election_to_bc(2, "dasdfasdf", 2, 2))

import json
import uuid
from web3 import Web3

# TODO: Setup a Ganache workspace
# TODO: Deploy contract to workspace
WEB3 = Web3(Web3.HTTPProvider("http://127.0.0.1:7545"))
# TODO: Create your own keys.json file based on the format provided in the keys_format.json file
keys = json.loads(open("keys.json", "r").read())
PRIVATE_KEY = keys['private']
PUBLIC_KEY = keys['public']
contract = json.loads(open("Voting.json", "r").read())
VOTING = WEB3.eth.contract(address=contract['networks']['5777']['address'], abi=contract['abi'])

def execute(tx):
    try:
        tx_dict = tx.buildTransaction({'nonce': WEB3.eth.getTransactionCount(PUBLIC_KEY)})
        signed_tx = WEB3.eth.account.sign_transaction(tx_dict, PRIVATE_KEY)
        result = WEB3.eth.sendRawTransaction(signed_tx.rawTransaction)
        receipt = WEB3.eth.getTransactionReceipt(result)
        return {'success': True, 'receipt': receipt}
    except ValueError:
        return {'success': False}

def add_election_to_bc(electionId, name, start_timestamp, end_timestamp):
    return execute(VOTING.functions.setElection(electionId, name, start_timestamp, end_timestamp))

def add_aspirant_to_bc(aspirantId, name):
    return execute(VOTING.functions.setAspirant(aspirantId, name))

def add_team_to_bc(electionId, teamId, name, chairmanId, secGenId, treasurerId):
    return execute(VOTING.functions.setTeam(electionId, teamId, name, chairmanId, secGenId, treasurerId))

def add_voting_token_bc(electionId):
    votingToken = uuid.uuid4().hex[:32]
    return execute(VOTING.functions.setVotingToken(electionId, votingToken)), votingToken

def cast_bc(electionId, teamId, votingToken):
    return execute(VOTING.functions.cast(electionId, teamId, votingToken))

def end_election_bc(electionId):
    return execute(VOTING.functions.endElection(electionId))

def get_winner_bc(electionId):
    return VOTING.functions.getWinner(electionId).call()

def get_team_bc(electionId, teamId):
    return VOTING.functions.getTeam(electionId, teamId).call()

if __name__ == "__main__":
    import time
    print(add_aspirant_to_bc(2, "John"))
    print(add_aspirant_to_bc(3, "Jane"))
    print(add_aspirant_to_bc(4, "Doe"))
    print(add_election_to_bc(4, "UNSA 2024", int(time.time()) + 86400, int(time.time()) + 86400 * 2))
    print(add_team_to_bc(4, 1, "Team Doe", 2, 3, 4))
    print(add_voting_token_bc(4))
    print(cast_bc(4, 1, "asdf"))
    print(end_election_bc(4))
    print(get_team_bc(4, 1))

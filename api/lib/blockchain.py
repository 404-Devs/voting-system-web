import json
from web3 import Web3

def load_env():
    keys = json.loads(open("api/lib/keys.json", "r").read())
    WEB3 = Web3(Web3.HTTPProvider(keys['url']))
    PRIVATE_KEY = keys['private']
    PUBLIC_KEY = keys['public']
    contract = json.loads(open("api/lib/Voting.json", "r").read())
    VOTING = WEB3.eth.contract(address="0x7398761b4D2Dd02Fb3DA3dD99f2719c650cb365e", abi=contract['abi'])
    return WEB3, PRIVATE_KEY, PUBLIC_KEY, VOTING

# too bad we won't block waiting for the transaction to complete
def execute(env, tx):
    tx_dict = tx.buildTransaction({'nonce': env[0].eth.getTransactionCount(env[2]), 'gas': 2000000,'gasPrice': Web3.toWei('50', 'gwei'),})
    signed_tx = env[0].eth.account.sign_transaction(tx_dict, env[1])
    env[0].eth.sendRawTransaction(signed_tx.rawTransaction)

def set_election_bc(env, electionId, name, start_timestamp, end_timestamp):
    execute(env, env[3].functions.setElection(electionId, name, start_timestamp, end_timestamp))

def set_aspirant_bc(env, aspirantId, name):
    execute(env, env[3].functions.setAspirant(aspirantId, name))

def set_team_bc(env, electionId, teamId, name, chairmanId, secGenId, treasurerId):
    execute(env, env[3].functions.setTeam(electionId, teamId, name, chairmanId, secGenId, treasurerId))

def set_voting_token_bc(env, electionId, token):
    execute(env, env[3].functions.setVotingToken(electionId, token))

def cast_bc(env, electionId, teamId, votingToken):
    execute(env, env[3].functions.cast(electionId, teamId, votingToken))

def end_election_bc(env, electionId):
    execute(env, env[3].functions.endElection(electionId))

def get_winner_bc(env, electionId):
    execute(env, env[3].functions.getWinner(electionId).call())

def get_team_bc(env, electionId, teamId):
    return env[3].functions.getTeam(electionId, teamId).call()

def get_ballot_bc(env, electionId, token):
    execute(env, env[3].functions.getBallot(electionId, token).call())

def get_results_bc(env, electionId):
    return env[3].functions.getResults(electionId).call()
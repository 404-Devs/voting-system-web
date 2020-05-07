import json
import uuid
import time
from web3 import Web3

def load_env():
    keys = json.loads(open("api/lib/keys.json", "r").read())
    WEB3 = Web3(Web3.HTTPProvider(keys['url']))
    PRIVATE_KEY = keys['private']
    PUBLIC_KEY = keys['public']
    contract = json.loads(open("api/lib/Voting.json", "r").read())
    VOTING = WEB3.eth.contract(address="0xb820C669F12001c48C56ad40136f9A539c0147c3", abi=contract['abi'])
    return WEB3, PRIVATE_KEY, PUBLIC_KEY, VOTING

# too bad we won't block waiting for the transaction to complete
def execute(env, tx):
    try:
        tx_dict = tx.buildTransaction({'nonce': env[0].eth.getTransactionCount(env[2]), 'gas': 2000000,'gasPrice': Web3.toWei('50', 'gwei'),})
        signed_tx = env[0].eth.account.sign_transaction(tx_dict, env[1])
        env[0].eth.sendRawTransaction(signed_tx.rawTransaction)
    except ValueError as err:
        # print(dir(err))
        print(err.args, err.args[0])
        print(err.args[0]['code'])
        # err = json.loads(str(err))
        if err.args[0]['code'] == -32000:
            while True:
                time.sleep(60)
                execute(env, tx)
                break
        print("meeee", err)

def add_election_to_bc(env, electionId, name, start_timestamp, end_timestamp):
    execute(env, env[3].functions.setElection(electionId, name, start_timestamp, end_timestamp))

def add_aspirant_to_bc(env, aspirantId, name):
    execute(env, env[3].functions.setAspirant(aspirantId, name))

def add_team_to_bc(env, electionId, teamId, name, chairmanId, secGenId, treasurerId):
    execute(env, env[3].functions.setTeam(electionId, teamId, name, chairmanId, secGenId, treasurerId))

def add_voting_token_bc(env, electionId, token):
    execute(env, env[3].functions.setVotingToken(electionId, token))

def cast_bc(env, electionId, teamId, votingToken):
    execute(env, env[3].functions.cast(electionId, teamId, votingToken))

def end_election_bc(env, electionId):
    execute(env, env[3].functions.endElection(electionId))

def get_winner_bc(env, electionId):
    execute(env, env[3].functions.getWinner(electionId).call())

def get_team_bc(env, electionId, teamId):
    execute(env, env[3].functions.getTeam(electionId, teamId).call())

def get_ballot_bc(env, electionId, token):
    execute(env, env[3].functions.getBallot(electionId, token).call())
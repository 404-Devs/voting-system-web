### Code for CSC224 Project, Web Part

#### How to setup blockchain bit

1. Follow the instructions on the DiscussionGroup/voting-system-blockchain repository's README
2. Copy the Voting.json file in the folder above to the lib/ folder of this repository (replace)
3. Create a keys.json file in the lib/ folder & copy the contents of the lib/keys_format.json file to the created file
4. Copy the public & private key of the first account on Ganache and replace the placeholders in the lib/keys.json file

### "Docs" -> API Endpoints

Expected Error Response is in this format {'code': 0, 'status': 'error', 'msg': 'Reason'}.\
Expected Success Response is in this format {'code': 1, 'status': 'success', 'msg': 'Success Msg'}.\
The API works with POST calls only & the response is in JSON format.\
Listed below are the endpoints, & some example input.

#### Vote

POST <https://votingtest.herokuapp.com/api/voter/login>

Input\
reg_no=P15/1234/2018\
password=0123456789

#### Register school

POST <https://votingtest.herokuapp.com/api/school/register>

Input\
school_name=School of Computing and Informatics\

#### Update school information

POST <https://votingtest.herokuapp.com/api/school/update>

Input\
school_id=1\
&school_name=Medschool

#### Register voter

POST <https://votingtest.herokuapp.com/api/voter/register>

Input\
reg_no=P15/1234/2018\
&email=test@gmail.com\
&password=testpass123\
&school_id=2

#### Register election

POST <https://votingtest.herokuapp.com/api/election/register>

Input\
election_name=UNSA 2020\
&start_timestamp=2020-07-14 00:00\
&end_timestamp=2020-07-16 00:00

#### Register aspirant

POST <https://votingtest.herokuapp.com/api/aspirant/register>

Input\
aspirant_reg_no=P15/1234/2018\
&aspirant_photo=0

#### Register Team

POST <https://votingtest.herokuapp.com/api/team/register>

Input
team_name=Comrades Power\
&team_logo=0\
&election_id=4\
&chairman_reg=P15/1234/2018\
&sec_gen_reg=P15/1234/2018\
&treasurer_reg=P15/1234/2018

#### Vote

POST <https://votingtest.herokuapp.com/api/vote>

voter_reg=P15/1234/2018\
&election_id=4

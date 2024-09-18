import requests
import logging
import json
import time

http_settings = {
    'host_prod':'https://bio-agents-dev.sdu.dk/api',
    'host_local':'http://localhost:8000/api',
    'host_dev':'https://bio-agents-dev.sdu.dk/api',
    'login': '/rest-auth/login/',
    'agent': '/t',
    'validate': '/validate',
    'json': '?format=json',
    'dev':'https://bio-agents-dev.sdu.dk/' 
}

def login_prod(username, password):
    headers_token = {
        'Content-Type': 'application/json'
        }
    user = json.dumps({
        'username': username,
        'password': password
    })

    token_r = requests.post(http_settings['host_prod'] + http_settings['login'] + http_settings['json'], headers = headers_token, data = user)
    logging.info(token_r)
    token = json.loads(token_r.text)['key']
    return token


def validate_agent(agent, token):
    '''Validate a agent using the Bioagents API.'''
    url = '{h}{t}{v}{f}'.format(h=http_settings['host_prod'], 
                                t=http_settings['agent'],
                                v=http_settings['validate'],
                                f=http_settings['json'])   
    headers = {
        'Content-Type': 'application/json',
        'Authorization': 'Token ' + token
    }
    r = requests.post(url, headers=headers, data=json.dumps(agent))
    if r.ok:
        return (True, r.text)
    return (False, r.text)


def insert_agent(agent, url, headers):
    response = requests.post(url, headers=headers, data=json.dumps(agent))
        
    if response.ok:
        print(f"{agent['bioagentsID']} Added {response.status_code}")
        return True, response.text

    print("An Error:",agent['bioagentsID'], response.text)
    return False, response.text


def add_agents(agents, token, WRITE_TO_DB=False):
    if not(WRITE_TO_DB):
        return
        
    url = '{h}{t}{f}'.format(h=http_settings['host_prod'], t=http_settings['agent'], f=http_settings['json'])
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Token {token}'
    }
    problem_agents = []
    ok_agents = 0
    for agent in agents:
        added, txt = insert_agent(agent, url, headers)
        if added:
            ok_agents += 1
        else:
            problem_agents.append({'agent_id': agent['bioagentsID'], 'error': txt})
        print('--------------')
        time.sleep(2)

            
    print("Total agents added: {added} out of a total of: {total} ".format(added=ok_agents, total=len(agents)))
    if problem_agents:
        print(f"{len(problem_agents)} agents with problems:")
        print(problem_agents)

    print("Finished adding agents")
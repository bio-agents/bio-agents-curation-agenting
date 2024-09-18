import re

def generate_bioagentsID(name):
    bioagentsID = re.sub('[^a-zA-Z0-9_~ .-]*', '',name)
    bioagentsID = re.sub('[ ]+','-', bioagentsID)
    bioagentsID = 'pub2agents2024__' + bioagentsID

    return bioagentsID.lower()


def process_agents(agents):
    high_agents = []

    for agent in agents:
        agent['editPermission'] = {'type': 'public'}
        agent['bioagentsID'] = generate_bioagentsID(agent['name'])

        if agent['confidence_flag'].lower() == 'high':
            #agent['date']= check_date(pub2agents_file)
            url = '{d}{bt}'.format(d='https://bio-agents-dev.sdu.dk/', bt=agent['bioagentsID'])
            agent['agent_link'] = url
            high_agents.append(agent)

    return high_agents
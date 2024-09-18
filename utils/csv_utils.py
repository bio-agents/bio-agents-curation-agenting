import csv


def filter_agents(agents, to_curate, filter_condition=lambda x: True):
    """Filters agents based on a condition and curate limit."""
    filtered_agents = [agent for agent in agents if filter_condition(agent)]
    if to_curate != 'all':
        filtered_agents = filtered_agents[:int(to_curate)]
    return filtered_agents


def generate_file_name(prefix, file_date):
    """Generates a file name based on a prefix and a date tuple."""
    year, month = file_date[0], file_date[1]
    return f"{prefix}_{year}_{month}.csv"


def generate_csv(pub_agents, pub_preprints, to_curate, file_date):
    """Generates a CSV file for published agents and newly published preprints."""
    file_name = generate_file_name('pub2agents', file_date)
    to_curate_agents = filter_agents(pub_agents, to_curate)
    # Use to_curate publications and previously identified preprints
    combined_agents = to_curate_agents + pub_preprints    
    # Write to CSV
    with open(file_name, 'w', newline='') as fileobj:
        writerobj = csv.writer(fileobj)
        writerobj.writerow(['agent_link', 'agent_name', 'homepage', 'publication_link'])
        for agent in combined_agents[:to_curate]:
            writerobj.writerow([agent['agent_link'], agent['name'], agent['homepage'], agent['publication_link']])
        writerobj.writerow(['NEWLY PUBLISHED PREPRINTS'])
        for agent in combined_agents[to_curate:]:
            writerobj.writerow([agent['agent_link'], agent['name'], agent['homepage'], agent['publication_link']])
    
    leftover_agents = [agent for agent in pub_agents if agent not in combined_agents]
    return combined_agents, leftover_agents


import logging
from utils.json_utils import load_agents_from_json, save_agents_to_json
from utils.utils import search_europe_pmc


def query_for_potential_match(external_id: str, original_doi: str):
    """Query Europe PMC for a potential match based on external ID, excluding the original DOI."""
    query = f'ext_id:"{external_id}" NOT DOI:"{original_doi}"'
    response = search_europe_pmc(query)
    if response and response.get('hitCount', 0) > 0:
        return response['resultList']['result'][0]
    return None


def update_publication_with_match(match):
    """Update the original publication information with data from the match if available.
    Exclude fields that do not have a value."""
    return {
        key: value
        for key, value in (('doi', match.get('doi')), 
                           ('pmid', match.get('pmid')), 
                           ('pmcid', match.get('pmcid')))
        if value is not None
    }


def is_preprint_from_response(response):
    if not response or 'resultList' not in response or not response['resultList']['result']:
        logging.error("Invalid response format.")
        return False, {}
    
    original_result = response['resultList']['result'][0]
    original_publication = original_result.get('publication', [{}])[0]
    commentCorrectionList = original_result.get('commentCorrectionList')

    if original_result.get('source') == 'PPR' and not commentCorrectionList:
        return True, original_result
    
    if commentCorrectionList:
        commentCorrection = commentCorrectionList.get('commentCorrection')[0]
        if commentCorrection.get('source') == 'PPR':
            return True, original_result
        
        external_id = commentCorrection.get('id')
        doi = original_publication.get('doi')
        match = query_for_potential_match(external_id, doi)
        
        if match:
            updated_publication = update_publication_with_match(match)
            return False, updated_publication

    return False, original_result


def update_agent_with_publication(agent, is_preprint, publication_info):
    """Update the agent with publication information based on preprint status."""
    
    if is_preprint:
        doi_url = f"https://doi.org/{agent['publication'][0]['doi']}"
        agent['publication_link'] = doi_url
        agent['is_preprint'] = True
    else:
        if publication_info:
            agent['publication'] = [publication_info]
        if 'doi' in agent['publication'][0]:
            agent['publication_link'] = f"https://doi.org/{agent['publication'][0]['doi']}"
        elif 'pmid' in agent['publication'][0]:
            agent['publication_link'] = f"https://pubmed.ncbi.nlm.nih.gov/{agent['publication'][0]['pmid']}"
        else:
            agent['publication_link'] = f"https://pubmed.ncbi.nlm.nih.gov/{agent['publication'][0]['pmcid']}"
        
        agent['is_preprint'] = False
  
    return agent


def identify_preprint(agent):
    """Identify if a agent's publication is a preprint and update its information."""
    if 'doi' not in agent['publication'][0]:
        print("No DOI found for this agent.")
        return update_agent_with_publication(agent, False, None)  # Assuming not a preprint if no DOI

    doi = agent['publication'][0]['doi']
    response = search_europe_pmc(doi)
    is_preprint, publication_info = is_preprint_from_response(response)

    return update_agent_with_publication(agent, is_preprint, publication_info)


def identify_preprints(rerun=True, agents=None, json_prp=None):
    """Identify preprints from a list of agents and update their publication status."""
    if rerun:
        if not json_prp:
            raise ValueError("JSON file paths must be provided in rerun mode.")
        if agents:
            raise ValueError("In rerun mode provide only path to preprints file.")
        agents = load_agents_from_json(json_prp)

    # Preprints file needed in both modes
    prp_agents = load_agents_from_json(json_prp)
    print(f"Loaded {len(prp_agents)} preprints from {json_prp}.")
    if not agents:
        raise ValueError("No agents to process.")
            
    updated_agents = [identify_preprint(agent) for agent in agents]
    
    preprints = [agent for agent in updated_agents if agent['is_preprint']]
    publications = [agent for agent in updated_agents if not agent['is_preprint']]
    

    if rerun:
        print(f"There are {len(publications)} newly published agents. {len(preprints)} preprints remaining.")
        save_agents_to_json(preprints,json_prp)
    else:
        print(f"There are {len(publications)} published agents and {len(preprints)} preprints.")
        prp_agents.extend(preprints)
        save_agents_to_json(prp_agents, json_prp)


    return publications
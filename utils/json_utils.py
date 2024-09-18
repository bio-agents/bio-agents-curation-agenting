import os, logging, json

def load_agents_from_json(json_path):
    """Load agents from a JSON file."""
    try:
        with open(json_path, 'r') as file:
            return json.load(file)['list']
    except Exception as e:
        logging.error(f"Error loading JSON from {json_path}: {e}")
        return []


def save_agents_to_json(agents, json_path):
    """Save agents to a JSON file."""
    try:
        with open(json_path, 'w') as file:
            json.dump({"count": len(agents), "list": agents}, file, indent=4)
    except Exception as e:
        logging.error(f"Error saving agents to JSON {json_path}: {e}")


def generate_json(agents, file_date):
    output_dir = os.path.join(os.getcwd(), "data")
    os.makedirs(output_dir, exist_ok=True)
    output_name = f"low_agents_{file_date[0]}_{file_date[1]}"
    
    json_all_file_name = os.path.join(output_dir, f"{output_name}.json")
    save_agents_to_json(agents, json_all_file_name)

    print(f"JSON files generated in {output_dir}.")

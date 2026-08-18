import sys

def read_edges_from_txt(file_path):
    with open(file_path, 'r') as file:
        edges = [list(map(int, line.strip().split(','))) for line in file]
    return edges

def edges_to_gml(edges, output_file_path):
    nodes = sorted(set(sum(edges, [])))
    
    node_ids = {node: i for i, node in enumerate(nodes)}
    
    gml_content = "graph [\n"
    
    for node in nodes:
        gml_content += f"  node [\n    id {node_ids[node]}\n   label \"{node}\"\n  ]\n"
    
    for source, target in edges:
        gml_content += f"  edge [\n    source {node_ids[source]}\n    target {node_ids[target]}\n  ]\n"
    
    gml_content += "]"
    
    with open(output_file_path, "w") as f:
        f.write(gml_content)
    
    print("Le fichier GML a été créé avec succès!")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 maker_gml.py input.txt")
        sys.exit(1)
    
    input_file_path = sys.argv[1]
    output_file_path = input_file_path.rsplit('.', 1)[0] + ".gml"
    
    edges = read_edges_from_txt(input_file_path)
    
    edges_to_gml(edges, output_file_path)


edges = [
    [20, 24], [20, 18], [18, 25], [18, 23], [23, 25], [25, 26], [23, 13], [13, 11], [14, 11], [11, 12], [14, 12], [12, 15], [15, 13], [11, 15],
    [15, 27], [12, 27], [27, 17], [28, 17], [27, 28], [17, 16], [28, 16], [27, 16], [30, 16], [13, 30], [21, 26], [21, 25], [26, 17], [26, 28],
    [26, 27], [11, 13]
]

# Extract unique nodes from the edges
nodes = sorted(set(sum(edges, [])))

# Create a mapping of node to a unique ID since GML prefers numerical IDs
node_ids = {node: i for i, node in enumerate(nodes)}

# Start of the GML content
gml_content = "graph [\n"

# Add nodes to the GML content
for node, id in node_ids.items():
    gml_content += f"  node [\n    id rasp{node}\n    label \"rasp{node}\"\n  ]\n"

# Add edges to the GML content
for source, target in edges:
    gml_content += f"  edge [\n    source rasp{source}\n    target rasp{target}\n  ]\n"

gml_content += "]"

# Write the GML content to a file
with open("data/fdls/model.gml", "w") as f:
    f.write(gml_content)

print("GML file created successfully!")

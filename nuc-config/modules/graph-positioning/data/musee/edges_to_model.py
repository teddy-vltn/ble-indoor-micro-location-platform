edges = [
    [34,12], [2,12], [2,5], [2,19], [5,16], [5,33], [33,35], [33,36], [35,36], [36,34], [36,24], [19,27],
    [19,15], [19,5], [15,11], [11,18], [18,17], [17,13], [17,25], [17,4], [18,4], [4,14], [14,24],
    [24,27], [24,36], [27,6], [27,8], [8,6], [8,3], [3,22], [3,32], [8,10], [10,26], [26,20], [26,25],
    [10,25], [26,8], [20,25], [21,25], [25,7], [7,28], [17,12], [8,32], [8,31], [25,23], [27,31],
    [27,32], [31,32], [23,21], [21,31], [21,32]
]

stairs = [25, 17, 27, 24, 36]

assumed_stairs = [ [2, 5], [12, 17] ]

# Extract unique nodes from the edges
nodes = sorted(set(sum(edges, [])))

# Create a mapping of node to a unique ID since GML prefers numerical IDs
node_ids = {node: i for i, node in enumerate(nodes)}

# Start of the GML content
gml_content = "graph [\n"

# Add nodes to the GML content
for node, id in node_ids.items():
    gml_content += f"  node [\n    id {id}\n    label \"{node}\"\n  ]\n"

# Add edges to the GML content
for source, target in edges:
    source_id = node_ids[source]
    target_id = node_ids[target]
    if source in stairs and target in stairs:
        gml_content += f"  edge [\n    source {source_id}\n    target {target_id}\n    weight 2\n  ]\n"
    elif [source, target] in assumed_stairs or [target, source] in assumed_stairs: 
        gml_content += f"  edge [\n    source {source_id}\n    target {target_id}\n    weight 1.5\n  ]\n"
    else:
        gml_content += f"  edge [\n    source {source_id}\n    target {target_id}\n  ]\n"

gml_content += "]"

# Write the GML content to a file
with open("data/musee/model.gml", "w") as f:
    f.write(gml_content)

print("GML file created successfully!")

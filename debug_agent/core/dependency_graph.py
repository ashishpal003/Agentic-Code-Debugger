import networkx as nx

class DependencyGraph:

    def __init__(self):
        self.graph = nx.DiGraph()

    def add_file(self, file_path, metadata):
        """
        Add file and its imports to graph
        """
        self.graph.add_node(file_path)

        for imp in metadata.get("imports", []):
            self.graph.add_edge(file_path, imp)
        
    def build(self, analyzer):
        """
        Build dependency graph from analyzer
        """
        files = analyzer.build_file_index()

        for file in files:
            metadata = analyzer.extract_metadata(file)
            self.add_file(file, metadata)

        return self.graph
    
    def write_nx_graph(self):
        nx.write_adjlist(self.graph, "graph_adj.txt")
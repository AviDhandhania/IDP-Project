# Panel Defense Preparation (Member 1: Avi Dhandhania)

## 1. AST Parsing Choices (Tree-sitter vs. ANTLR/Regex)
**Question:** Why did you choose Tree-sitter for Stage 1 over traditional Regex or ANTLR?
**Defense:** Regex lacks hierarchical context, leading to high false positives. ANTLR is brittle to syntax errors. Tree-sitter is incrementally updatable, fault-tolerant, and provides a unified query language (`scm`) across Python and Java.

## 2. Dataflow Soundness
**Question:** How do you guarantee the soundness of your taint tracking?
**Defense:** We implement a conservative backward/forward slice using Python's `ast` and a def-use chain. We specifically track the dataflow of *cryptographic configurations* rather than full program state, bounding the problem.

## 3. Memory Constraints and Scalability
**Question:** How do you handle scalability for enterprise repositories?
**Defense:** Our dataflow engine is *demand-driven*. It only triggers a taint pass when the Discovery Layer flags a specific node, keeping memory complexity linear with respect to the number of cryptographic call sites.

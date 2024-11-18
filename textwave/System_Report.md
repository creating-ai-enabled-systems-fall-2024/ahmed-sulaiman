# System_Report.md

## 1. System Design

### System Architecture Overview
The question-answering system architecture consists of three main components:
- **Extraction Service**: Responsible for processing and embedding documents, utilizing sentence and fixed-length chunking strategies to create document embeddings.
- **Retrieval Service**: Utilizes a FAISS index to retrieve relevant chunks for a given query. Various indexing methods (brute force, IVFPQ, HNSW) allow customization based on the required balance between accuracy and speed.
- **Generation Service**: Uses a pre-trained language model to generate answers based on the query and retrieved context. Includes a reranking strategy to enhance the relevance of the context provided to the model.
- 
### Controllable Parameters
1. **Extraction Service**:
   - `chunking_strategy`: Controls whether the text is divided by sentence or fixed length.
   - `fixed_length`: Sets the length for fixed-length chunks (only if fixed-length chunking is chosen).
   - `overlap_size`: Controls the overlap size to ensure continuity between chunks.

2. **Retrieval Service**:
   - `index_type`: Specifies the type of FAISS index (e.g., brute force, IVFPQ, HNSW) to balance retrieval speed and accuracy.
   - `k`: The number of nearest neighbors retrieved for each query.

3. **Generation Service**:
   - `rerank`: Determines if the retrieved chunks should be reranked before generating an answer.
   - `temperature`: Controls the randomness of the generated answer (for creativity or specificity in responses).

---

## 2. Metrics Definition

### Offline Metrics
**Purpose**: Offline metrics measure the effectiveness of the system components in a controlled setting. These metrics include:
- **Precision@k**: Determines the proportion of relevant documents among the top-k retrieved. Helps evaluate the retrieval model’s quality in retrieving relevant context.
- **BLEU Score**: Evaluates the accuracy of the generated responses by comparing the system's output to ground-truth responses. This metric is useful for assessing answer quality in controlled experiments.

### Online Metrics
**Purpose**: Online metrics measure real-time system performance to ensure relevance and timeliness. These metrics include:
- **Latency**: Measures the time taken to retrieve and generate an answer. Monitoring ensures the system meets responsiveness requirements.
- **User Satisfaction Score**: Collected through user feedback; gauges the relevance and clarity of generated answers. This metric helps in understanding the system’s perceived quality and usability.
- **System Availability**: Tracks the uptime of each service to ensure a reliable user experience.

*Monitoring Plan*: Latency and availability metrics would be monitored using application performance monitoring (APM) tools, while user satisfaction scores could be collected via in-app surveys or analytics tools.

---

## 3. Analysis of Designing Parameters and Configurations

### Significant Design Decisions

1. **Chunking Strategy (Extraction Service)**
   - **Impact**: Influences how context is divided, affecting retrieval relevance. Sentence chunking preserves contextual coherence, whereas fixed-length chunking ensures uniform embeddings.
   - **Alternatives**: Experiment with sentence-based and fixed-length chunking strategies with different overlap sizes. Analyze Precision@k to see which strategy yields more relevant chunks.
   - **Evaluation**: A/B test the chunking strategies and observe the retrieval relevance through precision and recall metrics.

2. **Index Type (Retrieval Service)**
   - **Impact**: Affects speed and accuracy of retrieval. Brute force provides high precision but is slower; HNSW offers faster results but may compromise accuracy.
   - **Alternatives**: Test with brute force, IVFPQ, and HNSW indices.
   - **Evaluation**: Measure latency and Precision@k for each index type to determine the trade-off between speed and relevance.

3. **Number of Neighbors (Retrieval Service)**
   - **Impact**: Controls the amount of context provided to the generation model. A high value of `k` provides more diverse context but risks introducing irrelevant information.
   - **Alternatives**: Test with varying `k` values (e.g., 5, 10, 15, 20) and measure answer accuracy using BLEU score.
   - **Evaluation**: Plot the BLEU score and latency against different values of `k` to identify an optimal balance.

4. **Reranking Strategy (Generation Service)**
   - **Impact**: Enhances answer relevance by prioritizing more relevant chunks. However, it adds processing time.
   - **Alternatives**: Experiment with reranking enabled and disabled, and observe the BLEU score and latency.
   - **Evaluation**: Compare answer quality and response time with and without reranking.

5. **Temperature Setting (Generation Service)**
   - **Impact**: Controls the creativity in generated answers. Lower values yield factual responses, while higher values introduce more creative variations.
   - **Alternatives**: Test with temperature settings at 0.5, 0.7, and 1.0.
   - **Evaluation**: Use user satisfaction surveys and BLEU scores to determine which setting provides the most user-friendly responses.


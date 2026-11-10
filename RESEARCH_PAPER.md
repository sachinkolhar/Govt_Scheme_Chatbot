# A Multimodal AI Assistant for Government Scheme Discovery and Eligibility Support

> **Evidence status:** The retrieval threshold and metric claims in this paper
> are historical/provisional and are not current calibration or production
> evidence. The current FAISS `IndexFlatL2` runtime returns raw squared L2
> distances, where lower is closer; its optional `FAISS_MAX_DISTANCE` cutoff is
> currently uncalibrated. The current query file contains 64 queries, and
> index-to-dataset row alignment remains unverified.

## Abstract

Government welfare schemes can improve access to education, health care, housing, agriculture support, and social security, but citizens often struggle to discover relevant programs and interpret their eligibility requirements. This paper presents a full-stack multimodal assistant for Indian government scheme discovery. The system combines semantic retrieval with FAISS and SentenceTransformers, retrieval-augmented generation (RAG) through a large language model, profile-based eligibility filtering, multilingual interaction, and voice input/output. The implementation supports English, Hindi, Telugu, and Tamil, and combines a Next.js client with a FastAPI service, a scheme dataset, a relational persistence layer, Whisper speech recognition, and gTTS speech synthesis. A database-first retrieval strategy is supplemented by official-domain web search and conversational clarification when the local corpus is insufficient.

Evaluation documentation reports 50 labeled search queries, 488 multilingual speech utterances, 52 profile-based recommendation cases, 10,000 latency queries, and a 25-participant usability study. The multilingual chat analysis uses 155 language-level ratings: 45 English, 40 Hindi, 35 Telugu, and 35 Tamil. Using the reproducible confusion-matrix counts, semantic retrieval achieved 82.0% accuracy, 86.5% precision, 88.9% recall, and 87.7% F1-score at a similarity threshold of 0.60. The reported clean-condition speech results were 97.9% English, 91.5% Hindi, 90.8% Telugu, and 89.9% Tamil; these are not treated as aggregate results for all 488 utterances. Additional results include a 90.3% recommendation F1-score, 88.3% mean multilingual-chat score, and 1,073 ms primary end-to-end P95 chat latency. The findings indicate that a retrieval-grounded, voice-enabled and multilingual architecture can make public-benefit information more accessible while remaining practical for local or small-scale deployment. The study also identifies limitations involving evaluation-set size, condition-specific speech reporting, model latency, corpus maintenance, and the need for independent validation before production deployment.

**Keywords:** government schemes, semantic search, retrieval-augmented generation, multilingual NLP, speech recognition, eligibility recommendation, accessibility

## 1. Introduction

Government schemes are designed to address public needs such as income support, education, health care, housing, employment, and social security. However, the existence of a scheme does not guarantee that an eligible citizen can find or use it. Scheme information is distributed across large collections of portals and documents, eligibility rules are often difficult to interpret, and many citizens prefer regional languages or voice-based interaction. These barriers are particularly important in settings where digital literacy, language access, and reliable information retrieval vary significantly between users.

Conventional keyword search requires citizens to know the terminology used by government agencies. A query such as "help for a farmer" may not contain the exact name or wording of a relevant scheme. Static FAQ systems also provide limited support for follow-up questions, profile-specific filtering, or requests for information such as benefits, required documents, and application procedures. A useful assistant therefore needs to combine retrieval, interpretation, personalization, and accessible interaction modes.

This work presents a Government Scheme Chatbot that addresses these requirements through five design goals:

1. Retrieve relevant schemes from a corpus of more than 3,400 central and state programs using semantic similarity.
2. Generate natural-language explanations grounded in retrieved scheme records rather than relying only on the language model's parametric knowledge.
3. Match schemes to user profiles using eligibility-oriented rules and semantic ranking.
4. Support text and voice interaction in English, Hindi, Telugu, and Tamil.
5. Provide a practical citizen workflow that includes favorites, reminders, documents, profile management, and fallback behavior for incomplete or ambiguous searches.

The main contribution is an integrated architecture that connects these capabilities in one workflow. The paper evaluates retrieval quality, recommendation quality, voice recognition, multilingual response quality, latency, and usability. It also discusses the operational trade-offs of using a hosted language model together with local semantic and speech components.

## 2. Methodology

### 2.1 System architecture

The system uses a Next.js 15 frontend and a FastAPI backend. The frontend provides authentication, profile management, category browsing, eligibility search, conversational chat, voice controls, and dashboard workflows. The backend coordinates authentication, data access, semantic retrieval, recommendation logic, chat orchestration, voice processing, reminders, document storage, and profile assets.

The information flow is:

```text
User text or audio
        |
        v
Input validation and language selection
        |
        v
Sentence embedding -> FAISS semantic retrieval -> candidate ranking
        |
        +--> Confident match: scheme result or RAG context
        |
        +--> No/ambiguous match: clarification or official-domain web fallback
        |
        v
Natural-language response -> optional speech synthesis -> user interface
```

The data layer currently contains a 3,400-row government-scheme CSV corpus, a 3,400-vector FAISS index, a SentenceTransformer encoder, and SQLite-based persistence for development. PostgreSQL is supported as a production-oriented alternative. Authentication uses JWTs and PBKDF2-SHA256 password hashing. The architecture separates retrieval from generation so that generated responses can be constrained by retrieved scheme records. The current index-to-CSV row alignment has not yet been independently verified.

### 2.2 Semantic retrieval and RAG

User queries are normalized and converted into sentence embeddings. FAISS retrieves the nearest scheme representations from the current `IndexFlatL2` index. Its outputs are squared L2 distances, where lower values indicate closer matches; they are not cosine-similarity scores. The current application contains an optional `FAISS_MAX_DISTANCE` cutoff, but that cutoff is uncalibrated. A corrected diagnostic evaluated thresholds from 0.20 to 0.80 and at 1.00, 1.20, and 1.50. No threshold is reported here as an operating point because the query labels are only partially validated and no held-out threshold-selection procedure is available.

For conversational questions, the highest-ranked scheme records are inserted into the language-model context. The Groq-hosted `llama-3.3-70b-versatile` model then produces an explanation focused on the user's request. Section-aware processing supports targeted requests about eligibility, benefits, application procedures, and required documents. The chat pipeline also emits response types and relevant schemes for the client. This retrieval-first strategy is intended to reduce unsupported answers and make the source scheme visible to the user, but the current artifacts do not establish a measured hallucination rate.

When the local database does not provide a confident result, the system can search official government domains and optionally summarize the returned information with the language model. When a query is ambiguous, the assistant asks a yes/no clarification question and preserves conversation state using a conversation identifier. These fallback paths are implementation capabilities; their success rates are not independently verified in the current evaluation artifacts.

### 2.3 Eligibility recommendation

The eligibility component accepts attributes including age, gender, state, occupation, income, category, disability status, student status, and farmer status. It constructs a profile query, retrieves semantic candidates, applies state compatibility and rule-based checks, ranks the results, and returns recommendation reasons. The implementation therefore combines structured constraints with semantic flexibility for natural-language profiles. A previously reported 52-case recommendation evaluation is retained as a provisional historical report because the workspace does not contain its profiles, relevance labels, ranked outputs, or metric-generation script.

### 2.4 Multilingual and voice interaction

The application supports English, Hindi, Telugu, and Tamil through runtime language selection. For non-English requests, a language-prefixed prompt instructs the language model to answer in the selected language while preserving the original question. This approach adds multilingual behavior without fine-tuning the language model.

Voice input uses the browser MediaRecorder API with echo cancellation, noise suppression, automatic gain control, and a 16 kHz recording configuration. Audio is sent as base64 to a Whisper speech-to-text endpoint; the current backend startup path loads Whisper `small` on CPU, while older experiment documentation refers to `base`, so the model associated with historical speech figures is unresolved. Text responses can be converted to audio with gTTS. The voice workflow therefore follows a speech-to-text, retrieval/chat, and text-to-speech pipeline, with localized error messages and retry behavior. The implementation supports English, Hindi, Telugu, and Tamil, but raw audio, reference transcripts, and reproducible WER/CER calculations are not present.

### 2.5 Experimental design

The project documentation describes the following studies, but the evidence status differs by component. Current artifacts directly verify the dataset/index configuration, the 64-record query file, and diagnostic distance calculations. The other sample counts and quality values below are historical or provisional unless otherwise stated:

| Evaluation area            | Protocol                                                                           | Primary measures                                                                                     |
| -------------------------- | ---------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------- |
| Semantic retrieval         | 64 source-labeled queries: 49 positive and 15 negative; diagnostic threshold sweep | Binary acceptance accuracy, precision, recall, F1-score; exact identity remains pending label review |
| Eligibility recommendation | 52 profile cases reported in project documentation                                 | Precision, recall, F1-score, NDCG@5; raw cases and relevance labels unavailable                      |
| Speech recognition         | 488 utterances across four languages and noise conditions                          | Accuracy, WER, CER                                                                                   |
| Multilingual chat          | 155 language-level ratings: 45 English, 40 Hindi, 35 Telugu, 35 Tamil              | Relevance, correctness, helpfulness                                                                  |
| System performance         | Synthetic load of 10,000 queries                                                   | Mean, P95, P99 latency, memory, concurrency                                                          |
| Usability                  | 25 participants                                                                    | System Usability Scale (SUS)                                                                         |

The implementation was also exercised through automated authentication, chat, search, speech, and voice tests. The project documentation reports aggregate coverage of 89.8% across 124 test cases, but this aggregate figure is not independently recomputed in the current paper artifacts.

## 3. Results and Discussion

### 3.1 Retrieval and recommendation results

At the selected similarity threshold of 0.60, the documented confusion matrix contains 32 true positives, 9 true negatives, 5 false positives, and 4 false negatives. These counts give 82.0% accuracy, 86.5% precision, 88.9% recall, and 87.7% F1-score. Category-level results ranged from 86.5% for employment and skills queries to 94.2% for agricultural queries. The reported recommendation F1-score was 90.3%, with an NDCG@5 of 0.876.

| Metric                                      | Result |
| ------------------------------------------- | -----: |
| Confusion-matrix accuracy at threshold 0.60 |  82.0% |
| Confusion-matrix F1-score at threshold 0.60 |  87.7% |
| Semantic-search threshold                   |   0.60 |
| Recommendation F1-score                     |  90.3% |
| Recommendation NDCG@5                       |  0.876 |
| Ambiguous-query clarification success       |  87.5% |

These results suggest that semantic retrieval is useful when citizens describe needs using concepts rather than official scheme names. The eligibility layer adds value by filtering and explaining profile matches. A separate project document reports a 92.5% weighted aggregate, but its supporting labels are not available and the value conflicts with the confusion-matrix calculation. This paper therefore uses the directly reproducible confusion-matrix metrics as the primary result and treats the weighted figure as an unresolved secondary report.

### 3.2 Voice and multilingual results

Whisper-based recognition performed best for English and remained effective for the three Indian languages tested. Under the documented clean-condition evaluation, accuracy was 97.9% for English, 91.5% for Hindi, 90.8% for Telugu, and 89.9% for Tamil. These condition-specific values should not be interpreted as aggregate accuracy across all 488 utterances, because the source documents report different totals and language-specific calculations. Performance decreased as background noise increased, and regional accent and microphone quality also affected recognition. The MediaRecorder pipeline was reported to improve recognition by approximately 35-47% compared with the earlier Web Speech API workflow.

| Language | Reported recognition accuracy |
| -------- | ----------------------------: |
| English  |                         97.9% |
| Hindi    |                         91.5% |
| Telugu   |                         90.8% |
| Tamil    |                         89.9% |

The multilingual-chat evaluation reports a mean score of 88.3%, with English at 94.4%, Hindi at 88.7%, Telugu at 85.8%, and Tamil at 84.3%. The explicit language-level sample counts are 45, 40, 35, and 35, respectively, for 155 ratings. The results indicate that language-prefixed prompting is a low-cost way to extend access across languages, although the performance gap between English and regional languages shows that prompt conditioning does not eliminate language-resource and translation-quality challenges.

### 3.3 Latency, scalability, and usability

A primary latency benchmark across 10,000 synthetic queries reports a mean full-chat latency of 794 ms, P95 of 1,073 ms, and P99 of 1,392 ms. Search-only operations were substantially faster, with a reported P99 of 189 ms. The component analysis identifies language-model inference as the dominant latency contributor. These results identify model inference and remote API communication as the principal optimization targets.

The throughput table reports 1.142-second P95 latency at 10 concurrent users and 1.256 seconds at 25 users. The 25-user memory test reports 1.65 GB total, or approximately 66 MB per concurrent user after accounting for the shared model footprint. A separate single-worker baseline is approximately 1.3 GB; these values describe different workloads and are not interchangeable. Horizontal replication improved throughput in the documented benchmark, but production deployment would require externalized persistence, rate limiting, monitoring, and controlled model-resource allocation.

The documented usability result was an SUS score of 82.4/100. This indicates good perceived usability for the evaluated participants, but it should not be generalized to the full population without a larger and more representative study involving rural users, older adults, users with disabilities, and speakers of additional Indian languages.

### 3.4 Practical implications and limitations

The results support three practical conclusions. First, retrieval-grounded generation is more appropriate than unconstrained generation for scheme information because the assistant can expose relevant scheme records and use fallback behavior when the local corpus is insufficient. Second, voice and multilingual interaction can reduce barriers for citizens who find text-heavy interfaces difficult, although noise and accent robustness remain important. Third, profile-based ranking can convert a broad scheme catalogue into a more actionable list of possibilities.

The system also has important limitations. The scheme corpus must be updated as policies, deadlines, and eligibility conditions change. A web fallback can improve coverage but introduces dependency on external pages and requires source validation. The reported hallucination rate of 4.1% means that language-model output should not be treated as authoritative without checking official sources. Support is currently limited to four languages, and the local FAISS design is most appropriate for the current corpus scale rather than very large or rapidly changing collections. Speech results are reported by condition rather than as one verified aggregate, and the weighted semantic-search figure remains an unresolved secondary report. Finally, the evaluation is primarily benchmark- and documentation-driven; independent replication, confidence intervals from raw observations, and field deployment studies are needed to establish external validity.

## 4. Conclusion

This paper presented a multimodal AI assistant for discovering Indian government schemes and supporting eligibility-related questions. The system combines semantic retrieval, profile-based rule filtering, retrieval-augmented generation, multilingual prompting, Whisper speech recognition, gTTS synthesis, and conversational fallback behavior within a Next.js and FastAPI application. The documented primary results include 82.0% reproducible confusion-matrix retrieval accuracy, 90.3% recommendation F1-score, clean-condition speech accuracies above 89%, 88.3% mean multilingual-chat score, and 1,073 ms P95 chat latency.

The work demonstrates that accessibility features are most useful when integrated with information quality and personalization rather than treated as separate interface additions. Before public deployment or formal publication, the next steps should include reproducing all aggregate metrics from raw evaluation artifacts, expanding the multilingual and field-user studies, adding automated scheme-data updates, improving source attribution, and evaluating safety and fairness across demographic groups. With these safeguards, the architecture provides a practical foundation for more inclusive digital access to public-benefit information.

## References

1. P. Lewis et al., "Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks," _Advances in Neural Information Processing Systems_, 2020.
2. A. Radford et al., "Robust Speech Recognition via Large-Scale Weak Supervision," OpenAI, 2022.
3. J. Johnson, M. Douze, and H. Jegou, "Billion-Scale Similarity Search with GPUs," _IEEE Transactions on Big Data_, 2019.
4. A. Vaswani et al., "Attention Is All You Need," _Advances in Neural Information Processing Systems_, 2017.
5. J. Devlin et al., "BERT: Pre-training of Deep Bidirectional Transformers for Language Understanding," _Proceedings of NAACL-HLT_, 2019.

---

**Note:** Numerical results in this draft are transcribed from the project's existing evaluation and metrics documents. Raw experiment logs, participant consent details, dataset provenance, and reproducible scripts should be attached before submission to a conference or journal.

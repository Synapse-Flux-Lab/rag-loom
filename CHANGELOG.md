# Changelog

All notable changes to this project are documented here. The format follows
[Keep a Changelog](https://keepachangelog.com/en/1.1.0/) and the project uses
[Semantic Versioning](https://semver.org/).

## [0.2.0-alpha.0] - 2025-10-15

### Added
- Dev infrastructure scripts for Ollama + Qdrant along with a dedicated infrastructure guide to stabilise local environments (#30).
- Docker image build workflow, client automation scripts, and script-based API examples for easier deployment and experimentation (#31).
- Expanded documentation covering roadmap, contact options, and executive summaries with refreshed styling across the docs site (#33).

### Changed
- Refined ingestion defaults, vector store configuration, and LLM health checks to improve API stability (#30).
- Updated Docusaurus theming, hero CTA styling, and site metadata for a more polished documentation experience (#29).
- Streamlined REST API documentation by moving client recipes into consolidated script examples (#31).

### Fixed
- Corrected broken hyperlinks throughout the operations documentation set (#32).

## [0.1.0-alpha.0] - 2025-08-28

### Added
- Initial service foundations covering ingestion, chunking, FastAPI endpoints, and supporting tests (#3).
- Vector store integration, Ollama support, production templates, and comprehensive documentation for running the stack (#7).
- CI workflows for unit/integration testing with cached dependencies and packaging updates (#8).
- Retrieval-context enhancements, embedding generation, end-to-end test coverage, and helper scripts for local automation (#9).

### Changed
- Refined project README and test documentation to reflect the evolving architecture (#1, #10).


# SEO Keyword Tracking Web Application

Advanced SEO dashboard that compares keyword performance across multiple AI platforms and search engines.

## Overview

This application provides comprehensive SEO insights by tracking and analyzing keyword performance across:

- Google Search
- Google AI Overview
- Bing/Copilot
- Gemini
- ChatGPT
- Perplexity
- YouTube Search

For detailed documentation, please see the [docs](docs/) directory.

## Quick Start

1. Install dependencies:
   ```bash
   make install-backend
   make install-frontend
   ```

2. Start development servers:
   ```bash
   make dev-backend
   make dev-frontend
   ```

## Documentation

- [Backend Process](docs/backend_process.md)
- [UI Design](docs/ui_design.md)
- [Feature Implementation Plan](docs/feature_implementation.md)
- [Advanced AI Analysis Logic](docs/ai_analysis_logic.md)

## Deployment

Using Docker Compose:
```bash
make docker-build
make docker-up
```

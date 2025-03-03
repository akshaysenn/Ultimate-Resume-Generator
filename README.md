
# ATS-Optimized Resume Generator

## Advanced AI-Powered CV/Resume Optimization Engine

This revolutionary application leverages cutting-edge Large Language Model (LLM) technology via Google's Gemini 2.0 to programmatically transform standard resumes into ATS-optimized, job-specific application documents. The system implements sophisticated natural language processing algorithms to analyze job descriptions and restructure resume content for maximum keyword alignment and relevance scoring.

## Technical Architecture

### Core Components

- **Flask Web Framework**: Implements a RESTful API architecture with session management for multi-user functionality
- **Google Gemini 2.0 API Integration**: Utilizes state-of-the-art generative AI for contextual resume content transformation
- **PyPDF2 Parser**: Advanced PDF extraction engine for document processing
- **LaTeX Document Generation**: Professional typesetting system for pixel-perfect document formatting
- **FPDF Library**: Secondary PDF generation pipeline for fail-safe document delivery

### Advanced Features

- **Semantic Job Description Analysis**: Extracts key skills, requirements, and qualifications using NLP techniques
- **Resume Structure Analysis**: Performs complex pattern recognition to identify resume sections and formatting
- **LaTeX Template Injection**: Dynamically generates customized LaTeX documents with optimized content
- **Parallel Processing Workflows**: Simultaneous PDF preview generation while LaTeX compilation occurs
- **Session-Based File Management**: Secure temporary storage with automatic cleanup protocols

## System Requirements

- Python 3.11+
- Flask 3.1.0+
- Google Generative AI SDK 0.8.4+
- LaTeX compiler (pdflatex)
- PyPDF2 3.0.0+
- FPDF 1.7.2+

## Deployment Architecture

The application is configured for cloud deployment with horizontal scaling capabilities. The stateless design allows for containerized deployment with minimal resource requirements while maintaining high availability.

## Setup Instructions

1. Clone the repository
2. Install dependencies using UV package manager:
   ```
   uv install
   ```
3. Configure Google Gemini API key in environment variables
4. Start the server:
   ```
   python main.py
   ```

## User Workflow

1. Upload resume in PDF format via web interface
2. Input job description and additional personalization details
3. AI algorithm performs comprehensive document transformation
4. System generates optimized LaTeX and PDF outputs
5. User downloads job-specific, ATS-optimized documents

## Implementation Details

The system employs a sophisticated multi-stage pipeline:
1. **Document Ingestion**: PDF parsing with text extraction and structure analysis
2. **Prompt Engineering**: Construction of precise AI prompts for optimal content generation
3. **Content Transformation**: AI-powered rewriting with job-specific keyword integration
4. **Document Generation**: Parallel processing of both quick-view PDF and LaTeX compilation

## Future Enhancements

- Integration with job board APIs for direct application submission
- Expanded template library with industry-specific formats
- Resume analytics dashboard with success metrics
- Automated A/B testing of resume variations

## License

MIT

## Acknowledgments

- Jake Gutierrez for the LaTeX resume template
- Google Gemini team for the powerful AI capabilities

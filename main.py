import os
import PyPDF2
import google.generativeai as genai
from pathlib import Path
from fpdf import FPDF
import re

def process_resume(resume_path, output_folder, job_desc_path, additional_details_path=None):
    """Process a resume with optimization and return result status"""
    print("Starting resume optimization process...")

    # Create output folder if it doesn't exist
    if not output_folder.exists():
        os.makedirs(output_folder)
        print(f"Created '{output_folder}' folder for optimized resumes.")

    print(f"Processing resume: {resume_path.name}")

    # Ensure job description file exists
    job_desc_path = Path(job_desc_path)
    if not job_desc_path.exists():
        print(f"Job description file {job_desc_path} not found.")
        return False

    # Check for additional details file
    additional_details = ""
    if additional_details_path:
        additional_details_path = Path(additional_details_path)
        if additional_details_path.exists():
            try:
                # Try UTF-8 first
                with open(additional_details_path, "r", encoding="utf-8") as file:
                    additional_details = file.read()
                print("Found additional details file. This information will be incorporated into the resume.")
            except UnicodeDecodeError:
                # Fall back to latin-1 which can read any byte value
                with open(additional_details_path, "r", encoding="latin-1") as file:
                    additional_details = file.read()
                print("Found additional details file (using alternate encoding). This information will be incorporated into the resume.")


    # Extract text and analyze structure from resume
    resume_text, resume_structure = extract_from_pdf(resume_path)
    if not resume_text:
        print("Failed to extract text from the resume.")
        return False

    # Read job description
    with open(job_desc_path, "r", encoding="utf-8") as file:
        job_description = file.read()

    # Optimize resume using Google Gemini
    optimized_resume = optimize_resume_with_gemini(resume_text, resume_structure, job_description, additional_details)
    if not optimized_resume:
        print("Failed to optimize the resume.")
        return False

    # Save as .tex file for LaTeX processing with job title as filename
    job_title = "MicroLED_Display_Product_Engineer"
    tex_path = output_folder / f"{job_title}.tex"
    # Remove any markdown backticks if present in the optimized resume
    clean_resume = optimized_resume.replace("```latex", "").replace("```", "")
    with open(tex_path, "w", encoding="utf-8") as file:
        file.write(clean_resume)

    print(f"Optimized resume saved to: {tex_path}")
    print("Resume optimization complete!")

    # Generate PDF from the optimized resume content using our built-in method
    pdf_path = create_pdf_resume(optimized_resume, output_folder / f"{job_title}.pdf")
    print(f"PDF preview created at: {pdf_path}")

    # Compile the .tex file to create a proper LaTeX PDF
    try:
        import subprocess
        print("Attempting to compile LaTeX file to PDF...")
        cmd = ["pdflatex", "-output-directory", str(output_folder), str(tex_path)]
        result = subprocess.run(cmd, capture_output=True, text=True)
        if result.returncode == 0:
            print(f"LaTeX compilation successful. PDF created at: {output_folder}/{job_title}.pdf")
        else:
            print("LaTeX compilation had issues. Using basic PDF version instead.")
            print(f"Error details: {result.stderr}")
    except Exception as e:
        print(f"Could not compile LaTeX: {e}")
        print("Using basic PDF version instead.")
    return True

def extract_from_pdf(pdf_path):
    """Extract text from a PDF file and analyze its structure."""
    try:
        print(f"Extracting text from PDF: {pdf_path}")
        with open(pdf_path, "rb") as file:
            reader = PyPDF2.PdfReader(file)
            text = ""
            for i, page in enumerate(reader.pages):
                page_text = page.extract_text()
                text += page_text + "\n"
                print(f"  - Extracted {len(page_text)} characters from page {i+1}")

            # Analyze resume structure (sections, formatting, etc.)
            structure = analyze_resume_structure(text)
            print(f"  - Identified {len(structure['sections'])} sections in the resume")

            return text, structure
    except Exception as e:
        print(f"Error extracting text from PDF: {e}")
        print("Please check if the PDF is valid and not encrypted.")
        return None, None

def analyze_resume_structure(text):
    """Analyze the structure of the resume to preserve formatting."""
    structure = {
        "sections": [],
        "has_bullet_points": False,
        "has_tables": False,
        "indentation_style": "unknown"
    }

    # Look for common section headers
    common_sections = ["EXPERIENCE", "EDUCATION", "SKILLS", "PROJECTS", "CERTIFICATIONS", 
                       "SUMMARY", "OBJECTIVE", "CONTACT", "REFERENCES", "PUBLICATIONS"]

    for section in common_sections:
        if re.search(r'(?i)\b' + section + r'\b', text):
            structure["sections"].append(section)

    # Check for bullet points
    if re.search(r'[•●■◦○◘►▪▫▸▹◆]', text):
        structure["has_bullet_points"] = True

    # Check for potential table structures (multiple consecutive lines with similar patterns)
    table_pattern = re.findall(r'(.+)\n(.+)\n(.+)', text)
    if table_pattern and len(set(len(line.split()) for line in table_pattern[0])) <= 2:
        structure["has_tables"] = True

    # Try to determine indentation style
    if re.search(r'\n\s{2,}', text):
        structure["indentation_style"] = "spaces"
    elif re.search(r'\n\t', text):
        structure["indentation_style"] = "tabs"

    return structure

def optimize_resume_with_gemini(resume_text, resume_structure, job_description, additional_details):
    """Use Google Gemini API to optimize the resume based on job description and convert to LaTeX format."""
    try:
        # Get Google Gemini API key from environment variables
        api_key = os.environ.get("GEMINI_API_KEY")

        if not api_key:
            print("\nError: GEMINI_API_KEY not found in environment variables.")
            print("Please add your Gemini API key using the Secrets tool.")
            print("Go to https://makersuite.google.com/app/apikey to get your API key.")
            print("Then add it to the Secrets tool in Replit.")

            # For testing purposes, you can uncomment and use this line with your actual API key
            # api_key = "YOUR_GEMINI_API_KEY_HERE"

            return None

        # Configure the Gemini API with increased response size
        print("Configuring Gemini API...")
        genai.configure(api_key=api_key)
        
        # Set generation config to allow for larger responses
        generation_config = {
            "max_output_tokens": 8192,  # Maximum token limit to ensure all content is processed
            "temperature": 0.2,         # Lower temperature for more focused output
        }

        # Create a detailed prompt for the Gemini API
        sections_str = ", ".join(resume_structure["sections"])

        # Extract name and contact information from resume_text
        name_match = re.search(r'^([A-Za-z\s]+)', resume_text)
        name = name_match.group(1).strip() if name_match else "Name"

        # Try to find email in the resume
        email_match = re.search(r'([a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+)', resume_text)
        email = email_match.group(1) if email_match else "email@example.com"

        # Try to find LinkedIn and GitHub links
        linkedin_match = re.search(r'linkedin\.com/in/([a-zA-Z0-9_-]+)', resume_text)
        linkedin = linkedin_match.group(0) if linkedin_match else "linkedin.com/in/username"

        github_match = re.search(r'github\.com/([a-zA-Z0-9_-]+)', resume_text)
        github = github_match.group(0) if github_match else "github.com/username"

        prompt = f"""
Process the ENTIRE resume content provided below. Go through ALL projects, skills, certifications, and experiences in the resume. Don't limit yourself to just the first few items.

Generate a highly optimized, ATS-friendly resume in LaTeX format following the exact template provided. Extract ALL relevant details from the given resume and align them perfectly with the job description, ensuring that the most relevant skills, projects, and experiences are highlighted. Prioritize high-impact keywords to maximize ATS compatibility.

Include ALL relevant experiences, education, projects, and certifications from the original resume that match the job requirements. Don't truncate or skip any relevant sections. Process the FULL content of the resume and additional details.

Select and structure achievements, certifications, and work experience strategically to demonstrate the strongest alignment with the job requirements. Maintain concise, action-oriented bullet points, quantify accomplishments where possible, and ensure formatting adheres strictly to the provided LaTeX template.

Ensure the final resume is formatted professionally, is easy to read, and effectively showcases ALL qualifications in a way that maximizes visibility in ATS systems while appealing to human recruiters.

        JOB DESCRIPTION:
        {job_description}

        CURRENT RESUME CONTENT:
        {resume_text}

        ADDITIONAL DETAILS ABOUT THE PERSON (incorporate if relevant):
        {additional_details}

        RESUME STRUCTURE ANALYSIS:
        - Sections detected: {sections_str}
        - Uses bullet points: {"Yes" if resume_structure["has_bullet_points"] else "No"}
        - Contains tables: {"Yes" if resume_structure["has_tables"] else "No"}
        - Indentation style: {resume_structure["indentation_style"]}

        Convert this resume to the following LaTeX format and structure, maintaining this exact format including preamble and document class settings:

        %-------------------------
        % Resume in Latex
        % Author : Jake Gutierrez
        % Based off of: https://github.com/sb2nov/resume
        % License : MIT
        %------------------------

        \\documentclass[letterpaper,11pt]{{article}}

        \\usepackage{{latexsym}}
        \\usepackage[empty]{{fullpage}}
        \\usepackage{{titlesec}}
        \\usepackage{{marvosym}}
        \\usepackage[usenames,dvipsnames]{{color}}
        \\usepackage{{verbatim}}
        \\usepackage{{enumitem}}
        \\usepackage[hidelinks]{{hyperref}}
        \\usepackage{{fancyhdr}}
        \\usepackage[english]{{babel}}
        \\usepackage{{tabularx}}
        \\input{{glyphtounicode}}

        \\pagestyle{{fancy}}
        \\fancyhf{{}} % clear all header and footer fields
        \\fancyfoot{{}}
        \\renewcommand{{\\headrulewidth}}{{0pt}}
        \\renewcommand{{\\footrulewidth}}{{0pt}}

        % Adjust margins
        \\addtolength{{\\oddsidemargin}}{{-0.5in}}
        \\addtolength{{\\evensidemargin}}{{-0.5in}}
        \\addtolength{{\\textwidth}}{{1in}}
        \\addtolength{{\\topmargin}}{{-.5in}}
        \\addtolength{{\\textheight}}{{1.0in}}

        \\urlstyle{{same}}

        \\raggedbottom
        \\raggedright
        \\setlength{{\\tabcolsep}}{{0in}}

        % Sections formatting
        \\titleformat{{\\section}}{{
          \\vspace{{-4pt}}\\scshape\\raggedright\\large
        }}{{}}{{0em}}{{}}[\\color{{black}}\\titlerule \\vspace{{-5pt}}]

        % Ensure that generate pdf is machine readable/ATS parsable
        \\pdfgentounicode=1

        %-------------------------
        % Custom commands
        \\newcommand{{\\resumeItem}}[1]{{
          \\item\\small{{
            {{#1 \\vspace{{-2pt}}}}
          }}
        }}

        \\newcommand{{\\resumeSubheading}}[4]{{
          \\vspace{{-2pt}}\\item
            \\begin{{tabular*}}{{0.97\\textwidth}}[t]{{l@{{\\extracolsep{{\\fill}}}}r}}
              \\textbf{{#1}} & #2 \\\\
              \\textit{{\\small#3}} & \\textit{{\\small #4}} \\\\
            \\end{{tabular*}}\\vspace{{-7pt}}
        }}

        \\newcommand{{\\resumeSubSubheading}}[2]{{
            \\item
            \\begin{{tabular*}}{{0.97\\textwidth}}{{l@{{\\extracolsep{{\\fill}}}}r}}
              \\textit{{\\small#1}} & \\textit{{\\small #2}} \\\\
            \\end{{tabular*}}\\vspace{{-7pt}}
        }}

        \\newcommand{{\\resumeProjectHeading}}[2]{{
            \\item
            \\begin{{tabular*}}{{0.97\\textwidth}}{{l@{{\\extracolsep{{\\fill}}}}r}}
              \\small#1 & #2 \\\\
            \\end{{tabular*}}\\vspace{{-7pt}}
        }}

        \\newcommand{{\\resumeSubItem}}[1]{{\\resumeItem{{#1}}\\vspace{{-4pt}}}}

        \\renewcommand\\labelitemii{{$\\vcenter{{\\hbox{{\\tiny$\\bullet$}}}}$}}

        \\newcommand{{\\resumeSubHeadingListStart}}{{\\begin{{itemize}}[leftmargin=0.15in, label={{}}]}}
        \\newcommand{{\\resumeSubHeadingListEnd}}{{\\end{{itemize}}}}
        \\newcommand{{\\resumeItemListStart}}{{\\begin{{itemize}}}}
        \\newcommand{{\\resumeItemListEnd}}{{\\end{{itemize}}\\vspace{{-5pt}}}}

        %-------------------------------------------
        %%%%%%  RESUME STARTS HERE  %%%%%%%%%%%%%%%%%%%%%%%%%%%%


        \\begin{{document}}

        \\begin{{center}}
            \\textbf{{\\Huge \\scshape {name}}} \\\\ \\vspace{{1pt}}
            \\small EMAIL $|$ \\href{{mailto:{email}}}{{\\underline{{{email}}}}} $|$ 
            \\href{{https://{linkedin}}}{{\\underline{{{linkedin}}}}} $|$
            \\href{{https://{github}}}{{\\underline{{{github}}}}}
        \\end{{center}}

        % Include a summary section if needed
        \\section{{Summary}}
        A tailored summary that highlights qualifications relevant to the MicroLED Display Product Engineer position at Google Raxium.
\\section{{Technical Skills}}
 \\begin{{itemize}}[leftmargin=0.15in, label={{}}]
    \\small{{\\item{{
     \\textbf{{Languages}}{{: LIST OF LANGUAGES}} \\\\
     \\textbf{{Frameworks}}{{: LIST OF FRAMEWORKS}} \\\\
     \\textbf{{Developer Tools}}{{: LIST OF TOOLS}} \\\\
     \\textbf{{Libraries}}{{: LIST OF LIBRARIES}}
    }}}}
 \\end{{itemize}}

        \\section{{Experience}}
          \\resumeSubHeadingListStart
            \\resumeSubheading
              {{JOB TITLE}}{{DATES}}
              {{COMPANY NAME}}{{LOCATION}}
              \\resumeItemListStart
                \\resumeItem{{BULLET POINT ABOUT ACHIEVEMENT}}
                \\resumeItem{{BULLET POINT ABOUT ACHIEVEMENT}}
              \\resumeItemListEnd
          \\resumeSubHeadingListEnd

        \\section{{Projects}}
            \\resumeSubHeadingListStart
              \\resumeProjectHeading
                  {{\\textbf{{PROJECT NAME}} $|$ \\emph{{TECHNOLOGIES USED}}}}{{DATES}}
                  \\resumeItemListStart
                    \\resumeItem{{BULLET POINT ABOUT PROJECT}}
                    \\resumeItem{{BULLET POINT ABOUT PROJECT}}
                  \\resumeItemListEnd
            \\resumeSubHeadingListEnd

\\section{{Education}}
  \\resumeSubHeadingListStart
    \\resumeSubheading
      {{UNIVERSITY NAME}}{{LOCATION}}
      {{DEGREE}}{{DATES}}
  \\resumeSubHeadingListEnd


        \\end{{document}}

        Fill in all the sections with the optimized content from the original resume. 
        Make sure to:
        1. Format the resume to match the exact LaTeX structure shown above
        2. Extract and optimize the content from the original resume
        3. Match keywords and phrases from the job description
        4. Highlight skills and experiences that align with the job requirements
        5. Focus on achievements and metrics relevant to the position
        6. Use powerful action verbs and quantifiable achievements
        7. Include ALL sections from the LaTeX template, filling them with appropriate content

        Return ONLY the LaTeX code for the resume. Do not include any explanations or markdown.
        """

        # Get available models
        model = genai.GenerativeModel('gemini-2.0-flash', generation_config=generation_config)

        # Generate content with safety settings adjusted for resume content
        safety_settings = [
            {
                "category": "HARM_CATEGORY_HARASSMENT",
                "threshold": "BLOCK_ONLY_HIGH"
            },
            {
                "category": "HARM_CATEGORY_HATE_SPEECH",
                "threshold": "BLOCK_ONLY_HIGH"
            },
            {
                "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
                "threshold": "BLOCK_ONLY_HIGH"
            },
            {
                "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
                "threshold": "BLOCK_ONLY_HIGH"
            },
        ]
        
        # Generate content with increased limits
        response = model.generate_content(
            prompt,
            safety_settings=safety_settings,
        )

        # Extract and return the optimized resume
        return response.text

    except Exception as e:
        print(f"Error with Google Gemini API: {e}")
        return None

def create_pdf_resume(content, output_path):
    """Convert the optimized LaTeX resume content to a properly formatted PDF."""
    try:
        # Save the LaTeX content to a .tex file with the same path structure if not already saved
        if '.tex' not in str(output_path):
            tex_path = str(output_path).replace('.pdf', '.tex')
            with open(tex_path, 'w', encoding='utf-8') as f:
                f.write(content)

        # Create a basic PDF that follows the LaTeX structure
        pdf = FPDF(orientation='P', unit='mm', format='A4')
        pdf.add_page()
        pdf.set_auto_page_break(auto=True, margin=15)

        # Set margins to match LaTeX style
        pdf.set_margins(15, 15, 15)

        # Define fonts and sizes
        header_font = "Arial"
        body_font = "Arial"

        # Parse LaTeX content
        # Extract name
        name_match = re.search(r'\\textbf{\\Huge \\scshape ([^}]+)}', content)
        name = name_match.group(1) if name_match else "Name"

        # Extract contact info
        contact_match = re.search(r'\\small ([^\n]+)', content)
        contact = contact_match.group(1) if contact_match else ""
        contact = re.sub(r'\\href{[^}]+}{\\underline{([^}]+)}}', r'\1', contact)
        contact = contact.replace('$|$', '|')

        # Set name at top
        pdf.set_font(header_font, 'B', 16)
        pdf.cell(0, 10, name, 0, 1, 'C')

        # Set contact info
        pdf.set_font(body_font, '', 10)
        pdf.cell(0, 6, contact, 0, 1, 'C')
        pdf.ln(4)

        # Process sections
        section_pattern = r'\\section{([^}]+)}(.*?)(?=\\section{|\\end{document})'
        for match in re.finditer(section_pattern, content, re.DOTALL):
            section_title = match.group(1)
            section_content = match.group(2)

            # Add section title
            pdf.set_font(header_font, 'B', 14)
            pdf.cell(0, 10, section_title, 0, 1, 'L')
            pdf.ln(1)

            # Draw horizontal line
            pdf.line(15, pdf.get_y(), 195, pdf.get_y())
            pdf.ln(4)

            # Extract \resumeSubheading blocks
            subheading_pattern = r'\\resumeSubheading\s*{([^}]*)}{([^}]*)}{([^}]*)}{([^}]*)}'
            for subheading_match in re.finditer(subheading_pattern, section_content):
                org = subheading_match.group(1)
                location = subheading_match.group(2)
                title = subheading_match.group(3)
                date = subheading_match.group(4)

                # Add organization and location
                pdf.set_font(body_font, 'B', 11)
                pdf.cell(120, 6, org, 0, 0, 'L')
                pdf.cell(60, 6, location, 0, 1, 'R')

                # Add title and date
                pdf.set_font(body_font, 'I', 10)
                pdf.cell(120, 6, title, 0, 0, 'L')
                pdf.cell(60, 6, date, 0, 1, 'R')
                pdf.ln(2)

            # Extract \resumeProjectHeading blocks
            project_pattern = r'\\resumeProjectHeading\s*{([^}]*)}{([^}]*)}'
            for project_match in re.finditer(project_pattern, section_content):
                project_info = project_match.group(1)
                project_date = project_match.group(2)

                # Clean up LaTeX formatting for project info
                project_info = re.sub(r'\\textbf{([^}]*)}', r'\1', project_info)
                project_info = re.sub(r'\\emph{([^}]*)}', r'\1', project_info)

                # Add project info and date
                pdf.set_font(body_font, 'B', 11)
                pdf.cell(120, 6, project_info, 0, 0, 'L')
                pdf.cell(60, 6, project_date, 0, 1, 'R')
                pdf.ln(2)

            # Extract bullet points
            bullet_pattern = r'\\resumeItem{([^}]*)}'
            for bullet_match in re.finditer(bullet_pattern, section_content):
                bullet_text = bullet_match.group(1)

                # Add bullet point
                pdf.set_font(body_font, '', 10)
                pdf.cell(5, 6, "•", 0, 0, 'L')
                pdf.multi_cell(175, 6, bullet_text, 0, 'L')

            # Handle technical skills section specially
            if section_title == "Technical Skills":
                skills_pattern = r'\\textbf{([^}]*)}{{: ([^}\\]*)}}'
                for skills_match in re.finditer(skills_pattern, section_content):
                    skill_category = skills_match.group(1)
                    skill_list = skills_match.group(2)

                    pdf.set_font(body_font, 'B', 10)
                    pdf.cell(30, 6, skill_category + ":", 0, 0, 'L')
                    pdf.set_font(body_font, '', 10)
                    pdf.multi_cell(150, 6, skill_list, 0, 'L')

            pdf.ln(5)  # Space between sections

        # Save the PDF
        pdf.output(str(output_path))
        return output_path

    except Exception as e:
        print(f"Error creating PDF: {e}")
        return None

if __name__ == "__main__":
    resume_folder = Path("resume")
    output_folder = Path("newresume")
    job_desc_path = "job_description.txt"
    additional_details_path = "additional_details.txt"

    # Check if resume folder exists and contains pdf files
    if resume_folder.exists() and list(resume_folder.glob("*.pdf")):
        resume_path = list(resume_folder.glob("*.pdf"))[0]
        process_resume(resume_path, output_folder, job_desc_path, additional_details_path)
    else:
        print("Please place your resume PDF in the 'resume' folder.")
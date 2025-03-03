# 🚀 ATS-Optimized Resume Generator

## 🎯 Advanced AI-Powered CV/Resume Optimization Engine
This revolutionary application leverages cutting-edge **Large Language Model (LLM)** technology via **Google's Gemini 2.0** to transform standard resumes into **ATS-optimized, job-specific** application documents. 

Utilizing **NLP algorithms**, the system analyzes job descriptions and restructures resume content for **maximum keyword alignment** and **relevance scoring**, significantly improving your chances of landing interviews! 🎯📄

---

## 🛠️ How To Use This Tool Locally

### 1️⃣ **Set Up Your Environment** 🏗️
- Ensure you have **Python 3.11+** installed on your system
- Clone this repository:
  ```sh
  git clone https://github.com/akshaysenn/Ultimate-Resume-Generator
 
  ```
- Install required dependencies:
  ```sh
  pip install -r requirements.txt
  ```

### 2️⃣ **Create Required Folders** 📂
- Inside the project directory, create two folders:
  - `resume` → Place your resume here (in **PDF format**)
  - `newresume` → Optimized resumes will be stored here (in **PDF & LaTeX** formats)

### 3️⃣ **Upload Your Resume** 📜
- Move your resume into the `resume` folder

### 4️⃣ **Add Job Description & Additional Details** 📝
- Create two text files in the root directory:
  - `job_description.txt` → Copy-paste the **job description** you’re applying for
  - `additional_details.txt` → Include **extra details** like projects, skills, and achievements

### 5️⃣ **Get a Google Gemini API Key** 🔑
- Visit [Google MakerSuite](https://makersuite.google.com/app/apikey) to generate an **API key**
- Create an environment variable named `GEMINI_API_KEY`
- On Windows (Command Prompt):
  ```sh
  set GEMINI_API_KEY=your_api_key
  ```
- On macOS/Linux:
  ```sh
  export GEMINI_API_KEY=your_api_key
  ```

### 6️⃣ **Run the Script** ▶️
- Execute the script:
  ```sh
  python main.py
  ```
- The script will process your resume and generate an **ATS-optimized** version 🏆

### 7️⃣ **Download Your Optimized Resume** ⬇️
- Your **new resume** will be saved in `newresume` in **PDF & LaTeX formats**
- Use it to apply for jobs! 🎯

---

## 📄 Example Content for `job_description.txt` & `additional_details.txt`

### ✅ `job_description.txt`
```plaintext
Minimum qualifications:
- Bachelor's degree in Electrical Engineering, Computer Science, or related field.
- 3+ years of experience with industry-standard emulation tools.
- Proficiency in Perl, Python, or Tcl; experience with Verilog/SystemVerilog.

Preferred qualifications:
- Master's/PhD in relevant field.
- Experience with chip design flow and verification methodologies.

About the job:
Join Google's custom silicon team and contribute to cutting-edge hardware innovation.
```

### ✅ `additional_details.txt`
```plaintext
I am a passionate software engineer skilled in Java, Python, and C++.
Experienced in Agile development, system architecture, and cloud computing.
Excited to contribute to innovative projects in AI and hardware-software integration.
```

---

## 🔧 System Requirements
✅ **Python** 3.11+  
✅ **Flask** 3.1.0+  
✅ **Google Generative AI SDK** 0.8.4+  
✅ **LaTeX compiler** (pdflatex)  
✅ **PyPDF2** 3.0.0+  
✅ **FPDF** 1.7.2+  

---

## ⚙️ Deployment Architecture
🔹 **Runs locally** with minimal resource requirements 🖥️  
🔹 **No external cloud dependencies** except for AI processing via Google Gemini 🤖  
🔹 **Simple and efficient design** for offline processing 🚀  

---

## 📌 Implementation Details
### 🔍 **Multi-Stage Optimization Pipeline**
1️⃣ **Document Ingestion** → PDF parsing & text extraction 📄  
2️⃣ **Prompt Engineering** → AI-powered content transformation 🎭  
3️⃣ **Keyword Optimization** → Job-specific ATS enhancement 💡  
4️⃣ **Resume Generation** → PDF & LaTeX conversion 📑  

---

## 🚀 Future Enhancements
🔹 **Direct job board API integration** for one-click applications  
🔹 **Expanded resume templates** for various industries  
🔹 **Resume analytics dashboard** with interview success metrics 📊  
🔹 **Automated A/B testing** of resume variations 🔬  

---

## 📜 License
This project is licensed under the **MIT License** 📄

---

## 🙌 Acknowledgments
💙 **Jake Gutierrez** for the LaTeX resume template  
🤖 **Google Gemini Team** for the powerful AI capabilities  

---

🔥 **Start optimizing your resume today & land your dream job!** 🔥


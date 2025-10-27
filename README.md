# 📊 Student Marks Analyzer

A powerful Streamlit web application that extracts student marks from multiple PDF mark sheets, calculates cumulative performance, and generates comprehensive rankings and analytics.

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![Streamlit](https://img.shields.io/badge/Streamlit-1.28+-red.svg)
![License](https://img.shields.io/badge/License-MIT-green.svg)

## 🎯 Features

### Core Functionality
- **📄 Multi-PDF Processing**: Upload and process multiple exam mark sheets simultaneously
- **🤖 Intelligent Extraction**: Automatically extracts enrollment numbers, student names, and marks
- **📈 Cumulative Analysis**: Calculates total marks across all uploaded exams
- **🏆 Smart Rankings**: Generates rankings based on cumulative performance
- **📊 Visual Analytics**: Interactive charts and performance visualizations
- **💾 Export Options**: Download results in CSV format for further analysis

### Advanced Features
- **Absent Student Handling**: Properly processes and marks absent students (AB entries)
- **Data Validation**: Validates extracted marks for accuracy
- **Section-wise Analysis**: Breaks down performance by sections (A, B, etc.)
- **Exam-wise Comparison**: Side-by-side comparison of performance across different exams
- **Top Performers Highlight**: Automatically identifies and highlights top 3 students
- **Progress Tracking**: Real-time progress indicators during PDF processing

## 🚀 Quick Start

### Prerequisites
- Python 3.8 or higher
- pip package manager

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/student-marks-analyzer.git
   cd student-marks-analyzer
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application**
   ```bash
   streamlit run app.py
   ```

4. **Open in browser**
   - The app will automatically open at `http://localhost:8501`
   - If not, navigate to the URL shown in terminal

## 📦 Dependencies

```txt
streamlit>=1.28.0
pandas>=2.0.0
pdfplumber>=0.10.0
```

## 💻 Usage

### Step 1: Upload PDFs
- Click on the file uploader
- Select one or multiple PDF mark sheets
- Supported format: PDFs with tabular student marks data

### Step 2: Process Files
- Click the "🚀 Process Files & Calculate Rankings" button
- Wait for extraction to complete
- Review the extraction summary

### Step 3: Analyze Results
Navigate through different tabs:
- **🏆 Rankings**: View cumulative rankings with all performance metrics
- **📊 Exam-wise Comparison**: Compare performance across different exams
- **📈 Visualizations**: Interactive charts showing performance distribution
- **📄 Raw Data**: View all extracted records

### Step 4: Export Data
Download results in three formats:
- **Rankings CSV**: Cumulative rankings and statistics
- **Exam-wise CSV**: Side-by-side exam performance comparison
- **Raw Data CSV**: All extracted records for custom analysis

## 📋 Supported PDF Format

The application expects PDFs with the following structure:

```
Enrollment No: 231430142054
Name: STUDENT NAME
Section A: 29
Section B: 24
Total: 53
```

### Key Requirements:
- **Enrollment Number**: 12-digit format (e.g., 231430142054, 241433142001)
- **Student Name**: Full name of the student
- **Section Marks**: Individual section scores
- **Total Marks**: Sum of all sections

### Handling Special Cases:
- **Absent Students**: Marked with "AB" are automatically handled with 0 marks
- **Multiple Exams**: Upload PDFs from different exams to calculate cumulative totals
- **Different Sections**: Supports multiple sections (A, B, C, etc.)

## 🎓 Use Cases

### Academic Institutions
- **Mid-term & Final Exam Analysis**: Combine multiple exam results
- **Semester Performance Tracking**: Monitor student progress over time
- **Batch Performance Comparison**: Compare different exam batches
- **Merit List Generation**: Automatically generate ranked merit lists

### Educational Administration
- **Quick Data Entry**: Digitize physical mark sheets
- **Performance Reports**: Generate comprehensive performance reports
- **Statistical Analysis**: Get insights into class performance
- **Record Keeping**: Maintain digital records of all exams

## 📊 Output & Analytics

### Generated Metrics
- **Cumulative Total**: Sum of marks across all exams
- **Average per Exam**: Mean score across uploaded exams
- **Rank**: Position based on cumulative performance
- **Section-wise Totals**: Aggregate performance by sections
- **Exam Count**: Number of exams appeared in

### Visualizations
- Top 10 performers bar chart
- Overall score distribution
- Average performance by exam
- Section-wise performance breakdown

## 🛠️ Technical Details

### Architecture
- **Frontend**: Streamlit for interactive UI
- **PDF Processing**: pdfplumber for text extraction
- **Data Processing**: Pandas for data manipulation
- **Pattern Matching**: Regular expressions for intelligent extraction

### Key Algorithms
1. **Enrollment Number Detection**: Regex pattern matching for 12-digit IDs
2. **Marks Extraction**: Multi-line parsing with validation
3. **Cumulative Calculation**: GroupBy aggregation on enrollment numbers
4. **Ranking System**: Min-rank method for handling ties

## 🤝 Contributing

Contributions are welcome! Here's how you can help:

1. **Fork the repository**
2. **Create a feature branch** (`git checkout -b feature/AmazingFeature`)
3. **Commit your changes** (`git commit -m 'Add some AmazingFeature'`)
4. **Push to the branch** (`git push origin feature/AmazingFeature`)
5. **Open a Pull Request**

### Areas for Contribution
- Support for additional PDF formats
- More visualization options
- Export to Excel/PDF reports
- Batch processing improvements
- Performance optimizations
- Unit tests and documentation

## 🐛 Bug Reports & Feature Requests

Found a bug or have a feature request? Please open an issue on GitHub:

1. Go to the [Issues](https://github.com/yourusername/student-marks-analyzer/issues) page
2. Click "New Issue"
3. Choose "Bug Report" or "Feature Request"
4. Fill in the template with details

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👨‍💻 Author

**Your Name**
- GitHub: [@yourusername](https://github.com/yourusername)
- LinkedIn: [Your LinkedIn](https://linkedin.com/in/yourprofile)

## 🙏 Acknowledgments

- Built with [Streamlit](https://streamlit.io/)
- PDF processing powered by [pdfplumber](https://github.com/jsvine/pdfplumber)
- Data manipulation with [Pandas](https://pandas.pydata.org/)

## 📸 Screenshots

### Main Dashboard
![Dashboard](screenshots/dashboard.png)

### Rankings View
![Rankings](screenshots/rankings.png)

### Visualizations
![Charts](screenshots/charts.png)

---

## 🔗 Quick Links

- [Documentation](https://github.com/yourusername/student-marks-analyzer/wiki)
- [Report Issues](https://github.com/yourusername/student-marks-analyzer/issues)
- [Request Features](https://github.com/yourusername/student-marks-analyzer/issues/new)
- [View Changelog](CHANGELOG.md)

---

<div align="center">
  
### ⭐ Star this repository if you find it helpful!

Made with ❤️ for educational institutions

</div>

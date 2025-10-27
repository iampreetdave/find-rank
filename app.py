import streamlit as st
import pandas as pd
import pdfplumber
import re
from typing import Dict, List, Tuple

def extract_marks_from_pdf(pdf_file) -> pd.DataFrame:
    """
    Extract marks data from PDF file with improved pattern matching
    """
    data = []
    
    try:
        with pdfplumber.open(pdf_file) as pdf:
            for page_num, page in enumerate(pdf.pages):
                text = page.extract_text()
                
                if not text:
                    continue
                
                lines = text.split('\n')
                
                for i, line in enumerate(lines):
                    # Pattern 1: Look for enrollment number pattern (e.g., 231430142054)
                    enrollment_match = re.search(r'\b(2[34]14[0-9]{8})\b', line)
                    
                    if enrollment_match:
                        enrollment_no = enrollment_match.group(1)
                        
                        # Extract name (comes after enrollment number)
                        name_match = re.search(r'CSE\(AIML\)\s+D[12]\s+(.+?)\s+[A-Z]{3}', line)
                        name = name_match.group(1).strip() if name_match else "Unknown"
                        
                        # Look for marks in the next few lines or same line
                        marks_found = False
                        
                        # Check current line and next 3 lines for marks pattern
                        for offset in range(4):
                            if i + offset < len(lines):
                                check_line = lines[i + offset]
                                
                                # Pattern: two numbers followed by total (e.g., "29 24 53")
                                marks_match = re.search(r'\b(\d{1,2})\s+(\d{1,2})\s+(\d{1,2})\b', check_line)
                                
                                if marks_match:
                                    section_a = int(marks_match.group(1))
                                    section_b = int(marks_match.group(2))
                                    total = int(marks_match.group(3))
                                    
                                    # Validate that marks make sense (total should be sum of sections)
                                    if abs((section_a + section_b) - total) <= 1:  # Allow 1 mark tolerance
                                        data.append({
                                            'Enrollment No': enrollment_no,
                                            'Name': name,
                                            'Section A': section_a,
                                            'Section B': section_b,
                                            'Total Marks': total,
                                            'Source File': pdf_file.name
                                        })
                                        marks_found = True
                                        break
                        
                        # Pattern 2: Handle "AB AB AB" (absent students)
                        if not marks_found and i + 1 < len(lines):
                            check_line = lines[i + 1]
                            if 'AB' in check_line:
                                data.append({
                                    'Enrollment No': enrollment_no,
                                    'Name': name,
                                    'Section A': 0,
                                    'Section B': 0,
                                    'Total Marks': 0,
                                    'Source File': pdf_file.name,
                                    'Status': 'Absent'
                                })
    
    except Exception as e:
        st.error(f"Error reading PDF {pdf_file.name}: {str(e)}")
        return pd.DataFrame()
    
    return pd.DataFrame(data)

def process_multiple_pdfs(uploaded_files) -> pd.DataFrame:
    """
    Process multiple PDF files and combine data
    """
    all_data = []
    processed_files = 0
    
    progress_bar = st.progress(0)
    status_text = st.empty()
    
    for i, uploaded_file in enumerate(uploaded_files):
        status_text.text(f"Processing {uploaded_file.name}... ({i+1}/{len(uploaded_files)})")
        
        try:
            df = extract_marks_from_pdf(uploaded_file)
            if not df.empty:
                all_data.append(df)
                processed_files += 1
                st.success(f"✅ Successfully processed {uploaded_file.name} - Found {len(df)} records")
            else:
                st.warning(f"⚠️ No data extracted from {uploaded_file.name}")
        except Exception as e:
            st.error(f"❌ Error processing {uploaded_file.name}: {str(e)}")
        
        progress_bar.progress((i + 1) / len(uploaded_files))
    
    status_text.text("Processing complete!")
    
    if all_data:
        combined_df = pd.concat(all_data, ignore_index=True)
        st.success(f"🎉 Successfully processed {processed_files}/{len(uploaded_files)} files. Total records: {len(combined_df)}")
        return combined_df
    else:
        st.error("❌ No data could be extracted from any of the uploaded files.")
        return pd.DataFrame()

def calculate_cumulative_rankings(all_data: pd.DataFrame) -> pd.DataFrame:
    """
    Calculate cumulative rankings across all PDFs for each enrollment number
    """
    if all_data.empty:
        return all_data
    
    # Group by enrollment number
    cumulative_data = all_data.groupby('Enrollment No').agg({
        'Name': 'first',
        'Total Marks': 'sum',
        'Section A': 'sum',
        'Section B': 'sum',
        'Source File': lambda x: list(x.unique())
    }).reset_index()
    
    # Rename columns
    cumulative_data.columns = ['Enrollment No', 'Name', 'Cumulative Total', 
                                 'Total Section A', 'Total Section B', 'Source Files']
    
    # Count number of exams
    cumulative_data['Exam Count'] = cumulative_data['Source Files'].apply(len)
    
    # Calculate average marks per exam
    cumulative_data['Average per Exam'] = (cumulative_data['Cumulative Total'] / 
                                            cumulative_data['Exam Count']).round(2)
    
    # Calculate rank (higher marks = better rank)
    cumulative_data['Rank'] = cumulative_data['Cumulative Total'].rank(
        method='min', ascending=False
    ).astype(int)
    
    # Sort by rank
    cumulative_data = cumulative_data.sort_values('Rank').reset_index(drop=True)
    
    # Format source files for display
    cumulative_data['Source Files'] = cumulative_data['Source Files'].apply(
        lambda x: ', '.join(x)
    )
    
    return cumulative_data

def create_exam_wise_view(all_data: pd.DataFrame) -> pd.DataFrame:
    """
    Create a view showing marks from each exam side by side
    """
    if all_data.empty:
        return pd.DataFrame()
    
    # Pivot to show each exam's marks
    pivot_data = all_data.pivot_table(
        index=['Enrollment No', 'Name'],
        columns='Source File',
        values='Total Marks',
        aggfunc='first'
    ).reset_index()
    
    # Calculate row totals
    exam_columns = [col for col in pivot_data.columns if col not in ['Enrollment No', 'Name']]
    pivot_data['Cumulative Total'] = pivot_data[exam_columns].sum(axis=1)
    
    # Add rank
    pivot_data['Rank'] = pivot_data['Cumulative Total'].rank(
        method='min', ascending=False
    ).astype(int)
    
    # Sort by rank
    pivot_data = pivot_data.sort_values('Rank').reset_index(drop=True)
    
    return pivot_data

def main():
    st.set_page_config(
        page_title="Student Marks Analyzer", 
        page_icon="📊", 
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    # Custom CSS for better styling
    st.markdown("""
        <style>
        .stMetric {
            background-color: #f0f2f6;
            padding: 15px;
            border-radius: 10px;
        }
        </style>
    """, unsafe_allow_html=True)
    
    # Sidebar
    with st.sidebar:
        st.title("📊 Student Marks Analyzer")
        st.markdown("---")
        st.markdown("### 📖 How to Use")
        st.markdown("""
        1. **Upload** multiple PDF mark sheets
        2. **Extract** enrollment numbers and marks automatically
        3. **View** cumulative totals and rankings
        4. **Download** results as CSV
        """)
        
        st.markdown("---")
        st.markdown("### ✅ Supported Format")
        st.markdown("""
        - Student enrollment numbers (12 digits)
        - Section A and Section B marks
        - Total marks column
        - Multiple exam PDFs supported
        """)
        
        st.markdown("---")
        st.info("💡 **Tip**: Upload all exam PDFs at once for best results!")
    
    # Main content
    st.title("🎓 Cumulative Student Performance Analyzer")
    st.markdown("Upload multiple exam PDFs to calculate cumulative totals and generate rankings.")
    
    # File upload section
    st.header("📁 Step 1: Upload PDF Files")
    uploaded_files = st.file_uploader(
        "Choose multiple PDF mark sheets", 
        type="pdf", 
        accept_multiple_files=True,
        help="Upload PDFs for different exams to calculate cumulative performance"
    )
    
    if uploaded_files:
        st.success(f"✅ {len(uploaded_files)} file(s) selected")
        
        # Show uploaded files
        with st.expander("📋 View Uploaded Files"):
            for i, file in enumerate(uploaded_files, 1):
                st.write(f"{i}. {file.name}")
        
        # Process button
        if st.button("🚀 Process Files & Calculate Rankings", type="primary", use_container_width=True):
            with st.spinner("🔄 Processing PDF files..."):
                all_data = process_multiple_pdfs(uploaded_files)
            
            if not all_data.empty:
                st.session_state.all_data = all_data
                st.session_state.processed = True
                st.balloons()
        
        # Display results
        if hasattr(st.session_state, 'processed') and st.session_state.processed:
            all_data = st.session_state.all_data
            
            st.markdown("---")
            st.header("📊 Step 2: Analysis Results")
            
            # Calculate cumulative data
            cumulative_data = calculate_cumulative_rankings(all_data)
            exam_wise_data = create_exam_wise_view(all_data)
            
            # Key Statistics
            st.subheader("📈 Key Statistics")
            col1, col2, col3, col4, col5 = st.columns(5)
            
            with col1:
                st.metric("Total Students", len(cumulative_data))
            with col2:
                st.metric("Highest Score", f"{cumulative_data['Cumulative Total'].max()}")
            with col3:
                st.metric("Average Score", f"{cumulative_data['Cumulative Total'].mean():.1f}")
            with col4:
                st.metric("Lowest Score", f"{cumulative_data['Cumulative Total'].min()}")
            with col5:
                st.metric("Total Exams", len(uploaded_files))
            
            # Top Performer Highlight
            top_student = cumulative_data.iloc[0]
            st.success(f"🏆 **Top Performer**: {top_student['Name']} (Enrollment: {top_student['Enrollment No']}) with {top_student['Cumulative Total']} marks!")
            
            # Tabs for different views
            st.subheader("📋 Detailed Results")
            tab1, tab2, tab3, tab4 = st.tabs([
                "🏆 Rankings", 
                "📊 Exam-wise Comparison", 
                "📈 Visualizations", 
                "📄 Raw Data"
            ])
            
            with tab1:
                st.write("### Cumulative Rankings")
                
                # Display columns selection
                display_cols = ['Rank', 'Enrollment No', 'Name', 'Cumulative Total', 
                               'Total Section A', 'Total Section B', 'Average per Exam', 'Exam Count']
                
                display_df = cumulative_data[display_cols].copy()
                
                # Highlight top 3
                def highlight_top3(row):
                    if row['Rank'] <= 3:
                        return ['background-color: #90EE90'] * len(row)
                    return [''] * len(row)
                
                st.dataframe(
                    display_df.style.apply(highlight_top3, axis=1),
                    use_container_width=True,
                    hide_index=True,
                    height=600
                )
            
            with tab2:
                st.write("### Exam-wise Performance Comparison")
                st.dataframe(
                    exam_wise_data,
                    use_container_width=True,
                    hide_index=True,
                    height=600
                )
            
            with tab3:
                st.write("### Performance Distribution")
                
                col1, col2 = st.columns(2)
                
                with col1:
                    st.write("#### Top 10 Students")
                    top_10 = cumulative_data.head(10)[['Name', 'Cumulative Total']].copy()
                    top_10['Name'] = top_10['Name'].str[:20]  # Truncate long names
                    st.bar_chart(top_10.set_index('Name'))
                
                with col2:
                    st.write("#### Score Distribution")
                    st.bar_chart(cumulative_data['Cumulative Total'])
                
                # Average performance per exam
                st.write("#### Average Performance by Exam")
                exam_avg = all_data.groupby('Source File')['Total Marks'].mean().round(2)
                st.bar_chart(exam_avg)
            
            with tab4:
                st.write("### All Extracted Records")
                st.dataframe(all_data, use_container_width=True, height=600)
            
            # Download section
            st.markdown("---")
            st.header("💾 Step 3: Download Results")
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.subheader("📊 Rankings")
                csv_rankings = display_df.to_csv(index=False)
                st.download_button(
                    label="📥 Download Rankings CSV",
                    data=csv_rankings,
                    file_name="student_rankings.csv",
                    mime="text/csv",
                    use_container_width=True
                )
            
            with col2:
                st.subheader("📋 Exam-wise Data")
                csv_examwise = exam_wise_data.to_csv(index=False)
                st.download_button(
                    label="📥 Download Exam-wise CSV",
                    data=csv_examwise,
                    file_name="exam_wise_comparison.csv",
                    mime="text/csv",
                    use_container_width=True
                )
            
            with col3:
                st.subheader("📄 Raw Data")
                csv_raw = all_data.to_csv(index=False)
                st.download_button(
                    label="📥 Download Raw Data CSV",
                    data=csv_raw,
                    file_name="raw_extracted_data.csv",
                    mime="text/csv",
                    use_container_width=True
                )
    
    else:
        # Welcome section
        st.info("👆 Please upload PDF mark sheets to begin analysis.")
        
        with st.expander("💡 Example & Instructions"):
            st.markdown("""
            ### 📋 What This App Does:
            
            1. **Extracts Data**: Automatically reads enrollment numbers, names, and marks from PDFs
            2. **Combines Results**: Aggregates marks from multiple exams
            3. **Calculates Rankings**: Ranks students based on cumulative performance
            4. **Generates Reports**: Creates downloadable reports and visualizations
            
            ### 📊 Expected PDF Format:
            
            Your PDF should contain:
            - **Enrollment Number**: 12-digit student ID (e.g., 231430142054)
            - **Student Name**: Full name of the student
            - **Section A Marks**: Marks obtained in Section A
            - **Section B Marks**: Marks obtained in Section B
            - **Total Marks**: Sum of both sections
            
            ### 🎯 Example Use Case:
            
            Upload 3 exam PDFs:
            - Mid-Term 1: Student gets 45/60
            - Mid-Term 2: Student gets 50/60
            - Final: Student gets 52/60
            
            **Cumulative Total**: 147/180
            **Rank**: Based on cumulative score across all exams
            """)

if __name__ == "__main__":
    main()
from fpdf import FPDF

# Initialize PDF
pdf = FPDF()
pdf.set_auto_page_break(auto=True, margin=15)
pdf.add_page()
pdf.set_font("Arial", size=12)

# Title
pdf.set_font("Arial", style="B", size=16)
pdf.cell(200, 10, txt="Popular Python Libraries", ln=True, align="C")
pdf.ln(10)

# Categories and Libraries
categories = {
    "Data Analysis": ["Pandas", "NumPy", "Dask"],
    "Machine Learning": ["Scikit-learn", "TensorFlow", "PyTorch"],
    "Web Development": ["Flask", "Django", "FastAPI"],
    "Visualization": ["Matplotlib", "Seaborn", "Plotly"],
    "Networking": ["Requests", "Socket", "Paramiko"],
    "Automation": ["Selenium", "PyAutoGUI", "APScheduler"],
    "Game Development": ["Pygame", "Arcade", "Godot-Python"],
    "Others": ["BeautifulSoup", "OpenCV", "PyPDF2"]
}

# Add content to PDF
for category, libraries in categories.items():
    pdf.set_font("Arial", style="B", size=14)
    pdf.cell(0, 10, txt=category, ln=True)
    pdf.set_font("Arial", size=12)
    for library in libraries:
        pdf.cell(0, 10, txt=f"- {library}", ln=True)
    pdf.ln(5)

# Save PDF
pdf.output("Python_Libraries_List.pdf")

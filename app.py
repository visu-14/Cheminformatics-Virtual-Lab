
import streamlit as st
import pandas as pd
from rdkit import Chem
from rdkit.Chem import Descriptors, Draw, rdMolDescriptors
from io import BytesIO
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table
)
from reportlab.lib.styles import getSampleStyleSheet

st.set_page_config(
    page_title="Cheminformatics Virtual Lab",
    page_icon="🧪",
    layout="wide"
)

st.title("🧪 Cheminformatics Virtual Laboratory")
st.sidebar.title("Virtual Laboratory")

pages = [
    "🏠 Home",
    "📖 Theory",
    "🧬 Molecular Visualization",
    "📊 Molecular Properties Report",
    "📈 Structure–Property Analysis",
    "📝 Assessment",
    "📄 Final Project Report"
]

page = st.sidebar.radio("Select Module", pages)

def calculate(smiles):
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return None, None

    props = {
        "Molecular Formula": rdMolDescriptors.CalcMolFormula(mol),
        "Molecular Weight": round(Descriptors.MolWt(mol), 2),
        "LogP": round(Descriptors.MolLogP(mol), 2),
        "TPSA": round(Descriptors.TPSA(mol), 2),
        "H-Bond Donors": rdMolDescriptors.CalcNumHBD(mol),
        "H-Bond Acceptors": rdMolDescriptors.CalcNumHBA(mol),
        "Rotatable Bonds": rdMolDescriptors.CalcNumRotatableBonds(mol)
    }
    return mol, props

# HOME
if page == "🏠 Home":
    st.header("Welcome to Cheminformatics Virtual Lab")
    st.image(
        "https://images.unsplash.com/photo-1532187863486-abf9dbad1b69",
        use_container_width=True
    )

    st.write("""
    Cheminformatics combines chemistry, computer science
    and information technology to analyse chemical structures.

    This virtual laboratory helps students visualize molecules,
    calculate molecular properties and study chemical structures.
    """)

    st.subheader("Objectives")
    st.write("""
    1. Understand cheminformatics.
    2. Learn SMILES notation.
    3. Visualize molecular structures.
    4. Calculate molecular descriptors.
    5. Compare molecular properties.
    6. Understand molecular fingerprints.
    """)

    st.success("Select a module from the sidebar to begin.")

# THEORY
elif page == "📖 Theory":
    st.header("Theory of Cheminformatics")

    st.subheader("1. Introduction")
    st.write("""
    Cheminformatics is the use of computational techniques
    to store, analyse and interpret chemical information.
    It is widely used in drug discovery and pharmaceutical research.
    """)

    st.subheader("2. SMILES")
    st.write("""
    SMILES stands for Simplified Molecular Input Line Entry System.
    It represents molecular structures using text.
    Examples:
    - Ethanol: CCO
    - Benzene: c1ccccc1
    - Acetic acid: CC(=O)O
    """)

    st.subheader("3. Molecular Fingerprints")
    st.write("""
    Molecular fingerprints are digital representations of
    chemical structures used for molecular similarity searching.
    Examples include Morgan fingerprints and MACCS keys.
    """)

    st.subheader("4. Molecular Descriptors")
    st.write("""
    Molecular descriptors are numerical values describing
    molecular characteristics such as molecular weight, LogP and TPSA.
    """)

    st.subheader("5. Applications")
    st.write("""
    - Drug discovery
    - QSAR analysis
    - Toxicity prediction
    - Chemical database searching
    - Pharmaceutical research
    """)

# MOLECULAR VISUALIZATION
elif page == "🧬 Molecular Visualization":
    st.header("Molecular Visualization")

    examples = {
        "Ethanol": "CCO",
        "Benzene": "c1ccccc1",
        "Acetic Acid": "CC(=O)O",
        "Aspirin": "CC(=O)Oc1ccccc1C(=O)O",
        "Caffeine": "Cn1c(=O)c2c(ncn2C)n(C)c1=O",
        "Paracetamol": "CC(=O)NC1=CC=C(O)C=C1",
        "Ibuprofen": "CC(C)CC1=CC=C(C=C1)C(C)C(=O)O"
    }

    selected = st.selectbox("Choose a molecule", list(examples.keys()))
    smiles = st.text_input("Enter SMILES", examples[selected])

    if st.button("Visualize Molecule"):
        mol, props = calculate(smiles)
        if mol:
            st.image(Draw.MolToImage(mol, size=(500, 400)))
            st.success("Molecular structure generated!")
            st.write("Molecular formula:", props["Molecular Formula"])
        else:
            st.error("Invalid SMILES notation.")

# MOLECULAR PROPERTIES
elif page == "📊 Molecular Properties Report":
    st.header("Molecular Properties Report")

    smiles = st.text_input("Enter SMILES", "CCO")

    if st.button("Calculate Properties"):
        mol, props = calculate(smiles)
        if mol:
            st.dataframe(
                pd.DataFrame(
                    list(props.items()),
                    columns=["Property", "Value"]
                ),
                use_container_width=True
            )
        else:
            st.error("Invalid SMILES.")

# STRUCTURE PROPERTY ANALYSIS
elif page == "📈 Structure–Property Analysis":
    st.header("Structure–Property Analysis")

    s1 = st.text_input("First molecule", "CCO")
    s2 = st.text_input("Second molecule", "CCCO")

    if st.button("Compare Molecules"):
        m1, p1 = calculate(s1)
        m2, p2 = calculate(s2)

        if m1 and m2:
            df = pd.DataFrame({
                "Property": list(p1.keys())[1:],
                "Molecule 1": list(p1.values())[1:],
                "Molecule 2": list(p2.values())[1:]
            })

            st.dataframe(df, use_container_width=True)
            st.bar_chart(df.set_index("Property"))
        else:
            st.error("Enter valid SMILES for both molecules.")

# ASSESSMENT
elif page == "📝 Assessment":
    st.header("Cheminformatics Assessment")

    questions = [
        ("What does SMILES represent?",
         ["Molecular notation", "Protein sequence", "Atomic mass"], 0),
        ("Which library is used for cheminformatics?",
         ["Tkinter", "RDKit", "Flask"], 1),
        ("Which property describes lipophilicity?",
         ["TPSA", "LogP", "HBD"], 1),
        ("What is the SMILES of ethanol?",
         ["CCO", "CCC", "COC"], 0),
        ("What does TPSA stand for?",
         ["Topological Polar Surface Area",
          "Total Protein Surface Area", "Thermal Pressure"], 0)
    ]

    answers = []
    for i, (q, options, correct) in enumerate(questions):
        answer = st.radio(q, options, key=f"quiz{i}")
        answers.append(options.index(answer))

    if st.button("Submit Quiz"):
        score = sum(
            answers[i] == questions[i][2]
            for i in range(len(questions))
        )
        st.success(f"Your score: {score}/{len(questions)}")
        st.progress(score / len(questions))

# FINAL PROJECT REPORT
elif page == "📄 Final Project Report":
    st.header("Final Project Report")

    name = st.text_input("Student Name")
    title = st.text_input("Experiment Title")
    smiles = st.text_input("Molecular SMILES", "CCO")

    if st.button("Generate PDF Report"):
        mol, props = calculate(smiles)

        if mol:
            buffer = BytesIO()
            doc = SimpleDocTemplate(buffer)
            styles = getSampleStyleSheet()

            content = [
                Paragraph("CHEMINFORMATICS VIRTUAL LAB REPORT",
                          styles["Title"]),
                Spacer(1, 20),
                Paragraph(f"Student Name: {name}", styles["Normal"]),
                Paragraph(f"Experiment: {title}", styles["Normal"]),
                Paragraph(f"SMILES: {smiles}", styles["Normal"]),
                Spacer(1, 20),
                Paragraph("Molecular Properties",
                          styles["Heading2"]),
                Table(
                    [["Property", "Value"]] +
                    [[k, str(v)] for k, v in props.items()]
                ),
                Spacer(1, 20),
                Paragraph("Conclusion", styles["Heading2"]),
                Paragraph(
                    "Molecular descriptors were calculated using RDKit.",
                    styles["Normal"]
                )
            ]

            doc.build(content)
            buffer.seek(0)

            st.download_button(
                "Download Project Report",
                buffer,
                "Cheminformatics_Report.pdf",
                "application/pdf"
            )
        else:
            st.error("Enter a valid SMILES.")

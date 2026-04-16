# Clinical Trial Risk Prediction System

## 📋 Project Overview

The **Clinical Trial Risk Prediction System** is a machine learning-powered web application designed to predict the success risk of clinical trials based on various patient and trial characteristics. This application leverages advanced data science techniques to provide healthcare professionals and research teams with data-driven insights for trial risk assessment.

### 🎯 Purpose

Clinical trials are critical for pharmaceutical development, but they carry inherent risks of failure. This system helps:
- **Predict trial success/failure probability** based on historical data
- **Identify high-risk trials** early in the planning phase
- **Support decision-making** for resource allocation and trial design
- **Analyze patient demographics** and comorbidities affecting trial outcomes

---

## 🛠️ Technologies & Tools Used

### Core Technologies
| Technology | Version | Purpose |
|------------|---------|---------|
| **Python** | 3.8+ | Primary programming language |
| **Streamlit** | Latest | Interactive web framework for UI |
| **Scikit-Learn** | Latest | Machine learning models and preprocessing |
| **Pandas** | Latest | Data manipulation and analysis |
| **NumPy** | Latest | Numerical computing and arrays |
| **Joblib** | Latest | Model serialization and loading |
| **SQLite3** | Built-in | Local database for predictions storage |

### Machine Learning Model
- **Algorithm**: Random Forest Classifier
- **Estimators**: 200 decision trees
- **Max Depth**: 10 levels
- **Class Weighting**: Balanced weights to handle imbalanced data
- **Validation**: 80-20 train-test split with stratification

---

## 📊 Project Structure

```
Clinical_Trail_Risk_Prediction-main/
├── app.py                              # Main Streamlit web application
├── Train_model.py                      # Model training script
├── predict.py                          # Command-line prediction interface
├── Preparing_the_data.py               # Data preprocessing and feature engineering
├── Covid-19_cleaned_dataset.csv        # Source clinical trial dataset
├── final_trial_risk_dataset.csv        # Processed dataset for model training
├── trial_risk_model.pkl                # Trained Random Forest model (binary)
├── README.md                           # Original documentation
├── README_PROFESSIONAL.md              # This comprehensive guide
└── trial_predictions.db                # SQLite database (auto-created on first run)
```

---

## ⚙️ Prerequisites

Before running the application, ensure you have:
- **Python 3.8** or higher installed
- **pip** package manager
- **Git** (optional, for cloning the repository)
- **4GB RAM** minimum recommended

---

## 📥 Installation

### Step 1: Clone or Download the Project
```bash
git clone https://github.com/yourusername/Clinical_Trail_Risk_Prediction.git
cd Clinical_Trail_Risk_Prediction-main
```

### Step 2: Create a Virtual Environment (Recommended)
```bash
# On Windows
python -m venv venv
venv\Scripts\activate

# On macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### Step 3: Install Required Dependencies
```bash
pip install streamlit pandas scikit-learn joblib numpy
```

Or create a `requirements.txt` and install:
```bash
streamlit>=1.28.0
pandas>=2.0.0
scikit-learn>=1.3.0
joblib>=1.3.0
numpy>=1.24.0
```

Then run:
```bash
pip install -r requirements.txt
```

---

## 🚀 How to Run the Application

### Option 1: Run the Web Application (Recommended)
This provides an interactive web interface for predictions.

```bash
streamlit run app.py
```

**Output:**
```
  You can now view your Streamlit app in your browser.
  Local URL: http://localhost:8501
  Network URL: http://192.xxx.xxx.xxx:8501
```

Access the application at `http://localhost:8501` in your web browser.

### Option 2: Run Command-Line Prediction
Interactive terminal-based prediction interface.

```bash
python predict.py
```

You'll be prompted to enter:
- Trial phase (1-4)
- Number of patients
- Trial duration
- Age group
- Region
- Comorbidity status

### Option 3: Train a New Model
Retrain the Random Forest model on the dataset.

```bash
python Train_model.py
```

This generates:
- `trial_risk_model.pkl` - Serialized trained model
- Model accuracy metrics printed to console

### Option 4: Prepare/Process Data
Process raw data and generate features.

```bash
python Preparing_the_data.py
```

This creates:
- `final_trial_risk_dataset.csv` - Processed features
- Feature engineering for model training

---

## 🎮 Web Application Features

### Input Form
1. **Trial Phase**: Dropdown (Phase 1, 2, 3, or 4)
2. **Number of Patients**: Integer input
3. **Trial Duration**: Months and Days separate inputs
4. **Age Group**: Selection from Young/Middle/Old categories
5. **Region**: Geographic location dropdown
6. **Comorbidity**: Medical condition selection

### Output Dashboard
- **Risk Probability**: Percentage likelihood (0-100%)
- **Risk Classification**: Low/Medium/High risk level
- **Visual Metrics**: Cards displaying results with styling
- **Prediction History**: Sortable table of past predictions
- **Database Integration**: Auto-saved to SQLite

### User Interface
- **Custom Styling**: Gradient backgrounds and modern design
- **Responsive Layout**: Works on desktop and tablet
- **Dark Theme**: Professional gradient color scheme
- **Real-time Updates**: Instant feedback on predictions

---

## 📈 Model Training Details

### Dataset Information
- **Source**: COVID-19 clinical trials dataset
- **Raw Size**: Large clinical trial database
- **Processed Size**: Cleaned and engineered features
- **Target**: Binary classification (Success/Failure)

### Features Used
| Feature | Type | Values | Description |
|---------|------|--------|-------------|
| Phase | Integer | 1, 2, 3, 4 | Clinical trial phase |
| Patients | Integer | Variable | Enrolled patient count |
| Duration | Integer | Days | Total trial duration |
| Age Group | Categorical | Young, Middle, Old | Patient age category |
| Region | Categorical | Multiple | Geographic location |
| Comorbidity | Categorical | Multiple | Existing conditions |

### Model Training Process
1. **Data Loading**: Read CSV into pandas DataFrame
2. **Train-Test Split**: 80% training, 20% testing with stratification
3. **Model Initialization**: Random Forest with 200 trees, max_depth=10
4. **Training**: Fit on training data with balanced class weights
5. **Evaluation**: Calculate accuracy and classification metrics
6. **Serialization**: Save model as `.pkl` file using joblib

### Model Performance Metrics
- Handles imbalanced datasets via class weighting
- Stratified splitting ensures representative proportions
- Cross-validation ready (can be enhanced)
- Serialized for production deployment

---

## 🔍 Detailed Workflow

### Data Pipeline
```
Raw Dataset (CSV)
    ↓
Data Cleaning (Preparing_the_data.py)
    ↓
Feature Engineering
    ↓
final_trial_risk_dataset.csv
    ↓
Model Training (Train_model.py)
    ↓
trial_risk_model.pkl
    ↓
Web Application (app.py)
    ↓
User Predictions & Database Storage
```

### Prediction Pipeline
```
User Input (Web Form)
    ↓
Feature Encoding
    ↓
Model Inference
    ↓
Risk Probability (0-1)
    ↓
Risk Classification
    ↓
Database Save
    ↓
Display Results
```

---

## 💾 Database Schema

### SQLite Table: `predictions`

```sql
CREATE TABLE predictions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    phase INTEGER,
    patients INTEGER,
    duration_months INTEGER,
    duration_days INTEGER,
    age_group TEXT,
    region TEXT,
    comorbidity TEXT,
    probability REAL,
    risk_level TEXT,
    timestamp TEXT
);
```

Each prediction is automatically logged with:
- Trial parameters
- Calculated probability
- Risk classification
- Prediction timestamp

---

## 📝 Feature Descriptions

### Input Variables

**Phase (Integer 1-4)**
- Phase I: Safety and dosage studies
- Phase II: Efficacy and side effects
- Phase III: Effectiveness and monitoring
- Phase IV: Post-market surveillance

**Patients (Integer)**
- Number of enrolled participants
- Impacts trial complexity and success likelihood

**Duration (Integer - Days)**
- Total trial length
- Affects patient retention and data quality

**Age Group (Categorical)**
- Young (18-35): Lower comorbidity risk
- Middle (36-55): Moderate risk profile
- Old (56+): Higher comorbidity risk

**Region (Categorical)**
- India, USA, Europe, Asia, Other
- Affects regulatory requirements and infrastructure

**Comorbidity (Categorical)**
- None, Diabetes, Heart disease, Lung disease, Hypertension
- Major factor in trial outcome

---

## 🔧 Troubleshooting Guide

### Issue: `ModuleNotFoundError: No module named 'streamlit'`
**Solution**: 
```bash
pip install streamlit
```
Or check your virtual environment is activated.

### Issue: `trial_risk_model.pkl` not found
**Solution**: 
```bash
python Train_model.py
```
This trains and saves the model.

### Issue: `final_trial_risk_dataset.csv` not found
**Solution**: 
```bash
python Preparing_the_data.py
```
This processes the raw COVID-19 dataset.

### Issue: Port 8501 already in use
**Solution**: 
```bash
streamlit run app.py --server.port 8502
```
Use a different port number.

### Issue: Permission denied on database
**Solution**: 
Ensure write permissions in the project directory.

### Issue: Predictions not saving to database
**Solution**: 
Check SQLite3 is properly installed:
```bash
python -c "import sqlite3; print(sqlite3.version)"
```

---

## 🎓 Learning Outcomes

This project demonstrates:
- **Machine Learning**: Random Forest classification and model training
- **Data Science**: Data preprocessing, feature engineering, EDA
- **Web Application**: Streamlit for rapid UI development
- **Database**: SQLite for local data persistence
- **Python**: Object-oriented programming and best practices
- **Deployment**: Serialization and model loading for production

---

## 🚀 Future Enhancements

- [ ] Add cross-validation and hyperparameter tuning
- [ ] Implement feature importance visualization
- [ ] Deploy to cloud (AWS, Azure, GCP)
- [ ] Add batch prediction API
- [ ] Implement user authentication
- [ ] Add data visualization dashboard
- [ ] Export predictions to report formats (PDF, Excel)
- [ ] Integration with medical databases
- [ ] Model versioning and tracking
- [ ] A/B testing framework

---

## 📊 Use Cases

1. **Clinical Research Teams** - Assess trial viability before launch
2. **Pharmaceutical Companies** - Budget planning and resource allocation
3. **Regulatory Affairs** - Trial design compliance checking
4. **Healthcare Organizations** - Trial participation decision-making
5. **Medical Universities** - Educational tool for trial design

---

## 🔐 Security Considerations

- All predictions stored locally in SQLite
- No external API calls (offline capable)
- Data remains on-premise
- No authentication required for local deployment
- Consider adding encryption for production use

---

## 📄 License

This project is open-source and available under the MIT License.

---

## 🤝 Contributing

Contributions are welcome! To contribute:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/improvement`)
3. Commit changes (`git commit -am 'Add improvement'`)
4. Push to branch (`git push origin feature/improvement`)
5. Create a Pull Request

---

## 📧 Support & Feedback

For issues, suggestions, or feedback:
- Open an issue on GitHub
- Contact the development team
- Submit pull requests for improvements

---

## 📚 Additional Resources

- [Streamlit Documentation](https://docs.streamlit.io/)
- [Scikit-Learn Documentation](https://scikit-learn.org/)
- [Clinical Trials Best Practices](https://www.fda.gov/patients/drug-development-process)
- [Random Forest Tutorial](https://scikit-learn.org/stable/modules/ensemble.html#random-forests)
- [Pandas Documentation](https://pandas.pydata.org/)

---

## 🏆 Key Highlights

✅ **End-to-End ML Pipeline** - From data to predictions  
✅ **Production-Ready** - Serialized models for deployment  
✅ **Interactive UI** - User-friendly web interface  
✅ **Data Persistence** - SQLite database integration  
✅ **Scalable Architecture** - Ready for cloud deployment  
✅ **Well-Documented** - Comprehensive code comments  
✅ **Best Practices** - Follows ML and Python conventions  

---

**Last Updated**: April 2026  
**Version**: 1.0  
**Status**: Production Ready

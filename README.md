# 💬 Chat2Data

**Chat2Data** is a Streamlit-based AI-powered app that lets you **ask questions in natural language** and get accurate SQL-generated insights from a global economic dataset.

It uses **Google Gemini (via Gemini Pro)** to convert plain English into SQL queries and executes them against a SQLite database built from a Kaggle dataset.

---

## 🌍 Dataset

- **Source**: [Kaggle](https://www.kaggle.com/](https://www.kaggle.com/datasets/tanishksharma9905/global-economic-indicators-20102025))  
- **Topic**: Global Economic Indicators  
- **Years Covered**: 2010 to 2025  

---

## ⚙️ Features

- ✅ Ask questions like _“Top 5 countries by GDP in 2020”_
- ✅ Powered by **Gemini Pro** for Text-to-SQL generation
- ✅ Displays generated SQL queries
- ✅ Executes queries against **SQLite DB**
- ✅ Interactive result table (via `pandas` + Streamlit)
- ✅ Query history log (for successful queries only)

---

## 💡 Sample Questions to Ask

- "Which countries had the highest GDP in 2020?"
- "List the top 5 countries by GDP growth in 2022."
- "Show unemployment rates in India from 2015 to 2020."
- "Compare public debt between USA and China in 2018."
- "What was the average inflation for the EU over the last decade?"

---

## 🙌 Acknowledgments
- [Kaggle](https://github.com/kaggle) for the dataset
- [Google Gemini](https://github.com/google-gemini) for the Text-to-SQL model
- [Streamlit](https://github.com/streamlit) for the frontend framework

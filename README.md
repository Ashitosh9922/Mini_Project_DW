# Enterprise Employee Analytics & Data Warehouse System

> End-to-end employee analytics and data warehousing project built with Python, MySQL, SQL, Pandas, and Streamlit.

![Python](https://img.shields.io/badge/Python-3.x-3776AB?logo=python&logoColor=white)
![MySQL](https://img.shields.io/badge/MySQL-8.x-4479A1?logo=mysql&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-App-FF4B4B?logo=streamlit&logoColor=white)
![Pandas](https://img.shields.io/badge/Pandas-Data%20Processing-150458?logo=pandas&logoColor=white)
![Plotly](https://img.shields.io/badge/Plotly-Analytics-3F4F75?logo=plotly&logoColor=white)

---

## 📌 Overview

The **Enterprise Employee Analytics & Data Warehouse System** is an end-to-end data engineering and analytics application designed to manage employee operations and transform operational data into an analytical data warehouse.

The system combines:

- MySQL OLTP for operational data
- MySQL OLAP using a star schema
- Slowly Changing Dimension Type 2 (SCD2)
- Python Object-Oriented Programming
- Pandas-based data processing
- Synthetic large-scale data generation
- SQL CTEs and window functions
- Stored procedures
- Streamlit data-entry forms
- Analytical dashboards
- Data-quality and warehouse validation

### End-to-End Flow

```text
Data Sources
     ↓
Python / Pandas Data Generation
     ↓
CSV Staging
     ↓
MySQL OLTP
     ↓
ETL + SCD Type 2
     ↓
MySQL OLAP Star Schema
     ↓
SQL Analytics
     ↓
Python Managers
     ↓
Streamlit Application

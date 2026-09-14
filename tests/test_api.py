import pytest
from fastapi.testclient import TestClient
from app import app
import io

client = TestClient(app)


def test_health_endpoint():
    response = client.get("/api/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert data["service"] == "Customer Churn Prediction API"


def test_metrics_endpoint():
    response = client.get("/api/metrics")
    assert response.status_code == 200
    data = response.json()
    assert "accuracy" in data
    assert "precision" in data
    assert "recall" in data
    assert "F1_score" in data


def test_home_page_rendered():
    response = client.get("/")
    assert response.status_code == 200
    assert "ChurnSense AI" in response.text
    assert "Quick Churn Predictor" in response.text


def test_single_prediction_endpoint():
    payload = {
        "Gender": "Male",
        "Age": 45,
        "Under30": "No",
        "SeniorCitizen": "No",
        "Married": "No",
        "NumberofDependents": 0,
        "Latitude": 34.0522,
        "Longitude": -118.2437,
        "Population": 35000,
        "Number_of_Referrals": 0,
        "TenureinMonths": 2,
        "Offer": "Offer E",
        "PhoneService": "Yes",
        "AvgMonthlyLongDistanceCharges": 25.0,
        "MultipleLines": "No",
        "InternetType": "Fiber Optic",
        "AvgMonthlyGBDownload": 20,
        "OnlineSecurity": "No",
        "OnlineBackup": "No",
        "DeviceProtectionPlan": "No",
        "PremiumTechSupport": "No",
        "StreamingTV": "No",
        "StreamingMovies": "No",
        "StreamingMusic": "No",
        "UnlimitedData": "Yes",
        "Contract": "Month-to-Month",
        "PaperlessBilling": "Yes",
        "PaymentMethod": "Bank Withdrawal",
        "MonthlyCharge": 95.5,
        "TotalCharges": 191.0,
        "TotalRefunds": 0.0,
        "TotalExtraDataCharges": 0,
        "TotalLongDistanceCharges": 50.0,
        "TotalRevenue": 241.0,
        "SatisfactionScore": 1
    }
    response = client.post("/api/predict", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert "prediction" in data
    assert "label" in data
    assert "churn_probability" in data
    assert "risk_level" in data
    assert data["prediction"] in [0, 1]


def test_sample_csv_download():
    response = client.get("/api/sample-csv")
    assert response.status_code == 200
    assert "text/csv" in response.headers["content-type"]
    assert "MonthlyCharge" in response.text


def test_batch_prediction_endpoint():
    csv_content = (
        "Gender,Age,Under30,SeniorCitizen,Married,NumberofDependents,Latitude,Longitude,Population,Number_of_Referrals,TenureinMonths,Offer,PhoneService,AvgMonthlyLongDistanceCharges,MultipleLines,InternetType,AvgMonthlyGBDownload,OnlineSecurity,OnlineBackup,DeviceProtectionPlan,PremiumTechSupport,StreamingTV,StreamingMovies,StreamingMusic,UnlimitedData,Contract,PaperlessBilling,PaymentMethod,MonthlyCharge,TotalCharges,TotalRefunds,TotalExtraDataCharges,TotalLongDistanceCharges,TotalRevenue,SatisfactionScore\n"
        "Male,67,No,Yes,Yes,0,38.91,-123.60,1352,0,54,,Yes,38.48,Yes,Fiber Optic,13,No,No,Yes,No,Yes,Yes,No,No,Month-to-Month,Yes,Credit Card,99.05,5295.7,0.0,40,2077.92,7413.62,5\n"
        "Female,35,No,No,No,0,34.11,-118.19,64672,0,7,Offer E,Yes,18.99,Yes,Fiber Optic,23,No,No,No,No,No,No,No,Yes,Month-to-Month,Yes,Bank Withdrawal,75.1,552.95,0.0,0,132.93,685.88,1\n"
    )
    files = {"file": ("test_batch.csv", io.BytesIO(csv_content.encode("utf-8")), "text/csv")}
    response = client.post("/api/predict/batch", files=files)
    assert response.status_code == 200
    data = response.json()
    assert data["total_count"] == 2
    assert len(data["results"]) == 2
    assert "prediction" in data["results"][0]

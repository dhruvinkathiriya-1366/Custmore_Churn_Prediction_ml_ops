from typing import Optional
from pydantic import BaseModel, Field
import pandas as pd


class CustomerData(BaseModel):
    # Demographics & Location
    Gender: str = Field(default="Female", description="Gender of the customer (Female, Male)")
    Age: int = Field(default=35, ge=18, le=100, description="Age of the customer")
    Under30: str = Field(default="No", description="Is customer under 30 (Yes, No)")
    SeniorCitizen: str = Field(default="No", description="Is customer a senior citizen (Yes, No)")
    Married: str = Field(default="No", description="Is customer married (Yes, No)")
    NumberofDependents: int = Field(default=0, ge=0, description="Number of dependents")
    Latitude: float = Field(default=34.0522, description="Latitude coordinate")
    Longitude: float = Field(default=-118.2437, description="Longitude coordinate")
    Population: int = Field(default=30000, ge=0, description="City population")
    Number_of_Referrals: int = Field(default=0, ge=0, description="Number of customer referrals")

    # Subscription & Services
    TenureinMonths: int = Field(default=12, ge=0, description="Customer tenure in months")
    Offer: Optional[str] = Field(default=None, description="Marketing offer (Offer A, Offer B, Offer C, Offer D, Offer E, or None)")
    PhoneService: str = Field(default="Yes", description="Has phone service (Yes, No)")
    AvgMonthlyLongDistanceCharges: float = Field(default=15.0, ge=0.0, description="Avg monthly long distance charge")
    MultipleLines: str = Field(default="No", description="Multiple phone lines (Yes, No)")
    InternetType: Optional[str] = Field(default="Fiber Optic", description="Internet type (Fiber Optic, Cable, DSL, or None)")
    AvgMonthlyGBDownload: int = Field(default=25, ge=0, description="Monthly GB download")
    OnlineSecurity: str = Field(default="No", description="Online security add-on (Yes, No)")
    OnlineBackup: str = Field(default="No", description="Online backup add-on (Yes, No)")
    DeviceProtectionPlan: str = Field(default="No", description="Device protection plan (Yes, No)")
    PremiumTechSupport: str = Field(default="No", description="Premium tech support (Yes, No)")
    StreamingTV: str = Field(default="No", description="Streaming TV (Yes, No)")
    StreamingMovies: str = Field(default="No", description="Streaming movies (Yes, No)")
    StreamingMusic: str = Field(default="No", description="Streaming music (Yes, No)")
    UnlimitedData: str = Field(default="Yes", description="Unlimited data (Yes, No)")

    # Contract & Billing
    Contract: str = Field(default="Month-to-Month", description="Contract term (Month-to-Month, One Year, Two Year)")
    PaperlessBilling: str = Field(default="Yes", description="Paperless billing (Yes, No)")
    PaymentMethod: str = Field(default="Bank Withdrawal", description="Payment method (Bank Withdrawal, Credit Card, Mailed Check)")
    MonthlyCharge: float = Field(default=75.0, ge=0.0, description="Monthly charge amount")
    TotalCharges: float = Field(default=900.0, ge=0.0, description="Total charges to date")
    TotalRefunds: float = Field(default=0.0, ge=0.0, description="Total refunds")
    TotalExtraDataCharges: int = Field(default=0, ge=0, description="Total extra data charges")
    TotalLongDistanceCharges: float = Field(default=180.0, ge=0.0, description="Total long distance charges")
    TotalRevenue: float = Field(default=1080.0, ge=0.0, description="Total revenue generated")
    SatisfactionScore: int = Field(default=3, ge=1, le=5, description="Customer satisfaction score (1 to 5)")

    def to_dataframe(self) -> pd.DataFrame:
        data_dict = {
            "Gender": [self.Gender],
            "Age": [self.Age],
            "Under30": [self.Under30],
            "SeniorCitizen": [self.SeniorCitizen],
            "Married": [self.Married],
            "NumberofDependents": [self.NumberofDependents],
            "Latitude": [self.Latitude],
            "Longitude": [self.Longitude],
            "Population": [self.Population],
            "Number_of_Referrals": [self.Number_of_Referrals],
            "TenureinMonths": [self.TenureinMonths],
            "Offer": [None if self.Offer in [None, "", "None"] else self.Offer],
            "PhoneService": [self.PhoneService],
            "AvgMonthlyLongDistanceCharges": [self.AvgMonthlyLongDistanceCharges],
            "MultipleLines": [self.MultipleLines],
            "InternetType": [None if self.InternetType in [None, "", "None"] else self.InternetType],
            "AvgMonthlyGBDownload": [self.AvgMonthlyGBDownload],
            "OnlineSecurity": [self.OnlineSecurity],
            "OnlineBackup": [self.OnlineBackup],
            "DeviceProtectionPlan": [self.DeviceProtectionPlan],
            "PremiumTechSupport": [self.PremiumTechSupport],
            "StreamingTV": [self.StreamingTV],
            "StreamingMovies": [self.StreamingMovies],
            "StreamingMusic": [self.StreamingMusic],
            "UnlimitedData": [self.UnlimitedData],
            "Contract": [self.Contract],
            "PaperlessBilling": [self.PaperlessBilling],
            "PaymentMethod": [self.PaymentMethod],
            "MonthlyCharge": [self.MonthlyCharge],
            "TotalCharges": [self.TotalCharges],
            "TotalRefunds": [self.TotalRefunds],
            "TotalExtraDataCharges": [self.TotalExtraDataCharges],
            "TotalLongDistanceCharges": [self.TotalLongDistanceCharges],
            "TotalRevenue": [self.TotalRevenue],
            "SatisfactionScore": [self.SatisfactionScore],
        }
        return pd.DataFrame(data_dict)

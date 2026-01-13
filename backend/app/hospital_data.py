import json
import os
from typing import List, Dict, Optional

# Define the path relative to this file
DATA_FILE_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "data", "hospital_info.json")

class HospitalData:
    def __init__(self):
        self.data = self._load_data()

    def _load_data(self) -> Dict:
        try:
            with open(DATA_FILE_PATH, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            print(f"Error: Data file not found at {DATA_FILE_PATH}")
            return {}

    def get_general_info(self) -> str:
        info = self.data.get("general_info", {})
        return "\n".join([f"{k.replace('_', ' ').title()}: {v}" for k, v in info.items()])

    def get_departments(self) -> str:
        depts = self.data.get("departments", [])
        return "\n".join([f"- {d['name']} ({d['location']})" for d in depts])

    def get_doctors(self) -> str:
        docs = self.data.get("doctors", [])
        return "\n".join([f"- {d['name']} ({d['specialty']}): {d['availability']}" for d in docs])
    
    def get_doctor_by_name(self, name_query: str) -> str:
        docs = self.data.get("doctors", [])
        matching_docs = [d for d in docs if name_query.lower() in d['name'].lower()]
        if not matching_docs:
            return "No doctor found with that name."
        return "\n".join([f"- {d['name']} ({d['specialty']}): {d['availability']}" for d in matching_docs])

    def get_billing_info(self) -> str:
        billing = self.data.get("billing", {})
        insurance = ", ".join(billing.get("insurance_accepted", []))
        methods = ", ".join(billing.get("payment_methods", []))
        return f"Insurance Accepted: {insurance}\nPayment Methods: {methods}"

# Global instance for easy access
hospital_data = HospitalData()

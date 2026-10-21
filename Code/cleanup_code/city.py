
import csv
import re
from pathlib import Path

import pandas as pd


INPUT_FILE = Path("Datasets/merged.csv")
OUTPUT_FILE = Path("Datasets/merged_city_cleaned.csv")
REVIEW_FILE = Path("Datasets/city_values_to_review.csv")


# Indian city names and common spelling variants/localities.
ALIASES = {
    "Bengaluru": [
        "bengaluru", "bangalore", "banglore", "koramangala",
        "kormangala", "whitefield", "electronic city",
    ],
    "Mumbai": [
        "mumbai", "bombay", "andheri", "andheri east", "andheri west",
        "powai", "chembur", "bandra", "navi mumbai", "vasai", "virar",
    ],
    "Delhi": ["delhi", "new delhi", "newdelhi", "nw delhi"],
    "Gurugram": ["gurugram", "gurgaon", "gurgoan"],
    "Noida": ["noida", "greater noida"],
    "Ahmedabad": ["ahmedabad", "ahmadabad", "ahemdabad", "ahemadabad"],
    "Kolkata": ["kolkata", "calcutta", "kolkatta"],
    "Chennai": ["chennai", "madras"],
    "Hyderabad": ["hyderabad", "secunderabad", "hydrabad"],
    "Pune": ["pune", "poona"],
    "Jaipur": ["jaipur"],
    "Chandigarh": ["chandigarh"],
    "Indore": ["indore"],
    "Kochi": ["kochi", "cochin"],
    "Thiruvananthapuram": ["thiruvananthapuram", "trivandrum"],
    "Coimbatore": ["coimbatore"],
    "Vadodara": ["vadodara", "baroda"],
    "Surat": ["surat"],
    "Rajkot": ["rajkot"],
    "Gandhinagar": ["gandhinagar"],
    "Bhopal": ["bhopal"],
    "Nagpur": ["nagpur"],
    "Nashik": ["nashik", "nasik"],
    "Lucknow": ["lucknow"],
    "Kanpur": ["kanpur"],
    "Varanasi": ["varanasi", "banaras"],
    "Agra": ["agra"],
    "Prayagraj": ["prayagraj", "allahabad"],
    "Patna": ["patna"],
    "Ranchi": ["ranchi"],
    "Bhubaneswar": ["bhubaneswar", "bhubaneshwar"],
    "Visakhapatnam": ["visakhapatnam", "vizag", "vishakhapatnam"],
    "Vijayawada": ["vijayawada"],
    "Guntur": ["guntur"],
    "Tirupati": ["tirupati"],
    "Mysuru": ["mysuru", "mysore"],
    "Mangaluru": ["mangaluru", "mangalore"],
    "Hubballi": ["hubballi", "hubli"],
    "Belagavi": ["belagavi", "belgaum"],
    "Amritsar": ["amritsar"],
    "Ludhiana": ["ludhiana"],
    "Jalandhar": ["jalandhar"],
    "Dehradun": ["dehradun"],
    "Haridwar": ["haridwar"],
    "Siliguri": ["siliguri"],
    "Jodhpur": ["jodhpur"],
    "Udaipur": ["udaipur"],
    "Kota": ["kota"],
    "Ajmer": ["ajmer"],
    "Jamshedpur": ["jamshedpur"],
    "Dhanbad": ["dhanbad"],
    "Guwahati": ["guwahati"],
    "Panaji": ["panaji", "panjim"],
    "Goa": ["goa"],
    "Thane": ["thane"],
    "Faridabad": ["faridabad"],
    "Ghaziabad": ["ghaziabad"],
    "Srinagar": ["srinagar"],
    "Rourkela": ["rourkela"],
    "Gaya": ["gaya"],
    "Karur": ["karur"],
    "Rajsamand": ["rajsamand"],
}


# Known foreign cities, countries, states, and regions.
FOREIGN = {
    "usa", "us", "u s a", "united states", "united states of america",
    "america", "uk", "u k", "united kingdom", "england", "scotland",
    "canada", "australia", "new zealand", "singapore", "dubai", "uae",
    "united arab emirates", "bangladesh", "pakistan", "sri lanka",
    "nepal", "china", "japan", "hong kong", "south korea", "germany",
    "france", "ireland", "netherlands", "switzerland", "sweden",
    "finland", "norway", "denmark", "spain", "italy", "portugal",
    "russia", "israel", "indonesia", "malaysia", "thailand", "vietnam",}
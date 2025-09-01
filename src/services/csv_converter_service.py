import csv
import json
import os
from datetime import datetime
import logging
from typing import Optional

logger = logging.getLogger(__name__)

class CSVConverterService:
    """Service for converting csv to json"""
    def convert_csv_to_json(self, csv_path: str, json_path: Optional[str] = None) -> str:
        "Converts csv files to json format"
        if json_path is None:
            json_path = os.path.splitext(csv_path)[0] + ".json"
            
        try:
            documents = []
            
            # Read the csv file
            with open(csv_path, "r", encoding="utf-8") as f:
                reader = csv.DictReader(f)
                for row in reader:
                    # Parse the date string to ISO format
                    date_str = row.get('CreateDate', '')
                    try:
                        # Handle the date format: "2020-02-15 17:57:21+00:00"
                        if date_str:
                            # Remove timezone info and parse
                            date_str_clean = date_str.split('+')[0].strip()
                            parsed_date = datetime.strptime(date_str_clean, "%Y-%m-%d %H:%M:%S")
                            iso_date = parsed_date.isoformat()
                        else:
                            iso_date = datetime.now().isoformat()
                    except ValueError:
                        logger.warning(f"Could not parse date: {date_str}, using current time")
                        iso_date = datetime.now().isoformat()
                    
                    doc = {
                        "text": row.get('text', ''),
                        "is_antisemitic": row.get('Antisemitic', '0') in ['1', 'true', 'yes'],
                        "created_at": iso_date
                    }
                    if doc['text']:
                        documents.append(doc)
            
            # Create a json file with the name of the csv and load the data to it
            with open(json_path, "w", encoding="utf-8") as f:
                json.dump(documents, f, indent=2, ensure_ascii=False)
                
            logger.info(f"Converted {len(documents)} records from {csv_path} to {json_path}.")
            return json_path
            
        except Exception as e:
            logger.error(f"Error converting from csv: {e}")
            raise
        
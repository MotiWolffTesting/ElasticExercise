import re
import os
import nltk
import logging
from typing import List

logger = logging.getLogger(__name__)

class WeaponsService:
    """Service for detecting weapon keywords in text"""
    
    def __init__(self):
        "Initialize service"
        try:
            # Download required NLTK data
            nltk.download('punkt', quiet=True)
            nltk.download('stopwords', quiet=True)
            logger.info("NLTK data loaded for weapon detection")
        except Exception as e:
            logger.warning(f"Could not download NLTK data: {e}")
            
        self.weapon_keywords = self._load_weapon_keywords()
        # Create compiled regex patterns
        self.weapon_patterns = [re.compile(r'\b' + re.escape(keyword) + r'\b', re.IGNORECASE) 
                               for keyword in self.weapon_keywords]
        
    def _load_weapon_keywords(self) -> List[str]:
        "Load weapon keywords from file"
        try:
            # Get the path to the file
            current_dir = os.path.dirname(os.path.abspath(__file__))
            weapons_file_path = os.path.join(current_dir, "weapons_list.txt")
            
            if not os.path.exists(weapons_file_path):
                logger.error(f"Weapons list file not found: {weapons_file_path}")
                return self._get_default_weapons()
            
            with open(weapons_file_path, 'r', encoding='utf-8') as file:
                weapons = [line.strip() for line in file if line.strip()]
                
            logger.info(f"Loaded {len(weapons)} weapon keywords from {weapons_file_path}")
            return weapons
        
        except Exception as e:
            logger.error(f"Error loading weapons list from file: {e}")
            return self._get_default_weapons()
        
    def _get_default_weapons(self) -> List[str]:
        "Get default weapon keywords as backup"
        return [
            "rifle", "gun", "pistol", "revolver", "shotgun", "machine gun",
            "assault rifle", "sniper rifle", "submachine gun", "handgun",
            "knife", "blade", "sword", "dagger", "machete", "bayonet",
            "bomb", "explosive", "grenade", "dynamite", "TNT", "C4",
            "rocket", "mtrissile", "launcher", "mortar", "artillery",
            "tank", "armored vehicle", "helicopter", "fighter jet",
            "ammunition", "bullet", "shell", "cartridge", "round",
            "weapon", "firearm", "armament", "ordnance"
        ]
        
    def detect_weapons(self, text: str) -> List[str]:
        "Detect weapon keywords in text using NLTK tokenization"
        if not text:
            return []
        
        try:
            # Use NLTK for better tokenization
            tokens = nltk.word_tokenize(text.lower())
            detected_weapons = []
            
            for keyword in self.weapon_keywords:
                # Check for exact matches and partial matches
                if (keyword.lower() in tokens or 
                    keyword.lower() in text.lower() or
                    any(keyword.lower() in token.lower() for token in tokens)):
                    detected_weapons.append(keyword)
            
            return list(set(detected_weapons))  # Remove duplicates
        
        except Exception as e:
            logger.error(f"Error in NLTK weapon detection, falling back to regex: {e}")
            return self._detect_weapons_regex(text)
        
    def _detect_weapons_regex(self, text: str) -> List[str]:
        "Backup weapon detection using regex patterns"
        if not text:
            return []
        
        detected_weapons = []
        for pattern in self.weapon_patterns:
            if pattern.search(text):
                # Extract the keyword from the pattern
                keyword = pattern.pattern.replace(r'\b', '').replace(r'\\', '')
                detected_weapons.append(keyword)
        
        return list(set(detected_weapons))
    
    def batch_detect_weapons(self, texts: List[str]) -> List[List[str]]:
        "Detect weapons in multiple texts"
        return [self.detect_weapons(text) for text in texts]
    
    def get_weapon_count(self, text: str) -> int:
        "Get count of unique weapons detected in text"
        return len(self.detect_weapons(text))
    
    def get_weapon_keywords(self) -> List[str]:
        "Get the current list of weapon keywords"
        return self.weapon_keywords.copy()

    async def detect_weapons_via_es(self, es_service, text: str) -> List[str]:
        """Detect weapons using Elasticsearch analyzer via provided ES service.

        es_service is expected to expose `detect_weapons_in_text(text: str) -> List[str]`.
        """
        if not text:
            return []
        try:
            return await es_service.detect_weapons_in_text(text)
        except Exception:
            # Fallback to local detection if ES call fails
            return self.detect_weapons(text)

        
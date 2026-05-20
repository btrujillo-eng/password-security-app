from backend.app.core import IVulnerabilityDetector, SAFETY_RULES
from backend.app.schemas import PasswordVulnerabilities, PasswordAnalyzed

from typing import List

class VulnerabilityDetector(IVulnerabilityDetector):
        
    def detect(self, raw_data: PasswordAnalyzed, default_vulnerabilty_value: PasswordVulnerabilities) -> List[PasswordVulnerabilities]:
        detected_vulnerabilities = []
        
        for attribute_name, triggier_value, vulnerability in SAFETY_RULES:
            current_value = getattr(raw_data, attribute_name)
            
            if current_value == triggier_value:
                detected_vulnerabilities.append(vulnerability)
                
        if not detected_vulnerabilities:
              return [default_vulnerabilty_value]
          
        return detected_vulnerabilities
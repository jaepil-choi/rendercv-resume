"""
Validation logic for CV items and profiles.
"""

from typing import Dict, List, Set
from datetime import datetime
from cv_builder.models import CVItem, Profile


class ValidationError(Exception):
    """Custom exception for validation errors."""
    pass


class Validator:
    """Validates CV items and profiles."""
    
    @staticmethod
    def validate_date_format(date_str: str) -> bool:
        """Validate date format (YYYY-MM or 'present')."""
        if date_str == 'present':
            return True
        
        try:
            datetime.strptime(date_str, '%Y-%m')
            return True
        except ValueError:
            return False
    
    @staticmethod
    def validate_date_order(start_date: str, end_date: str) -> bool:
        """Validate that start_date <= end_date."""
        if end_date == 'present':
            return True
        
        start = datetime.strptime(start_date, '%Y-%m')
        end = datetime.strptime(end_date, '%Y-%m')
        return start <= end
    
    @staticmethod
    def validate_bilingual_field(field: Dict[str, str], field_name: str) -> List[str]:
        """Validate that a field has both en and kr values."""
        errors = []
        if not isinstance(field, dict):
            errors.append(f"{field_name} must be a dictionary with 'en' and 'kr' keys")
            return errors
        
        if 'en' not in field or not field['en']:
            errors.append(f"{field_name} missing English translation")
        if 'kr' not in field or not field['kr']:
            errors.append(f"{field_name} missing Korean translation")
        
        return errors
    
    def validate_work_experience(self, item: CVItem) -> List[str]:
        """Validate work experience item."""
        errors = []
        data = item.data
        
        # Required fields
        required_fields = ['company', 'position', 'start_date', 'end_date', 'location', 'highlights']
        for field in required_fields:
            if field not in data:
                errors.append(f"Work experience '{item.id}' missing required field: {field}")
        
        # Validate bilingual fields
        if 'company' in data:
            errors.extend(self.validate_bilingual_field(data['company'], f"{item.id}.company"))
        if 'position' in data:
            errors.extend(self.validate_bilingual_field(data['position'], f"{item.id}.position"))
        if 'location' in data:
            errors.extend(self.validate_bilingual_field(data['location'], f"{item.id}.location"))
        
        # Validate dates
        if 'start_date' in data:
            if not self.validate_date_format(data['start_date']):
                errors.append(f"Work experience '{item.id}' has invalid start_date format")
        
        if 'end_date' in data:
            if not self.validate_date_format(data['end_date']):
                errors.append(f"Work experience '{item.id}' has invalid end_date format")
        
        if 'start_date' in data and 'end_date' in data:
            if self.validate_date_format(data['start_date']) and self.validate_date_format(data['end_date']):
                if not self.validate_date_order(data['start_date'], data['end_date']):
                    errors.append(f"Work experience '{item.id}' has end_date before start_date")
        
        # Validate highlights
        if 'highlights' in data:
            if not isinstance(data['highlights'], list) or len(data['highlights']) == 0:
                errors.append(f"Work experience '{item.id}' must have at least one highlight")
            else:
                for i, highlight in enumerate(data['highlights']):
                    errors.extend(self.validate_bilingual_field(highlight, f"{item.id}.highlights[{i}]"))
        
        return errors
    
    def validate_project(self, item: CVItem) -> List[str]:
        """Validate project item."""
        errors = []
        data = item.data
        
        # Required fields
        if 'name' not in data:
            errors.append(f"Project '{item.id}' missing required field: name")
        if 'highlights' not in data:
            errors.append(f"Project '{item.id}' missing required field: highlights")
        
        # Validate bilingual fields
        if 'name' in data:
            errors.extend(self.validate_bilingual_field(data['name'], f"{item.id}.name"))
        
        # Validate highlights
        if 'highlights' in data:
            if not isinstance(data['highlights'], list) or len(data['highlights']) == 0:
                errors.append(f"Project '{item.id}' must have at least one highlight")
            else:
                for i, highlight in enumerate(data['highlights']):
                    errors.extend(self.validate_bilingual_field(highlight, f"{item.id}.highlights[{i}]"))
        
        return errors
    
    def validate_education(self, item: CVItem) -> List[str]:
        """Validate education item."""
        errors = []
        data = item.data
        
        # Required fields
        required_fields = ['institution', 'area', 'degree']
        for field in required_fields:
            if field not in data:
                errors.append(f"Education '{item.id}' missing required field: {field}")
        
        # Validate bilingual fields
        if 'institution' in data:
            errors.extend(self.validate_bilingual_field(data['institution'], f"{item.id}.institution"))
        if 'area' in data:
            errors.extend(self.validate_bilingual_field(data['area'], f"{item.id}.area"))
        if 'degree' in data:
            errors.extend(self.validate_bilingual_field(data['degree'], f"{item.id}.degree"))
        if 'location' in data:
            errors.extend(self.validate_bilingual_field(data['location'], f"{item.id}.location"))
        
        # Validate dates if present
        if 'start_date' in data:
            if not self.validate_date_format(data['start_date']):
                errors.append(f"Education '{item.id}' has invalid start_date format")
        
        if 'end_date' in data:
            if not self.validate_date_format(data['end_date']):
                errors.append(f"Education '{item.id}' has invalid end_date format")
        
        # Validate highlights if present
        if 'highlights' in data:
            if isinstance(data['highlights'], list):
                for i, highlight in enumerate(data['highlights']):
                    errors.extend(self.validate_bilingual_field(highlight, f"{item.id}.highlights[{i}]"))
        
        return errors
    
    def validate_additional_info(self, item: CVItem) -> List[str]:
        """Validate additional info item."""
        errors = []
        data = item.data
        
        # Required fields
        if 'label' not in data:
            errors.append(f"Additional info '{item.id}' missing required field: label")
        if 'details' not in data:
            errors.append(f"Additional info '{item.id}' missing required field: details")
        
        # Validate bilingual fields
        if 'label' in data:
            errors.extend(self.validate_bilingual_field(data['label'], f"{item.id}.label"))
        if 'details' in data:
            errors.extend(self.validate_bilingual_field(data['details'], f"{item.id}.details"))
        
        return errors
    
    def validate_items(self, items: Dict[str, CVItem]) -> List[str]:
        """Validate all CV items."""
        errors = []
        
        # Check for unique IDs (should be guaranteed by dict, but check anyway)
        ids = set()
        for item in items.values():
            if item.id in ids:
                errors.append(f"Duplicate item ID: {item.id}")
            ids.add(item.id)
        
        # Validate each item based on type
        for item in items.values():
            if item.type == 'work_experience':
                errors.extend(self.validate_work_experience(item))
            elif item.type == 'project':
                errors.extend(self.validate_project(item))
            elif item.type == 'education':
                errors.extend(self.validate_education(item))
            elif item.type == 'additional_info':
                errors.extend(self.validate_additional_info(item))
            else:
                errors.append(f"Unknown item type: {item.type} for item {item.id}")
        
        return errors
    
    def validate_profile(self, profile: Profile, available_items: Dict[str, CVItem]) -> List[str]:
        """Validate profile against available items."""
        errors = []
        
        # Check that all referenced IDs exist
        for section_name, section_spec in profile.sections.items():
            for item_id in section_spec.include_ids:
                if item_id not in available_items:
                    errors.append(f"Profile '{profile.name}' section '{section_name}' references unknown item: {item_id}")
        
        return errors


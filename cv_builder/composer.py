"""
Composition logic for building RenderCV-compatible YAMLs.
"""

from typing import Dict, List, Any
from cv_builder.models import CVItem, Profile
import yaml


class Composer:
    """Composes CV from items and profile specifications."""
    
    @staticmethod
    def calculate_char_count(text: str) -> int:
        """Calculate character count for text."""
        return len(text)
    
    @staticmethod
    def extract_locale_text(data: Any, locale: str) -> Any:
        """Recursively extract text for a specific locale from bilingual data."""
        if isinstance(data, dict):
            # Check if this is a bilingual field
            if 'en' in data and 'kr' in data:
                return data.get(locale, data.get('en'))  # Fallback to en if locale not found
            else:
                # Recursively process dict
                return {k: Composer.extract_locale_text(v, locale) for k, v in data.items()}
        elif isinstance(data, list):
            return [Composer.extract_locale_text(item, locale) for item in data]
        else:
            return data
    
    def compose_work_experience_entry(self, item: CVItem, locale: str) -> Dict[str, Any]:
        """Compose a work experience entry for RenderCV."""
        data = item.data
        
        return {
            'company': data['company'].get(locale),
            'position': data['position'].get(locale),
            'start_date': data['start_date'],
            'end_date': data['end_date'],
            'location': data['location'].get(locale),
            'highlights': [h.get(locale) for h in data['highlights']]
        }
    
    def compose_project_entry(self, item: CVItem, locale: str) -> Dict[str, Any]:
        """Compose a project entry for RenderCV."""
        data = item.data
        
        return {
            'name': data['name'].get(locale),
            'highlights': [h.get(locale) for h in data['highlights']]
        }
    
    def compose_education_entry(self, item: CVItem, locale: str) -> Dict[str, Any]:
        """Compose an education entry for RenderCV."""
        data = item.data
        
        entry = {
            'institution': data['institution'].get(locale),
            'area': data['area'].get(locale),
        }
        
        # Add optional fields if present
        if 'degree' in data:
            entry['degree'] = data.get('degree', {}).get(locale)
        if 'start_date' in data:
            entry['start_date'] = data['start_date']
        if 'end_date' in data:
            entry['end_date'] = data['end_date']
        if 'location' in data:
            entry['location'] = data['location'].get(locale)
        if 'highlights' in data:
            entry['highlights'] = [h.get(locale) for h in data['highlights']]
        
        return entry
    
    def compose_additional_info_entry(self, item: CVItem, locale: str) -> Dict[str, Any]:
        """Compose an additional info entry for RenderCV."""
        data = item.data
        
        return {
            'label': data['label'].get(locale),
            'details': data['details'].get(locale)
        }
    
    def calculate_item_char_count(self, item: CVItem, locale: str) -> int:
        """Calculate total character count for an item in a specific locale."""
        data = item.data
        total_chars = 0
        
        # Count all text fields
        for key, value in data.items():
            if isinstance(value, dict) and locale in value:
                total_chars += len(value[locale])
            elif isinstance(value, list):
                for list_item in value:
                    if isinstance(list_item, dict) and locale in list_item:
                        total_chars += len(list_item[locale])
        
        return total_chars
    
    def select_items(self, all_items: Dict[str, CVItem], profile: Profile) -> Dict[str, List[CVItem]]:
        """Select items for each section based on profile specification."""
        selected = {}
        
        for section_name, section_spec in profile.sections.items():
            section_items = []
            
            # Select items by ID
            for item_id in section_spec.include_ids:
                if item_id in all_items:
                    section_items.append(all_items[item_id])
            
            # Sort by priority (lower number = higher priority)
            section_items.sort(key=lambda x: x.priority)
            
            # Apply max_items limit
            if section_spec.max_items:
                section_items = section_items[:section_spec.max_items]
            
            selected[section_name] = section_items
        
        return selected
    
    def build_sections(self, selected_items: Dict[str, List[CVItem]], locale: str) -> Dict[str, List[Dict[str, Any]]]:
        """Build RenderCV section structure from selected items."""
        sections = {}
        
        for section_name, items in selected_items.items():
            section_entries = []
            
            for item in items:
                if item.type == 'work_experience':
                    entry = self.compose_work_experience_entry(item, locale)
                elif item.type == 'project':
                    entry = self.compose_project_entry(item, locale)
                elif item.type == 'education':
                    entry = self.compose_education_entry(item, locale)
                elif item.type == 'additional_info':
                    entry = self.compose_additional_info_entry(item, locale)
                else:
                    continue
                
                section_entries.append(entry)
            
            sections[section_name] = section_entries
        
        return sections
    
    def compose_cv(self, base: Dict[str, Any], sections: Dict[str, List[Dict[str, Any]]]) -> Dict[str, Any]:
        """Merge base CV structure with composed sections."""
        cv = base.copy()
        
        # Add sections to cv
        if 'cv' not in cv:
            cv['cv'] = {}
        
        cv['cv']['sections'] = sections
        
        return cv
    
    def calculate_section_stats(self, selected_items: Dict[str, List[CVItem]], locale: str) -> Dict[str, Dict[str, int]]:
        """Calculate character count statistics for each section."""
        stats = {}
        
        for section_name, items in selected_items.items():
            total_chars = sum(self.calculate_item_char_count(item, locale) for item in items)
            stats[section_name] = {
                'item_count': len(items),
                'total_chars': total_chars
            }
        
        return stats


#!/usr/bin/env python3
"""
Supabase News Analysis Import Script

Imports analyzed news articles from CSV files into Supabase database.
Handles categories table population and stories table insertion with proper foreign keys.
"""

import os
import csv
import sys
from pathlib import Path
from typing import List, Dict, Optional
from dotenv import load_dotenv
from supabase import create_client, Client

# Load environment variables
load_dotenv()

SUPABASE_URL = os.getenv('SUPABASE_URL')
SUPABASE_KEY = os.getenv('SUPABASE_KEY')

if not SUPABASE_URL or not SUPABASE_KEY:
    print("ERROR: SUPABASE_URL and SUPABASE_KEY must be set in environment variables")
    sys.exit(1)


class NewsAnalysisImporter:
    """Handles import of news analysis data into Supabase."""
    
    def __init__(self, supabase_url: str, supabase_key: str):
        """Initialize Supabase client."""
        self.supabase: Client = create_client(supabase_url, supabase_key)
        self.category_map: Dict[str, int] = {}
    
    def clear_categories(self):
        """Clear all existing categories from the database."""
        try:
            print("Clearing categories table...")
            result = self.supabase.table('categories').delete().neq('id', 0).execute()
            print(f"✓ Categories cleared")
        except Exception as e:
            print(f"✗ Error clearing categories: {e}")
            raise
    
    def extract_categories(self, csv_file: Path) -> List[str]:
        """Extract unique categories from CSV file."""
        categories = set()
        
        try:
            with open(csv_file, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    # Extract categories from article metadata
                    # For this demo, we'll use Politics as default
                    # In production, you'd parse from article content or metadata
                    categories.add('Politics')
                    
                    # You could also infer categories from:
                    # - Article title keywords
                    # - Source classification
                    # - Content analysis
                    
        except Exception as e:
            print(f"✗ Error reading CSV {csv_file}: {e}")
        
        return list(categories)
    
    def insert_categories(self, categories: List[str]) -> Dict[str, int]:
        """Insert categories and return mapping of name to ID."""
        category_map = {}
        
        print(f"\nInserting {len(categories)} categories...")
        
        for category in categories:
            try:
                result = self.supabase.table('categories').insert({
                    'name': category
                }).execute()
                
                if result.data and len(result.data) > 0:
                    category_id = result.data[0]['id']
                    category_map[category] = category_id
                    print(f"  ✓ {category} (ID: {category_id})")
                else:
                    print(f"  ✗ Failed to insert category: {category}")
                    
            except Exception as e:
                print(f"  ✗ Error inserting category {category}: {e}")
        
        return category_map
    
    def import_story(self, row: Dict[str, str], category_id: int) -> bool:
        """Import a single story into the database."""
        try:
            story_data = {
                'summary': row.get('summary', ''),
                'accuracy_assessment': row.get('accuracy_assessment', ''),
                'accuracy_score': int(row.get('accuracy_score', 0)) if row.get('accuracy_score') else None,
                'propaganda_indicators': row.get('propaganda_indicators', ''),
                'propaganda_score': int(row.get('propaganda_score', 0)) if row.get('propaganda_score') else None,
                'author_sources': row.get('author_sources', ''),
                'author_source_bias': row.get('author_source_bias', ''),
                'ai_sources': row.get('ai_sources', ''),
                'overall_metrics': row.get('overall_metrics', ''),
                'category_id': category_id
            }
            
            result = self.supabase.table('stories').insert(story_data).execute()
            
            if result.data and len(result.data) > 0:
                return True
            else:
                return False
                
        except Exception as e:
            print(f"  ✗ Error importing story: {e}")
            return False
    
    def import_from_csv(self, csv_file: Path):
        """Import all stories from a CSV file."""
        imported = 0
        failed = 0
        
        print(f"\nImporting stories from {csv_file.name}...")
        
        try:
            with open(csv_file, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                
                for row in reader:
                    # For demo, use Politics category
                    # In production, determine category from article
                    category_name = 'Politics'
                    category_id = self.category_map.get(category_name)
                    
                    if not category_id:
                        print(f"  ⚠️  Category not found: {category_name}")
                        failed += 1
                        continue
                    
                    if self.import_story(row, category_id):
                        imported += 1
                        print(f"  ✓ Imported: {row.get('article_title', 'Unknown')[:60]}")
                    else:
                        failed += 1
                        print(f"  ✗ Failed: {row.get('article_title', 'Unknown')[:60]}")
                        
        except Exception as e:
            print(f"✗ Error processing CSV: {e}")
            return imported, failed
        
        return imported, failed
    
    def run_import(self, analysis_dir: Path):
        """Run complete import process."""
        print("=" * 70)
        print("NEWS ANALYSIS IMPORT TO SUPABASE")
        print("=" * 70)
        
        # Step 1: Clear categories
        self.clear_categories()
        
        # Step 2: Find master CSV
        master_csv = analysis_dir / 'master_analysis.csv'
        
        if not master_csv.exists():
            print(f"\n✗ Master CSV not found: {master_csv}")
            sys.exit(1)
        
        # Step 3: Extract and insert categories
        categories = self.extract_categories(master_csv)
        self.category_map = self.insert_categories(categories)
        
        if not self.category_map:
            print("\n✗ No categories inserted, aborting import")
            sys.exit(1)
        
        # Step 4: Import stories
        total_imported, total_failed = self.import_from_csv(master_csv)
        
        # Step 5: Summary
        print("\n" + "=" * 70)
        print("IMPORT SUMMARY")
        print("=" * 70)
        print(f"Categories created: {len(self.category_map)}")
        print(f"Stories imported: {total_imported}")
        print(f"Stories failed: {total_failed}")
        print("=" * 70)
        
        if total_failed > 0:
            print("\n⚠️  Some stories failed to import. Check error messages above.")
            return False
        else:
            print("\n✓ Import completed successfully!")
            return True


def main():
    """Main entry point."""
    analysis_dir = Path(__file__).parent / 'news_analysis_md'
    
    if not analysis_dir.exists():
        print(f"✗ Analysis directory not found: {analysis_dir}")
        sys.exit(1)
    
    importer = NewsAnalysisImporter(SUPABASE_URL, SUPABASE_KEY)
    success = importer.run_import(analysis_dir)
    
    sys.exit(0 if success else 1)


if __name__ == '__main__':
    main()

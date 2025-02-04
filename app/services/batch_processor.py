from typing import Dict, List, Any, Tuple
import pandas as pd
import structlog
from concurrent.futures import ThreadPoolExecutor, as_completed
from .data_pipeline import DataPipeline

class BatchPropertyProcessor:
    """Process multiple properties from CSV file"""
    
    def __init__(self):
        self.data_pipeline = DataPipeline()
        self.logger = structlog.get_logger().bind(service="batch_processor")

    def process_csv(self, csv_path: str, max_workers: int = 4) -> Dict[str, Any]:
        """
        Process multiple properties from a CSV file
        
        Args:
            csv_path: Path to the CSV file
            max_workers: Maximum number of concurrent processing threads
            
        Returns:
            Dict containing results summary and detailed status
        """
        try:
            # Read CSV file
            self.logger.info("reading_csv_file", path=csv_path)
            df = pd.read_csv(csv_path)
            
            # Initialize results tracking
            results = {
                'total': len(df),
                'successful': 0,
                'failed': 0,
                'errors': [],
                'processed_ids': []
            }

            # Process properties concurrently
            with ThreadPoolExecutor(max_workers=max_workers) as executor:
                # Create future tasks
                future_to_property = {
                    executor.submit(self.process_single_property, row): row 
                    for _, row in df.iterrows()
                }
                
                # Process completed tasks
                for future in as_completed(future_to_property):
                    property_row = future_to_property[future]
                    try:
                        success, property_id, error = future.result()
                        if success:
                            results['successful'] += 1
                            results['processed_ids'].append(property_id)
                        else:
                            results['failed'] += 1
                            results['errors'].append({
                                'property_id': property_id,
                                'error': str(error)
                            })
                    except Exception as e:
                        results['failed'] += 1
                        results['errors'].append({
                            'property_id': property_row.get('CRM Reference', 'Unknown'),
                            'error': str(e)
                        })

            self.logger.info(
                "csv_processing_completed",
                total=results['total'],
                successful=results['successful'],
                failed=results['failed']
            )
            
            return results

        except Exception as e:
            self.logger.error("csv_processing_error", error=str(e))
            raise

    def process_single_property(self, row: pd.Series) -> Tuple[bool, str, str]:
        """
        Process a single property from CSV row
        
        Args:
            row: Pandas Series containing property data
            
        Returns:
            Tuple of (success: bool, property_id: str, error: str)
        """
        property_id = row.get('CRM Reference', 'Unknown')
        
        try:
            # Convert row to dictionary and clean null values
            property_data = row.to_dict()
            property_data = {
                k: ('' if pd.isna(v) else v) 
                for k, v in property_data.items()
            }

            # Process through pipeline
            self.data_pipeline.process_property_data(property_data)
            
            return True, property_id, ''

        except Exception as e:
            self.logger.error(
                "property_processing_error",
                property_id=property_id,
                error=str(e)
            )
            return False, property_id, str(e)

    def validate_csv_format(self, csv_path: str) -> Tuple[bool, List[str]]:
        """
        Validate CSV file format and required columns
        
        Args:
            csv_path: Path to the CSV file
            
        Returns:
            Tuple of (is_valid: bool, missing_columns: List[str])
        """
        required_columns = {
            'id', 'title', 'description', 'type',
            'price', 'country', 'region', 'municipality', 'town',
            'postcode', 'features'
        }
        
        try:
            df = pd.read_csv(csv_path)
            existing_columns = set(df.columns)
            missing_columns = required_columns - existing_columns
            
            is_valid = len(missing_columns) == 0
            
            if not is_valid:
                self.logger.warning(
                    "csv_validation_failed",
                    missing_columns=list(missing_columns)
                )
            
            return is_valid, list(missing_columns)
            
        except Exception as e:
            self.logger.error("csv_validation_error", error=str(e))
            return False, ["Error reading CSV file: " + str(e)]
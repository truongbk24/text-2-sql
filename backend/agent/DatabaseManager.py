import psycopg2
from psycopg2.extras import RealDictCursor
from typing import List, Dict, Any, Sequence


class DatabaseManager:
    """Manages database connections and operations for the text-2-sql agent."""
    
    def __init__(self, host: str = "localhost", port: int = 5432, 
                 user: str = "postgres", password: str = "password", 
                 database: str = "text2sql"):
        """
        Initialize database connection parameters.
        
        Args:
            host: Database host address
            port: Database port number
            user: Database user
            password: Database password
            database: Database name
        """
        self.host = host
        self.port = port
        self.user = user
        self.password = password
        self.database = database
        self.connection = None
    
    def get_schema(self, schema_name: str = "public") -> Dict[str, Any]:
        """
        Retrieve the database schema information.
        
        Returns:
            Dictionary containing tables, columns, and their data types
        """
        try:
            conn = psycopg2.connect(
                host=self.host,
                port=self.port,
                user=self.user,
                password=self.password,
                database=self.database
            )
            cursor = conn.cursor(cursor_factory=RealDictCursor)
            
            # Query to get table and column information
            schema_query = f"""
                SELECT 
                    t.table_name,
                    c.column_name,
                    c.data_type,
                    c.is_nullable,
                    ccu.table_name AS foreign_table_name,
                    ccu.column_name AS foreign_column_name
                FROM 
                    information_schema.tables t
                JOIN information_schema.columns c 
                    ON t.table_name = c.table_name 
                    AND t.table_schema = c.table_schema
                LEFT JOIN information_schema.key_column_usage kcu
                    ON c.table_name = kcu.table_name
                    AND c.column_name = kcu.column_name
                    AND c.table_schema = kcu.table_schema
                LEFT JOIN information_schema.table_constraints tc
                    ON kcu.constraint_name = tc.constraint_name
                    AND kcu.table_schema = tc.table_schema
                    AND tc.constraint_type = 'FOREIGN KEY'
                LEFT JOIN information_schema.constraint_column_usage ccu
                    ON tc.constraint_name = ccu.constraint_name
                    AND tc.table_schema = ccu.table_schema
                WHERE 
                    t.table_schema = '{schema_name}'
                ORDER BY 
                    t.table_name, 
                    c.ordinal_position;
            """
            cursor.execute(schema_query)
            rows = cursor.fetchall()
            schema = {}
            for row in rows:
                table_name = row['table_name']
                if table_name not in schema:
                    schema[table_name] = {
                        'table_name': f"{schema_name}.{table_name}",
                        'columns': []
                    }
                schema[table_name]['columns'].append({
                    'column_name': row['column_name'],
                    'data_type': row['data_type'],
                    'is_nullable': row['is_nullable'],
                    'foreign_table_name': row['foreign_table_name'],
                    'foreign_column_name': row['foreign_column_name']
                })
            
            cursor.close()
            conn.close()
            return schema
            
        except Exception as e:
            raise Exception(f"Error retrieving schema: {str(e)}")
    
    def execute_query(self, query: str) -> Sequence[Dict[str, Any]]:
        """
        Execute a SQL query and return results.
        
        Args:
            query: SQL query string to execute
            
        Returns:
            List of dictionaries containing query results
        """
        try:
            conn = psycopg2.connect(
                host=self.host,
                port=self.port,
                user=self.user,
                password=self.password,
                database=self.database
            )
            cursor = conn.cursor(cursor_factory=RealDictCursor)
            print(f"Executing query: {query}")
            cursor.execute(query)
            results = cursor.fetchall()
            
            cursor.close()
            conn.close()
            
            return results
            
        except Exception as e:
            raise Exception(f"Error executing query: {str(e)}")

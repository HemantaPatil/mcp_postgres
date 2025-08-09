import asyncio
import asyncpg
from mcp.server.fastmcp import FastMCP
import json
import logging

logger = logging.getLogger(__name__)

# Initialize the FastMCP server
mcp = FastMCP("usda-postgres")

# Database configuration
db_config = {
    "host": "localhost",
    "port": 5432,
    "database": "usda",
    "user": "postgres",
    "password": "postgres"
}

# Global database pool
db_pool = None

async def get_db_pool():
    global db_pool
    if db_pool is None:
        try:
            db_pool = await asyncpg.create_pool(**db_config)
            logger.info("Successfully connected to USDA PostgreSQL database")
        except Exception as e:
            logger.error(f"Failed to connect to database: {e}")
            raise
    return db_pool

@mcp.tool()
async def execute_query(query: str, params: list[str] = None) -> str:
    """Execute a SQL query on the USDA database
    
    Args:
        query: The SQL query to execute
        params: Optional parameters for the query
        
    Returns:
        JSON string containing the query results
    """
    try:
        pool = await get_db_pool()
        async with pool.acquire() as conn:
            if params:
                result = await conn.fetch(query, *params)
            else:
                result = await conn.fetch(query)
            
            rows = [dict(row) for row in result]
            return json.dumps(rows, indent=2, default=str)
    except Exception as e:
        logger.error(f"Error executing query: {e}")
        return f"Error: {str(e)}"

@mcp.tool()
async def list_tables() -> str:
    """List all tables in the USDA database
    
    Returns:
        JSON string containing list of table names
    """
    try:
        pool = await get_db_pool()
        query = """
        SELECT table_name 
        FROM information_schema.tables 
        WHERE table_schema = 'public' 
        ORDER BY table_name;
        """
        async with pool.acquire() as conn:
            result = await conn.fetch(query)
            tables = [row['table_name'] for row in result]
            return json.dumps(tables, indent=2)
    except Exception as e:
        logger.error(f"Error listing tables: {e}")
        return f"Error: {str(e)}"

@mcp.tool()
async def describe_table(table_name: str) -> str:
    """Get the schema/structure of a specific table
    
    Args:
        table_name: Name of the table to describe
        
    Returns:
        JSON string containing table schema information
    """
    try:
        pool = await get_db_pool()
        query = """
        SELECT column_name, data_type, is_nullable, column_default
        FROM information_schema.columns 
        WHERE table_name = $1 AND table_schema = 'public'
        ORDER BY ordinal_position;
        """
        async with pool.acquire() as conn:
            result = await conn.fetch(query, table_name)
            columns = [dict(row) for row in result]
            return json.dumps(columns, indent=2)
    except Exception as e:
        logger.error(f"Error describing table {table_name}: {e}")
        return f"Error: {str(e)}"

@mcp.tool()
async def get_table_sample(table_name: str, limit: int = 10) -> str:
    """Get a sample of data from a specific table
    
    Args:
        table_name: Name of the table to sample
        limit: Number of rows to return (default: 10)
        
    Returns:
        JSON string containing sample data
    """
    try:
        pool = await get_db_pool()
        query = f"SELECT * FROM {table_name} LIMIT $1;"
        async with pool.acquire() as conn:
            result = await conn.fetch(query, limit)
            rows = [dict(row) for row in result]
            return json.dumps(rows, indent=2, default=str)
    except Exception as e:
        logger.error(f"Error getting sample from table {table_name}: {e}")
        return f"Error: {str(e)}"

@mcp.tool()
async def search_foods(keyword: str, limit: int = 20) -> str:
    """Search for foods by keyword in their names or descriptions
    
    Args:
        keyword: Search term to look for in food names
        limit: Maximum number of results to return (default: 20)
        
    Returns:
        JSON string containing matching foods with their categories
    """
    try:
        pool = await get_db_pool()
        query = """
        SELECT 
            fd.ndb_no,
            fd.long_desc,
            fd.shrt_desc,
            fg.fddrp_desc as food_group
        FROM food_des fd
        JOIN fd_group fg ON fd.fdgrp_cd = fg.fdgrp_cd
        WHERE fd.long_desc ILIKE $1 OR fd.shrt_desc ILIKE $1
        ORDER BY fd.long_desc
        LIMIT $2;
        """
        async with pool.acquire() as conn:
            result = await conn.fetch(query, f"%{keyword}%", limit)
            foods = [dict(row) for row in result]
            return json.dumps(foods, indent=2, default=str)
    except Exception as e:
        logger.error(f"Error searching foods: {e}")
        return f"Error: {str(e)}"

@mcp.tool()
async def get_nutrition_profile(ndb_no: str) -> str:
    """Get complete nutrition profile for a specific food
    
    Args:
        ndb_no: USDA food database number (NDB number)
        
    Returns:
        JSON string containing complete nutrition information
    """
    try:
        pool = await get_db_pool()
        query = """
        SELECT 
            fd.long_desc,
            fd.shrt_desc,
            fg.fddrp_desc as food_group,
            nd.nutrdesc,
            nd.units,
            n.nutr_val,
            nd.sr_order
        FROM food_des fd
        JOIN fd_group fg ON fd.fdgrp_cd = fg.fdgrp_cd
        JOIN nut_data n ON fd.ndb_no = n.ndb_no
        JOIN nutr_def nd ON n.nutr_no = nd.nutr_no
        WHERE fd.ndb_no = $1 AND n.nutr_val > 0
        ORDER BY nd.sr_order;
        """
        async with pool.acquire() as conn:
            result = await conn.fetch(query, ndb_no)
            if not result:
                return json.dumps({"error": f"No food found with NDB number: {ndb_no}"})
            
            profile = [dict(row) for row in result]
            return json.dumps(profile, indent=2, default=str)
    except Exception as e:
        logger.error(f"Error getting nutrition profile: {e}")
        return f"Error: {str(e)}"

@mcp.tool()
async def get_foods_by_category(category: str, limit: int = 50) -> str:
    """Get foods from a specific food category
    
    Args:
        category: Food category name (e.g., "Fruits and Fruit Juices")
        limit: Maximum number of results to return (default: 50)
        
    Returns:
        JSON string containing foods in the specified category
    """
    try:
        pool = await get_db_pool()
        query = """
        SELECT 
            fd.ndb_no,
            fd.long_desc,
            fd.shrt_desc
        FROM food_des fd
        JOIN fd_group fg ON fd.fdgrp_cd = fg.fdgrp_cd
        WHERE fg.fddrp_desc ILIKE $1
        ORDER BY fd.long_desc
        LIMIT $2;
        """
        async with pool.acquire() as conn:
            result = await conn.fetch(query, f"%{category}%", limit)
            foods = [dict(row) for row in result]
            return json.dumps(foods, indent=2, default=str)
    except Exception as e:
        logger.error(f"Error getting foods by category: {e}")
        return f"Error: {str(e)}"

@mcp.tool()
async def get_food_categories() -> str:
    """Get all available food categories
    
    Returns:
        JSON string containing all food categories with food counts
    """
    try:
        pool = await get_db_pool()
        query = """
        SELECT 
            fg.fdgrp_cd,
            fg.fddrp_desc,
            COUNT(fd.ndb_no) as food_count
        FROM fd_group fg
        LEFT JOIN food_des fd ON fg.fdgrp_cd = fd.fdgrp_cd
        GROUP BY fg.fdgrp_cd, fg.fddrp_desc
        ORDER BY food_count DESC;
        """
        async with pool.acquire() as conn:
            result = await conn.fetch(query)
            categories = [dict(row) for row in result]
            return json.dumps(categories, indent=2, default=str)
    except Exception as e:
        logger.error(f"Error getting food categories: {e}")
        return f"Error: {str(e)}"

@mcp.tool()
async def compare_foods_nutrition(ndb_numbers: list[str], nutrients: list[str] = None) -> str:
    """Compare nutrition values between multiple foods
    
    Args:
        ndb_numbers: List of USDA food database numbers to compare
        nutrients: List of specific nutrients to compare (optional, defaults to key nutrients)
        
    Returns:
        JSON string containing nutrition comparison
    """
    try:
        pool = await get_db_pool()
        
        # Default nutrients if none specified
        if nutrients is None:
            nutrients = ['Energy', 'Protein', 'Total lipid (fat)', 'Carbohydrate, by difference']
        
        # Build query with placeholders
        ndb_placeholders = ','.join([f'${i+1}' for i in range(len(ndb_numbers))])
        nutrient_conditions = ' OR '.join([f'nd.nutrdesc = ${len(ndb_numbers) + i + 1}' for i in range(len(nutrients))])
        
        query = f"""
        SELECT 
            fd.ndb_no,
            fd.long_desc,
            nd.nutrdesc,
            nd.units,
            n.nutr_val
        FROM food_des fd
        JOIN nut_data n ON fd.ndb_no = n.ndb_no
        JOIN nutr_def nd ON n.nutr_no = nd.nutr_no
        WHERE fd.ndb_no IN ({ndb_placeholders})
        AND ({nutrient_conditions})
        ORDER BY fd.long_desc, nd.sr_order;
        """
        
        params = ndb_numbers + nutrients
        async with pool.acquire() as conn:
            result = await conn.fetch(query, *params)
            comparison = [dict(row) for row in result]
            return json.dumps(comparison, indent=2, default=str)
    except Exception as e:
        logger.error(f"Error comparing foods: {e}")
        return f"Error: {str(e)}"

@mcp.tool()
async def find_foods_high_in_nutrient(nutrient: str, limit: int = 20) -> str:
    """Find foods that are highest in a specific nutrient
    
    Args:
        nutrient: Name of the nutrient (e.g., "Protein", "Vitamin C")
        limit: Maximum number of results to return (default: 20)
        
    Returns:
        JSON string containing foods with highest amounts of the nutrient
    """
    try:
        pool = await get_db_pool()
        query = """
        SELECT 
            fd.long_desc,
            fg.fddrp_desc as food_group,
            nd.nutrdesc,
            nd.units,
            n.nutr_val
        FROM food_des fd
        JOIN fd_group fg ON fd.fdgrp_cd = fg.fdgrp_cd
        JOIN nut_data n ON fd.ndb_no = n.ndb_no
        JOIN nutr_def nd ON n.nutr_no = nd.nutr_no
        WHERE nd.nutrdesc ILIKE $1 AND n.nutr_val > 0
        ORDER BY n.nutr_val DESC
        LIMIT $2;
        """
        async with pool.acquire() as conn:
            result = await conn.fetch(query, f"%{nutrient}%", limit)
            foods = [dict(row) for row in result]
            return json.dumps(foods, indent=2, default=str)
    except Exception as e:
        logger.error(f"Error finding foods high in nutrient: {e}")
        return f"Error: {str(e)}"

async def cleanup():
    """Close database connections"""
    global db_pool
    if db_pool:
        await db_pool.close()

async def main():
    try:
        await mcp.run_stdio_async()
    finally:
        await cleanup()

if __name__ == "__main__":
    asyncio.run(main())

# USDA Nutrition Database MCP Server

A comprehensive Model Context Protocol (MCP) server that provides intelligent access to the USDA nutrition database through AI assistants like Claude Desktop. Transform complex nutrition data into conversational queries and get authoritative answers about food composition, nutritional content, and dietary analysis.

[![Python Version](https://img.shields.io/badge/python-3.13+-blue.svg)](https://python.org)
[![MCP Compatible](https://img.shields.io/badge/MCP-Compatible-green.svg)](https://modelcontextprotocol.io)
[![Database](https://img.shields.io/badge/database-PostgreSQL-blue.svg)](https://postgresql.org)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)

## <N What This Provides

- **= Smart Food Search** - Find foods by keywords across 7,146+ items
- **=Ê Complete Nutrition Profiles** - Get detailed nutrition data for any food
- **– Food Comparisons** - Compare nutritional content between foods
- **=ª Nutrient-Focused Discovery** - Find foods highest in specific nutrients
- **=Â Category Browsing** - Explore foods by category (24 major groups)
- **>ì Scientific Data Access** - Direct access to USDA's authoritative nutrition database

## =€ Quick Start

### Prerequisites

- Python 3.13+
- PostgreSQL with USDA nutrition database loaded
- Claude Desktop (recommended) or MCP-compatible client

### Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/your-username/usda-mcp-server.git
   cd usda-mcp-server
   ```

2. **Install dependencies:**
   ```bash
   # Using pip
   pip install -r requirements.txt
   
   # Using uv (recommended)
   uv sync
   ```

3. **Configure database connection:**
   
   Edit the database configuration in `main.py` if needed:
   ```python
   db_config = {
       "host": "localhost",
       "port": 5432,
       "database": "usda",
       "user": "postgres",
       "password": "postgres"
   }
   ```

4. **Configure Claude Desktop:**
   
   Add to your `claude_desktop_config.json`:
   ```json
   {
     "mcpServers": {
       "usda-postgres": {
         "command": "python",
         "args": ["/absolute/path/to/main.py"]
       }
     }
   }
   ```

5. **Start using:**
   
   Restart Claude Desktop and ask questions like:
   - "Find foods high in protein"
   - "Compare the nutrition of chicken and salmon"
   - "What are the different types of apples in the database?"

## =à Available Tools

The MCP server provides 10 specialized tools:

### Core Database Tools
| Tool | Description |
|------|-------------|
| `execute_query` | Execute custom SQL queries on the database |
| `list_tables` | List all available database tables |
| `describe_table` | Get schema information for any table |
| `get_table_sample` | View sample data from any table |

### Nutrition-Specific Tools
| Tool | Description |
|------|-------------|
| `search_foods` | Search foods by keyword in names/descriptions |
| `get_nutrition_profile` | Get complete nutrition data for a specific food |
| `get_foods_by_category` | Browse foods within specific categories |
| `get_food_categories` | List all food categories with counts |
| `compare_foods_nutrition` | Compare nutrition between multiple foods |
| `find_foods_high_in_nutrient` | Find foods with highest amounts of specific nutrients |

## =¬ Claude Desktop Integration Examples

### Finding High-Protein Foods
![Claude Desktop - Finding High-Protein Foods](claude_desktop_protein_search.png)

### Nutrition Comparison Between Foods  
![Claude Desktop - Nutrition Comparison](claude_desktop_nutrition_comparison.png)

### Interactive Food Search
![Claude Desktop - Food Search Interface](claude_desktop_food_search.png)

## >ê Testing

### Method 1: Automated Test Suite
```bash
python test_mcp_server.py
```

This comprehensive test script validates:
- Database connectivity
- All tool functionality
- Performance benchmarking
- Interactive demos

### Method 2: MCP Inspector (Web UI)
```bash
# Install MCP Inspector
npm install -g @modelcontextprotocol/inspector

# Launch web interface
mcp-inspector python main.py
```

Open `http://localhost:5173` to browse tools and test interactively.

### Method 3: Command Line Testing
```bash
# Install MCP CLI
npm install -g @modelcontextprotocol/cli

# List available tools
mcp list-tools python main.py

# Test a specific tool
mcp call-tool python main.py search_foods '{"keyword": "apple", "limit": 5}'
```

### Method 4: Direct Python Testing
```python
import asyncio
from main import mcp

async def test():
    result = await mcp.call_tool("search_foods", {"keyword": "chicken"})
    print(result)

asyncio.run(test())
```

## =Ê Database Overview

The USDA database contains:

| Table | Rows | Description |
|-------|------|-------------|
| `food_des` | 7,146 | Food descriptions and metadata |
| `nut_data` | 253,825 | Nutrition values for each food/nutrient |
| `nutr_def` | 136 | Nutrient definitions and units |
| `fd_group` | 24 | Food category classifications |
| `data_src` | 366 | Scientific references and sources |
| Others | 5,100+ | Supporting data (weights, footnotes, etc.) |

**Total:** 368,416+ records of authoritative nutrition data

### Key Statistics
- **7,146 foods** across 24 major categories
- **136 different nutrients** tracked (vitamins, minerals, macronutrients)
- **Most tracked nutrient:** Energy (6,746 foods have calorie data)
- **Largest category:** Vegetables and Vegetable Products (788 foods)
- **Data sources:** 366 scientific studies and references

## <× Architecture

### Technology Stack
- **Python 3.13+** with asyncio for high-performance async operations
- **FastMCP** for clean, decorator-based tool definitions
- **asyncpg** for high-performance PostgreSQL connectivity
- **Connection pooling** for efficient database resource management

### Key Components

```python
# MCP Server with tool decorators
mcp = FastMCP("usda-postgres")

@mcp.tool()
async def search_foods(keyword: str, limit: int = 20) -> str:
    """Search for foods by keyword"""
    # Implementation with optimized queries
```

### Performance Features
- **Connection pooling** for database efficiency
- **Async operations** for concurrent request handling
- **Optimized SQL queries** with proper indexing
- **JSON responses** with structured data formatting

## =' Configuration

### Database Connection
Update `main.py` database configuration as needed:

```python
db_config = {
    "host": "localhost",        # Database host
    "port": 5432,              # PostgreSQL port  
    "database": "usda",        # Database name
    "user": "postgres",        # Database user
    "password": "postgres"     # Database password
}
```

### Claude Desktop Setup
Location of config file by OS:
- **macOS:** `~/Library/Application Support/Claude/claude_desktop_config.json`
- **Windows:** `%APPDATA%\Claude\claude_desktop_config.json`
- **Linux:** `~/.config/Claude/claude_desktop_config.json`

## = Troubleshooting

### Common Issues

**"Database connection failed"**
```bash
# Check if PostgreSQL is running
pg_ctl status

# Verify database exists
psql -h localhost -U postgres -l | grep usda

# Test connection
psql -h localhost -U postgres -d usda -c "SELECT COUNT(*) FROM food_des;"
```

**"No module named 'mcp'"**
```bash
# Install dependencies
pip install -r requirements.txt
# or
uv sync
```

**"Tools not appearing in Claude Desktop"**
1. Verify absolute path in config file
2. Restart Claude Desktop completely
3. Check server logs: `python main.py 2>&1 | tee server.log`

**Performance Issues**
```bash
# Check database indexes
psql -h localhost -U postgres -d usda -c "SELECT schemaname, tablename, indexname FROM pg_indexes WHERE schemaname = 'public';"
```

## =È Performance Benchmarks

Based on testing with the included test suite:

- **Average response time:** ~70ms per query
- **Concurrent requests:** Handles 5+ simultaneous requests efficiently
- **Database queries:** Optimized with proper indexing and connection pooling
- **Memory usage:** Efficient with connection pooling and async operations

## <¯ Use Cases

### For Nutritionists & Dietitians
- Quick lookup of comprehensive nutrition data
- Compare foods for meal planning
- Find best sources of specific nutrients
- Generate evidence-based recommendations

### For Researchers
- Access authoritative USDA nutrition data
- Analyze nutritional patterns across food categories
- Cross-reference multiple nutrients efficiently
- Export data for further analysis

### For Health-Conscious Consumers
- Make informed food choices
- Find foods high in desired nutrients
- Compare nutritional value of alternatives
- Learn about food composition

### For Food Industry
- Analyze competitive products
- Develop recipes targeting nutritional goals
- Ensure accurate nutritional labeling
- Research ingredient alternatives

## =ã Roadmap

### Planned Features
- [ ] **Recipe Analysis** - Calculate nutrition for complete recipes
- [ ] **Dietary Matching** - Find foods meeting specific dietary requirements
- [ ] **Portion Size Calculations** - Convert between different serving sizes
- [ ] **Trend Analysis** - Nutritional patterns across food categories
- [ ] **Export Functionality** - CSV/Excel export of query results

### Technical Improvements  
- [ ] **Caching Layer** for frequently accessed data
- [ ] **Full-text Search** for more sophisticated food discovery
- [ ] **GraphQL Interface** for flexible data querying
- [ ] **Real-time Updates** as USDA releases new data
- [ ] **Docker Support** for easier deployment

## > Contributing

Contributions are welcome! Please feel free to submit a Pull Request. For major changes, please open an issue first to discuss what you would like to change.

### Development Setup
1. Fork the repository
2. Create a feature branch: `git checkout -b feature-name`
3. Install dependencies: `uv sync`
4. Run tests: `python test_mcp_server.py`
5. Make your changes
6. Run tests again to ensure everything works
7. Submit a pull request

## =Ý License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## =O Acknowledgments

- **USDA** for maintaining the comprehensive nutrition database
- **Anthropic** for developing the Model Context Protocol
- **PostgreSQL** team for the robust database system
- **FastMCP** developers for the excellent Python framework

## =Ú Additional Resources

- [USDA Food Data Central](https://fdc.nal.usda.gov/) - Official USDA nutrition database
- [Model Context Protocol Documentation](https://modelcontextprotocol.io/) - MCP specification and guides
- [Claude Desktop](https://claude.ai/download) - Download Claude Desktop application
- [PostgreSQL Documentation](https://www.postgresql.org/docs/) - Database setup and configuration

## =Þ Support

If you encounter any issues or have questions:

1. Check the [Troubleshooting](#-troubleshooting) section
2. Run the test suite: `python test_mcp_server.py`
3. Check existing [Issues](../../issues)
4. Create a new issue with detailed information

---

**Built with d for the nutrition and AI communities**

*Making authoritative nutrition data accessible through intelligent AI conversations*

# ElasticSearch Malicious Text Analysis - CLI Commands

 "=== ElasticSearch Malicious Text Analysis - CLI Commands ==="
 ""

# 1. Start the services
 "1. START SERVICES:"
 "   docker-compose up --build -d"
 ""

# 2. Check service status
 "2. CHECK SERVICE STATUS:"
 "   # Check if containers are running"
 "   docker-compose ps"
 ""
 "   # Check Elasticsearch health"
 "   curl http://localhost:9200/_cluster/health"
 ""
 "   # Check app health"
 "   curl http://localhost:8080/health"
 ""

# 3. Process data
 "3. PROCESS DATA:"
 "   # Load and process CSV data (REQUIRED FIRST STEP)"
 "   curl -X POST http://localhost:8080/api/documents/process"
 ""

# 4. Check processing status
 "4. CHECK PROCESSING STATUS:"
 "   # Get current processing status"
 "   curl http://localhost:8080/api/documents/status"
 ""

# 5. Query results
 "5. QUERY RESULTS:"
 "   # Get antisemitic documents with weapons"
 "   curl http://localhost:8080/api/documents/antisemitic-with-weapons"
 ""
 "   # Get documents with 2+ weapons"
 "   curl http://localhost:8080/api/documents/multiple-weapons"
 ""

# 6. Elasticsearch direct queries
 "6. ELASTICSEARCH DIRECT QUERIES:"
 "   # Check indices"
 "   curl http://localhost:9200/_cat/indices"
 ""
 "   # Check mapping"
 "   curl http://localhost:9200/malicious_documents/_mapping"
 ""
 "   # Search for documents with weapons"
 "   curl \"http://localhost:9200/malicious_documents/_search?q=weapon_count:>0&size=5\""
 ""

# 7. Troubleshooting
 "7. TROUBLESHOOTING:"
 "   # Check app logs"
 "   docker-compose logs malicious-text-app -f"
 ""
 "   # Check Elasticsearch logs"
 "   docker-compose logs elasticsearch -f"
 ""
 "   # Restart services"
 "   docker-compose restart"
 ""

# 8. Stop services
 "8. STOP SERVICES:"
 "   docker-compose down"
 ""

# 9. Reset everything
 "9. RESET EVERYTHING:"
 "   docker-compose down -v"
 "   docker-compose up --build -d"
 ""

 "=== END OF COMMANDS ==="
 ""
 "IMPORTANT: Always run step 3 (process data) first before querying results!"
 "The processing may take several minutes to complete."

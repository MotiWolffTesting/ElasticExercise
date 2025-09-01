# ElasticSearch Malicious Text Analysis

A comprehensive system for analyzing malicious text data using ElasticSearch, with automatic sentiment analysis and weapon detection capabilities.

## Project Overview

This project implements a complete pipeline for processing and analyzing text data to identify antisemitic content and detect weapon-related keywords. The system uses ElasticSearch for efficient data storage and retrieval, with automated sentiment analysis and weapon detection.

## Features

- **Data Processing Pipeline**: Complete CSV to ElasticSearch processing workflow
- **Sentiment Analysis**: Automatic sentiment classification (positive, negative, neutral)
- **Weapon Detection**: Comprehensive keyword-based weapon identification
- **Data Filtering**: Automatic removal of irrelevant documents
- **RESTful API**: Two main endpoints for data analysis
- **Docker Support**: Complete containerization with ElasticSearch and application
- **Real-time Processing**: Efficient bulk processing and indexing

## System Requirements

- Docker and Docker Compose
- Python 3.11+
- ElasticSearch 8.x
- FastAPI framework

## Project Structure

```
ElasticExercise/
├── data/                          # Data files
│   └── tweets_injected_3.csv     # Input CSV data
├── src/                          # Source code
│   ├── config/                   # Configuration settings
│   ├── controllers/              # API controllers
│   ├── models/                   # Data models
│   ├── services/                 # Business logic services
│   └── main.py                   # Application entry point
├── scripts/                      # Utility scripts
│   └── commands.sh               # CLI commands reference
├── docker-compose.yml            # Docker services configuration
├── Dockerfile                    # Application container definition
├── requirements.txt              # Python dependencies
└── README.md                     # This file
```

## Quick Start

### 1. Clone the Repository

```bash
git clone <repository-url>
cd ElasticExercise
```

### 2. Start the Services

```bash
docker-compose up --build -d
```

This will start:
- ElasticSearch on port 9200
- Malicious Text Analysis API on port 8080

### 3. Wait for Services to be Ready

```bash
# Check ElasticSearch health
curl http://localhost:9200/_cluster/health

# Check API health
curl http://localhost:8080/health
```

### 4. Process Data

```bash
# Load and process CSV data (REQUIRED FIRST STEP)
curl -X POST http://localhost:8080/api/documents/process
```

### 5. Check Processing Status

```bash
curl http://localhost:8080/api/documents/status
```

## API Endpoints

### Health Check
- **GET** `/health` - Check application health status

### Data Processing
- **POST** `/api/documents/process` - Process all documents from CSV
- **GET** `/api/documents/status` - Get current processing status

### Analysis Results
- **GET** `/api/documents/antisemitic-with-weapons` - Get antisemitic documents with weapons
- **GET** `/api/documents/multiple-weapons` - Get documents with 2+ weapons

## Data Processing Pipeline

1. **CSV Loading**: Read and parse CSV data with proper date handling
2. **Data Validation**: Validate and clean input data
3. **ElasticSearch Indexing**: Create index with proper mapping and bulk index documents
4. **Sentiment Analysis**: Analyze text sentiment using NLP techniques
5. **Weapon Detection**: Scan text for weapon-related keywords
6. **Data Filtering**: Remove irrelevant documents based on criteria
7. **Results Storage**: Store processed results in ElasticSearch

## Configuration

### Environment Variables

The application can be configured using the following environment variables:

- `ELASTICSEARCH_HOST`: ElasticSearch host (default: localhost)
- `ELASTICSEARCH_PORT`: ElasticSearch port (default: 9200)
- `ELASTICSEARCH_USERNAME`: ElasticSearch username (default: elastic)
- `ELASTICSEARCH_PASSWORD`: ElasticSearch password (default: changeme)
- `ELASTICSEARCH_INDEX`: Index name (default: malicious_documents)
- `API_HOST`: API host (default: 0.0.0.0)
- `API_PORT`: API port (default: 8080)
- `DATA_FILE_PATH`: Path to data file (default: data/tweets_injected_3.csv)

### Docker Configuration

The `docker-compose.yml` file configures:
- ElasticSearch service with health checks
- Application service with proper dependencies
- Network configuration for service communication
- Volume mounts for data access

## Data Model

### Document Structure

```json
{
  "text": "Document text content",
  "is_antisemitic": true,
  "created_at": "2020-01-01T00:00:00",
  "sentiment": "negative",
  "detected_weapons": ["gun", "knife"],
  "weapon_count": 2
}
```

### Field Descriptions

- `text`: The original text content
- `is_antisemitic`: Boolean flag for antisemitic classification
- `created_at`: Timestamp of document creation
- `sentiment`: Sentiment analysis result (positive, negative, neutral)
- `detected_weapons`: Array of detected weapon keywords
- `weapon_count`: Total number of weapons detected

## Weapon Detection

The system includes a comprehensive list of weapon keywords covering:
- Firearms (gun, rifle, pistol, etc.)
- Explosives (bomb, grenade, IED, etc.)
- Bladed weapons (knife, sword, bayonet, etc.)
- Other weapons (bat, bow, lance, etc.)

## Sentiment Analysis

Text sentiment is automatically classified using NLP techniques:
- **Positive**: Optimistic or supportive language
- **Negative**: Hostile or aggressive language
- **Neutral**: Balanced or factual language

## Error Handling

The system includes comprehensive error handling for:
- File I/O operations
- ElasticSearch connection issues
- Data processing failures
- API request validation
- Network timeouts

## Monitoring and Logging

- Application health checks
- Processing status monitoring
- Comprehensive logging throughout the pipeline
- Error tracking and reporting

## Performance Considerations

- Bulk ElasticSearch operations for efficiency
- Optimized data processing algorithms
- Memory-efficient text processing
- Scalable architecture design

## Troubleshooting

### Common Issues

1. **ElasticSearch Connection Failed**
   - Check if ElasticSearch container is running
   - Verify network configuration in docker-compose.yml
   - Check ElasticSearch logs: `docker-compose logs elasticsearch`

2. **Data Processing Errors**
   - Verify CSV file format and encoding
   - Check file permissions for data directory
   - Review application logs: `docker-compose logs malicious-text-app`

3. **API Endpoint Issues**
   - Verify service health status
   - Check port availability
   - Review API logs for specific error messages

### Useful Commands

```bash
# View all logs
docker-compose logs

# View specific service logs
docker-compose logs malicious-text-app
docker-compose logs elasticsearch

# Restart services
docker-compose restart

# Rebuild and restart
docker-compose down
docker-compose up --build -d

# Check container status
docker-compose ps

# Access ElasticSearch directly
curl http://localhost:9200/_cat/indices
```

## Development

### Local Development Setup

1. Install Python dependencies: `pip install -r requirements.txt`
2. Start ElasticSearch: `docker-compose up elasticsearch -d`
3. Run application: `python src/main.py`

### Code Structure

- **Services**: Business logic and external integrations
- **Controllers**: API endpoint handlers
- **Models**: Data structures and validation
- **Config**: Application configuration and settings

### Testing

Test the API endpoints using curl or any HTTP client:

```bash
# Test health endpoint
curl http://localhost:8080/health

# Test data processing
curl -X POST http://localhost:8080/api/documents/process

# Test analysis endpoints
curl http://localhost:8080/api/documents/antisemitic-with-weapons
curl http://localhost:8080/api/documents/multiple-weapons
```

## Deployment

### Production Considerations

- Use proper ElasticSearch security configuration
- Implement API authentication and authorization
- Configure proper logging and monitoring
- Set up backup and recovery procedures
- Use production-grade Docker images

### Scaling

The architecture supports horizontal scaling:
- Multiple application instances
- ElasticSearch cluster configuration
- Load balancing for API endpoints

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## Support

For issues and questions:
1. Check the troubleshooting section
2. Review application logs
3. Check ElasticSearch documentation
4. Create an issue in the repository

## Version History

- **v1.0.0**: Initial release with complete functionality
  - CSV data processing
  - ElasticSearch integration
  - Sentiment analysis
  - Weapon detection
  - RESTful API endpoints
  - Docker containerization
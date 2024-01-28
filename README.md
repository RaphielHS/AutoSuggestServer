# AutoSuggestServer

<!-- Python Flask based -->

## Installation
    
```bash
    pip install -r requirements.txt
```

## Usage

```bash
    python server.py
```

## API

### /suggest

#### Request

```bash
curl -X POST -H "Content-Type: application/json" -d '{"query":"hello"}' http://localhost:5000/suggest
```

#### Response

```json
    {
        "suggestions": [
            "hello",
            "hello world",
            "hello world 2",
            "hello world 3",
            "hello world 4",
            "hello world 5",
            "hello world 6",
            "hello world 7",
            "hello world 8",
            "hello world 9"
        ]
    }
```

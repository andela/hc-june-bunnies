check = {
    "properties": {
        "name": {"type": "string"},
        "tags": {"type": "string"},
        "critical": {"type": "boolean"},
        "department": {"type": "string", "maximum": 30},
        "timeout": {"type": "number", "minimum": 60, "maximum": 15552000},
        "grace": {"type": "number", "minimum": 60, "maximum": 15552000},
        "channels": {"type": "string"}
    }
}

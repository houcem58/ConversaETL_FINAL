from typing import Dict, List, Any
from dataclasses import dataclass, field
from enum import Enum

class SourceType(str, Enum):
    CSV = 'csv'
    JSON = 'json'
    SQL = 'sql'

class TargetType(str, Enum):
    POSTGRESQL = 'postgresql'
    SQLITE = 'sqlite'
    MYSQL = 'mysql'

@dataclass
class DataSource:
    type: SourceType
    location: str
    schema: Dict[str, str] = field(default_factory=dict)
    
    def __post_init__(self):
        if isinstance(self.type, str):
            self.type = SourceType(self.type.lower())

@dataclass
class DataTarget:
    type: TargetType
    connection_string: str
    table: str
    
    def __post_init__(self):
        if isinstance(self.type, str):
            self.type = TargetType(self.type.lower())

@dataclass
class PipelineSpecification:
    name: str
    source: DataSource
    target: DataTarget
    transformations: List[str] = field(default_factory=list)
    requirements: List[str] = field(default_factory=list)

@dataclass
class PipelineResult:
    generated_code: str
    validation_score: float
    optimization_score: float
    performance_metrics: Dict[str, Any] = field(default_factory=dict)
    retrieved_examples: List[Dict[str, Any]] = field(default_factory=list)
    
    def save_code(self, filepath: str):
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(self.generated_code)
        print(f' Saved: {filepath}')

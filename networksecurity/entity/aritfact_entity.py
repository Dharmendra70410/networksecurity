from dataclasses import dataclass #it help me to make varible without object

@dataclass
class DataIngestionArtifact:
    trained_file_path:str
    test_file_path:str
    

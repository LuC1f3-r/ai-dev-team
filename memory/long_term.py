import json
from typing import Dict, List, Any, Optional
from pathlib import Path
from datetime import datetime
import chromadb
from chromadb.config import Settings as ChromaSettings

class LongTermMemory:
    def __init__(self, persist_path: str = "./data/chroma_db"):
        self.persist_path = Path(persist_path)
        self.persist_path.mkdir(parents=True, exist_ok=True)

        self.client = chromadb.PersistentClient(
            path=str(self.persist_path),
            settings=ChromaSettings(anonymized_telemetry=False)
        )

        self.collection = self.client.get_or_create_collection(
            name="dev_team_memory",
            metadata={"description": "AI Dev Team long-term memory store"}
        )

        self.mind_maps: Dict[str, Dict[str, Any]] = {}
        self.projects: Dict[str, Dict[str, Any]] = {}

    def add_project(self, project_name: str, data: Dict[str, Any]):
        project_data = {
            "name": project_name,
            "created_at": datetime.now().isoformat(),
            "data": data,
            "mind_map": self.create_project_mind_map(project_name, data)
        }
        self.projects[project_name] = project_data
        self.mind_maps[project_name] = project_data["mind_map"]

        self.collection.add(
            documents=[json.dumps(project_data)],
            ids=[f"project_{project_name}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"],
            metadatas=[{"project": project_name, "type": "project"}]
        )

    def add_learning(self, project_name: str, learning: str, category: str = "general"):
        self.collection.add(
            documents=[learning],
            ids=[f"learning_{project_name}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"],
            metadatas=[{"project": project_name, "category": category, "type": "learning"}]
        )

    def search(self, query: str, project: Optional[str] = None, n_results: int = 5) -> List[Dict]:
        where_filter = {"project": project} if project else None

        results = self.collection.query(
            query_texts=[query],
            n_results=n_results,
            where=where_filter
        )

        return [
            {"document": doc, "metadata": meta}
            for doc, meta in zip(results["documents"], results["metadatas"])
        ]

    def create_project_mind_map(self, project_name: str, data: Dict[str, Any]) -> Dict[str, Any]:
        return {
            "project": project_name,
            "created_at": datetime.now().isoformat(),
            "nodes": [
                {"id": "root", "label": project_name, "type": "project"},
                {"id": "features", "label": "Core Features", "type": "category", "children": data.get("features", [])},
                {"id": "tech_stack", "label": "Tech Stack", "type": "category", "children": data.get("tech_stack", [])},
                {"id": "patterns", "label": "Code Patterns", "type": "category", "children": data.get("patterns", [])},
                {"id": "decisions", "label": "Architecture Decisions", "type": "category", "children": data.get("decisions", [])},
            ],
            "links": [
                {"source": "root", "target": "features"},
                {"source": "root", "target": "tech_stack"},
                {"source": "root", "target": "patterns"},
                {"source": "root", "target": "decisions"},
            ]
        }

    def get_mind_map(self, project_name: str) -> Optional[Dict[str, Any]]:
        return self.mind_maps.get(project_name)

    def export_mind_map(self, project_name: str, output_path: Optional[Path] = None) -> Dict[str, Any]:
        mind_map = self.get_mind_map(project_name)
        if mind_map and output_path:
            output_path.write_text(json.dumps(mind_map, indent=2))
        return mind_map or {}

    def get_all_projects(self) -> List[str]:
        return list(self.projects.keys())

    def clear_project(self, project_name: str):
        if project_name in self.projects:
            del self.projects[project_name]
        if project_name in self.mind_maps:
            del self.mind_maps[project_name]

        try:
            self.client.delete_collection(name="dev_team_memory")
            self.collection = self.client.get_or_create_collection(name="dev_team_memory")
        except Exception:
            pass

    def to_json(self) -> str:
        return json.dumps({
            "projects": self.projects,
            "mind_maps": self.mind_maps
        }, indent=2, default=str)
from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List

from jinja2 import Environment, FileSystemLoader, select_autoescape

BASE_DIR = Path(__file__).resolve().parent
SCHEMA_DIR = BASE_DIR / "schemas"
TEMPLATE_DIR = BASE_DIR / "templates"


env = Environment(
    loader=FileSystemLoader(str(TEMPLATE_DIR)),
    autoescape=select_autoescape(enabled_extensions=("html", "xml"), default_for_string=False),
)


class RealtorDocumentAgent:
    """A simple question-driven agent that gathers inputs and renders realtor documents."""

    def __init__(self, doc_types: List[str]) -> None:
        self.doc_types = doc_types
        self.schemas = self._load_schemas(doc_types)
        self.field_order = self._build_field_order(self.schemas)

    def _load_schemas(self, doc_types: List[str]) -> Dict[str, Dict[str, Any]]:
        schemas: Dict[str, Dict[str, Any]] = {}
        for doc_type in doc_types:
            schema_file = SCHEMA_DIR / f"{doc_type}.json"
            if not schema_file.exists():
                raise ValueError(f"Unsupported document type: {doc_type}")
            schemas[doc_type] = json.loads(schema_file.read_text())
        return schemas

    @staticmethod
    def _build_field_order(schemas: Dict[str, Dict[str, Any]]) -> List[str]:
        all_fields: List[str] = []
        for schema in schemas.values():
            for field in schema["fields"]:
                if field["name"] not in all_fields:
                    all_fields.append(field["name"])
        return all_fields

    def get_missing_fields(self, collected_data: Dict[str, Any]) -> List[str]:
        return [field for field in self.field_order if field not in collected_data or not collected_data[field]]

    def next_question(self, collected_data: Dict[str, Any]) -> str | None:
        missing = self.get_missing_fields(collected_data)
        if not missing:
            return None

        target_field = missing[0]
        return self._field_prompt(target_field)

    def _field_prompt(self, field_name: str) -> str:
        for schema in self.schemas.values():
            for field in schema["fields"]:
                if field["name"] == field_name:
                    example = field.get("example")
                    prompt = field["prompt"]
                    if example:
                        return f"{prompt} (example: {example})"
                    return prompt
        return f"Please provide: {field_name}"

    def parse_answer(self, question: str, answer: str, collected_data: Dict[str, Any]) -> Dict[str, Any]:
        missing = self.get_missing_fields(collected_data)
        if not missing:
            return collected_data

        target_field = missing[0]
        collected_data[target_field] = answer.strip()
        return collected_data

    def generate_documents(self, collected_data: Dict[str, Any]) -> Dict[str, str]:
        documents: Dict[str, str] = {}
        for doc_type in self.doc_types:
            template = env.get_template(f"{doc_type}.j2")
            documents[doc_type] = template.render(**collected_data)
        return documents


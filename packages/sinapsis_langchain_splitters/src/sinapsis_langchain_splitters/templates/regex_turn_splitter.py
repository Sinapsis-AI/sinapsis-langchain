# -*- coding: utf-8 -*-
import re
from typing import List
from langchain_core.documents.base import Document
from sinapsis_core.data_containers.data_packet import DataContainer, TextPacket

from sinapsis_core.template_base.template import Template

from sinapsis_core.template_base.base_models import TemplateAttributes, TemplateAttributeType


class RegexTurnSplitterAttributes(TemplateAttributes):
    pattern_1: list[str] | None = None
    remove_pattern: bool = True
    pattern_2: str | None = None
    generic_key: str | None = None
    return_as_text_packets: bool = True


class RegexTurnSplitter(Template):
    """
    Split text into chunks based on a regex that defines record boundaries.
    Each regex match start becomes a new chunk (no merging, no packing).
    """

    AttributesBaseModel = RegexTurnSplitterAttributes

    def __init__(self, attributes: TemplateAttributeType)->None:
        super().__init__(attributes)
        newline = r"(?:\r?\n|\\n)"
        if self.attributes.pattern_1 and self.attributes.pattern_2:
            first_pattern = "|".join(re.escape(s) for s in self.attributes.pattern_1)
            self.prefix = re.compile(rf"^(?:{first_pattern}):\s*")

            full_pattern = rf"(?=(?:^|{newline}){self.attributes.pattern_2}(?:\+)?(?:{first_pattern}))"
        elif self.attributes.pattern_2:
            full_pattern = rf"(?=(?:^|{newline}){self.attributes.pattern_2}[^\r\n]+)"
        elif self.attributes.pattern_1:

            first_pattern = "|".join(re.escape(s) for s in self.attributes.pattern_1)
            self.prefix = re.compile(rf"^(?:{first_pattern}):\s*") if self.attributes.remove_pattern else None
            full_pattern = rf"(?=(?:^|{newline})(?:{first_pattern}):)"
        else:
            full_pattern = rf"(?=(?:^|{newline})"

        self.pattern = re.compile(full_pattern, re.MULTILINE)

    def split_text(self, text: str) -> List[str]:
        parts = self.pattern.split(text)

        chunks = []
        for p in parts:
            p = p.strip()

            if p:
                p = self.prefix.sub("", p) if self.prefix else p
                chunks.append(p)
        return chunks

    def split_documents(self, documents: List[Document]) -> List[Document]:

        out = [
            {"content": chunk, "source": doc.metadata.get("source")}
            for doc in documents
            for chunk in self.split_text(doc.page_content)
        ]
        # for doc in documents:
        #     for chunk in self.split_text(doc.page_content):
        #         out.append({"content":chunk, "source":doc.metadata})
        return out

    def execute(self, container: DataContainer) -> DataContainer:
        if self.attributes.generic_key:
            documents = self._get_generic_data(container)
            chunks = self.split_documents(documents)

        else:
            chunks = []
            for text in container.texts:
                parts = self.split_text(text.content)
                chunks.extend(parts)

        if self.attributes.return_as_text_packets:
            new_packets = [TextPacket(content=c.get('content'),source=c.get("source")) for c in chunks]
            container.texts.extend(new_packets)
        else:
            self._set_generic_data(container, chunks)
        print ('FINAL CONTAINER', container)
        return container
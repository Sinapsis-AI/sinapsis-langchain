# -*- coding: utf-8 -*-
import re
from langchain_core.documents.base import Document

from sinapsis_core.data_containers.data_packet import DataContainer, TextPacket
from sinapsis_core.template_base.template import Template
from sinapsis_core.template_base.base_models import TemplateAttributes, TemplateAttributeType


class SpeakerAggregatorAttributes(TemplateAttributes):
    pattern_1: list[str] | None = None  # speakers
    generic_key: str | None = None
    return_as_text_packets: bool = True


class PatternAggregatorSplitter(Template):
    """
    Aggregate all utterances per speaker into a single text chunk.
    Example:
        Speaker 1: Hello
        Speaker 0: Hi
        Speaker 1: How are you

    →
        Speaker 1 → "Hello How are you"
        Speaker 0 → "Hi"
    """

    AttributesBaseModel = SpeakerAggregatorAttributes

    def __init__(self, attributes: TemplateAttributeType):
        super().__init__(attributes)

        if not self.attributes.pattern_1:
            raise ValueError("pattern_1 (speaker list) is required")

        speakers = "|".join(map(re.escape, self.attributes.pattern_1))

        # match: Speaker X: <text until next speaker>
        self.pattern = re.compile(
            rf"(?:^|\r?\n)({speakers}):\s*(.*?)(?=(?:\r?\n(?:{speakers}):)|\Z)",
            re.DOTALL,
        )

    # ---------- core aggregation ----------
    def aggregate_text(self, text: str) -> dict[str, str]:
        pattern_map: dict[str, list[str]] = {}

        for pattern, content in self.pattern.findall(text):
            pattern_map.setdefault(pattern, []).append(content.strip())

        return {sp: " ".join(parts) for sp, parts in pattern_map.items()}

    # ---------- document mode ----------
    def aggregate_documents(self, documents: list[Document]) -> list[dict]:
        out = []

        for doc in documents:
            aggregated = self.aggregate_text(doc.page_content)

            for speaker, content in aggregated.items():
                out.append(
                    {
                        "content": content,
                        "source": doc.metadata.get("source"),
                        "speaker": speaker,
                    }
                )

        return out

    # ---------- template execute ----------
    def execute(self, container: DataContainer) -> DataContainer:
        if self.attributes.generic_key:
            documents = self._get_generic_data(container)
            chunks = self.aggregate_documents(documents)

        else:
            chunks = []
            for text in container.texts:
                aggregated = self.aggregate_text(text.content)
                for speaker, content in aggregated.items():
                    chunks.append(
                        {"content": content, "source": speaker}
                    )

        if self.attributes.return_as_text_packets:
            new_packets = [
                TextPacket(
                    content=c["content"],
                    source=c.get("source"),
                    #annotations={"speaker": c.get("speaker")},
                )
                for c in chunks
            ]
            container.texts.extend(new_packets)

        else:
            self._set_generic_data(container, chunks)

        return container
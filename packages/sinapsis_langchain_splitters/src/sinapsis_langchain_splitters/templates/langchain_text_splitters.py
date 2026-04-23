# -*- coding: utf-8 -*-
from typing import Any

import langchain_text_splitters
from langchain_core.documents.base import Document
from sinapsis_core.data_containers.data_packet import DataContainer, TextPacket
from sinapsis_core.template_base.base_models import OutputTypes, TemplateAttributes, UIPropertiesMetadata
from sinapsis_core.template_base.dynamic_template import (
    BaseDynamicWrapperTemplate,
    WrapperEntryConfig,
)
from sinapsis_core.template_base.dynamic_template_factory import make_dynamic_template
from sinapsis_core.utils.env_var_keys import SINAPSIS_BUILD_DOCS

from sinapsis_langchain_splitters.helpers.tags import Tags

SOURCE: str = "source"
CONTENT: str = "content"

EXCLUDED_MODULES = [
    "Language",
    "Tokenizer",
    "ElementType",
    "LineType",
    "TextSplitter",
    "HeaderType",
    "RecursiveJsonSplitter",
    "split_text_on_tokens",
]


class LangChainTextSplitterBase(BaseDynamicWrapperTemplate):
    """
    Dynamic templates for LangChain library to split texts using different classes from
    the text_splitter list
    The template takes a Document from the generic_data field of DataContainers or the text
    in a TextPacket, and process the chunks, creating dictionaries with source and context keys

    Usage example

    agent:
      name: my_test_agent
    templates:
    - template_name: InputTemplate
      class_name: InputTemplate
      attributes: {}
    - template_name: RecursiveCharacterTextSplitterWrapper
      class_name: RecursiveCharacterTextSplitterWrapper
      template_input: InputTemplate
      attributes:
        add_document_as_text_packet: false
        generic_key: null
        recursivecharactertextsplitter_init:
          separators: null
          keep_separator: true
          is_separator_regex: false


    """

    WrapperEntry = WrapperEntryConfig(wrapped_object=langchain_text_splitters, exclude_module_atts=EXCLUDED_MODULES)
    UIProperties = UIPropertiesMetadata(
        category="LangChain",
        output_type=OutputTypes.TEXT,
        tags=[
            Tags.DOCUMENTS,
            Tags.DYNAMIC,
            Tags.FILES,
            Tags.LANGCHAIN,
            Tags.SPLITTERS,
            Tags.TEXT,
        ],
    )

    class AttributesBaseModel(TemplateAttributes):
        """
        add_document_as_text_packet(bool): Whether to add the document as a TextPacket or not.
        generic_key : str | list[str] | None: Optional generic key to retrieve the data from
        """

        add_document_as_text_packet: bool = False
        generic_key: str | list[str] | None = None

    attributes: AttributesBaseModel
    wrapped_callable: Any

    def split_document(
        self, text_to_split: Document | list[Document] | TextPacket, chunks: list[dict] | None = None
    ) -> list:
        """For the document entry split the text with the langchain text_splitter
        Args:
                text_to_split (Document | list[Document] | TextPacket): The text to split. Can be of type
                        Langchain Document, a list of Langchain Documents or a TextPacket
                chunks (list | None): The incoming list of chunks if any.
        Returns:
                list : list of processed chunks
        """

        if not chunks:
            chunks = []
        if isinstance(text_to_split, Document):
            split_chunks = self.wrapped_callable.split_text(text_to_split.page_content)

            new_chunks = [
                {SOURCE: text_to_split.metadata[SOURCE], CONTENT: split_chunk} for split_chunk in split_chunks
            ]
            chunks.extend(new_chunks)

        elif isinstance(text_to_split, list):
            for text in text_to_split:
                if isinstance(text, Document):
                    split_parts = self.wrapped_callable.split_text(text.page_content)
                    new_chunks = [{SOURCE: text.metadata[SOURCE], CONTENT: part} for part in split_parts]
                    chunks.extend(new_chunks)
                elif isinstance(text, str):
                    split_parts = self.wrapped_callable.split_text(text)
                    new_chunks = [{CONTENT: part} for part in split_parts]
                    chunks.extend(new_chunks)

        elif isinstance(text_to_split, TextPacket):
            split_chunks = self.wrapped_callable.split_text(text_to_split.content)
            new_chunks = [{SOURCE: text_to_split.source, CONTENT: split_chunk} for split_chunk in split_chunks]
            chunks.extend(new_chunks)
        else:
            unsup_type = type(text_to_split)
            log_msg = f"Unsupported text_to_split type: {unsup_type}. Expected: Document, list[Document], TextPacket."
            self.logger.warning(log_msg)

        return chunks

    def execute(self, container: DataContainer) -> DataContainer:
        """Execute method of the template. It extracts the generic_data field of the container and
        uses a TextSplitter from Langchain to split the text into chunks, to later be stored in the
        container"""
        chunks: list[dict] = []
        if self.attributes.generic_key is not None:
            document = self._get_generic_data(container)
            chunks = self.split_document(document, chunks)  #  ty: ignore[invalid-argument-type]
        else:
            for text_packet in container.texts:
                chunks.extend(self.split_document(text_packet, chunks))

        if not chunks:
            log_msg = (
                "No chunks were created from the input text. Please check the input and the splitter configuration."
            )
            self.logger.warning(log_msg)
            return container

        if self.attributes.add_document_as_text_packet:
            text_packets = [TextPacket(content=chunk.get(CONTENT), source=chunk.get(SOURCE)) for chunk in chunks]
            container.texts = text_packets
        else:
            self._set_generic_data(container, chunks)
        return container


def __getattr__(name: str) -> type[BaseDynamicWrapperTemplate]:
    """Only create a template if it's imported, this avoids creating all the base models for all templates
    and potential import errors due to not available packages.
    """

    if name in LangChainTextSplitterBase.WrapperEntry.module_att_names:
        return make_dynamic_template(name, LangChainTextSplitterBase)

    raise AttributeError(f"template `{name}` not found in {__name__}")


__all__ = LangChainTextSplitterBase.WrapperEntry.module_att_names


if SINAPSIS_BUILD_DOCS:
    dynamic_templates = [__getattr__(template_name) for template_name in __all__]
    for template in dynamic_templates:
        globals()[template.__name__] = template
        del template

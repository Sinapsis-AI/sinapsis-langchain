# -*- coding: utf-8 -*-
from typing import cast

from langchain_community.document_loaders.blob_loaders import Blob
from langchain_core.documents.base import Document
from sinapsis_core.data_containers.data_packet import DataContainer, TextPacket
from sinapsis_core.template_base import (
    Template,
)
from sinapsis_core.template_base.base_models import (
    OutputTypes,
    UIPropertiesMetadata,
)

from sinapsis_langchain_readers.helpers.tags import Tags


class BaseStaticLoader(Template):
    """Base class for Loaders that can't be constructed dynamically"""

    UIProperties = UIPropertiesMetadata(
        category="LangChain",
        output_type=OutputTypes.TEXT,
        tags=[
            Tags.DOCUMENTS,
            Tags.DOCUMENT_LOADING,
            Tags.DYNAMIC,
            Tags.FILES,
            Tags.LANGCHAIN,
            Tags.LOADERS,
            Tags.READERS,
        ],
    )

    @staticmethod
    def append_documents_as_text_packet(container: DataContainer, documents: list[Document | Blob]) -> None:
        """Method to append each string of the Document or list[Documents] to a new TextPacket
        Args:
            container (DataContainer) : Container to store the TextPackets
            documents (list[Document]) : list of documents to split and append to TextPacket
        """
        for document in documents:
            document = cast(Document, document)
            text_packet = TextPacket(content=document.page_content)
            container.texts.append(text_packet)

    def execute(self, container: DataContainer) -> DataContainer:
        documents = self.loader.load()
        if documents:
            if self.attributes.add_document_as_text_packet:
                self.append_documents_as_text_packet(container, documents)
            else:
                self._set_generic_data(container, documents)
        return container

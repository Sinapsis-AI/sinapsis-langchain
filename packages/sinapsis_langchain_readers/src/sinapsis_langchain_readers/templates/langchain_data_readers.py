# -*- coding: utf-8 -*-

from typing import cast

from langchain_community import document_loaders
from langchain_community.document_loaders.base import BaseLoader as LangChainBaseLoader
from langchain_community.document_loaders.blob_loaders import Blob
from langchain_community.document_loaders.blob_loaders import (
    BlobLoader as LangChainBlobLoader,  # avoid name collision
)
from langchain_core.documents.base import Document
from sinapsis_core.data_containers.data_packet import DataContainer, TextPacket
from sinapsis_core.template_base import Template
from sinapsis_core.template_base.base_models import OutputTypes, TemplateAttributes, UIPropertiesMetadata
from sinapsis_core.template_base.dynamic_template import (
    BaseDynamicWrapperTemplate,
    WrapperEntryConfig,
)
from sinapsis_core.template_base.dynamic_template_factory import make_dynamic_template
from sinapsis_core.template_base.multi_execute_template import (
    execute_template_n_times_wrapper,
)
from sinapsis_core.utils.env_var_keys import SINAPSIS_BUILD_DOCS

# base classes or loaders that require non built in object instance
EXCLUDED_LOADER_MODULE_OBJECTS = [
    "Blob",
    "BlobLoader",
    "OracleTextSplitter",
    "OracleDocLoader",
    "TrelloLoaderExecute",
    "TwitterTweetLoader",
    "TrelloLoader",
    "GoogleApiYoutubeLoader",
    "GoogleApiClient",
    "DiscordChatLoader",
    "AssemblyAIAudioTranscriptLoader",
    "ArcGISLoader",
]


class LangChainDataReaderBase(BaseDynamicWrapperTemplate):
    """
    Dynamic Template to load documents from Langchain document_loaders module
    The template loads the document either as a Document object in the generic_data field
    of DataContainer of each string as a TextPacket if add_document_as_text_packet is set as True

    Usage example:

    agent:
      name: my_test_agent
    templates:
    - template_name: InputTemplate
      class_name: InputTemplate
      attributes: {}
    - template_name: WikipediaLoaderWrapper
      class_name: WikipediaLoaderWrapper    ## note that because it is a dynamic template,
      template_input: InputTemplate         ##  the class name depends on the actual class that is used.
      attributes:
        add_document_as_text_packet: false
        wikipedialoader_init:
            query: the query for wikipedia
            lang: en
            load_max_docs: 5000
            load_all_available_meta: False
            doc_content_chars_max: 4000

    """

    WrapperEntry = WrapperEntryConfig(
        wrapped_object=document_loaders, exclude_module_atts=EXCLUDED_LOADER_MODULE_OBJECTS
    )
    UIProperties = UIPropertiesMetadata(category="LangChain", output_type=OutputTypes.TEXT)

    class AttributesBaseModel(TemplateAttributes):
        """
        add_document_as_text_packet(bool): Whether to add document as text packet or not.
        """

        add_document_as_text_packet: bool = False

    @staticmethod
    def append_documents_as_text_packet(container: DataContainer, documents: list[Document | Blob]) -> None:
        """Method to append each string of the Document or list[Documents] to a new TextPacket
        Args:
            container (DataContainer) : Container to store the TextPackets
            documents (list[Document]) : list of documents to split and append to TextPacket
        """
        for document in documents:
            if document.metadata:
                text_packet = TextPacket(
                    content=document.metadata["summary"],
                    source=document.metadata["title"],
                )
            else:
                document = cast(Document, document)
                text_packet = TextPacket(content=document.page_content)
            container.texts.append(text_packet)

    def execute(self, container: DataContainer) -> DataContainer:
        documents: list[Document | Blob] = []
        if isinstance(self.wrapped_callable, LangChainBlobLoader):
            documents = list(self.wrapped_callable.yield_blobs())
        elif isinstance(self.wrapped_callable, LangChainBaseLoader):
            documents = self.wrapped_callable.load()
        else:
            self.logger.warning("Unsupported wrapped_callable type for langchain data loader.")

        if documents:
            if self.attributes.add_document_as_text_packet:
                self.append_documents_as_text_packet(container, documents)
            else:
                self._set_generic_data(container, documents)
        return container


@execute_template_n_times_wrapper
class ExecuteNTimesLangchainDataReaders(LangChainDataReaderBase):
    WrapperEntry = WrapperEntryConfig(
        wrapped_object=document_loaders,
        exclude_module_atts=EXCLUDED_LOADER_MODULE_OBJECTS,
        template_name_suffix="ExecuteNTimes",
    )


def __getattr__(name: str) -> Template:
    """
    Only create a template if it's imported, this avoids creating all the base models for all templates
    and potential import errors due to not available packages.
    """
    if name in LangChainDataReaderBase.WrapperEntry.module_att_names:
        return make_dynamic_template(name, LangChainDataReaderBase)
    if name in ExecuteNTimesLangchainDataReaders.WrapperEntry.module_att_names:
        return make_dynamic_template(name, ExecuteNTimesLangchainDataReaders)
    raise AttributeError(f"template `{name}` not found in {__name__}")


__all__ = (
    LangChainDataReaderBase.WrapperEntry.module_att_names
    + ExecuteNTimesLangchainDataReaders.WrapperEntry.module_att_names
)


if SINAPSIS_BUILD_DOCS:
    dynamic_templates = [__getattr__(template_name) for template_name in __all__]
    for template in dynamic_templates:
        globals()[template.__name__] = template
        del template

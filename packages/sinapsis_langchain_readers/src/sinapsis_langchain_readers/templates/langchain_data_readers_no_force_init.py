# -*- coding: utf-8 -*-

from sinapsis_core.template_base import Template
from sinapsis_core.template_base.dynamic_template import (
    WrapperEntryConfig,
)
from sinapsis_core.template_base.dynamic_template_factory import make_dynamic_template
from sinapsis_core.template_base.multi_execute_template import (
    execute_template_n_times_wrapper,
)
from sinapsis_core.utils.env_var_keys import SINAPSIS_BUILD_DOCS

from sinapsis_langchain_readers.helpers import include_modules_no_force_init
from sinapsis_langchain_readers.templates.langchain_data_readers import (
    LangChainDataReaderBase,
)


class LangChainDataReaderNoForceInit(LangChainDataReaderBase):
    """
    Dynamic Template to load documents from Langchain document_loaders module without forced initialization.
    This variant does not force initialization as a method.

    Usage examples:

    agent:
      name: my_test_agent
    templates:
    - template_name: InputTemplate
      class_name: InputTemplate
      attributes: {}
    - template_name: DocugamiLoaderWrapper
      class_name: DocugamiLoaderWrapper
      template_input: InputTemplate
      attributes:
        add_document_as_text_packet: false
        docugamiloader_init:
          api: https://api.docugami.com/v1preview1
          access_token: null
          max_text_length: 4096
          min_text_length: 32
          max_metadata_length: 512
          include_xml_tags: false
          parent_hierarchy_levels: 0
          parent_id_key: doc_id
          sub_chunk_tables: false
          whitespace_normalize_text: true
          docset_id: null
          document_ids: null
          file_paths: null
          include_project_metadata_in_doc_metadata: true
    """

    WrapperEntry = WrapperEntryConfig(
        wrapped_object=include_modules_no_force_init,
        force_init_as_method=False,
    )


@execute_template_n_times_wrapper
class ExecuteNTimesLangchainDataReadersNoForceInit(LangChainDataReaderBase):
    WrapperEntry = WrapperEntryConfig(
        wrapped_object=include_modules_no_force_init,
        template_name_suffix="ExecuteNTimes",
        force_init_as_method=False,
    )


def __getattr__(name: str) -> Template:
    """
    Only create a template if it's imported, this avoids creating all the base models for all templates
    and potential import errors due to not available packages.
    """
    if name in LangChainDataReaderNoForceInit.WrapperEntry.module_att_names:
        return make_dynamic_template(name, LangChainDataReaderNoForceInit)
    if name in ExecuteNTimesLangchainDataReadersNoForceInit.WrapperEntry.module_att_names:
        return make_dynamic_template(name, ExecuteNTimesLangchainDataReadersNoForceInit)
    raise AttributeError(f"template `{name}` not found in {__name__}")


__all__ = (
    LangChainDataReaderNoForceInit.WrapperEntry.module_att_names
    + ExecuteNTimesLangchainDataReadersNoForceInit.WrapperEntry.module_att_names
)

if SINAPSIS_BUILD_DOCS:
    dynamic_templates = [__getattr__(template_name) for template_name in __all__]
    for template in dynamic_templates:
        globals()[template.__name__] = template
        del template

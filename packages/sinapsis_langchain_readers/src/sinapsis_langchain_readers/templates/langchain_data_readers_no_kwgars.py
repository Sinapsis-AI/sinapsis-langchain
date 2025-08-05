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

from sinapsis_langchain_readers.helpers import include_modules_no_kwargs
from sinapsis_langchain_readers.templates.langchain_data_readers import LangChainDataReaderBase


class LangChainDataReaderNoKwargs(LangChainDataReaderBase):
    """
    Dynamic Template to load documents from Langchain document_loaders module without kwargs support.
    This variant excludes 'kwargs' and 'unstructured_kwargs' method attributes.
    Usage examples:

    agent:
      name: my_test_agent
    templates:
    - template_name: InputTemplate
      class_name: InputTemplate
      attributes: {}
    - template_name: AZLyricsLoaderWrapper
      class_name: AZLyricsLoaderWrapper
      template_input: InputTemplate
      attributes:
        add_document_as_text_packet: false
        azlyricsloader_init:
          web_path: 'https://www.azlyrics.com/lyrics/artist/song.html'
          header_template: null
          verify_ssl: true
          proxies: null
          continue_on_failure: false
          autoset_encoding: true
          encoding: null
          web_paths: []
          requests_per_second: 2
          default_parser: html.parser
          requests_kwargs: null
          raise_for_status: false
          bs_get_text_kwargs: null
          bs_kwargs: null
          session: null
          show_progress: true
          trust_env: false
    """

    WrapperEntry = WrapperEntryConfig(
        wrapped_object=include_modules_no_kwargs,
        exclude_method_attributes=["kwargs", "unstructured_kwargs"],
    )


@execute_template_n_times_wrapper
class ExecuteNTimesLangchainDataReadersNoKwargs(LangChainDataReaderBase):
    WrapperEntry = WrapperEntryConfig(
        wrapped_object=include_modules_no_kwargs,
        template_name_suffix="ExecuteNTimes",
        exclude_method_attributes=["kwargs", "unstructured_kwargs"],
    )


def __getattr__(name: str) -> Template:
    """
    Only create a template if it's imported, this avoids creating all the base models for all templates
    and potential import errors due to not available packages.
    """
    if name in LangChainDataReaderNoKwargs.WrapperEntry.module_att_names:
        return make_dynamic_template(name, LangChainDataReaderNoKwargs)
    if name in ExecuteNTimesLangchainDataReadersNoKwargs.WrapperEntry.module_att_names:
        return make_dynamic_template(name, ExecuteNTimesLangchainDataReadersNoKwargs)
    raise AttributeError(f"template `{name}` not found in {__name__}")


__all__ = (
    LangChainDataReaderNoKwargs.WrapperEntry.module_att_names
    + ExecuteNTimesLangchainDataReadersNoKwargs.WrapperEntry.module_att_names
)

if SINAPSIS_BUILD_DOCS:
    dynamic_templates = [__getattr__(template_name) for template_name in __all__]
    for template in dynamic_templates:
        globals()[template.__name__] = template
        del template

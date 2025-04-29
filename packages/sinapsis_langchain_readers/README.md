<h1 align="center">
<br>
<a href="https://sinapsis.tech/">
  <img
    src="https://github.com/Sinapsis-AI/brand-resources/blob/main/sinapsis_logo/4x/logo.png?raw=true"
    alt="" width="300">
</a><br>
Sinapsis Langchain Readers
<br>
</h1>

<h4 align="center">Templates for easy integration of LangChain document loaders within Sinapsis.</h4>

<p align="center">
<a href="#installation">🐍 Installation</a> •
<a href="#features">🚀 Features</a> •
<a href="#usage">📚 Usage example</a> •
<a href="#documentation">📙 Documentation</a> •
<a href="license"> 🔍 License</a>
</p>

The `sinapsis-langchain-readers` module adds support for the LangChain library, in particular, LangChain community data loaders.

<h2 id="installation">🐍 Installation</h2>
Install using your package manager of choice. We encourage the use of <code>uv</code>

Example with <code>uv</code>:

```bash
  uv pip install sinapsis-langchain-readers --extra-index-url https://pypi.sinapsis.tech
```
 or with raw <code>pip</code>:
```bash
  pip install sinapsis-langchain-readers --extra-index-url https://pypi.sinapsis.tech
```



> [!IMPORTANT]
> The langchain readers templates may require extra dependencies. For development, we recommend installing the package with all the optional dependencies:
>
```bash
  uv pip install sinapsis-langchain-readers[all] --extra-index-url https://pypi.sinapsis.tech
```
> [!IMPORTANT]
> Some langchain templates require additional system dependencies. Please refer to the official [LangChain Document Loaders documentation](https://python.langchain.com/docs/integrations/document_loaders/) for additional requirements.
>


<h2 id="features">🚀 Features</h2>

<h3> Templates Supported</h3>

The **Sinapsis Langchain** module provides wrapper templates for **LangChain's community data loaders**, making them seamlessly usable within Sinapsis.
> [!NOTE]
> Each loader template supports one attribute:
> - **`add_document_as_text_packet`** (`bool`, default: `False`): Whether to add the loaded document as a text packet.
> Other attributes can be dynamically assigned through the class initialization dictionary (`class init attributes`).

> [!TIP]
> Use CLI command ``` sinapsis info --all-template-names``` to show a list with all the available Template names installed with Sinapsis Langchain.

> [!TIP]
> Use CLI command ```sinapsis info --example-template-config TEMPLATE_NAME``` to produce an example Agent config for the Template specified in ***TEMPLATE_NAME***.


For example, for ***WikipediaLoaderWrapper*** use ```sinapsis info --example-template-config WikipediaLoaderWrapper``` to produce the following example config:

```yaml
agent:
  name: agent to load Wikipedia documents using WikipediaLoaderWrapper template
templates:
- template_name: InputTemplate
  class_name: InputTemplate
  attributes: {}
- template_name: WikipediaLoaderWrapper
  class_name: WikipediaLoaderWrapper
  template_input: InputTemplate
  attributes:
    add_document_as_text_packet: false
    wikipedialoader_init:
        query: the query for wikipedia
        lang: en
        load_max_docs: 5000
        load_all_available_meta: False
        doc_content_chars_max: 4000,
```

A complete list of available document loader classes in LangChain can be found at:
[LangChain Community Document Loaders](https://python.langchain.com/api_reference/community/document_loaders.html#langchain-community-document-loaders)

<details>
<summary><strong><span style="font-size: 1.25em;">🚫 Excluded Loaders</span></strong></summary>

Some base classes or loaders that required additional configuration have been excluded and support for this will be included in future releases.

- **Blob**
- **BlobLoader**
- **OracleTextSplitter**
- **OracleDocLoader**
- **TrelloLoaderExecute**
- **TwitterTweetLoader**
- **TrelloLoader**
- **GoogleApiYoutubeLoader**
- **GoogleApiClient**
- **DiscordChatLoader**
- **AssemblyAIAudioTranscriptLoader**
- **ArcGISLoader**

For all other supported loaders, refer to the LangChain API reference linked above.
</details>
<h2 id="usage">📚 Usage example</h2>


The following example demonstrates how to use the **WikipediaLoaderWrapper** template for loading documents from Wikipedia within Sinapsis. Below is the full YAML configuration, followed by a breakdown of each component.
<details>
<summary><strong><span style="font-size: 1.25em;">configuration </span></strong></summary>

```yaml
agent:
  name: my_test_agent
  description: "Wikipedia loader example"

templates:

- template_name: InputTemplate
  class_name: InputTemplate
  attributes: {}

- template_name: WikipediaLoaderWrapper
  class_name: WikipediaLoaderWrapper
  template_input: InputTemplate
  attributes:
    add_document_as_text_packet: false
    wikipedialoader_init:
      query: GenAI
      lang: en
      load_max_docs: 1
      load_all_available_meta: false
      doc_content_chars_max: 4000
```
To run, simply use:

```bash
sinapsis run name_of_the_config.yml
```


</details>

<h2 id="documentation">📙 Documentation</h2>

Documentation for this and other sinapsis packages is available on the [sinapsis website](https://docs.sinapsis.tech/docs)

Tutorials for different projects within sinapsis are available at [sinapsis tutorials page](https://docs.sinapsis.tech/tutorials)

<h2 id="license">🔍 License</h2>

This project is licensed under the AGPLv3 license, which encourages open collaboration and sharing. For more details, please refer to the [LICENSE](LICENSE) file.

For commercial use, please refer to our [official Sinapsis website](https://sinapsis.tech) for information on obtaining a commercial license.




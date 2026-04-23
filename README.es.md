<h1 align="center">
<br/>
<a href="https://sinapsis.tech/">
<img alt="" src="https://github.com/Sinapsis-AI/brand-resources/blob/main/sinapsis_logo/4x/logo.png?raw=true" width="300"/>
</a>
<br/>Sinapsis Langchain
<br/>
</h1>

<h4 align="center">Plantillas para la integración perfecta de LangChain frameword.</h4>

<p align="center">
<a href="#installation">🐍 Instalación</a> •
<a href="#features">🚀 Paquetes</a> •
<a href="#usage">📚 Ejemplo de uso</a> •
<a href="#documentation">📙 Documentación</a> •
<a href="license"> 🔍 Licencia</a>
</p>

El módulo <code>sinapsis-langchain</code>  añade soporte para el marco Langchain, en particular, cargadores de datos comunitarios Langchain y separadores de texto.

Añadimos soporte para los siguientes paquetes:

*<code> sinapsis-langchain-readers</code>

*<code> sinapsis-langchain-splitters</code>

<h2 id="installation">🐍 Instalación</h2>

Instala el administrador de tu paquete de elección. Alentamos el uso de <code>uv</code>

Ejemplo con <code>uv</code>:

```bash 
  uv pip install sinapsis-langchain-readers --extra-index-url https://pypi.sinapsis.tech
```

o con solo <code>pip</code>:

```bash 
  pip install sinapsis-langchain-readers --extra-index-url https://pypi.sinapsis.tech
```

<blockquote>

[!NOTE]
Cambia el nombre del paquete en consecuencia

[!IMPORTANT]
Las plantillas de langchain pueden requerir dependencias adicionales. Para el desarrollo, recomendamos instalar el paquete con todas las dependencias opcionales:

</blockquote>

```bash 
  uv pip install sinapsis-langchain-readers[all] --extra-index-url https://pypi.sinapsis.tech
```

<blockquote>

[!IMPORTANT]
Algunas plantillas de langchain requieren dependencias adicionales del sistema. Por favor consulta al funcionario <a href="https://python.langchain.com/docs/integrations/document_loaders/">LangChain Document Documentación de carga</a> para necesidades adicionales.

[!NOTE]
Cambia el nombre del paquete en consecuencia

[!TIP]
también puede instalar el repo mono completo

</blockquote>

■

```bash 
  uv pip install sinapsis-langchain[all] --extra-index-url https://pypi.sinapsis.tech
```

<h2 id="features">🚀 Características</h2>
<h3> Plantillas soportadas</h3>

El módulo **Sinapsis Langchain** proporciona plantillas de envoltura para **Cargadores de datos comunitarios de Langchain**, haciéndolos perfectamente utilizables dentro de Sinapsis.

<blockquote>

[!NOTE]
Cada plantilla de cargador soporta un atributo:

* **<code>add_document_as_text_packet</code>**
()<code>bool</code>, por defecto: <code>False</code>): Ya sea para añadir el documento cargado como paquete de texto.
Otros atributos se pueden asignar dinámicamente a través del diccionario de inicialización de clase (<code>class init attributes</code>).

[!TIP]
Usa el comando de CLI <code>sinapsis info --all-template-names</code> para mostrar una lista con todos los nombres disponibles de Plantillas instalados con Sinapsis Langchain.

[!TIP]
Usa el comando de CLI <code>sinapsis info --example-template-config TEMPLATE_NAME</code> para producir un ejemplo de configuración de Agente para la Plantilla especificado en **<em>TEMPLATE_NAME</em>
**.

</blockquote>

Por ejemplo, **<em>WikipediaLoaderWrapper</em>**
uso <code>sinapsis info --example-template-config WikipediaLoaderWrapper</code> para producir el siguiente ejemplo de configuración:

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

Se puede encontrar una lista completa de clases de cargador de documentos disponibles en
<a href="https://python.langchain.com/api_reference/community/document_loaders.html#langchain-community-document-loaders">LangChain</a>

<details>
<summary><strong><span style="font-size: 1.25em;">Cargadores excluidos</span></strong></summary>

Se han excluido algunas clases de base o cargadores que requerían configuración adicional y se incluirá apoyo para ello en futuras versiones.

* **Blob** * **BlobLoader** * **OracleTextSplitter** * **Oracle** * **TrelloLoaderEjecutar** * **TwitterTweetLoader** * **TrelloLoader** * **GoogleApiYoutubeLoader** * **GoogleApiClient** * **DiscordChatLoader** * **AssemblyAIAudioTranscriptLoader** * **ArcGISLoader** 

Para todos los demás cargadores compatibles, consulta la referencia de la API de LangChain vinculada anteriormente.

</details>
<h2 id="usage">📚 Ejemplo de uso</h2>

El siguiente ejemplo demuestra cómo utilizar el **WikipediaLoaderWrapper** plantilla para cargar documentos de Wikipedia dentro de Sinapsis. A continuación se encuentra la configuración completa de YAML, seguida de un desglose de cada componente.
<details>
<summary><strong><span style="font-size: 1.25em;">configuración </span></strong></summary>

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

Para correr, simplemente use:

```bash 
sinapsis run name_of_the_config.yml
```
</details>

<h2 id="documentation">📙 Documentación</h2>

La documentación para este y otros paquetes de sinapsis está disponible en la <a href="https://docs.sinapsis.tech/docs">web de sinapsis</a>

Los tutoriales para diferentes proyectos dentro de sinapsis están disponibles en <a href="https://docs.sinapsis.tech/tutorials">la página de tutoriales de sinapsis</a>

<h2 id="license">🔍 Licencia</h2>

Este proyecto está licenciado bajo la licencia AGPLv3, que fomenta la colaboración abierta y el intercambio. Para más detalles, consulta el <a href="LICENSE">LICENSE</a> archivo.

Para uso comercial, consulta nuestra página <a href="https://sinapsis.tech">Sitio web de Sinapsis</a> para información sobre la obtención de una licencia comercial.


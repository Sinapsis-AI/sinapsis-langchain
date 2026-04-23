<h1 align="center"><br/><a href="https://sinapsis.tech/"><img alt="" src="https://github.com/Sinapsis-AI/brand-resources/blob/main/sinapsis_logo/4x/logo.png?raw=true" width="300"/></a><br/>Sinapsis Langchain Readers
<br/></h1>
<h4 align="center">Plantillas para una fácil integración de los cargadores de documentos LangChain dentro de Sinapsis.</h4>
<p align="center"><a href="#installation">🐍 Instalación</a> •
<a href="#features">🚀 Características</a> •
<a href="#usage">📚 Ejemplo de uso</a> •
<a href="#documentation">📙 Documentación</a> •
<a href="license"> 🔍 Licencia</a>


El  módulo <code>sinapsis-langchain-readers</code> añade soporte para la biblioteca LangChain, en particular, cargadores de datos comunitarios LangChain.

<h2 id="installation">🐍 Instalación</h2>

Instala el administrador de paquetes de tu elección. Alentamos el uso de <code>uv</code>


Ejemplo con <code>uv</code>:



```bash
  uv pip install sinapsis-langchain-readers --extra-index-url https://pypi.sinapsis.tech
```

o con solo <code>pip</code>:

```bash
  pip install sinapsis-langchain-readers --extra-index-url https://pypi.sinapsis.tech
```

<blockquote>

[!IMPORTANT]
Las plantillas de lectores de langchain pueden requerir dependencias adicionales. Para el desarrollo, recomendamos instalar el paquete con todas las dependencias opcionales:

</blockquote>

```bash
  uv pip install sinapsis-langchain-readers[all] --extra-index-url https://pypi.sinapsis.tech
```

<blockquote>

[!IMPORTANT]
Algunas plantillas de langchain requieren dependencias adicionales del sistema. Por favor consulta el sitio web oficial de  <a href="https://python.langchain.com/docs/integrations/document_loaders/">LangChain Document Documentación de carga</a> para necesidades adicionales.

</blockquote>
<h2 id="features">🚀 Características</h2><h3> Plantillas soportadas</h3>
El <strong>Sinapsis Langchain</strong> módulo proporciona plantillas de envoltura para <strong>Cargadores de datos comunitarios de LangChain</strong>, haciéndolos perfectamente utilizables dentro de Sinapsis.

<blockquote>

[!NOTE]
Cada plantilla de cargador soporta un atributo:
<ul>
<li><strong><code>add_document_as_text_packet</code></strong> ()<code>bool</code>, por defecto: <code>False</code>): Ya sea para añadir el documento cargado como paquete de texto.
Otros atributos se pueden asignar dinámicamente a través del diccionario de inicialización de clase (<code>class init attributes</code>).</li>
</ul>
[! TIP]
Usa el comando de CLI <code>sinapsis info --all-template-names</code> para mostrar una lista con todos los nombres disponibles de Plantillas instalados con Sinapsis Langchain.

[! TIP]
Usa el comando de CLI <code>sinapsis info --example-template-config TEMPLATE_NAME</code> para producir un ejemplo Agente config para la Plantilla especificado en <strong><em>TEMPLATE_NAME</em></strong>.

</blockquote>

Por ejemplo, para <strong><em>WikipediaLoaderWrapper</em></strong> usa <code>sinapsis info --example-template-config WikipediaLoaderWrapper</code> para producir el siguiente ejemplo de configuración:

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

Se puede encontrar una lista completa de clases de cargador de documentos disponibles en LangChain:
<a href="https://python.langchain.com/api_reference/community/document_loaders.html#langchain-community-document-loaders">LangChain Comunidad Cargadores de documentos</a>


<details><summary><strong><span style="font-size: 1.25em;">Cargadores excluidos</span></strong></summary>
</details>


Se han excluido algunas clases de base o cargadores que requerían configuración adicional y se incluirá apoyo para ello en futuras versiones.
<ul>
<li><strong>Blob</strong></li>

<li><strong>BlobLoader</strong></li>

<li><strong>OracleTextSplitter</strong></li>

<li><strong>Oracle</strong></li>

<li><strong>TrelloLoaderEjecutar</strong></li>

<li><strong>TwitterTweetLoader</strong></li>

<li><strong>TrelloLoader</strong></li>

<li><strong>GoogleApiYoutubeLoader</strong></li>

<li><strong>GoogleApiClient</strong></li>

<li><strong>DiscordChatLoader</strong></li>

<li><strong>AssemblyAIAudioTranscriptLoader</strong></li>

<li><strong>ArcGISLoader</strong></li>
</ul>
Para todos los demás cargadores compatibles, consulta la referencia de la API de LangChain vinculada anteriormente.

<h2 id="usage">📚 Ejemplo de uso</h2>
El siguiente ejemplo demuestra cómo utilizar el <strong>WikipediaLoaderWrapper</strong> plantilla para cargar documentos de Wikipedia dentro de Sinapsis. A continuación se encuentra la configuración completa de YAML, seguida de un desglose de cada componente.

<details><summary><strong><span style="font-size: 1.25em;">configuración </span></strong></summary>
</details>


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

Para correr, simplemente usa:

```bash
sinapsis run name_of_the_config.yml
```


<h2 id="documentation">📙 Documentación</h2>
La documentación para este y otros paquetes de sinapsis está disponible en <a href="https://docs.sinapsis.tech/docs">web de sinapsis</a>

Los tutoriales para diferentes proyectos dentro de sinapsis están disponibles en <a href="https://docs.sinapsis.tech/tutorials">sinapsis tutoriales página</a>
<h2 id="license">🔍 Licencia</h2>
Este proyecto está licenciado bajo la licencia AGPLv3, que fomenta la colaboración abierta y el intercambio. Para más detalles, consulta el archivo <a href="LICENSE">LICENSE</a>.

Para uso comercial, consulta el  <a href="https://sinapsis.tech"> sitio web oficial de Sinapsis</a> para información sobre la obtención de una licencia comercial.


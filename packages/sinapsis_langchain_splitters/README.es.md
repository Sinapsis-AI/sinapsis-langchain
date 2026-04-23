<h1 align="center"><br/><a href="https://sinapsis.tech/"><img alt="" src="https://github.com/Sinapsis-AI/brand-resources/blob/main/sinapsis_logo/4x/logo.png?raw=true" width="300"/></a><br/>Divisores de Langchain Sinapsis
<br/></h1>
<h4 align="center">Plantillas para una fácil integración de separadores de texto LangChain con Sinapsis.</h4>
<p align="center"><a href="#installation">🐍 Instalación</a> •
<a href="#features">🚀 Características</a> •
<a href="#usage">📚 Ejemplo de uso</a> •
<a href="#documentation">📙 Documentación</a> •
<a href="license"> 🔍 Licencia</a>


El  módulo <code>sinapsis-langchain-splitters</code> añade soporte para todos los separadores de texto apoyados por LangChain

<h2 id="installation">🐍 Instalación</h2>

Instala el administrador de paquetes de tu elección. Alentamos el uso de <code>uv</code>


Ejemplo con <code>uv</code>:



```bash
  uv pip install sinapsis-langchain-splitters --extra-index-url https://pypi.sinapsis.tech
```

o con solo <code>pip</code>:

```bash
  pip install sinapsis-langchain-splitters --extra-index-url https://pypi.sinapsis.tech
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
El <strong>Sinapsis Langchain</strong> módulo proporciona plantillas de envoltura para <strong>Cargadores de datos comunitarios de Langchain</strong>, haciéndolos perfectamente utilizables dentro de Sinapsis.

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
  name: my_test_agent
  description: Agent to split text using the RecursiveCharacterTextSplitter class from LangChain
templates:
- template_name: InputTemplate
  class_name: InputTemplate
  attributes: {}
- template_name: RecursiveCharacterTextSplitterWrapper
  class_name: RecursiveCharacterTextSplitterWrapper
  template_input: InputTemplate
  attributes:
    add_document_as_text_packet: false
    generic_key: WikipediaLoaderWrapper
    recursivecharactertextsplitter_init:
      separators: [" "]
      keep_separator: true
      is_separator_regex: false
```

Se puede encontrar una lista completa de clases de cargador de documentos disponibles en LangChain:
<a href="https://python.langchain.com/api_reference/text_splitters/index.html">Divisores de texto de LangChain</a>
<h2 id="usage">📚 Ejemplo de uso</h2>
El siguiente ejemplo demuestra cómo utilizar el <strong>RecursiveCharacterTextSplitterWrapper</strong> plantilla para sacar los Documentos de una plantilla de WikipediaLoaderWrapper.

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
- template_name: InputTemplate
  class_name: WikipediaLoaderWrapper
  attributes: {}
- template_name: RecursiveCharacterTextSplitterWrapper
  class_name: RecursiveCharacterTextSplitterWrapper
  template_input: InputTemplate
  attributes:
    add_document_as_text_packet: false
    generic_key: WikipediaLoaderWrapper
    recursivecharactertextsplitter_init:
      separators: null
      keep_separator: true
      is_separator_regex: false
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


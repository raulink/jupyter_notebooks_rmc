# Script de python para la migracion
Se desarrolla un script en python para la imporación de datos desde la taxonomia y el plan de Mantenimiento 

```mermaid
graph TD;
    PlanMaestro -->Script;
    Script-->BaseDatos;    
```


```mermaid
gantt
    title Plan de Desarrollo de Software
    dateFormat  DD-MM-YYYY
    axisFormat  %d/%m

    section Análisis
    Recolección de Requisitos     :done,    a1, 2024-01-01, 10d
    Análisis de Requisitos        :done,    a2, after a1, 5d

    section Diseño
    Diseño de Arquitectura        :active,  a3, after a2, 7d
    Diseño de Interfaz            :         a4, after a3, 5d

    section Implementación
    Desarrollo del Backend        :         a5, after a4, 20d
    Desarrollo del Frontend       :         a6, after a4, 15d

    section Pruebas
    Pruebas Unitarias             :         a7, after a5, 10d
    Pruebas de Integración        :crit,    a8, after a7, 7d
    Pruebas de Usuario            :crit,    a9, after a8, 5d
    Lanzamiento                   :milestone, a10, after a9, 0d
```

```mermaid
pie title Distribución de equipos
    "Etiqueta 1" : 5
    "Etiqueta 2" : 10
    "Etiqueta 3" : 3
```


___



### 3. **Visualizar el Diagrama**:
Para ver el diagrama en VSCode:

- Guarda tu archivo Markdown con el código Mermaid.
- Abre la vista previa del archivo Markdown. Puedes hacerlo de varias maneras:
  - Haz clic derecho en el archivo y selecciona **"Open Preview"**.
  - O utiliza el atajo de teclado `Ctrl+Shift+V` (o `Cmd+Shift+V` en Mac).
  - O abre la vista dividida con `Ctrl+K V` (o `Cmd+K V` en Mac) para ver el código y la vista previa al mismo tiempo.
  
El diagrama Mermaid debería renderizarse en la vista previa del Markdown.

### 4. **Configuración Adicional (Opcional)**:
Si quieres personalizar la configuración de Mermaid, puedes hacerlo en la configuración de usuario o de espacio de trabajo en VSCode. Busca "Mermaid" en la configuración para ajustar opciones como el tema del diagrama, la fuente, entre otros.

¡Y eso es todo! Ahora deberías poder escribir y visualizar diagramas Mermaid en tus archivos Markdown directamente en VSCode.

# jupyter_notebooks_gma

# Dashboards

En este proyecto se elaboran los dashboards de:
- Ingresos salidas de almacen
1. Ingresos
2. *Salidas*



A continuación unos cuantos ejemplos de diagramas:
    
    Mermaid es un lenguaje de marcado que te permite crear diagramas y visualizaciones dinámicas y fáciles de mantener directamente en Markdown. Es ampliamente utilizado debido a su simplicidad y versatilidad, y es compatible con varias herramientas y plataformas, incluyendo VSCode, GitHub, GitLab y más.
    
---

## 1. **Diagramas de Flujo**

Los diagramas de flujo se utilizan para representar procesos, flujos de trabajo o algoritmos de manera visual.

### **Sintaxis Básica**

```mermaid
graph  LR
    Start --> Step1
    Step1 --> Decision{Decision?}
    Decision -- Yes --> Step2
    Decision -- No --> End

```

- `graph`: Indica que estás creando un diagrama de flujo.
- `[LR/TD/RL/BT]`: Dirección del flujo.
    - `LR`: Izquierda a Derecha
    - `TD`: Arriba a Abajo (por defecto)
    - `RL`: Derecha a Izquierda
    - `BT`: Abajo a Arriba
- `->`: Flecha sólida
- `- text -->`: Flecha con texto
- `--`: Línea punteada
- `node1((Circle))`: Nodo circular
- `node2[Rectangle]`: Nodo rectangular
- `node3{Rhombus}`: Nodo rombo (decisión)
- `node4>Asimétrico]`: Nodo asimétrico
- `node5[[Subrutina]]`: Nodo subrutina

### **Ejemplo**

```mermaid

graph TD
    Start((Inicio)) --> Input[Ingresar Datos]
    Input --> Process{Datos válidos?}
    Process -- Sí --> Output[Mostrar Resultados]
    Process -- No --> Error[Mostrar Error]
    Output --> End((Fin))
    Error --> End

```

**Visualización:**

```mermaid
graph TD
    Start((Inicio)) --> Input[Ingresar Datos]
    Input --> Process{Datos válidos?}
    Process -- Sí --> Output[Mostrar Resultados]
    Process -- No --> Error[Mostrar Error]
    Output --> End((Fin))
    Error --> End

```

---

## 2. **Diagramas de Secuencia**

Los diagramas de secuencia representan interacciones entre diferentes objetos o componentes en un sistema a lo largo del tiempo.

### **Sintaxis Básica**

```mermaid
sequenceDiagram
    ParticipantA ->> ParticipantB: Mensaje
    ParticipantB -->> ParticipantA: Respuesta
    ParticipantA --x ParticipantB: Finalizar
    ParticipantB --> ParticipantA: Evento
    ParticipantA ->>+ ParticipantB: Llamada asincrónica
    ParticipantB ->>- ParticipantA: Retorno
    Note right of ParticipantA: Nota al lado derecho
    Note over ParticipantA,ParticipantB: Nota sobre ambos participantes

```

- `>>`: Flecha sólida (llamada)
- `->>`: Flecha punteada (retorno)
- `-x`: Flecha de destrucción
- `-o`: Flecha de evento
- `>>+`: Llamada asincrónica iniciada
- `>>-`: Llamada asincrónica finalizada

### **Ejemplo**

```mermaid
sequenceDiagram
    participant Usuario
    participant Sistema
    participant BaseDeDatos

    Usuario ->> Sistema: Inicia sesión
    Sistema ->> BaseDeDatos: Verificar credenciales
    BaseDeDatos -->> Sistema: Credenciales válidas
    Sistema -->> Usuario: Acceso concedido
    Usuario ->> Sistema: Solicita datos
    Sistema ->> BaseDeDatos: Obtener datos
    BaseDeDatos -->> Sistema: Datos
    Sistema -->> Usuario: Muestra datos

```

**Visualización:**

```mermaid
sequenceDiagram
    participant Usuario
    participant Sistema
    participant BaseDeDatos

    Usuario ->> Sistema: Inicia sesión
    Sistema ->> BaseDeDatos: Verificar credenciales
    BaseDeDatos -->> Sistema: Credenciales válidas
    Sistema -->> Usuario: Acceso concedido
    Usuario ->> Sistema: Solicita datos
    Sistema ->> BaseDeDatos: Obtener datos
    BaseDeDatos -->> Sistema: Datos
    Sistema -->> Usuario: Muestra datos

```

---

## 3. **Diagramas de Clase**

Los diagramas de clase se utilizan para representar la estructura de clases en programación orientada a objetos, mostrando clases, interfaces y las relaciones entre ellas.

### **Sintaxis Básica**

```mermaid

classDiagram
    ClassName <|-- ParentClass : Inheritance
    ClassName *-- AggregatedClass : Aggregation
    ClassName o-- AssociatedClass : Association
    ClassName ..> DependencyClass : Dependency
    ClassName -- InterfaceName
    ClassName : +publicMethod()
    ClassName : -privateAttribute

```

- `<|--`: Herencia
- `--`: Agregación
- `o--`: Asociación
- `..>`: Dependencia
- `-`: Realización o implementación
- `+`: Público
- ``: Privado
- `#`: Protegido

### **Ejemplo**

```mermaid
classDiagram
    class Vehiculo {
        +marca: String
        +modelo: String
        +acelerar(): void
        +frenar(): void
    }

    class Coche {
        +numeroPuertas: int
        +abrirMaletero(): void
    }

    class Moto {
        +tipoManillar: String
        +hacerCaballito(): void
    }

    Vehiculo <|-- Coche
    Vehiculo <|-- Moto

```

**Visualización:**

```mermaid
classDiagram
    class Vehiculo {
        +marca: String
        +modelo: String
        +acelerar(): void
        +frenar(): void
    }

    class Coche {
        +numeroPuertas: int
        +abrirMaletero(): void
    }

    class Moto {
        +tipoManillar: String
        +hacerCaballito(): void
    }

    Vehiculo <|-- Coche
    Vehiculo <|-- Moto

```

---

## 4. **Diagramas de Estado**

Los diagramas de estado muestran los diferentes estados por los que pasa un objeto o sistema y las transiciones entre esos estados.

### **Sintaxis Básica**

```mermaid
stateDiagram
    [*] --> EstadoInicial
    EstadoInicial --> EstadoIntermedio : Evento
    EstadoIntermedio --> [*] : EventoFinal
    EstadoIntermedio --> EstadoAlternativo : Condición
    EstadoAlternativo --> EstadoIntermedio
    EstadoIntermedio : Entry / acción
    EstadoIntermedio : Exit / acción

```

- `[ * ]`: Estado inicial o final
- `->`: Transición de estado
- `Estado : Entry / acción`: Acción al entrar en el estado
- `Estado : Exit / acción`: Acción al salir del estado

### **Ejemplo**

```mermaid
stateDiagram
    [*] --> Apagado
    Apagado --> Encendido : Presionar botón de encendido
    Encendido --> EnEspera : Inactividad prolongada
    EnEspera --> Encendido : Movimiento detectado
    Encendido --> Apagado : Presionar botón de apagado
    Apagado : Entry / Mostrar logo
    Encendido : Do / Ejecutar aplicaciones

```

**Visualización:**

```mermaid

stateDiagram
    [*] --> Apagado
    Apagado --> Encendido : Presionar botón de encendido
    Encendido --> EnEspera : Inactividad prolongada
    EnEspera --> Encendido : Movimiento detectado
    Encendido --> Apagado : Presionar botón de apagado
    Apagado : Entry / Mostrar logo
    Encendido : Do / Ejecutar aplicaciones

```

---

## 5. **Diagramas de Entidad-Relación (ER)**

Los diagramas ER se utilizan para modelar bases de datos mostrando entidades y las relaciones entre ellas.

### **Sintaxis Básica**

```mermaid
erDiagram
    Entidad1 ||--o{ Entidad2 : "tiene"
    Entidad3 }o--o{ Entidad4 : "asocia"
    Entidad1 {
        int id
        string nombre
    }

```

- `||`: Relación uno a uno
- `}|`: Relación uno a muchos
- `}|{`: Relación muchos a muchos
- `o|`: Relación opcional uno
- `o{`: Relación opcional muchos

### **Ejemplo**

```mermaid
erDiagram
    CLIENTE ||--o{ PEDIDO : realiza
    PEDIDO ||--|{ LINEA_PEDIDO : contiene
    PRODUCTO ||--|{ LINEA_PEDIDO : esta_en
    CLIENTE {
        int id_cliente
        string nombre
        string email
    }
    PEDIDO {
        int id_pedido
        date fecha
    }
    PRODUCTO {
        int id_producto
        string descripcion
        float precio
    }
    LINEA_PEDIDO {
        int cantidad
        float subtotal
    }

```

**Visualización:**

```mermaid
erDiagram
    CLIENTE ||--o{ PEDIDO : realiza
    PEDIDO ||--|{ LINEA_PEDIDO : contiene
    PRODUCTO ||--|{ LINEA_PEDIDO : esta_en
    CLIENTE {
        int id_cliente
        string nombre
        string email
    }
    PEDIDO {
        int id_pedido
        date fecha
    }
    PRODUCTO {
        int id_producto
        string descripcion
        float precio
    }
    LINEA_PEDIDO {
        int cantidad
        float subtotal
    }

```

---

## 6. **Diagramas de Gantt**

Los diagramas de Gantt se utilizan para representar cronogramas de proyectos, mostrando tareas, duraciones y dependencias.

### **Sintaxis Básica**

```mermaid
gantt
    title Título del Proyecto
    dateFormat YYYY-MM-DD
    axisFormat %d/%m/%Y

    section Sección 1
    Tarea 1           :a1, 2024-01-01, 10d
    Tarea 2           :after a1, 5d

    section Sección 2
    Tarea 3           :2024-01-15, 7d
    Tarea 4           :crit, 2024-01-20, 3d
    Hito              :milestone, 2024-01-23, 0d

```

- `title`: Título del diagrama
- `dateFormat`: Formato de fecha
- `axisFormat`: Formato del eje de tiempo
- `section`: Agrupa tareas bajo una categoría
- `:crit`: Marca la tarea como crítica
- `:milestone`: Marca un hito
- `:active`: Marca la tarea como activa
- `after a1`: Comienza después de la tarea con ID `a1`

### **Ejemplo**

```mermaid
gantt
    title Plan de Desarrollo de Software
    dateFormat  YYYY-MM-DD
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

**Visualización:**

```mermaid
gantt
    title Plan de Desarrollo de Software
    dateFormat  YYYY-MM-DD
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

---

## 7. **Diagramas de Torta (Pie)**

Los diagramas de torta se utilizan para representar proporciones y porcentajes de manera visual.

### **Sintaxis Básica**

```mermaid
pie [title]
    "Etiqueta 1" : valor1
    "Etiqueta 2" : valor2
    "Etiqueta 3" : valor3

```

- `pie [title]`: Define un diagrama de torta con un título opcional.

### **Ejemplo**

```mermaid
pie title Distribución de Ventas
    "América" : 40
    "Europa" : 25
    "Asia" : 20
    "África" : 10
    "Oceanía" : 5

```

**Visualización:**

```mermaid
pie title Distribución de Ventas por Región
    "América" : 40
    "Europa" : 25
    "Asia" : 20
    "África" : 10
    "Oceanía" : 5

```

---

## 8. **Mapas Mentales**

Los mapas mentales se utilizan para representar ideas y conceptos de manera jerárquica y visual.

### **Sintaxis Básica**

```mermaid
mindmap
    root(Raíz)
        Subtema1
            Idea1
            Idea2
        Subtema2
            Idea3
            Idea4

```

- `mindmap`: Define un mapa mental.
- `root(Raíz)`: Nodo raíz del mapa mental.
- La indentación define la jerarquía.

### **Ejemplo**

```mermaid
mindmap
    root(Plan de Proyecto)
        Definición
            Objetivos
            Alcance
        Planificación
            Recursos
            Cronograma
        Ejecución
            Desarrollo
            Pruebas
        Cierre
            Entrega
            Retroalimentación

```

**Visualización:**

```mermaid
mindmap
    root(Plan de Proyecto)
        Definición
            Objetivos
            Alcance
        Planificación
            Recursos
            Cronograma
        Ejecución
            Desarrollo
            Pruebas
        Cierre
            Entrega
            Retroalimentación

```

---

## 9. **Diagramas de Viaje del Usuario (User Journey)**

Los diagramas de viaje del usuario representan las interacciones y emociones de un usuario a lo largo de un proceso o experiencia.

### **Sintaxis Básica**

```mermaid
journey
    title Título del Viaje
    section Sección 1
        Paso 1 : etapa1
        Paso 2 : etapa2
    section Sección 2
        Paso 3 : etapa3
        Paso 4 : etapa4

```

- `journey`: Define un diagrama de viaje del usuario.
- `title`: Título del diagrama.
- `section`: Agrupa pasos bajo una categoría.
- `etapa`: Nivel de satisfacción/emoción (puede ser numérico o textual).

### **Ejemplo**

```mermaid
journey
    title Compra en Línea
    section Navegación
        Buscar Producto : 5
        Ver Detalles : 4
    section Compra
        Agregar al Carrito : 4
        Realizar Pago : 2
    section Post-compra
        Recepción del Producto : 5
        Dejar Reseña : 4

```

**Visualización:**

```mermaid
journey
    title Compra en Línea
    section Navegación
        Buscar Producto : 5
        Ver Detalles : 4
    section Compra
        Agregar al Carrito : 4
        Realizar Pago : 2
    section Post-compra
        Recepción del Producto : 5
        Dejar Reseña : 4

```

---

## 10. **Estilos y Temas**

Mermaid permite personalizar el estilo y apariencia de los diagramas mediante clases y configuraciones globales.

### **Aplicar Estilos a Nodos**

```mermaid
graph TD
    A[Inicio] --> B[Proceso]
    B --> C[Fin]

    classDef clasePersonalizada fill:#f9f,stroke:#333,stroke-width:4px;
    class B clasePersonalizada;

```

- `classDef`: Define una clase de estilo personalizada.
- `class`: Asigna la clase a nodos específicos.

**Ejemplo con Estilos:**

```mermaid
graph TD
    A[Inicio] --> B[Proceso]
    B --> C[Fin]

    classDef importante fill:#ffcccc,stroke:#ff0000,stroke-width:2px;
    class B importante;

```

**Visualización:**

```mermaid
graph TD
    A[Inicio] --> B[Proceso]
    B --> C[Fin]

    classDef importante fill:#ffcccc,stroke:#ff0000,stroke-width:2px;
    class B importante;

```

### **Temas Globales**

Puedes cambiar el tema global de los diagramas configurando la variable `theme`.

```mermaid
%%{init: {'theme': 'dark'}}%%
graph TD
    A --> B
    B --> C

```

- Temas disponibles: `default`, `forest`, `dark`, `neutral`, etc.

**Ejemplo con Tema Oscuro:**

```mermaid
%%{init: {'theme': 'dark'}}%%
graph TD
    A --> B
    B --> C

```

**Visualización:**

```mermaid
%%{init: {'theme': 'dark'}}%%
graph TD
    A --> B
    B --> C

```

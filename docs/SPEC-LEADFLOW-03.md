# SPEC-LEADFLOW-03 — Quality gates honestos y CI reproducible

**Estado:** BORRADOR — requiere GATE 1
**Ticket:** LEADFLOW-03
**Responsable de ejecución:** Gemini, después de aprobación humana
**Tipo de cambio:** tooling, pruebas y CI; sin funcionalidad de producto

## 1. Objetivo

Convertir los comandos de calidad del repositorio en verificaciones reales y reproducibles. Ningún comando puede finalizar correctamente si omitió el paquete, archivo o suite que debía comprobar.

## 2. Problema actual

El diagnóstico del 2026-10-02 encontró:

- `pnpm lint` falla porque no encuentra archivos aplicables;
- `pnpm typecheck` usa una opción no soportada;
- `pnpm build:sdk` termina con código 0 aunque no existe el paquete SDK esperado;
- `pnpm test` solo imprime texto y produce un falso positivo.

Estos resultados son evidencia de una línea base incompleta, no defectos ya corregidos.

## 3. Precondiciones

- GATE 0 aprobado y registrado.
- SPEC en estado APROBADO mediante GATE 1.
- LEADFLOW-02 terminado, con estructura de workspace y versiones fijadas.
- Rama dedicada creada desde la base acordada.
- El árbol de trabajo fue inspeccionado y los cambios ajenos se preservan.

## 4. Alcance

### Incluido

- definir comandos reales para lint, typecheck, pruebas y build;
- hacer que cada comando compruebe explícitamente los paquetes que declara cubrir;
- eliminar scripts placebo o convertirlos en fallos explícitos hasta que exista su implementación;
- ejecutar CI en pull requests hacia la rama protegida definida por gobernanza;
- usar instalación reproducible con lockfile congelado;
- detectar referencias Markdown locales rotas;
- detectar archivos con nombres o patrones típicos de secretos antes del merge;
- conservar resultados y SHA como evidencia de revisión.

### Excluido

- implementar captura, SDK, mensajería o UI;
- desplegar servicios;
- modificar Supabase remoto, n8n o Evolution API;
- iniciar o despachar tareas mediante `orch run`;
- introducir una plataforma de observabilidad no requerida por el MVP.

## 5. Requisitos funcionales

### RF-03.1 — Lint real

El comando de lint debe:

- cubrir los tipos de archivo existentes en el workspace;
- fallar ante una infracción deliberada;
- no depender de globs que no coincidan con ningún archivo sin advertirlo;
- documentar qué carpetas quedan excluidas y por qué.

### RF-03.2 — Typecheck real

El comando de typecheck debe:

- usar opciones válidas para la versión instalada del gestor de paquetes;
- recorrer todos los paquetes TypeScript incluidos;
- fallar ante un error de tipos deliberado;
- no descargar dependencias ni herramientas durante la ejecución.

### RF-03.3 — Pruebas reales

El comando de pruebas debe ejecutar suites existentes. Si una suite obligatoria aún no existe, la tarea correspondiente no puede declararse terminada mediante un `echo`, `true` u otro reemplazo vacío.

### RF-03.4 — Build verificable

Cada comando `build:<paquete>` debe:

- fallar si el paquete no existe;
- fallar si el paquete no genera el artefacto esperado;
- impedir que un filtro sin coincidencias sea considerado éxito;
- registrar el artefacto o comprobación que demuestra el resultado.

### RF-03.5 — CI

La CI debe ejecutar, como mínimo:

1. instalación con lockfile congelado;
2. lint;
3. typecheck;
4. pruebas disponibles y exigidas por el cambio;
5. build de paquetes existentes;
6. controles documentales y de secretos definidos en esta SPEC.

La configuración debe cancelar el pipeline ante el primer gate obligatorio fallido o mostrar claramente cada gate fallido sin convertirlo en éxito.

## 6. Requisitos de seguridad

- La CI no debe imprimir valores de `.env`, claves, tokens ni payloads reales.
- Un archivo potencialmente sensible no debe abrirse ni publicarse para determinar que requiere cuarentena humana.
- Los escáneres no reemplazan la revisión humana de archivos ya presentes en el árbol de trabajo.
- Ningún secreto de producción se requiere para lint, typecheck o pruebas unitarias.

## 7. Escenarios de aceptación

```gherkin
Escenario: una infracción de lint rompe el gate
  Dado un cambio temporal que viola una regla activa
  Cuando se ejecuta el comando de lint
  Entonces el proceso finaliza con código distinto de cero

Escenario: un error TypeScript rompe el gate
  Dado un error de tipos deliberado en un paquete incluido
  Cuando se ejecuta el typecheck
  Entonces el proceso finaliza con código distinto de cero
  Y el diagnóstico identifica el archivo afectado

Escenario: un paquete inexistente no produce un falso verde
  Dado que el paquete SDK no existe
  Cuando se ejecuta su comando de build
  Entonces el proceso finaliza con código distinto de cero

Escenario: no se acepta una suite vacía
  Dado que una prueba es obligatoria para el ticket
  Y no existe ninguna suite que la implemente
  Cuando se ejecuta el gate de pruebas
  Entonces el pipeline falla o marca explícitamente el requisito como pendiente

Escenario: la línea base válida pasa
  Dado un checkout limpio del SHA revisado
  Cuando se ejecutan todos los gates documentados
  Entonces todos terminan correctamente
  Y la evidencia incluye comandos, versiones y SHA
```

## 8. Evidencia obligatoria

- salida resumida de cada comando, sin secretos;
- versión de Node, pnpm y herramientas relevantes;
- SHA exacto probado;
- enlace al run de CI cuando exista;
- prueba negativa temporal para lint, typecheck y build sin coincidencias;
- lista de artefactos producidos por los builds.

## 9. Condiciones de parada

Gemini debe detenerse y marcar `BLOCKED` si:

- LEADFLOW-02 no fijó la estructura real del workspace;
- corregir los scripts exige implementar producto fuera de esta SPEC;
- una herramienta solicita secretos o acceso remoto;
- el árbol de trabajo contiene cambios solapados cuyo propietario no está claro;
- la CI requiere una decisión humana sobre proveedor, rama protegida o permisos.

## 10. Definición de terminado

- todos los escenarios de aceptación fueron demostrados;
- no existe un script obligatorio que solo simule trabajo;
- un filtro sin coincidencias no puede producir éxito engañoso;
- la CI usa el lockfile y el SHA revisado;
- la documentación operativa refleja los comandos reales;
- un revisor humano concede GATE 3 antes del merge.

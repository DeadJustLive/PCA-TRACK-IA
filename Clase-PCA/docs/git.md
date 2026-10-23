# Gestión de Versiones con Git

> **Instrucción para la IA:** Aplica este flujo cuando el alumno trabaje con control de versiones. **Nunca** ejecutes `commit`, `push` ni `merge` sin aprobación explícita del alumno. Tu rol es proponer la rama y el mensaje de commit; el alumno decide.

---

## 1. Estrategia de Ramas

| Rama | Propósito | Regla |
| :--- | :--- | :--- |
| `main` | Código estable y funcional | **Protegida.** Nunca se programa directo aquí. |
| `develop` | Integración del trabajo en curso | Punto de partida de las nuevas ramas. |
| `feature/<ID>-<descripcion>` | Una nueva funcionalidad | Nace de `develop`, ej. `feature/T05-login-usuario`. |
| `fix/<ID>-<descripcion>` | Corrección de un bug | Nace de `develop` (o `main` si es urgente). |
| `chore/<descripcion>` | Tareas de mantenimiento | Configuración, dependencias, docs. |

**Regla:** el nombre de la rama **siempre incluye el ID del ticket** para mantener la trazabilidad.

---

## 2. Convención de Commits (Conventional Commits)

Formato:

```
<tipo>(<alcance opcional>): <descripción breve en imperativo>

<cuerpo opcional: por qué del cambio>

Refs: #<ID-ticket>
```

Tipos permitidos:

| Tipo | Cuándo usarlo |
| :--- | :--- |
| `feat` | Nueva funcionalidad |
| `fix` | Corrección de un error |
| `docs` | Solo documentación |
| `style` | Formato/estilo, sin cambiar lógica |
| `refactor` | Cambio de código que no agrega funcionalidad ni corrige bug |
| `test` | Añadir o ajustar pruebas |
| `chore` | Configuración, dependencias, build |

**Ejemplos:**
```
feat(auth): agregar inicio de sesión con email
fix(api): corregir error 500 al guardar sin token
docs(convenciones): documentar regla CONV-SEG-01
Refs: #T12
```

**Alcances recomendados para el monorepo:**

| Alcance | Uso |
| :--- | :--- |
| `web` | App pública y cuenta |
| `admin` | Backoffice |
| `ui` | `packages/ui` y tokens |
| `api` | BFF y Edge Functions |
| `db` | Migraciones, RLS y RPC |
| `flow` | Integración de pagos |
| `docs` | Documentación y anotaciones |
| `config` | Tooling, lint, build |

---

## 3. Flujo de Trabajo (paso a paso)

1. **Elegir ticket** en `docs/estado_proyecto.md`.
2. **Crear rama** desde `develop`:
   ```
   git checkout develop
   git pull
   git checkout -b feature/T05-login-usuario
   ```
3. **Programar en micro-tareas** (respetando `docs/convenciones.md`).
4. **Commits atómicos:** un commit = un cambio coherente. No mezcles varias tareas en un commit.
5. **Probar** antes de commitear (ver F4 del flujo en `AGENTS.md`).
6. **Integrar:** abrir un Pull Request (o merge) hacia `develop`. Nunca directo a `main`.
7. **Cerrar** el ticket y actualizar `docs/estado_proyecto.md`.

---

## 4. Reglas para la IA

- **CONV-GIT-01:** La IA **propone** el nombre de rama y el mensaje de commit, pero **no ejecuta** `commit`/`push`/`merge` sin que el alumno lo apruebe.
- **CONV-GIT-02:** Antes de proponer cambios, la IA revisa el estado con `git status` y `git diff` y los presenta.
- **CONV-GIT-03:** Nunca versionar secretos. Si detecta un `.env` o clave en el área de cambios, debe **alertar** y detenerse.
- **CONV-GIT-04:** Commits pequeños y frecuentes; evita commits gigantes "de todo junto".
- **CONV-GIT-05:** Si un commit falla o hay conflicto, se corrige con un commit nuevo; no se reescribe historia de forma destructiva (`--force`) sin permiso.

---

## 5. Qué NO versionar (`.gitignore` mínimo)

```gitignore
# Dependencias
node_modules/
vendor/

# Secretos y entorno
.env
.env.local
.env.*.local

# Build / salida
dist/
build/
out/

# Cachés y sistema
.cache/
*.log
.DS_Store
Thumbs.db

# Configuración local del editor
.vscode/
.idea/
```

> Ajusta la lista al stack cuando se defina en F0. Los archivos de ejemplo de entorno (`.env.example`) **sí** se versionan, pero sin valores reales.

---

## 6. Errores comunes (y cómo evitarlos)

| Error | Causa | Solución |
| :--- | :--- | :--- |
| Commiteé una clave secreta | `.env` no estaba en `.gitignore` | Rotar la clave y eliminarla del historial |
| Rama con nombre genérico (`cambios`) | Se ignoró la convención | Renombrar incluyendo el ID del ticket |
| Un commit con 20 archivos sin relación | Se programó sin micro-tareas | Dividir en commits atómicos |
| Programé directo en `main` | Se saltó el flujo de ramas | Mover el trabajo a una rama `feature/` |
| Conflicto de merge sin entender | Se integró a ciegas | Resolver revisando ambos lados con `git diff` |

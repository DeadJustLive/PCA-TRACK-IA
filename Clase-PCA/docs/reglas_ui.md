<!-- @pca:start
@id(docs.reglas_ui)
@kind(doc)
@relates(docs.convenciones)
@relates(docs.arquitectura)
@desc(Reglas de diseño, tokens, componentes CVA, accesibilidad y estados de UI)
@pca:end -->
# Reglas de UI

> **Instrucción para la IA:** Este documento responde **cómo se ve y se compone** la interfaz. Antes de crear un componente, revisa si ya existe en `packages/ui`. No inventes colores, tamaños ni variantes fuera de los tokens.

> **Alcance:** `apps/web`, `apps/admin` y `packages/ui`. Las reglas de datos y API están en `docs/reglas_backend.md`.

---

## 1. Principios

1. **Una sola fuente de tokens.** Los colores, tipografía, spacing y radios viven en `packages/tokens`.
2. **Componentes agnósticos.** `packages/ui` no sabe qué es una planta, un pedido o Flow.
3. **Variantes, no parches.** Si un botón necesita un estilo nuevo, se agrega una variante CVA, no un `className` suelto.
4. **Mobile-first.** La experiencia base es 360 px; el desktop se adapta, no al revés.
5. **Accesibilidad por defecto.** Foco visible, teclado, labels y contraste AA.
6. **Estados completos.** Todo componente que carga datos tiene loading, empty, error y success.
7. **Menos es más.** La narrativa botánica se expresa con tipografía, imágenes y detalles; no con ruido visual.

---

## 2. Tokens canónicos

> `DESIGN.md` contiene dos paletas: el front matter (la que consumen los mockups) y una narrativa de marca con otros hex. **La implementación usa el front matter como canónico**; la paleta narrativa se conserva como referencia y debe mapearse a tokens semánticos. OPEN-06 debe confirmar esta decisión.

### 2.1 Color

| Token | Valor | Uso |
| :--- | :--- | :--- |
| `--color-primary` | `#012D1D` | Marca, botones primarios, títulos |
| `--color-primary-container` | `#1B4332` | Superficies de marca, hover |
| `--color-on-primary` | `#FFFFFF` | Texto sobre primary |
| `--color-secondary` | `#735C00` | Acentos de texto y enlaces |
| `--color-secondary-container` | `#FED65B` | Botones dorados, badges |
| `--color-on-secondary-container` | `#745C00` | Texto sobre dorado |
| `--color-tertiary` | `#3B1B32` | Detalles editoriales |
| `--color-surface` | `#F7F9FF` | Fondo base |
| `--color-surface-container-lowest` | `#FFFFFF` | Tarjetas |
| `--color-surface-container-low` | `#F1F4F9` | Secciones alternas |
| `--color-surface-container` | `#EBEEF3` | Inputs y tablas |
| `--color-surface-container-high` | `#E5E8EE` | Hover de superficie |
| `--color-on-surface` | `#181C20` | Texto principal |
| `--color-on-surface-variant` | `#414844` | Texto secundario |
| `--color-outline` | `#717973` | Bordes fuertes |
| `--color-outline-variant` | `#C1C8C2` | Bordes suaves |
| `--color-error` | `#BA1A1A` | Errores |
| `--color-error-container` | `#FFDAD6` | Fondo de error |

**Tokens de marca decorativos (no semánticos):**

| Token | Valor | Uso permitido |
| :--- | :--- | :--- |
| `--brand-gold` | `#D4AF37` | Detalles decorativos, no texto pequeño |
| `--brand-canvas` | `#FAF7F0` | Fondos editoriales puntuales |
| `--brand-plum` | `#4A2840` | Acentos editoriales |
| `--brand-charcoal` | `#212529` | Texto editorial alternativo |

> No usar `#D4AF37` para texto sobre blanco: no alcanza contraste AA. Para texto dorado usar `--color-secondary` o `--color-on-secondary-container`.

### 2.2 Tipografía

| Rol | Fuente | Token Tailwind |
| :--- | :--- | :--- |
| Display / títulos | Playfair Display | `font-display` |
| Cuerpo / UI | Plus Jakarta Sans | `font-sans` |
| Iconos | Material Symbols Outlined | `font-icon` |

| Escala | Tamaño / line-height | Uso |
| :--- | :--- | :--- |
| `display-hero` | 64/72 · 700 | Hero desktop |
| `display-lg` | 48/56 · 700 | Títulos de sección |
| `headline-lg` | 32/40 · 600 | Títulos de página |
| `headline-md` | 24/32 · 600 | Cards y modales |
| `title-lg` | 20/28 · 600 | Subtítulos |
| `body-lg` | 18/28 · 400 | Texto de lectura |
| `body-md` | 16/24 · 400 | UI general |
| `label-md` | 14/20 · 600 | Botones y labels |
| `label-sm` | 12/16 · 600 | Labels compactos |
| `caption` | 12/16 · 500 | Metadatos |

> En móvil, `display-hero` baja a 40/48 y `display-lg` a 36/44.

### 2.3 Espaciado

| Token | Valor |
| :--- | :--- |
| `space-xs` | 4 px |
| `space-sm` | 8 px |
| `space-md` | 16 px |
| `space-lg` | 24 px |
| `space-xl` | 40 px |
| `space-2xl` | 64 px |
| `gutter` | 24 px |
| `margin` | 48 px desktop / 24 px móvil |

### 2.4 Radios y sombras

| Token | Valor | Uso |
| :--- | :--- | :--- |
| `radius-sm` | 4 px | Badges |
| `radius-md` | 8 px | Inputs |
| `radius-lg` | 12 px | Cards |
| `radius-xl` | 24 px | Modales |
| `radius-full` | 9999 px | Pills |
| `shadow-rest` | `0 4px 20px rgba(1,45,29,.06)` | Cards |
| `shadow-hover` | `0 12px 32px rgba(1,45,29,.12)` | Hover |
| `shadow-float` | `0 20px 48px rgba(1,45,29,.16)` | Modales |

### 2.5 Layout

- Ancho máximo de contenido: **1440 px**.
- Grid de 12 columnas con `gutter` de 24 px.
- Admin: rail lateral de 280 px, contenido fluido.
- Web: hero full-bleed, contenido centrado.
- Breakpoints: `sm 640`, `md 768`, `lg 1024`, `xl 1280`, `2xl 1440`.

---

## 3. Tailwind y CVA

### 3.1 Reglas de Tailwind

- Usar clases semánticas de tokens (`bg-surface`, `text-on-surface`, `rounded-lg`).
- Evitar valores arbitrarios (`bg-[#123456]`, `p-[13px]`) salvo layout puntual y justificado.
- No duplicar combinaciones gigantes en JSX; encapsular en componentes.
- El contenido de `packages/ui` debe estar en el `content` de Tailwind de ambas apps.
- Modo oscuro no es requisito del MVP; si se agrega, se hace con tokens, no con `dark:` disperso.
- **OPEN-09:** la versión de Tailwind (v3.4 con preset o v4 CSS-first) se decide en S0; los ejemplos usan utilidades compatibles con ambas.

### 3.2 CVA

Todo componente con variantes usa `cva` + `cn` (`clsx` + `tailwind-merge`):

```ts
const button = cva(
  "inline-flex items-center justify-center gap-2 font-label-md transition-colors focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-primary focus-visible:ring-offset-2 disabled:pointer-events-none disabled:opacity-50",
  {
    variants: {
      intent: {
        primary: "bg-primary text-on-primary hover:bg-primary-container",
        secondary: "bg-secondary-container text-on-secondary-container hover:brightness-95",
        ghost: "bg-transparent text-primary hover:bg-surface-container",
        danger: "bg-error text-white hover:brightness-95",
      },
      size: {
        sm: "h-9 px-3 text-label-sm",
        md: "h-11 px-5",
        lg: "h-14 px-7 text-body-lg",
      },
    },
    defaultVariants: { intent: "primary", size: "md" },
  },
);
```

**Reglas:**
- Nombres de variantes semánticos (`intent`, `size`, `tone`), no visuales (`green`, `big`).
- `defaultVariants` siempre.
- `className` se acepta al final para composición controlada.
- No usar `!important`.
- Documentar cada variante en Storybook.

---

## 4. Estructura de componentes

```text
packages/ui/src/
├── components/
│   ├── button/
│   │   ├── button.tsx
│   │   ├── button.styles.ts
│   │   ├── button.test.tsx
│   │   └── button.stories.tsx
│   └── ...
├── lib/cn.ts
├── index.ts
└── styles.css
```

**Reglas:**
- Un componente por carpeta; archivo en kebab-case; export nombrado en PascalCase.
- `forwardRef` cuando el componente envuelve un elemento nativo.
- No incluir `fetch`, Supabase, router ni reglas de negocio en `packages/ui`.
- Los componentes de dominio viven en `features/*/components`.
- Los iconos se envuelven en un componente `Icon` con `aria-hidden` por defecto.
- Las imágenes usan `loading="lazy"`, `decoding="async"`, `alt` obligatorio y `sizes`.

---

## 5. Componentes base

| Componente | Variantes / estados | Notas |
| :--- | :--- | :--- |
| `Button` | primary, secondary, ghost, danger; sm/md/lg; loading | Icono opcional, `aria-busy` |
| `Input` | default, error, disabled; con icono | Label y hint obligatorios |
| `Select` | default, error | Radix Select para accesibilidad |
| `Card` | rest, interactive, featured | No anidar sombras fuertes |
| `Badge` | neutral, success, warning, danger, gold | Texto corto |
| `Dialog` | base, destructive | Radix, focus trap, ESC |
| `Table` | default, compact | Header sticky en admin |
| `Pagination` | cursor | “Cargar más” en web; páginas en admin |
| `Skeleton` | text, card, table | Sin animación si `prefers-reduced-motion` |
| `EmptyState` | catálogo, pedidos, búsqueda | Icono + acción |
| `ErrorState` | red, validación, no encontrado | Mensaje accionable + `traceId` |
| `Toast` | success, error, info | No reemplaza validación inline |
| `StatCard` | tendencia, neutral | Admin dashboard |
| `Tabs` | línea, pills | Radix Tabs |

---

## 6. Estados de datos

Toda pantalla que consume API debe definir:

| Estado | Qué se muestra |
| :--- | :--- |
| **Loading inicial** | Skeleton con la forma del contenido, no spinner de pantalla completa |
| **Refetch** | Indicador sutil; no borrar el contenido existente |
| **Empty** | Ilustración/icono, texto y acción (limpiar filtros, explorar) |
| **Error** | Mensaje humano, acción de reintento y `traceId` si aplica |
| **Success** | Contenido + acciones |
| **Partial** | Si una sección falla, el resto sigue visible |

**Reglas:**
- No mostrar errores técnicos crudos.
- No usar `alert()`.
- Los formularios muestran errores junto al campo y un resumen al enviar.
- Los botones de envío se deshabilitan y muestran loading durante la mutación.

---

## 7. Accesibilidad

- Contraste mínimo AA (4.5:1 texto normal, 3:1 texto grande).
- Foco visible con `ring-2` y offset.
- Navegación completa por teclado; orden lógico.
- `label` asociado a cada input; `aria-describedby` para hints/errores.
- `aria-live` para toasts y mensajes de estado.
- Diálogos con focus trap, ESC y retorno de foco.
- Imágenes decorativas con `alt=""`; informativas con `alt` descriptivo.
- No transmitir información solo por color.
- Respetar `prefers-reduced-motion`.
- Tablas con `caption` o `aria-label`, headers y scope.

---

## 8. Responsive

- Mobile-first; probar 360, 768, 1024 y 1440.
- El catálogo usa 1 columna en móvil, 2 en tablet, 3–4 en desktop.
- El admin colapsa el rail en móvil y usa tabs o drawer.
- Las tablas del admin se convierten en cards o scroll horizontal accesible.
- No ocultar acciones críticas en móvil; moverlas a menú.
- Los formularios ocupan una columna en móvil.

---

## 9. Movimiento

- Transiciones de 150–250 ms; evitar animaciones largas.
- Hover: color/sombra; no escalar más de 1.02.
- Modales: fade + scale suave.
- Respetar `prefers-reduced-motion`.
- No animar layout que cause CLS.
- El movimiento debe reforzar jerarquía, no distraer.

---

## 10. Contenido y tono

- Español neutro, cercano y botánico; evitar tecnicismos innecesarios.
- Títulos con sentence case, no Title Case.
- Botones con verbo de acción: “Agregar al carrito”, “Confirmar pedido”.
- Errores: qué pasó + qué hacer; sin culpar al usuario.
- Precios con separador local y moneda visible (OPEN-01).
- Fechas en formato local; `timestamptz` en datos.
- No usar “galeones” en producción si la moneda es CLP/EUR; es narrativa de mockup.

---

## 11. Mapeo de mockups

| Mockup | Componentes | Notas |
| :--- | :--- | :--- |
| `inicio_enchanted_botanicals` | Hero, FeaturedGrid, CategoryCard, JournalTeaser, Newsletter | Usar tokens; evitar hex hardcodeados |
| `cat_logo_de_especies` | CatalogFilters, ProductCard, Pagination, EmptyState | Filtros en URL; drawer móvil |
| `mi_invernadero_modales_de_acceso` | AuthDialog, PlantCard, CareLog, OrderList | Un solo modal de auth reutilizable |
| `panel_de_gesti_n` | AdminShell, StatCard, OrdersTable, ProductDialog | Tabla accesible; acciones destructivas con confirmación |
| `vlog_bot_nico` | JournalGrid, Article, SymptomForm, Newsletter | Si es IA real, aislar en feature y marcar como experimental |

---

## 12. Hacer / No hacer

| Hacer | No hacer |
| :--- | :--- |
| Usar tokens y variantes CVA | Hex sueltos o `className` gigantes |
| Mantener `packages/ui` sin dominio | Importar Supabase o `fetch` en UI |
| Implementar loading/empty/error | Mostrar solo spinner o pantalla en blanco |
| Validar contraste y teclado | Depender solo del color o del mouse |
| Reutilizar `AuthDialog` | Duplicar el modal en cada página |
| Respetar `prefers-reduced-motion` | Animaciones infinitas decorativas |
| Probar 360 px | Diseñar solo para 1440 px |

---

## 13. Checklist de componente

- [ ] Tiene historia en Storybook.
- [ ] Tiene variantes CVA y `defaultVariants`.
- [ ] Tiene estados hover, focus, disabled y loading.
- [ ] Tiene test de render y accesibilidad básica.
- [ ] Usa tokens, no valores arbitrarios.
- [ ] No contiene lógica de dominio.
- [ ] Tiene `alt`/`aria` cuando corresponde.
- [ ] Funciona en móvil y desktop.
- [ ] No rompe el presupuesto de contraste.

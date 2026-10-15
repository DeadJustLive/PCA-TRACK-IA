# AutoEstudio Asistido — Empieza aquí

Esta carpeta te da **una forma de estudiar con IA que se adapta a cómo aprende tu cerebro**. La meta es que termines con **un solo archivo tuyo** (`Mi_Estudio_TuMateria.md`) que puedas llevar a cualquier IA, desde cualquier lugar, sin volver a configurar nada.

> ⚠️ **Privacidad:** tu archivo de estudio contiene tu **perfil personal de aprendizaje**. No lo compartas públicamente ni lo subas a repositorios públicos. Y nunca incluyas datos sensibles reales (contraseñas, datos de terceros, etc.) mientras conversas con la IA.

---

## ¿Qué hay en esta carpeta?

| Archivo | Para qué sirve | ¿Cuándo lo uso? |
| :--- | :--- | :--- |
| `01_Prompt_Diagnostico_Perfil.md` | Entrevista empática que descubre tu forma de aprender. | **Al principio**, una sola vez (o cuando quieras recalibrar). |
| `02_Prompt_Generador_Friccion.md` | Motor de ejercicios con "fricción deseable" (sin perfil). | Si solo quieres practicar un tema, sin diagnóstico. |
| `03_Plantilla_Estudio_Personalizado.md` | Molde del archivo único (Sección A: perfil · Sección B: motor). | Se sube **junto con el `01`** para generar tu archivo. |

---

## El flujo (recomendado)

```
   [ Subes 01 + 03 a tu IA ]
              │
              ▼
   Diagnóstico (4–5 preguntas)   →   confirmas el resumen
              │
              ▼
   La IA te entrega UN archivo:   Mi_Estudio_TuMateria.md
              │
              ▼
   Para estudiar: subes ESE archivo + escribes un tema
```

1. **Genera tu archivo:** sube `01_Prompt_Diagnostico_Perfil.md` **y** `03_Plantilla_Estudio_Personalizado.md` a tu IA (ChatGPT, Claude, Gemini, etc.). Responde el diagnóstico. Al final, la IA rellena la plantilla y te entrega **un único archivo**.
2. **Guárdalo** con un nombre que reconozcas, reemplazando `TuMateria` (por ejemplo `Mi_Estudio_Calculo.md`). Usa solo letras, números y `_`; **sin** espacios ni símbolos raros (`< > : " / \ | ? *`).
3. **Estudia:** sube **ese** archivo a cualquier IA y escribe el tema que quieras dominar. La IA ya conoce tu perfil y aplicará el método correcto.
4. **Si cambias de materia:** abre tu archivo y edita solo el campo *Materia* (Sección A). El resto sigue sirviendo.

> Si no tienes la plantilla `03` a mano, el `01` incluye una **Estructura de Reserva** de último recurso, pero lo ideal es usar la plantilla oficial.

---

## ¿Y el `02`? (modo sin perfil)

Si todavía no quieres hacer el diagnóstico y solo necesitas **practicar** (por ejemplo, antes de un examen), sube directamente `02_Prompt_Generador_Friccion.md` y dile el tema. Te guiará con el mismo método socrático, pero sin tu perfil.

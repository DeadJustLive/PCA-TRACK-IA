# Registro de Cicatrices de Guerra (Learning Loop)

> **Instrucción para la IA:** Si el proyecto falla, debes consultar este archivo para ver si cometiste este error en el pasado. Si resolvemos un bug complejo, debes agregar el error aquí siguiendo el formato estricto.

## Errores Registrados

```markdown
// @learn-error id='EJEMPLO-001'
// input='Intentar hacer un fetch a Supabase sin el token JWT en las Edge Functions'
// expected='Que la base de datos rechace la solicitud'
// actual='Error silencioso 500 sin mensaje descriptivo'
// fix='Siempre inyectar el Authorization Header con el Bearer Token extraído del contexto de Deno.'
```

*(El alumno y la IA añadirán más errores debajo de esta línea durante el desarrollo del Taller 4)*

"""
Generate PDF documentation for the Optidriver project.
"""
import io
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.lib.colors import HexColor
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, PageBreak, Table, TableStyle, Preformatted
)
from reportlab.lib.enums import TA_LEFT, TA_CENTER


def build_documentation_pdf() -> bytes:
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(
        buffer, pagesize=A4,
        leftMargin=2 * cm, rightMargin=2 * cm,
        topMargin=2 * cm, bottomMargin=2 * cm,
        title="Optidriver - Documentación Técnica",
    )
    styles = getSampleStyleSheet()

    title_style = ParagraphStyle(
        'Title', parent=styles['Title'],
        fontSize=28, textColor=HexColor('#007AFF'),
        alignment=TA_CENTER, spaceAfter=20,
    )
    h1 = ParagraphStyle(
        'H1', parent=styles['Heading1'],
        fontSize=18, textColor=HexColor('#007AFF'),
        spaceBefore=16, spaceAfter=10,
    )
    h2 = ParagraphStyle(
        'H2', parent=styles['Heading2'],
        fontSize=14, textColor=HexColor('#1A1A1A'),
        spaceBefore=12, spaceAfter=6,
    )
    body = ParagraphStyle(
        'Body', parent=styles['BodyText'],
        fontSize=10, leading=14, alignment=TA_LEFT,
    )
    code = ParagraphStyle(
        'Code', parent=styles['Code'],
        fontSize=9, leading=12, leftIndent=10, backColor=HexColor('#F4F4F5'),
    )

    story = []

    # Cover
    story.append(Spacer(1, 4 * cm))
    story.append(Paragraph("OPTIDRIVER", title_style))
    story.append(Paragraph("Documentación Técnica Completa", styles['Heading2']))
    story.append(Spacer(1, 1 * cm))
    story.append(Paragraph(
        "Aplicación de optimización avanzada para Windows con gestión inteligente de drivers "
        "y asistente IA basado en GPT-5.2.",
        body
    ))
    story.append(Spacer(1, 2 * cm))
    story.append(Paragraph("Versión 1.0 · 2026", body))
    story.append(PageBreak())

    # 1. Introducción
    story.append(Paragraph("1. Introducción", h1))
    story.append(Paragraph(
        "Optidriver es una aplicación profesional diseñada para optimizar el rendimiento de equipos Windows "
        "mediante perfiles de uso adaptativos, gestión centralizada de drivers, y un asistente inteligente "
        "que analiza el hardware y recomienda mejoras o equipos nuevos según el presupuesto del usuario.",
        body
    ))

    story.append(Paragraph("1.1 Objetivos", h2))
    story.append(Paragraph(
        "• Automatizar la optimización del sistema según el perfil de uso (Gaming / Oficina / Óptimo).<br/>"
        "• Centralizar la detección y actualización de drivers.<br/>"
        "• Ofrecer recomendaciones inteligentes basadas en IA para upgrades de hardware.<br/>"
        "• Proteger el sistema con puntos de restauración automáticos antes de cambios críticos.",
        body
    ))

    # 2. Arquitectura
    story.append(Paragraph("2. Arquitectura del Sistema", h1))
    story.append(Paragraph(
        "Optidriver usa una arquitectura cliente-servidor local basada en tecnologías web modernas, "
        "ejecutándose íntegramente en el equipo del usuario.",
        body
    ))

    arch_data = [
        ["Componente", "Tecnología", "Responsabilidad"],
        ["Backend", "FastAPI (Python 3.11)", "Lógica de negocio, integración Windows API, IA"],
        ["Frontend", "React 19 + Shadcn/UI", "Interfaz de usuario tactical dark-theme"],
        ["Base de datos", "MongoDB", "Persistencia de perfiles, logs, sesiones IA"],
        ["IA", "GPT-5.2 (OpenAI)", "Recomendaciones inteligentes de hardware"],
        ["Sistema", "psutil + wmi + winreg", "Métricas, procesos, drivers, registro"],
    ]
    table = Table(arch_data, colWidths=[4 * cm, 5 * cm, 7 * cm])
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), HexColor('#007AFF')),
        ('TEXTCOLOR', (0, 0), (-1, 0), HexColor('#FFFFFF')),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 9),
        ('GRID', (0, 0), (-1, -1), 0.5, HexColor('#27272A')),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('LEFTPADDING', (0, 0), (-1, -1), 6),
        ('RIGHTPADDING', (0, 0), (-1, -1), 6),
    ]))
    story.append(table)
    story.append(Spacer(1, 0.5 * cm))

    # 3. Módulos
    story.append(PageBreak())
    story.append(Paragraph("3. Módulos Funcionales", h1))

    modules = [
        ("3.1 Módulo de Optimización del Sistema",
         "Escanea procesos, servicios y aplicaciones de arranque. Aplica reglas específicas por perfil:",
         [
             "Gaming: cierra procesos pesados (OneDrive, Teams, Chrome), activa plan 'Alto Rendimiento' y desactiva efectos visuales.",
             "Oficina: equilibrio entre apps y efectos visuales. Plan 'Balanceado'.",
             "Óptimo: optimización moderada preservando experiencia del usuario.",
             "Protección: lista blanca de procesos críticos (smss.exe, csrss.exe, etc.) que nunca se tocan.",
         ]),
        ("3.2 Módulo de Gestión de Drivers",
         "Utiliza WMI + pnputil para enumerar drivers instalados y cotejarlos con versiones disponibles.",
         [
             "Detección de hardware completo (CPU, GPU, RAM, placa base).",
             "Imagen representativa del equipo descargada desde Unsplash para validación visual.",
             "Actualización individual o en lote con confirmación previa.",
             "Aviso detallado: versión actual vs nueva antes de aplicar cambios.",
         ]),
        ("3.3 Asistente IA (GPT-5.2)",
         "Endpoint POST /api/ai/analyze envía el informe de hardware + perfil + presupuesto a GPT-5.2.",
         [
             "Devuelve JSON estructurado: veredicto, puntuación, juegos compatibles, mejoras, equipos recomendados.",
             "Interfaz terminal-style con IBM Plex Mono.",
             "Chat libre vía POST /api/ai/chat para consultas abiertas.",
         ]),
        ("3.4 Puntos de Restauración",
         "Usa PowerShell Checkpoint-Computer para crear snapshots del sistema.",
         [
             "Creación automática antes de optimizaciones o actualizaciones de drivers.",
             "Creación manual desde el dashboard.",
             "Historial persistente en MongoDB.",
         ]),
    ]

    for title, desc, bullets in modules:
        story.append(Paragraph(title, h2))
        story.append(Paragraph(desc, body))
        story.append(Paragraph("<br/>".join(f"• {b}" for b in bullets), body))
        story.append(Spacer(1, 0.3 * cm))

    # 4. API
    story.append(PageBreak())
    story.append(Paragraph("4. API REST - Endpoints", h1))

    api_data = [
        ["Método", "Endpoint", "Descripción"],
        ["GET", "/api/hardware/full", "Informe completo de hardware"],
        ["GET", "/api/hardware/metrics", "Métricas en tiempo real (CPU/RAM/Disk)"],
        ["GET", "/api/system/processes", "Lista de procesos activos"],
        ["GET", "/api/system/services", "Lista de servicios Windows"],
        ["GET", "/api/system/startup", "Aplicaciones de inicio"],
        ["POST", "/api/optimize/analyze", "Analiza sistema contra un perfil"],
        ["POST", "/api/optimize/apply", "Aplica optimizaciones del perfil"],
        ["GET", "/api/drivers", "Lista todos los drivers"],
        ["GET", "/api/drivers/outdated", "Lista solo drivers desactualizados"],
        ["POST", "/api/drivers/update", "Actualiza drivers seleccionados"],
        ["POST", "/api/restore/create", "Crea punto de restauración"],
        ["GET", "/api/restore/history", "Historial de puntos creados"],
        ["POST", "/api/ai/analyze", "Análisis IA completo"],
        ["POST", "/api/ai/chat", "Chat libre con el asistente"],
        ["GET", "/api/docs/pdf", "Descarga esta documentación"],
    ]
    api_table = Table(api_data, colWidths=[2 * cm, 6 * cm, 8 * cm])
    api_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), HexColor('#007AFF')),
        ('TEXTCOLOR', (0, 0), (-1, 0), HexColor('#FFFFFF')),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 8),
        ('GRID', (0, 0), (-1, -1), 0.5, HexColor('#27272A')),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('FONTNAME', (1, 1), (1, -1), 'Courier'),
    ]))
    story.append(api_table)

    # 5. Instalación
    story.append(PageBreak())
    story.append(Paragraph("5. Instalación y Ejecución en Windows", h1))

    story.append(Paragraph("5.1 Requisitos previos", h2))
    story.append(Paragraph(
        "• Windows 10/11 (64-bit)<br/>"
        "• Python 3.11+ instalado<br/>"
        "• Node.js 18+ con Yarn<br/>"
        "• MongoDB Community Server instalado y corriendo en localhost:27017<br/>"
        "• Permisos de administrador (para puntos de restauración y gestión de drivers reales)",
        body
    ))

    story.append(Paragraph("5.2 Instalación", h2))
    install_code = """# 1. Clonar o copiar el proyecto
cd C:\\optidriver

# 2. Backend - Instalar dependencias
cd backend
pip install -r requirements.txt
pip install wmi pywin32   # específico Windows

# 3. Frontend - Instalar dependencias
cd ..\\frontend
yarn install

# 4. Configurar backend/.env
#    MONGO_URL="mongodb://localhost:27017"
#    DB_NAME="optidriver"
#    EMERGENT_LLM_KEY=<tu-clave>

# 5. Arrancar (script automático):
cd ..
run_windows.bat"""
    story.append(Preformatted(install_code, code))

    story.append(Paragraph("5.3 Ejecución con permisos de administrador", h2))
    story.append(Paragraph(
        "Para que las optimizaciones (cierre de procesos, creación de restore points, actualización de drivers) "
        "se apliquen realmente al sistema, ejecuta <b>run_windows.bat</b> con clic derecho → 'Ejecutar como administrador'. "
        "Sin permisos elevados, la app funciona en modo <i>simulación</i>: muestra qué haría, pero no lo aplica.",
        body
    ))

    # 6. Estructura de código
    story.append(PageBreak())
    story.append(Paragraph("6. Estructura de Código", h1))
    struct_code = """optidriver/
├── backend/
│   ├── server.py                  # FastAPI app + routing
│   ├── requirements.txt
│   ├── .env                       # MONGO_URL, DB_NAME, EMERGENT_LLM_KEY
│   └── optidriver/
│       ├── hardware.py           # Detección CPU/GPU/RAM/Mobo
│       ├── optimizer.py          # Perfiles + procesos críticos
│       ├── drivers.py            # pnputil + WMI
│       ├── restore.py            # PowerShell Checkpoint-Computer
│       ├── ai_assistant.py       # GPT-5.2 via emergentintegrations
│       └── docs.py               # Este PDF
├── frontend/
│   ├── src/
│   │   ├── App.js                # Router principal
│   │   ├── pages/
│   │   │   ├── Dashboard.jsx     # Home + perfiles + métricas
│   │   │   ├── Optimizer.jsx     # Detalle de optimización
│   │   │   ├── Drivers.jsx       # Gestión drivers
│   │   │   ├── AIAssistant.jsx   # Terminal IA
│   │   │   └── RestorePoints.jsx
│   │   ├── components/
│   │   │   ├── Layout.jsx        # Shell con nav
│   │   │   ├── MetricCard.jsx
│   │   │   └── ProfileCard.jsx
│   │   └── lib/api.js            # Axios wrapper
└── run_windows.bat                # Launcher local"""
    story.append(Preformatted(struct_code, code))

    # 7. Base de datos
    story.append(PageBreak())
    story.append(Paragraph("7. Base de Datos - MongoDB", h1))
    story.append(Paragraph("Colecciones utilizadas:", body))
    db_data = [
        ["Colección", "Descripción"],
        ["profiles", "Perfil activo seleccionado por el usuario"],
        ["optimization_logs", "Historial de optimizaciones aplicadas"],
        ["driver_updates", "Registro de actualizaciones de drivers"],
        ["restore_points", "Historial de puntos de restauración creados"],
        ["ai_sessions", "Sesiones del asistente IA (historial de chat)"],
    ]
    db_table = Table(db_data, colWidths=[4 * cm, 12 * cm])
    db_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), HexColor('#007AFF')),
        ('TEXTCOLOR', (0, 0), (-1, 0), HexColor('#FFFFFF')),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 9),
        ('GRID', (0, 0), (-1, -1), 0.5, HexColor('#27272A')),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
    ]))
    story.append(db_table)

    # 8. Decisiones técnicas
    story.append(PageBreak())
    story.append(Paragraph("8. Decisiones Técnicas", h1))
    decisions = [
        ("Python + FastAPI", "Velocidad de desarrollo, excelente acceso a APIs Windows vía psutil/wmi."),
        ("React + Shadcn", "UI moderna, componentes accesibles, fácil personalización."),
        ("MongoDB", "Flexibilidad de schema para logs heterogéneos; sin rigidez SQL."),
        ("GPT-5.2 via Emergent", "Última versión disponible; estructurada output JSON; costo centralizado."),
        ("Modo simulación por defecto", "Seguridad ante todo: el usuario ve qué se hará antes de ejecutar."),
        ("Lista blanca de procesos críticos", "Nunca se matan procesos del kernel / explorer / servicios vitales."),
        ("Puntos de restauración previos", "Reversibilidad total ante cualquier cambio."),
    ]
    for title, desc in decisions:
        story.append(Paragraph(f"<b>{title}</b>", body))
        story.append(Paragraph(desc, body))
        story.append(Spacer(1, 0.2 * cm))

    # 9. Uso
    story.append(PageBreak())
    story.append(Paragraph("9. Cómo Usar la Aplicación", h1))
    steps = [
        ("Paso 1", "Ejecuta run_windows.bat como administrador. Se abrirá el navegador en http://localhost:3000."),
        ("Paso 2", "En el dashboard, selecciona un perfil: Gaming, Oficina o Óptimo."),
        ("Paso 3", "Revisa el análisis: procesos a cerrar, servicios afectados, ajustes a aplicar."),
        ("Paso 4", "Crea un punto de restauración (botón top-right) antes de aplicar cambios."),
        ("Paso 5", "Pulsa 'Aplicar Optimización'. La app muestra el progreso en tiempo real."),
        ("Paso 6", "Ve a 'Drivers' para detectar y actualizar drivers desactualizados."),
        ("Paso 7", "Consulta el 'Asistente IA' para obtener recomendaciones personalizadas según tu presupuesto."),
    ]
    for label, desc in steps:
        story.append(Paragraph(f"<b>{label}:</b> {desc}", body))
        story.append(Spacer(1, 0.2 * cm))

    # 10. Compilación .exe
    story.append(PageBreak())
    story.append(Paragraph("10. Distribución como .exe (opcional)", h1))
    story.append(Paragraph(
        "El proyecto está diseñado como aplicación web local. Para distribuirlo como ejecutable único "
        "puedes empaquetarlo con <b>PyInstaller</b> (backend) y <b>Electron</b> (wrapper del frontend):",
        body
    ))
    exe_code = """# Opción A - Launcher Python con PyInstaller
pip install pyinstaller
pyinstaller --onefile --name Optidriver launcher.py
# Genera dist\\Optidriver.exe que arranca backend + abre navegador

# Opción B - Electron wrapper
cd frontend
yarn add --dev electron electron-builder
# Configurar main.js de Electron que cargue localhost:3000
yarn electron-builder --win --x64
# Genera dist\\Optidriver Setup.exe"""
    story.append(Preformatted(exe_code, code))

    # Footer
    story.append(PageBreak())
    story.append(Spacer(1, 8 * cm))
    story.append(Paragraph("OPTIDRIVER", title_style))
    story.append(Paragraph("— Fin del documento —", ParagraphStyle('center', parent=body, alignment=TA_CENTER)))

    doc.build(story)
    buffer.seek(0)
    return buffer.getvalue()

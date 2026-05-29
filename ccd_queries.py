import os
from typing import Any

import pandas as pd
import psycopg2
import psycopg2.extras


def db_config() -> dict[str, Any]:
    return {
        "host": os.getenv("DB_HOST", "localhost"),
        "port": int(os.getenv("DB_PORT", "5432")),
        "dbname": os.getenv("DB_NAME", "cosmos"),
        "user": os.getenv("DB_USER", "ccd_reader"),
        "password": os.getenv("DB_PASSWORD", ""),
    }


def run_query(sql: str, params: tuple[Any, ...] | None = None) -> pd.DataFrame:
    with psycopg2.connect(**db_config()) as conn:
        with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
            cur.execute(sql, params)
            rows = cur.fetchall()
    return pd.DataFrame(rows)


def buscar_estudiante(id_estudiante: str) -> pd.DataFrame:
    sql = """
    SELECT
        id_estudiante,
        nombre_completo,
        programa_academico,
        facultad,
        anio_ingreso,
        semestre_actual,
        email,
        CASE WHEN anio_ingreso >= 2025 THEN 'Nuevo' ELSE 'Antiguo' END AS plan
    FROM estudiante
    WHERE id_estudiante = %s;
    """
    return run_query(sql, (id_estudiante,))


def progreso_estudiante(id_estudiante: str) -> pd.DataFrame:
    sql = """
    SELECT
        e.id_estudiante,
        e.nombre_completo,
        e.programa_academico,
        e.anio_ingreso,
        CASE WHEN e.anio_ingreso >= 2025 THEN 'Nuevo' ELSE 'Antiguo' END AS plan,
        pe.pilar1_cumplido,
        pe.pilar2_cumplido,
        pe.pilar3_cumplido,
        pe.cursos_aprobados,
        pe.cursos_faltantes
    FROM progreso_estudiante pe
    JOIN estudiante e ON e.id_estudiante = pe.id_estudiante
    WHERE pe.id_estudiante = %s;
    """
    return run_query(sql, (id_estudiante,))


def historial_cursos(id_estudiante: str) -> pd.DataFrame:
    sql = """
    SELECT
        ce.semestre,
        ce.anio,
        ce.codigo_materia,
        ce.nombre_materia,
        cm.pilar,
        cm.plan,
        ce.fecha_matricula
    FROM cursos_estudiantes ce
    LEFT JOIN catalogo_materias_ccd cm
           ON cm.codigo_materia = ce.codigo_materia
    WHERE ce.id_estudiante = %s
    ORDER BY ce.anio, ce.semestre;
    """
    return run_query(sql, (id_estudiante,))


def notas_estudiante(id_estudiante: str) -> pd.DataFrame:
    sql = """
    SELECT
        rn.fecha_registro,
        rn.codigo_materia,
        cm.nombre_materia,
        cm.pilar,
        cm.plan,
        rn.tipo_registro,
        rn.nota,
        CASE rn.nota
            WHEN 'A' THEN 'Aprobado'
            WHEN 'R' THEN 'Reprobado'
        END AS resultado
    FROM registro_nota rn
    LEFT JOIN catalogo_materias_ccd cm ON cm.codigo_materia = rn.codigo_materia
    WHERE rn.id_estudiante = %s
    ORDER BY rn.fecha_registro;
    """
    return run_query(sql, (id_estudiante,))


def catalogo_materias() -> pd.DataFrame:
    sql = """
    SELECT
        pilar,
        plan,
        codigo_materia,
        codigo_curso,
        nombre_materia,
        descripcion
    FROM catalogo_materias_ccd
    ORDER BY pilar, plan DESC, nombre_materia;
    """
    return run_query(sql)


def oferta_vigente() -> pd.DataFrame:
    sql = """
    SELECT
        nombre_curso,
        pilar,
        modalidad,
        cupos,
        cupos_disponibles,
        fecha_inicio,
        fecha_fin,
        fecha_inicio_matricula,
        fecha_fin_matricula,
        aula,
        docente
    FROM oferta
    WHERE activo = TRUE
      AND (fecha_fin_matricula IS NULL OR fecha_fin_matricula >= CURRENT_DATE)
    ORDER BY fecha_inicio_matricula NULLS LAST;
    """
    return run_query(sql)


def estadisticas_progreso() -> pd.DataFrame:
    sql = """
    SELECT
        plan,
        COUNT(*) AS total,
        COUNT(*) FILTER (WHERE pilar1_cumplido) AS p1_cumplido,
        COUNT(*) FILTER (WHERE pilar2_cumplido) AS p2_cumplido,
        COUNT(*) FILTER (WHERE pilar3_cumplido) AS p3_cumplido,
        COUNT(*) FILTER (
            WHERE pilar1_cumplido AND pilar2_cumplido AND pilar3_cumplido
        ) AS ruta_completa,
        ROUND(
            100.0 * COUNT(*) FILTER (
                WHERE pilar1_cumplido AND pilar2_cumplido AND pilar3_cumplido
            ) / NULLIF(COUNT(*), 0),
            1
        ) AS pct_completado
    FROM progreso_estudiante
    GROUP BY plan
    ORDER BY plan;
    """
    return run_query(sql)

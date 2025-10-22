import pandas as pd
import re

# Ruta de tu archivo de ubicaciones
ruta_ubicaciones = r"D:\Maestria\Series de tiempo\Data\ubicación.xlsx"

# Leer el archivo Excel
df_ubicacion = pd.read_excel(ruta_ubicaciones)

# -----------------------------------------------------
# Función para convertir coordenadas DMS a decimal
# -----------------------------------------------------
def dms_a_decimal(dms):
    """Convierte coordenadas en formato DMS (grados, minutos, segundos) a decimal."""
    if pd.isna(dms):
        return None
    if isinstance(dms, (int, float)):
        return dms

    # Limpiar espacios y caracteres extraños
    dms = str(dms).strip().replace(" ", "")

    # Expresión regular más flexible (acepta grados, minutos y segundos con o sin espacios)
    match = re.match(r"(\d+)°(\d+)'([\d\.]+)\"?([NSEW])", dms)
    if not match:
        return None  # Si no se logra hacer match, devolver None

    grados, minutos, segundos, direccion = match.groups()
    decimal = float(grados) + float(minutos) / 60 + float(segundos) / 3600

    # Aplicar signo negativo para coordenadas del hemisferio sur u oeste
    if direccion in ['S', 'W']:
        decimal *= -1

    return decimal

# -----------------------------------------------------
# Aplicar la conversión a las columnas de coordenadas
# -----------------------------------------------------
df_ubicacion['latitud_decimal'] = df_ubicacion['Latitud'].apply(dms_a_decimal)
df_ubicacion['longitud_decimal'] = df_ubicacion['Longitud'].apply(dms_a_decimal)

# -----------------------------------------------------
# Mostrar coordenadas que no se pudieron convertir
# -----------------------------------------------------
errores = df_ubicacion[
    df_ubicacion['latitud_decimal'].isna() | df_ubicacion['longitud_decimal'].isna()
][['estacion', 'Latitud', 'Longitud']]

if not errores.empty:
    print("⚠️ Coordenadas que no se pudieron convertir:")
    print(errores)
else:
    print("✅ Todas las coordenadas fueron convertidas correctamente.")

# -----------------------------------------------------
# Guardar el archivo actualizado con nuevas columnas
# -----------------------------------------------------
df_ubicacion.to_excel(ruta_ubicaciones, index=False)
print(f"💾 Archivo actualizado guardado en:\n{ruta_ubicaciones}")

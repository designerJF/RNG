import pandas as pd
import matplotlib.pyplot as plt

class AnalizadorSorteos:
    def __init__(self):
        self.resultados = []

    def agregar_resultado(self, numero):
        """Agrega a un número individual a la secuencia histórica."""
        if 1 <= numero <= 38:
            self.resultados.append(numero)
        else:
            print(f"Error: El número {numero} está fuera del rango permitido (1-38)")

    def obtener_dataframe(self):
        """Convierte la lista en un DataFrame de Pandas para el análisis."""
        return pd.DataFrame({'numero': self.resultados})

    def analisis_frecuencia(self):
        """2. Identifica los números con mayor y menor aparición."""
        df = self.obtener_dataframe()
        if df.empty: return "No hay datos."

        frecuencias = df['numero'].value_counts()
        mas_frecuentes = frecuencias.head(5)
        menos_frecuentes = frecuencias.tail(5)

        return mas_frecuentes, menos_frecuentes

    def analisis_rezagados(self):
        """3. Calcula cuántas rondas han pasado desde la última vez que salió cada número."""
        df = self.obtener_dataframe()
        rezagados = {}
        total_sorteos = len(df)

        for i in range(1, 39):
            apariciones = df[df['numero'] == i]
            if not apariciones.empty:
                ultimo_indice = apariciones.index[-1]
                rezagados[i] = total_sorteos - 1 - ultimo_indice
            else:
                rezagados[i] = total_sorteos
        
        return pd.Series(rezagados).sort_values(ascending=False)

    def patrones_grupo(self):
        """4. Analiza proporciones de Pares/Impares y Altos/Bajos."""
        df = self.obtener_dataframe()
        if df.empty: return "No hay datos."

        total = len(df)
        pares = (df['numero'] % 2 == 0).sum()
        impares = (df['numero'] % 2 != 0).sum()
        bajos = (df['numero'] <= 18).sum()
        altos = (df['numero'] >= 19).sum()

        bajos_ajustado = (df['numero'] <= 19).sum()
        altos_ajustado = (df['numero'] >= 20).sum()

        return {
            'Pares (%)': round((pares / total) * 100, 2),
            'Impares (%)': round((impares / total) * 100, 2),
            'Bajos [1-19]': round((bajos_ajustado / total) * 100, 2),
            'Altos [20-38]': round((altos_ajustado / total) * 100, 2)
        }

    def graficar_distribucion(self):
        """5. Genera un gráfico de barras con la distribución de resultados."""
        df = self.obtener_dataframe()
        if df.empty:
            print("No hay datos para graficar.")
            return

        frecuencias = df['numero'].value_counts().reindex(range(1, 39), fill_value=0)

        plt.figure(figsize=(14, 6))
        frecuencias.plot(kind='bar', color='#4C72B0', edgecolor='black')
        plt.title('Distribución de Frecuencia Histórica (1-38)', fontsize=14)
        plt.xlabel('Número', fontsize=12)
        plt.ylabel('Frecuencia', fontsize=12)
        plt.xticks(rotation=0)
        plt.axhline(y=frecuencias.mean(), color='r', linestyle='--', label=f'Media Esperada ({frecuencias.mean():.1f})')
        plt.legend()
        plt.grid(axis='y', linestyle=':', alpha=0.7)
        plt.tight_layout()
        plt.show()

analizador = AnalizadorSorteos()

datos_historicos = [12, 5, 38, 12, 7, 19, 22, 5, 1, 38, 12, 20, 31, 14, 9, 12]
for num in datos_historicos:
    analizador.agregar_resultado(num)

# --- Mostrar resultados ---
print("=" * 45)
print("      ANÁLISIS DE SORTEOS DE RULETA")
print("=" * 45)

print("\n📊 FRECUENCIA (Top 5 más y menos frecuentes):")
mas, menos = analizador.analisis_frecuencia()
print("  Más frecuentes:\n", mas.to_string())
print("  Menos frecuentes:\n", menos.to_string())

print("\n⏳ NÚMEROS REZAGADOS (rondas sin aparecer):")
rezagados = analizador.analisis_rezagados()
print(rezagados.head(10).to_string())

print("\n🎯 PATRONES DE GRUPO:")
patrones = analizador.patrones_grupo()
for k, v in patrones.items():
    print(f"  {k}: {v}%")

print("\n📈 Generando gráfico...")
analizador.graficar_distribucion()
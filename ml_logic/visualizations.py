import matplotlib.pyplot as plt
from params import *
import datetime
from utils import find_candidate_fullname
import pandas as pd

def stacked_bars():
    plt.style.use('ggplot')

    # defining labels and hexa colors
    sentiment_colors = {
        'Negativo': '#000000',       # Negro
        'Neutral': '#F5F5DC',        # Beige
        'Positivo': '#008000',       # Verde
        'Alegría': '#FFFF00',        # Amarillo
        'Sorpresa': '#800080',       # Morado
        'Tristeza': '#ADD8E6',       # Azul claro
        'Enojo': '#FF0000',          # Rojo
        'Disgusto': '#8B4513',       # Marrón
        'Miedo': '#2E0854'           # Morado oscuro
    }

    # loading candidates dfs and names
    candidates_dfs = [bullrich_df, massa_df, milei_df]
    candidates_names = ['Patricia\nBullrich', 'Sergio\nMassa', 'Javier\nMilei']

    # Crear una lista para almacenar los datos apilados
    stacked_data = []

    for df in candidates_dfs:
        sentiment_counts = df[['Negativo', 'Neutral', 'Positivo', 'Alegria', 'Sorpresa', 'Tristeza', 'Enojo', 'Disgusto', 'Miedo']].sum()
        # Eliminar cualquier sentimiento con recuento de 0
        sentiment_counts = sentiment_counts[sentiment_counts != 0]

        # Calcular el porcentaje de cada sentimiento
        total_count = sentiment_counts.sum()
        sentiment_percentages = (sentiment_counts / total_count) * 100

        # Agregar las percentajes de sentimientos al conjunto de datos apilados
        stacked_data.append(sentiment_percentages)

    # Crear un DataFrame para los datos apilados
    stacked_df = pd.DataFrame(stacked_data, index=candidates_names)

    # Crear una figura y ejes con el diseño especificado
    fig, axes = plt.subplots(2, 1, figsize=(12, 12), gridspec_kw={'height_ratios': [0.8, 3.2]})

    # Configurar la primera fila con título y leyenda
    axes[0].axis('off')  # Desactivar ejes para la primera fila
    fig.text(0.5, 0.95, '\nDistribución de Sentimientos sobre\ncandidatos a Presidente Argentinos', fontsize=40, ha='center', fontweight='bold', color='#121212')
    fig.text(0.5, 0.91, 'En porcentaje de comentarios', fontsize=24, fontweight='light', ha='center', color='#121212')

    # Añadir leyenda con colores personalizados, a modo de lista, debajo del título
    legend_handles = [plt.Rectangle((0, 0), 1, 1, color=color) for color in sentiment_colors.values()]
    fig.legend(legend_handles, sentiment_colors.keys(), ncol=5, loc='upper center', bbox_to_anchor=(0.5, 0.89), fontsize=18, frameon=False)

    # Configurar la segunda fila con el gráfico de barras apiladas horizontal
    ax = stacked_df.plot.barh(stacked=True, color=sentiment_colors.values(), ax=axes[1], width=0.8, edgecolor='none', fontsize=16)
    ax.set_xlim(0, 100)
    ax.xaxis.set_major_formatter(plt.FuncFormatter(lambda x, loc: "{:,}%".format(int(x))))
    ax.get_legend().remove()
    ax.tick_params(labelcolor='#121212')

    ax.set_xlabel('\nFuente: KL Labs', fontsize=16, fontweight='bold', color='#121212')

    plt.tight_layout()
    plt.savefig(f'imgs/stacked_all_{datetime.datetime.now().strftime("%Y-%m-%d")}.png', dpi=300, bbox_inches='tight')

def plot_neg_pos(df, candidate):
    plt.style.use('ggplot')
    # deleting last row
    df = df[:-1]
    # Crear una figura y ejes con el diseño especificado
    fig, axes = plt.subplots(2, 1, figsize=(12, 12), gridspec_kw={'height_ratios': [0.6, 3.4]})

    # Configurar la primera fila con título y leyenda
    axes[0].axis('off')  # Desactivar ejes para la primera fila
    fig.text(0.5, 0.95, f'\nOpiniones Negativas y Positivas\nsobre {find_candidate_fullname(candidate)}', fontsize=40, ha='center', fontweight='bold', color='#121212')
    fig.text(0.5, 0.91, 'En porcentaje de comentarios', fontsize=24, fontweight='light', ha='center', color='#121212')

    colors= {
        'Negativo': 'red',
        'Positivo': 'green',
    }
    # Añadir leyenda con colores personalizados, a modo de lista, debajo del título
    legend_handles = [plt.Rectangle((0, 0), 1, 1, color=color) for color in colors.values()]
    fig.legend(legend_handles, colors.keys(), ncol=5, loc='upper center', bbox_to_anchor=(0.5, 0.89), fontsize=18, frameon=False)

    # Configurar la segunda fila con el gráfico de barras apiladas horizontal
    axes[1].plot(df['%Neg'], label = 'Negativo', linewidth=4, alpha = 0.9)
    axes[1].plot(df['%Pos'], label = 'Positivo', linewidth=4, alpha = 0.9, color='green')

    # keeping first, final and three middle dates in x axis
    xticks = [df.index[0], df.index[round(len(df)/4)], df.index[round(len(df)/2)], df.index[round(len(df)/4*3)], df.index[-1]]
    axes[1].set_xticks(xticks)
    axes[1].set_xlim([df.index[0], df.index[-1]])
    axes[1].yaxis.set_major_formatter(plt.FuncFormatter(lambda x, loc: "{:,}%".format(int(x*100))))

    axes[1].set_xlabel('\nFuente: KL Labs', fontsize=16, fontweight='bold', color='#121212')

    plt.tight_layout()
    #plt.show()
    plt.savefig(f'imgs/{candidate}_neg_pos_{datetime.datetime.now().strftime("%Y-%m-%d")}.png', dpi=300, bbox_inches='tight')

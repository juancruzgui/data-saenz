import matplotlib.pyplot as plt
from params import *
import datetime
from utils import find_candidate_fullname
import pandas as pd
from io import BytesIO
from google.cloud import storage
from matplotlib.patheffects import withStroke

def plot_neg_pos(df, candidate):
    plt.style.use('ggplot')
    # deleting last row
    df = df[:-1]
    # Crear una figura y ejes con el diseño especificado
    fig, axes = plt.subplots(2, 1, figsize=(12, 12), dpi=300, gridspec_kw={'height_ratios': [0.6, 3.4]})

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
    axes[1].plot(df['%Neg'], label = 'Negativo', linewidth=5, alpha = 0.9)
    axes[1].plot(df['%Pos'], label = 'Positivo', linewidth=5, alpha = 0.9, color='green')

    # keeping first, final and three middle dates in x axis
    xticks = [df.index[0], df.index[round(len(df)/4)], df.index[round(len(df)/2)], df.index[round(len(df)/4*3)], df.index[-1]]
    axes[1].set_xticks(xticks)
    axes[1].set_xlim([df.index[0], df.index[-1]])
    axes[1].yaxis.set_major_formatter(plt.FuncFormatter(lambda x, loc: "{:,}%".format(int(x*100))))

    axes[1].set_xlabel('\nFuente: KL Labs', fontsize=16, fontweight='bold', color='#121212')

    plt.tight_layout()
    #plt.savefig(f'imgs/{candidate}_neg_pos_{datetime.datetime.now().strftime("%Y-%m-%d")}.png', dpi=300, bbox_inches='tight')
    image_buffer = BytesIO()
    plt.savefig(image_buffer, format='png', dpi=300, bbox_inches='tight')
    plt.close()
    image_buffer.seek(0)

    try:
        print(f"\nSaving {candidate} neg_pos plot to GCS")
        client = storage.Client()
        bucket = client.get_bucket(BUCKET_NAME)
        blob_png = bucket.blob(f'imgs/{candidate}_neg_pos.png')
        blob_png.upload_from_file(image_buffer, content_type='image/png')

        blob_png.acl.all().grant_read()
        blob_png.acl.save(client=client)

        public_url = blob_png.public_url

        print(f"\n✅ {candidate} neg_pos plot saved to GCS")
        print(f"\n{public_url}")
    except:
        print(f"\n❌Could not save plot for {candidate}")

def plot_bar_hor(df, candidate):
    plt.style.use('ggplot')

    sentiment_colors = {
    'Negativo': '#3d0000',       # Gris
    'Neutral': '#F5F5DC',       # Beige
    'Positivo': '#008000',      # Verde
    'Alegria': '#FFFF00',       # Amarillo
    'Sorpresa': '#800080',     # Morado
    'Tristeza': '#ADD8E6',     # Azul claro
    'Enojo': '#FF0000',         # Rojo
    'Disgusto': '#8B4513',     # Marrón
    'Miedo': '#2E0854'         # Morado oscuro
    }

    new_df = df[['Negativo', 'Neutral', 'Positivo', 'Alegria', 'Sorpresa', 'Tristeza', 'Enojo', 'Disgusto', 'Miedo']].sum()
    new_df = new_df[new_df > 1]
    new_df = new_df.sort_values(ascending=True)

    # changing sentiment_colors in order to match the order of the new_df
    new_sentiment_colors = {}
    for i in new_df.index:
        new_sentiment_colors[i] = sentiment_colors[i]

    sentiment_colors = new_sentiment_colors

    # deleting last row
    df = df[:-1]
    # Crear una figura y ejes con el diseño especificado
    fig, axes = plt.subplots(2, 1, figsize=(12, 12), dpi=300, gridspec_kw={'height_ratios': [0.6, 3.4]}, constrained_layout=True)

    # Configurar la primera fila con título y leyenda
    axes[0].axis('off')  # Desactivar ejes para la primera fila
    fig.text(0.5, 0.95, f'\nDistribución de Sentimientos sobre\n{find_candidate_fullname(candidate)}', fontsize=40, ha='center', fontweight='bold', color='#121212')
    fig.text(0.5, 0.91, 'En porcentaje de comentarios de los últimos 30 días', fontsize=24, fontweight='light', ha='center', color='#121212')

    # Configurar la segunda fila con el gráfico de barras horizontal sobre porcentaje de cada sentimiento
    margin = 0.10  # 15% de margen
    left = margin
    right = 1 - margin
    bottom, width, height = 0.1, 0.7, 0.8  # Establece la posición y el tamaño de axes[1]

    axes[1].set_position([left, bottom, right - left, height])

    ax = (new_df / new_df.sum() * 100).round(2).plot.barh(color=sentiment_colors.values(), ax=axes[1], width=0.8, edgecolor='none', figsize=(12, 12))


    # adding percentage values inside at the end of each bar (if doesn't fit, it will be outside the bar)
    white_border = withStroke(linewidth=2, foreground='white')
    for p in ax.patches:
        if p.get_width() > 4:
            ax.annotate(str(p.get_width()) + '%', (p.get_x()-6 + p.get_width(), p.get_y()+0.2), xytext=(5, 10),
                        textcoords='offset points', fontsize=16, color='#121212', fontweight='bold',path_effects=[white_border])
        else:
            ax.annotate(str(p.get_width()) + '%', (p.get_x() + p.get_width(), p.get_y()+0.2), xytext=(5, 10),
                        textcoords='offset points', fontsize=16, color='#121212', fontweight='bold',path_effects=[white_border])

    # creating a vertical line at the left border of the plot
    ax.axvline(x=0, linewidth=4, color='#121212')
    ax.set_xticks([])
    ax.tick_params(labelcolor='#121212', labelsize=16)
    ax.set_xlabel('\nFuente: KL Labs', fontsize=16, fontweight='bold', color='#121212')

    #plt.tight_layout()
    #plt.savefig(f'imgs/{candidate}_neg_pos_{datetime.datetime.now().strftime("%Y-%m-%d")}.png', dpi=300, bbox_inches='tight')
    image_buffer = BytesIO()
    plt.savefig(image_buffer, format='png', dpi=300, bbox_inches='tight')
    plt.close()
    image_buffer.seek(0)

    try:
        print(f"\nSaving {candidate} bar_hor plot to GCS")
        client = storage.Client()
        bucket = client.get_bucket(BUCKET_NAME)
        blob_png = bucket.blob(f'imgs/{candidate}_bar_hor.png')
        blob_png.upload_from_file(image_buffer, content_type='image/png')

        blob_png.acl.all().grant_read()
        blob_png.acl.save(client=client)

        public_url = blob_png.public_url

        print(f"\n✅ {candidate} bar_hor plot saved to GCS")
        print(f"\n{public_url}")
    except:
        print(f"\n❌Could not save plot for {candidate}")

def stacked_bars(df_list):
    # Define un diccionario que asigne colores a cada sentimiento
    sentiment_colors = {
        'Negativo': '#3d0000',       # Negro
        'Neutral': '#F5F5DC',       # Beige
        'Positivo': '#008000',      # Verde
        'Alegria': '#FFFF00',       # Amarillo
        'Sorpresa': '#800080',     # Morado
        'Tristeza': '#ADD8E6',     # Azul claro
        'Enojo': '#FF0000',         # Rojo
        'Disgusto': '#8B4513',     # Marrón
        'Miedo': '#2E0854'         # Morado oscuro
    }

    # Utilizar un estilo de gráfico
    plt.style.use('ggplot')

    # Datos de los candidatos y sus nombres
    candidates_dfs = df_list
    candidates_names = ["Sergio\nMassa", "Javier\nMilei", "Patricia\nBullrich"]

    # Crear una lista para almacenar los datos apilados
    stacked_data = []

    for df in candidates_dfs:
        sentiment_counts = df[['Negativo', 'Neutral', 'Positivo', 'Alegria', 'Sorpresa', 'Tristeza', 'Enojo', 'Disgusto', 'Miedo']].sum()

        # Calcular el porcentaje de cada sentimiento
        total_count = sentiment_counts.sum()
        sentiment_percentages = (sentiment_counts / total_count) * 100

        # Agregar las percentajes de sentimientos al conjunto de datos apilados
        stacked_data.append(sentiment_percentages)

    # Crear un DataFrame para los datos apilados
    stacked_df = pd.DataFrame(stacked_data, index=candidates_names)
    print(stacked_df)
    # Crear una figura y ejes con el diseño especificado
    fig, axes = plt.subplots(2, 1, figsize=(12, 12), dpi=300, gridspec_kw={'height_ratios': [0.8, 3.2]}, constrained_layout=True)

    # Configurar la primera fila con título y leyenda
    axes[0].axis('off')  # Desactivar ejes para la primera fila
    fig.text(0.5, 0.95, '\nDistribución de Sentimientos sobre\ncandidatos a Presidente Argentinos', fontsize=40, ha='center', fontweight='bold', color='#121212')
    fig.text(0.5, 0.91, 'En porcentaje de comentarios', fontsize=24, fontweight='light', ha='center', color='#121212')

    # Añadir leyenda con colores personalizados, a modo de lista, debajo del título
    legend_handles = [plt.Rectangle((0, 0), 1, 1, color=color) for color in sentiment_colors.values()]
    fig.legend(legend_handles, sentiment_colors.keys(), ncol=5, loc='upper center', bbox_to_anchor=(0.5, 0.89), fontsize=18, frameon=False)

    # Filtrar las columnas que tienen valores diferentes de cero en al menos una fila
    visible_columns = stacked_df.columns[(stacked_df != 0).any()]

    # Crear una lista de colores basada en el orden de las columnas visibles
    colors = [sentiment_colors.get(sentimiento, '#FFFFFF') for sentimiento in visible_columns]
    print(colors)

    # Configurar el gráfico de barras apiladas horizontal
    ax = stacked_df[visible_columns].plot.barh(stacked=True, color=colors, ax=axes[1], width=0.8, edgecolor='none', fontsize=16)
    ax.set_xlim(0, 100)
    ax.xaxis.set_major_formatter(plt.FuncFormatter(lambda x, loc: "{:,}%".format(int(x))))
    ax.get_legend().remove()
    ax.tick_params(labelcolor='#121212')

    ax.set_xlabel('\nFuente: KL Labs', fontsize=16, fontweight='bold', color='#121212')

    image_buffer = BytesIO()
    plt.savefig(image_buffer, format='png', dpi=300, bbox_inches='tight')
    plt.close()
    image_buffer.seek(0)

    try:
        print(f"\nSaving all candidates stacked plot to GCS")
        client = storage.Client()
        bucket = client.get_bucket(BUCKET_NAME)
        blob_png = bucket.blob(f'imgs/all_stacked_plot.png')
        blob_png.upload_from_file(image_buffer, content_type='image/png')

        blob_png.acl.all().grant_read()
        blob_png.acl.save(client=client)

        public_url = blob_png.public_url

        print(f"\n✅ All candidates stacked plot saved to GCS")
        print(f"\n{public_url}")
    except:
        print(f"\n❌Could not save all candidates stacked plot")

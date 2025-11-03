# CELDA: interfaz interactiva para Colab (ipywidgets + matplotlib)

import math
import ipywidgets as widgets
from IPython.display import display, clear_output
import matplotlib.pyplot as plt
from matplotlib.patches import Circle
import numpy as np

# --- funciones matemáticas ---
def sigmoid(x):
    try:
        return 1.0 / (1.0 + math.exp(-x))
    except OverflowError:
        return 0.0 if x < 0 else 1.0

# parámetros
INPUT_COUNT = 3
HIDDEN_COUNT = 2

# posiciones (coordenadas en un plano sencillo)
positions = {
    'inputs': [(0.1, 0.8 - i*0.3) for i in range(INPUT_COUNT)],
    'hiddens': [(0.45, 0.6 - i*0.3) for i in range(HIDDEN_COUNT)],
    'output': (0.8, 0.45)
}

# --- widgets ---
# entradas: ToggleButtons por cada entrada con valores -1 / +1
input_widgets = []
for i in range(INPUT_COUNT):
    tb = widgets.ToggleButtons(options=[('+1', 1), ('-1', -1)],
                               value=1,
                               description=f'In {i+1}:',
                               button_style='info')
    input_widgets.append(tb)

# pesos input->hidden (matriz)
w_ih_widgets = []
for h in range(HIDDEN_COUNT):
    row = []
    for i in range(INPUT_COUNT):
        s = widgets.FloatSlider(value=1.0, min=-10.0, max=10.0, step=0.1,
                                description=f'w{i+1}->h{h+1}', readout_format='.2f',
                                layout=widgets.Layout(width='330px'))
        row.append(s)
    w_ih_widgets.append(row)

# pesos hidden->output
w_ho_widgets = []
for h in range(HIDDEN_COUNT):
    s = widgets.FloatSlider(value=1.0, min=-10.0, max=10.0, step=0.1,
                            description=f'h{h+1}->o', readout_format='.2f',
                            layout=widgets.Layout(width='330px'))
    w_ho_widgets.append(s)

# biases
b_h_widgets = []
for h in range(HIDDEN_COUNT):
    s = widgets.FloatSlider(value=0.0, min=-10.0, max=10.0, step=0.1,
                            description=f'b_h{h+1}', readout_format='.2f',
                            layout=widgets.Layout(width='330px'))
    b_h_widgets.append(s)

b_o_widget = widgets.FloatSlider(value=0.0, min=-10.0, max=10.0, step=0.1,
                                 description='b_out', readout_format='.2f',
                                 layout=widgets.Layout(width='330px'))

# botón para forzar actualización (opcional)
update_button = widgets.Button(description='Actualizar', button_style='success')

# Contenedor vertical para controles (ordenado)
left_col = []
left_col.extend(input_widgets)
left_col.append(widgets.HTML("<hr><b>Pesos Input→Hidden</b>"))
for row in w_ih_widgets:
    left_col.append(widgets.HBox(row))
left_col.append(widgets.HTML("<hr><b>Pesos Hidden→Output</b>"))
for w in w_ho_widgets:
    left_col.append(w)
left_col.append(widgets.HTML("<hr><b>Biases</b>"))
for b in b_h_widgets:
    left_col.append(b)
left_col.append(b_o_widget)
left_col.append(widgets.HTML("<hr>"))
left_col.append(update_button)

controls_box = widgets.VBox(left_col, layout=widgets.Layout(overflow='auto', height='700px', width='380px'))

# --- dibujo con matplotlib ---
fig, ax = plt.subplots(figsize=(8,5))
plt.close(fig)  # evitamos que Matplotlib muestre figura extra automáticamente

def draw_network():
    ax.clear()
    ax.set_xlim(0,1)
    ax.set_ylim(0,1)
    ax.axis('off')
    # leyenda de instrucciones
    ax.text(0.02, 0.98, "Red: 3 -> 2 -> 1 (arr. valores en widgets)", fontsize=9, verticalalignment='top')

    # leer valores actuales
    input_vals = [w.value for w in input_widgets]
    w_ih = [[w_ih_widgets[h][i].value for i in range(INPUT_COUNT)] for h in range(HIDDEN_COUNT)]
    w_ho = [w_ho_widgets[h].value for h in range(HIDDEN_COUNT)]
    b_h = [b_h_widgets[h].value for h in range(HIDDEN_COUNT)]
    b_o = b_o_widget.value

    # calcular ocultas
    hidden_z = []
    hidden_a = []
    for h in range(HIDDEN_COUNT):
        z = 0.0
        for i in range(INPUT_COUNT):
            z += w_ih[h][i] * input_vals[i]
        z += b_h[h]
        a = sigmoid(z)
        hidden_z.append(z)
        hidden_a.append(a)

    # salida
    z_o = 0.0
    for h in range(HIDDEN_COUNT):
        z_o += w_ho[h] * hidden_a[h]
    z_o += b_o
    a_o = sigmoid(z_o)

    # dibujar líneas input->hidden con etiquetas de peso
    for h_idx, hpos in enumerate(positions['hiddens']):
        hx, hy = hpos
        for i_idx, ipos in enumerate(positions['inputs']):
            ix, iy = ipos
            ax.plot([ix+0.05, hx-0.05], [iy, hy], linestyle='--', linewidth=1, color='gray')
            midx = (ix+0.05 + hx-0.05)/2
            midy = (iy + hy)/2
            ax.text(midx-0.02, midy, f"{w_ih[h_idx][i_idx]:.2f}", fontsize=8, rotation=0)

    # dibujar líneas hidden->output
    ox, oy = positions['output']
    for h_idx, hpos in enumerate(positions['hiddens']):
        hx, hy = hpos
        ax.plot([hx+0.05, ox-0.05], [hy, oy], linestyle='--', linewidth=1, color='gray')
        midx = (hx+0.05 + ox-0.05)/2
        midy = (hy + oy)/2
        ax.text(midx+0.02, midy, f"{w_ho[h_idx]:.2f}", fontsize=8, rotation=0)

    # dibujar nodos: inputs
    for i_idx, pos in enumerate(positions['inputs']):
        x,y = pos
        circ = Circle((x,y), 0.04, facecolor='#ffd05b', edgecolor='#e6a800', linewidth=2)
        ax.add_patch(circ)
        ax.text(x, y+0.01, f"In {i_idx+1}", fontsize=9, ha='center')
        ax.text(x, y-0.03, f"val: {input_vals[i_idx]}", fontsize=9, ha='center')

    # nodos ocultos
    for h_idx, pos in enumerate(positions['hiddens']):
        x,y = pos
        circ = Circle((x,y), 0.05, facecolor='#efefef', edgecolor='#f0b84d', linewidth=2)
        ax.add_patch(circ)
        ax.text(x, y+0.015, f"h{h_idx+1}", fontsize=9, ha='center', fontweight='bold')
        ax.text(x-0.02, y-0.02, f"z={hidden_z[h_idx]:.3f}", fontsize=8, ha='center')
        ax.text(x-0.02, y-0.06, f"f(z)={hidden_a[h_idx]:.3f}", fontsize=8, ha='center')

    # nodo salida
    x,y = positions['output']
    circ = Circle((x,y), 0.06, facecolor='#39d6c6', edgecolor='#28a797', linewidth=2)
    ax.add_patch(circ)
    ax.text(x, y+0.02, "Output", fontsize=10, ha='center', fontweight='bold')
    ax.text(x, y-0.02, f"z={z_o:.3f}", fontsize=9, ha='center')
    ax.text(x, y-0.06, f"f(z)={a_o:.3f}", fontsize=9, ha='center')

    ax.set_aspect('equal')
    fig.canvas.draw_idle()

# función que invoca redraw (usa clear_output + display para Colab)
out = widgets.Output(layout={'border': '1px solid black'})

def refresh(_=None):
    with out:
        clear_output(wait=True)
        draw_network()
        display(fig)

# conectar observadores a todos los widgets para actualizar en tiempo real
all_widgets = []
all_widgets.extend(input_widgets)
for row in w_ih_widgets: all_widgets.extend(row)
all_widgets.extend(w_ho_widgets)
all_widgets.extend(b_h_widgets)
all_widgets.append(b_o_widget)

for w in all_widgets:
    # on_trait_change para versión antigua ipywidgets; .observe es actual
    w.observe(lambda change: refresh(), names='value')

update_button.on_click(refresh)

# Display: controles a la izquierda y figura a la derecha (o debajo en Colab)
ui = widgets.HBox([controls_box, out])
display(ui)

# inicializamos dibujo
refresh()

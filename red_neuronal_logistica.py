'''
Red neuronal visual e interactiva (regresión logística)
- Topología: 3 entradas -> 2 neuronas ocultas -> 1 salida
- Entradas: cada nodo de entrada es +1 o -1 (toggle)
- Pesos: sliders por cada conexión con rango -10..10
- Bias: slider por cada neurona oculta y salida
- Muestra z y f(z)=sigmoid(z) en cada neurona
- Interfaz: tkinter (solo stdlib), ejecutar con: python red_neuronal_logistica.py

Autor: Chaves Nahuel
'''

import tkinter as tk
from tkinter import ttk
import math

# --- funciones matemáticas ---
def sigmoid(x):
    try:
        return 1 / (1 + math.exp(-x))
    except OverflowError:
        return 0.0 if x < 0 else 1.0

# --- parámetros iniciales ---
INPUT_COUNT = 3
HIDDEN_COUNT = 2

class NeuralGui:
    def __init__(self, root):
        self.root = root
        root.title("Red neuronal: regresión logística (visual)")

        self.canvas = tk.Canvas(root, width=900, height=500, bg='#fbfbfb')
        self.canvas.grid(row=0, column=0, rowspan=6, padx=10, pady=10)

        controls = ttk.Frame(root)
        controls.grid(row=0, column=1, sticky='n')

        # variables
        self.inputs = [tk.IntVar(value=1) for _ in range(INPUT_COUNT)]  # +1/-1
        # weights: input->hidden (HIDDEN_COUNT x INPUT_COUNT)
        self.w_ih = [[tk.DoubleVar(value=1.0) for _ in range(INPUT_COUNT)] for _ in range(HIDDEN_COUNT)]
        # weights: hidden->output (1 x HIDDEN_COUNT)
        self.w_ho = [tk.DoubleVar(value=1.0) for _ in range(HIDDEN_COUNT)]
        # biases
        self.b_h = [tk.DoubleVar(value=0.0) for _ in range(HIDDEN_COUNT)]
        self.b_o = tk.DoubleVar(value=0.0)

        # build controls: inputs toggles
        ttk.Label(controls, text='Entradas (toggle +1 / -1)').pack(pady=(0,5))
        for i in range(INPUT_COUNT):
            frm = ttk.Frame(controls)
            frm.pack(anchor='w')
            btn = ttk.Button(frm, text=f'Entrada {i+1}: +1', command=lambda i=i: self.toggle_input(i))
            btn.pack(side='left')
            lbl = ttk.Label(frm, textvariable=self.inputs[i])
            lbl.pack(side='left', padx=6)

        # weights and biases controls
        ttk.Separator(controls, orient='horizontal').pack(fill='x', pady=6)
        ttk.Label(controls, text='Pesos Input -> Hidden').pack()
        for h in range(HIDDEN_COUNT):
            lab = ttk.Label(controls, text=f'Neurona oculta {h+1}')
            lab.pack()
            for i in range(INPUT_COUNT):
                s = tk.Scale(controls, from_=-10, to=10, resolution=0.1, orient='horizontal', length=200,
                             variable=self.w_ih[h][i], command=lambda *_: self.update())
                s.pack()

        ttk.Separator(controls, orient='horizontal').pack(fill='x', pady=6)
        ttk.Label(controls, text='Pesos Hidden -> Output').pack()
        for h in range(HIDDEN_COUNT):
            s = tk.Scale(controls, from_=-10, to=10, resolution=0.1, orient='horizontal', length=200,
                         variable=self.w_ho[h], command=lambda *_: self.update())
            s.pack()

        ttk.Separator(controls, orient='horizontal').pack(fill='x', pady=6)
        ttk.Label(controls, text='Biases').pack()
        for h in range(HIDDEN_COUNT):
            s = tk.Scale(controls, from_=-10, to=10, resolution=0.1, orient='horizontal', length=200,
                         variable=self.b_h[h], command=lambda *_: self.update())
            ttk.Label(controls, text=f'Bias oculta {h+1}').pack()
            s.pack()
        ttk.Label(controls, text='Bias salida').pack()
        bs = tk.Scale(controls, from_=-10, to=10, resolution=0.1, orient='horizontal', length=200,
                      variable=self.b_o, command=lambda *_: self.update())
        bs.pack()

        # draw fixed layout positions
        self.positions = {
            'inputs': [(80, 80 + i*120) for i in range(INPUT_COUNT)],
            'hiddens': [(360, 150 + i*150) for i in range(HIDDEN_COUNT)],
            'output': (700, 240)
        }

        # placeholders for canvas ids
        self.node_ids = {'inputs': [], 'hiddens': [], 'output': None}
        self.text_ids = []
        self.line_ids = []

        self.draw_base()
        self.update()

    def toggle_input(self, i):
        # toggle between +1 and -1
        current = self.inputs[i].get()
        self.inputs[i].set(-1 if current == 1 else 1)
        # update button text in controls - find the button and update text
        # easier approach: just redraw canvas labels
        self.update()

    def draw_base(self):
        self.canvas.delete('all')
        # draw inputs
        self.node_ids['inputs'] = []
        for idx, pos in enumerate(self.positions['inputs']):
            x,y = pos
            nid = self.canvas.create_oval(x-30, y-30, x+30, y+30, fill='#ffd05b', outline='#e6a800', width=3)
            self.node_ids['inputs'].append(nid)
            self.canvas.create_text(x, y-6, text=f'+1/-1', font=('Arial',9,'bold'))
            # value text placeholder
            t = self.canvas.create_text(x, y+12, text=str(self.inputs[idx].get()), font=('Arial',11))
            self.text_ids.append(t)

        # draw hiddens
        self.node_ids['hiddens'] = []
        for idx, pos in enumerate(self.positions['hiddens']):
            x,y = pos
            nid = self.canvas.create_oval(x-35, y-35, x+35, y+35, fill='#efefef', outline='#f0b84d', width=4)
            self.node_ids['hiddens'].append(nid)
            # placeholders for z and f(z)
            t1 = self.canvas.create_text(x, y-8, text='z\n0.000', font=('Arial',10,'bold'))
            t2 = self.canvas.create_text(x, y+18, text='f(z)\n0.000', font=('Arial',10))
            self.text_ids.extend([t1, t2])

        # draw output
        x,y = self.positions['output']
        oid = self.canvas.create_oval(x-45, y-45, x+45, y+45, fill='#39d6c6', outline='#28a797', width=4)
        self.node_ids['output'] = oid
        t1 = self.canvas.create_text(x, y-8, text='z\n0.000', font=('Arial',11,'bold'))
        t2 = self.canvas.create_text(x, y+18, text='f(z)\n0.000', font=('Arial',11))
        self.text_ids.extend([t1, t2])

        # draw lines (and store ids) - input->hidden
        self.line_ids = []
        for h_idx, hpos in enumerate(self.positions['hiddens']):
            hx,hy = hpos
            for i_idx, ipos in enumerate(self.positions['inputs']):
                ix,iy = ipos
                lid = self.canvas.create_line(ix+30, iy, hx-35, hy, dash=(4,6), width=2)
                # weight label
                wx = (ix + hx)/2 - 20
                wy = (iy + hy)/2
                wtid = self.canvas.create_text(wx, wy, text=f'{self.w_ih[h_idx][i_idx].get():.2f}', font=('Arial',9,'italic'))
                self.line_ids.append((lid, wtid))

        # hidden->output lines
        for h_idx, hpos in enumerate(self.positions['hiddens']):
            hx,hy = hpos
            ox,oy = self.positions['output']
            lid = self.canvas.create_line(hx+35, hy, ox-45, oy, dash=(4,6), width=2)
            wx = (hx + ox)/2 + 20
            wy = (hy + oy)/2
            wtid = self.canvas.create_text(wx, wy, text=f'{self.w_ho[h_idx].get():.2f}', font=('Arial',9,'italic'))
            self.line_ids.append((lid, wtid))

    def update(self):
        # redraw base to refresh line positions and texts (simple approach)
        self.draw_base()

        # compute hidden activations
        input_vals = [self.inputs[i].get() for i in range(INPUT_COUNT)]
        hidden_z = []
        hidden_a = []
        for h in range(HIDDEN_COUNT):
            z = 0.0
            for i in range(INPUT_COUNT):
                z += self.w_ih[h][i].get() * input_vals[i]
            z += self.b_h[h].get()
            a = sigmoid(z)
            hidden_z.append(z)
            hidden_a.append(a)

        # compute output
        z_o = 0.0
        for h in range(HIDDEN_COUNT):
            z_o += self.w_ho[h].get() * hidden_a[h]
        z_o += self.b_o.get()
        a_o = sigmoid(z_o)

        # update input value texts
        t_idx = 0
        for i in range(INPUT_COUNT):
            pos = self.positions['inputs'][i]
            x,y = pos
            # update value text
            self.canvas.itemconfigure(self.text_ids[t_idx], text=str(self.inputs[i].get()))
            t_idx += 1

        # update hidden z and f(z) texts
        for h in range(HIDDEN_COUNT):
            # each hidden had two text ids created (z and f(z)) placed in order
            z_text_id = self.text_ids[INPUT_COUNT + h*2]
            f_text_id = self.text_ids[INPUT_COUNT + h*2 + 1]
            self.canvas.itemconfigure(z_text_id, text=f'z\n{hidden_z[h]:.3f}')
            self.canvas.itemconfigure(f_text_id, text=f'f(z)\n{hidden_a[h]:.3f}')

        # update output texts
        out_z_id = self.text_ids[-2]
        out_f_id = self.text_ids[-1]
        self.canvas.itemconfigure(out_z_id, text=f'z\n{z_o:.3f}')
        self.canvas.itemconfigure(out_f_id, text=f'f(z)\n{a_o:.3f}')

        # update line labels with latest weights
        # first HIDDEN_COUNT * INPUT_COUNT items
        li = 0
        for h in range(HIDDEN_COUNT):
            for i in range(INPUT_COUNT):
                line_id, wtext_id = self.line_ids[li]
                wval = self.w_ih[h][i].get()
                self.canvas.itemconfigure(wtext_id, text=f'{wval:.2f}')
                li += 1
        # hidden->output
        for h in range(HIDDEN_COUNT):
            line_id, wtext_id = self.line_ids[li]
            wval = self.w_ho[h].get()
            self.canvas.itemconfigure(wtext_id, text=f'{wval:.2f}')
            li += 1

        # schedule next automatic update (in case variables changed programmatically)
        self.root.after(200, lambda: None)


if __name__ == '__main__':
    root = tk.Tk()
    app = NeuralGui(root)
    root.mainloop()

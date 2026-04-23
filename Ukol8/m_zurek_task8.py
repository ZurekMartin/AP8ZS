import numpy as np
import tkinter as tk
import matplotlib.gridspec as gridspec
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from tkinter import ttk

class SpectrumApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Spectrum leakage")
        self.geometry("1400x900")
        self.create_menu()
        self.create_layout()
        self.update_plot()

    def create_menu(self):
        menubar = tk.Menu(self)
        filemenu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="File", menu=filemenu)
        self.config(menu=menubar)

    def create_layout(self):
        self.left_frame = tk.Frame(self, width=300)
        self.left_frame.pack(side=tk.LEFT, fill=tk.Y, padx=10, pady=10)
        self.right_frame = tk.Frame(self)
        self.right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        self.create_controls()
        self.create_plots()

    def create_controls(self):
        indep_frame = tk.LabelFrame(self.left_frame, text="Independent variable (time)")
        indep_frame.pack(fill=tk.X, pady=5)
        self.indep_var = tk.IntVar(value=1)
        tk.Radiobutton(indep_frame, text="Length N and number of periods P", variable=self.indep_var, value=1).pack(anchor=tk.W)
        tk.Radiobutton(indep_frame, text="Sampling frequency Fs and length N", variable=self.indep_var, value=2).pack(anchor=tk.W)
        
        top_spec_win = tk.Frame(self.left_frame)
        top_spec_win.pack(fill=tk.X, pady=5)
        
        spec_frame = tk.LabelFrame(top_spec_win, text="Spectrum")
        spec_frame.pack(side=tk.LEFT, anchor='n')
        self.spec_var = tk.IntVar(value=2)
        tk.Radiobutton(spec_frame, text="One-sided", variable=self.spec_var, value=1).pack(anchor=tk.W)
        tk.Radiobutton(spec_frame, text="Double-sided", variable=self.spec_var, value=2).pack(anchor=tk.W)
        
        win_container = tk.Frame(top_spec_win)
        win_container.pack(side=tk.LEFT, padx=8)
        self.win_chk_var = tk.IntVar(value=0)
        tk.Checkbutton(win_container, text="Window function", variable=self.win_chk_var, command=self.update_window_state).pack(anchor=tk.W)
        self.win_combo = ttk.Combobox(win_container, values=["Rect", "Hamming", "Hann", "Blackman"], state="disabled", width=10)
        self.win_combo.current(0)
        self.win_combo.pack(anchor=tk.W, pady=2)
        
        func_frame = tk.Frame(self.left_frame)
        func_frame.pack(fill=tk.X, pady=10)
        self.func_combo = ttk.Combobox(func_frame, values=["DC + A * sin(2*pi*Freq*k*Ts + Phi)", "DC + A * cos(2*pi*Freq*k*Ts + Phi)"], state="readonly")
        self.func_combo.current(0)
        self.func_combo.pack(fill=tk.X)
        
        param_frame = tk.Frame(self.left_frame)
        param_frame.pack(fill=tk.X, pady=5)
        tk.Label(param_frame, text="Fs [Hz]").grid(row=0, column=0)
        self.fs_var = tk.StringVar(value="341.33")
        self.fs_entry = ttk.Entry(param_frame, textvariable=self.fs_var, width=8, state='disabled')
        self.fs_entry.grid(row=1, column=0, padx=2, sticky='we')
        tk.Label(param_frame, text="N").grid(row=0, column=1)
        self.n_var = tk.StringVar(value="64")
        self.n_entry = ttk.Entry(param_frame, textvariable=self.n_var, width=8)
        self.n_entry.grid(row=1, column=1, padx=2, sticky='we')
        tk.Label(param_frame, text="Periods [-]").grid(row=0, column=2)
        self.p_var = tk.StringVar(value="3")
        self.p_entry = ttk.Entry(param_frame, textvariable=self.p_var, width=8)
        self.p_entry.grid(row=1, column=2, padx=2, sticky='we')
        
        try:
            param_frame.columnconfigure(0, weight=1)
            param_frame.columnconfigure(1, weight=1)
            param_frame.columnconfigure(2, weight=1)
        except Exception:
            pass
            
        param_frame2 = tk.Frame(self.left_frame)
        param_frame2.pack(fill=tk.X, pady=5)
        tk.Label(param_frame2, text="Freq [Hz]").grid(row=0, column=0)
        self.freq_var = tk.StringVar(value="16")
        self.freq_entry = ttk.Entry(param_frame2, textvariable=self.freq_var, width=6)
        self.freq_entry.grid(row=1, column=0, padx=2, sticky='we')
        tk.Label(param_frame2, text="A [V]").grid(row=0, column=1)
        self.a_var = tk.StringVar(value="2")
        self.a_entry = ttk.Entry(param_frame2, textvariable=self.a_var, width=6)
        self.a_entry.grid(row=1, column=1, padx=2, sticky='we')
        tk.Label(param_frame2, text="Phi [deg]").grid(row=0, column=2)
        self.phi_var = tk.StringVar(value="0")
        self.phi_entry = ttk.Entry(param_frame2, textvariable=self.phi_var, width=6)
        self.phi_entry.grid(row=1, column=2, padx=2, sticky='we')
        tk.Label(param_frame2, text="DC [V]").grid(row=0, column=3)
        self.dc_var = tk.StringVar(value="0")
        self.dc_entry = ttk.Entry(param_frame2, textvariable=self.dc_var, width=6)
        self.dc_entry.grid(row=1, column=3, padx=2, sticky='we')
        
        try:
            for c in range(4):
                param_frame2.columnconfigure(c, weight=1)
        except Exception:
            pass
            
        res_frame = tk.Frame(self.left_frame)
        res_frame.pack(fill=tk.X, pady=20)
        tk.Label(res_frame, text="Frequency resolution [Hz]").pack(side=tk.LEFT)
        self.fres_var = tk.StringVar()
        ttk.Entry(res_frame, textvariable=self.fres_var, state='disabled', width=8).pack(side=tk.RIGHT)
        
        supp_frame = tk.Frame(self.left_frame)
        supp_frame.pack(fill=tk.X, pady=10)
        self.supp_var = tk.IntVar(value=1)
        tk.Checkbutton(supp_frame, text="Suppress small components", variable=self.supp_var).pack(anchor=tk.W)
        val_frame = tk.Frame(supp_frame)
        val_frame.pack(fill=tk.X, padx=20)
        self.thresh_var = tk.StringVar(value="5e-2")
        ttk.Entry(val_frame, textvariable=self.thresh_var, width=8).pack(side=tk.LEFT)
        tk.Label(val_frame, text="multiple of abs(max) value").pack(side=tk.LEFT, padx=5)
        
        button_frame = tk.Frame(self.left_frame)
        button_frame.pack(fill=tk.X, pady=8)
        tk.Button(button_frame, text="Update", command=self.update_plot).pack(side=tk.LEFT, expand=True, fill=tk.X, padx=(0, 5))
        tk.Button(button_frame, text="Komentář", command=self.show_commentary).pack(side=tk.RIGHT, expand=True, fill=tk.X, padx=(5, 0))

        try:
            self.indep_var.trace_add('write', lambda *args: self.update_entry_states())
        except Exception:
            self.indep_var.trace('w', lambda *args: self.update_entry_states())
        self.update_entry_states()
        self.update_window_state()

    def update_window_state(self):
        if self.win_chk_var.get() == 1:
            self.win_combo.config(state='readonly')
        else:
            self.win_combo.config(state='disabled')

    def update_entry_states(self):
        mode = self.indep_var.get()
        if mode == 1:
            self.fs_entry.config(state='disabled')
            self.n_entry.config(state='normal')
            self.p_entry.config(state='normal')
        else:
            self.fs_entry.config(state='normal')
            self.n_entry.config(state='normal')
            self.p_entry.config(state='disabled')

    def show_commentary(self):
        commentary_window = tk.Toplevel(self)
        commentary_window.title("Komentář")
        commentary_window.geometry("800x650")
        
        text_widget = tk.Text(commentary_window, wrap=tk.WORD, padx=15, pady=15, font=("Arial", 11))
        text_widget.pack(fill=tk.BOTH, expand=True)
        
        commentary_text = """KOMENTÁŘ

Nejprve jsem definoval výchozí hodnoty základních parametrů harmonického signálu s nastavitelnou stejnosměrnou složkou DC, amplitudou, frekvencí a fázovým posunem, které uživatel zadává přes grafické rozhraní. Výpočet vzorkovací frekvence je na základě zvoleného počtu bodů posloupnosti a počtu period.

Při zkoumání vlivu počtu period signálu jsem provedl srovnávací analýzu. Vizuálním porovnáním jsem potvrdil, že při celočíselném počtu period (např. P = 3) analyzované okno zachycuje přesný násobek periody signálu. V grafu periodického prodloužení na intervalu 3*N je vidět, že signál na sebe plynule navazuje. Ve frekvenční oblasti to vede ke koherentnímu vzorkování, což znamená že spektrum vykazuje ostré maximum bez úniku energie do okolních frekvenčních binů. Naopak při neceločíselném počtu period (např. P = 3.3) dochází k ustřižení signálu mimo průchod nulou. Graf periodického prodloužení v tomto případě jasně odhaluje ostré skoky na okrajích každého bloku. Jelikož algoritmus FFT předpokládá nekonečné periodické opakování vstupního bloku, tyto umělé skoky zanáší do spektra širokopásmový šum, což se přímo projevuje jako prosakování spektra.

Pro potlačení tohoto nežádoucího jevu jsem následně aplikoval vybrané okénkové funkce na časový průběh před výpočtem FFT. Zatímco použití implicitního obdélníkového okna (Rectangular) pouze ostře ořízne blok a ponechá únik energie na maximu, aplikace funkcí jako Hann, Hamming či Blackman modifikuje hrany analyzovaného signálu. Vynásobením těmito funkcemi se amplituda na okrajích bloku plynule utlumí k nule, čímž se vyhladí skoky patrné v periodickém prodloužení. Ve výsledném amplitudovém spektru jsem potvrdil razantní snížení postranních laloků (výrazné potlačení spectral leakage), avšak na úkor mírného rozšíření hlavního frekvenčního laloku, což koresponduje se snížením frekvenčního rozlišení.

Závěrem z těchto dílčích kroků vyplývá, že pro striktně přesnou detekci amplitudy harmonických složek je nezbytné zajistit koherentní vzorkování (celočíselný počet period). Pokud to povaha reálného asynchronního signálu neumožňuje, je nutné kompenzovat skokové změny na okrajích použitím vhodné okénkové funkce. Výběr konkrétního okna tak vždy představuje kompromis mezi schopností rozlišit blízké frekvence a přesností naměřené amplitudy dané složky."""
      
        text_widget.insert(tk.END, commentary_text)
        text_widget.config(state=tk.DISABLED)

    def create_plots(self):
        self.fig = Figure(figsize=(10, 8), dpi=100, facecolor='white')
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.right_frame)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        self.right_frame.configure(bg='white')
        try:
            self.canvas.get_tk_widget().config(bg='white')
        except Exception:
            pass

    def update_plot(self):
        n = int(self.n_var.get())
        freq = float(self.freq_var.get())
        a = float(self.a_var.get())
        phi = float(self.phi_var.get())
        dc = float(self.dc_var.get())
        
        if self.indep_var.get() == 1:
            p = float(self.p_var.get())
            fs = (n * freq) / p if p != 0 else 1.0
            self.fs_var.set(f"{fs:.2f}")
        else:
            fs = float(self.fs_var.get())
            p = (n * freq) / fs if fs != 0 else 0.0
            self.p_var.set(f"{p:.6g}")
            
        fres = fs / n if n != 0 else 0.0
        self.fres_var.set(f"{fres:.1f}")
        ts = 1 / fs if fs != 0 else 1.0
        t = np.arange(n) * ts
        
        func_str = self.func_combo.get()
        if "sin" in func_str:
            y = dc + a * np.sin(2 * np.pi * freq * t + np.deg2rad(phi))
        else:
            y = dc + a * np.cos(2 * np.pi * freq * t + np.deg2rad(phi))
            
        w = np.ones(n)
        if self.win_chk_var.get() == 1:
            w_type = self.win_combo.get()
            if w_type == "Hamming":
                w = np.hamming(n)
            elif w_type == "Hann":
                w = np.hanning(n)
            elif w_type == "Blackman":
                w = np.blackman(n)
                
        y_win = y * w
        self.fig.clf()
        gs = gridspec.GridSpec(4, 2, figure=self.fig, hspace=0.4)
        ax1 = self.fig.add_subplot(gs[0, 0])
        ax2 = self.fig.add_subplot(gs[0, 1])
        ax3 = self.fig.add_subplot(gs[1, :])
        ax4 = self.fig.add_subplot(gs[2, :])
        ax5 = self.fig.add_subplot(gs[3, :])
        
        for ax in (ax1, ax2, ax3, ax4, ax5):
            ax.set_facecolor('white')
            try:
                ax.xaxis.set_ticks_position('both')
                ax.yaxis.set_ticks_position('both')
            except Exception:
                pass
            ax.tick_params(axis='both', which='both', direction='in', top=True, right=True, left=True, bottom=True)
            
        ax1.plot(t, y, 'ko-', mfc='none', lw=0.8)
        if self.win_chk_var.get() == 1:
            ax1.plot(t, w, 'mo-', mfc='none', lw=0.8)
        ax1.set_xlabel("Time [s]")
        ax1.set_ylabel("Amplitude [V]")
        
        ax2.plot(t, y_win, 'ro-', mfc='none', lw=0.8)
        ax2.set_xlabel("Time [s]")
        ax2.set_ylabel("Amplitude [V]")
        
        t_ext = np.arange(3 * n) * ts
        y_ext = np.tile(y_win, 3)
        ax3.plot(t_ext, y_ext, 'ro-', mfc='none', lw=0.8)
        ax3.set_xlabel("Time [s]")
        ax3.set_ylabel("Amplitude [V]")
        
        Y = np.fft.fft(y_win) / n
        freqs = np.fft.fftfreq(n, ts)
        
        if self.spec_var.get() == 2:
            Y = np.fft.fftshift(Y)
            freqs = np.fft.fftshift(freqs)
        else:
            Y = Y[:n//2]
            freqs = freqs[:n//2]
            Y[1:] *= 2
            
        amps = np.abs(Y)
        phases = np.angle(Y, deg=True)
        thresh_mult = float(self.thresh_var.get())
        max_amp = np.max(amps)
        thresh = thresh_mult * max_amp
        
        if self.supp_var.get() == 1:
            phases[amps < thresh] = 0
            
        mline, sline, bline = ax4.stem(freqs, amps, linefmt='b-', basefmt='k-')
        mline.set_markerfacecolor('none')
        mline.set_markeredgecolor('b')
        if self.supp_var.get() == 1:
            ax4.plot(freqs, np.ones_like(freqs) * thresh, 'r--', lw=1)
        ax4.set_xlabel("Frequency [Hz]")
        ax4.set_ylabel("Amplitude [V]")
        
        mline2, sline2, bline2 = ax5.stem(freqs, phases, linefmt='b-', basefmt='k-')
        mline2.set_markerfacecolor('none')
        mline2.set_markeredgecolor('b')
        ax5.set_xlabel("Frequency [Hz]")
        ax5.set_ylabel("Phase [deg]")
        self.canvas.draw()

if __name__ == "__main__":
    app = SpectrumApp()
    app.mainloop()

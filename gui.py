import os
import threading
import time
import tkinter as tk
from tkinter import filedialog, messagebox, ttk

from calculos import aporte_agente, costo_agente, es_aplicable, esfuerzo, extremismo
from generador import generar_caso
from io_salida import guardar_csv, guardar_entrada, guardar_salida, leer_salida
from red_social import cargar_red_social
from soluciones import modexFB, modexV, modexPD
from verificacion import comparar_optimalidad, verificar_estrategia

CARPETA_PRUEBAS = os.path.join(os.path.dirname(os.path.abspath(__file__)), "Bateria de pruebas")


class ModExApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("ModEx - Moderando el extremismo de opiniones en una red social")
        self.geometry("1200x800")
        self.minsize(1100, 700)

        self.red = None
        self.resultado_actual = None
        self.limite_fb = 25
        self.algoritmos = {
            "Fuerza bruta": modexFB,
            "Voraz": modexV,
            "Programación dinámica": modexPD,
        }

        self._build_ui()

    def _build_ui(self):
        notebook = ttk.Notebook(self)
        notebook.pack(fill="both", expand=True, padx=10, pady=10)

        self.entrada_tab = ttk.Frame(notebook)
        self.resultado_tab = ttk.Frame(notebook)
        self.comparacion_tab = ttk.Frame(notebook)
        self.generador_tab = ttk.Frame(notebook)
        self.bateria_tab = ttk.Frame(notebook)

        notebook.add(self.entrada_tab, text="Entrada")
        notebook.add(self.resultado_tab, text="Salida")
        notebook.add(self.comparacion_tab, text="Comparación")
        notebook.add(self.generador_tab, text="Generar caso")
        notebook.add(self.bateria_tab, text="Batería")

        self._build_entrada_tab()
        self._build_resultado_tab()
        self._build_comparacion_tab()
        self._build_generador_tab()
        self._build_bateria_tab()

    def _build_entrada_tab(self):
        top = ttk.Frame(self.entrada_tab)
        top.pack(fill="x", padx=10, pady=10)

        ttk.Button(top, text="Abrir archivo de entrada...", command=self.abrir_archivo).pack(side="left", padx=(0, 10))
        ttk.Button(top, text="Abrir prueba predefinida...", command=self.abrir_prueba).pack(side="left", padx=(0, 10))

        self.input_info = tk.StringVar(value="Ninguna entrada cargada.")
        ttk.Label(top, textvariable=self.input_info, foreground="#1f3a5f").pack(side="left", padx=(20, 0))

        tree_frame = ttk.Frame(self.entrada_tab)
        tree_frame.pack(fill="both", expand=True, padx=10, pady=(0, 10))

        self.entrada_tree = ttk.Treeview(
            tree_frame,
            columns=("idx", "opinion", "receptividad", "influencia", "costo", "aporte"),
            show="headings",
        )
        self.entrada_tree.heading("idx", text="Índice")
        self.entrada_tree.heading("opinion", text="Opinión")
        self.entrada_tree.heading("receptividad", text="Receptividad")
        self.entrada_tree.heading("influencia", text="Influencia")
        self.entrada_tree.heading("costo", text="Costo")
        self.entrada_tree.heading("aporte", text="Aporte")

        self.entrada_tree.column("idx", width=70, anchor="center")
        self.entrada_tree.column("opinion", width=100, anchor="center")
        self.entrada_tree.column("receptividad", width=130, anchor="center")
        self.entrada_tree.column("influencia", width=120, anchor="center")
        self.entrada_tree.column("costo", width=120, anchor="center")
        self.entrada_tree.column("aporte", width=120, anchor="center")

        scroll = ttk.Scrollbar(tree_frame, orient="vertical", command=self.entrada_tree.yview)
        self.entrada_tree.configure(yscrollcommand=scroll.set)
        self.entrada_tree.pack(side="left", fill="both", expand=True)
        scroll.pack(side="right", fill="y")

    def _build_resultado_tab(self):
        top = ttk.Frame(self.resultado_tab)
        top.pack(fill="x", padx=10, pady=10)

        self.alg_sel = ttk.Combobox(top, values=list(self.algoritmos.keys()), state="readonly", width=22)
        self.alg_sel.set("Voraz")
        self.alg_sel.pack(side="left", padx=(0, 10))

        ttk.Button(top, text="Ejecutar algoritmo", command=self.ejecutar_algoritmo_seleccionado).pack(side="left", padx=(0, 10))
        ttk.Button(top, text="Guardar salida", command=self.guardar_salida_actual).pack(side="left", padx=(0, 10))
        ttk.Button(top, text="Comparar con óptimo (PD)", command=self.comparar_con_optimo).pack(side="left")

        self.estado_label = tk.StringVar(value="Sin cálculo aún.")
        ttk.Label(top, textvariable=self.estado_label, foreground="#0b5a1a").pack(side="left", padx=(20, 0))

        summary = ttk.LabelFrame(self.resultado_tab, text="Resumen")
        summary.pack(fill="x", padx=10, pady=(0, 8))
        self.resumen_var = tk.StringVar(value="")
        ttk.Label(summary, textvariable=self.resumen_var, justify="left", anchor="w", wraplength=1050).pack(fill="x", padx=10, pady=10)

        detalle_frame = ttk.LabelFrame(self.resultado_tab, text="Desglose de costo y validación")
        detalle_frame.pack(fill="both", expand=True, padx=10, pady=(0, 10))
        self.detalle_text = tk.Text(detalle_frame, height=14, wrap="word")
        self.detalle_text.pack(fill="both", expand=True, padx=10, pady=10)

        self.resultado_tree = ttk.Treeview(
            self.resultado_tab,
            columns=("idx", "moderado", "costo", "aporte", "estado"),
            show="headings",
        )
        self.resultado_tree.heading("idx", text="Índice")
        self.resultado_tree.heading("moderado", text="e_i")
        self.resultado_tree.heading("costo", text="Costo")
        self.resultado_tree.heading("aporte", text="Aporte")
        self.resultado_tree.heading("estado", text="¿Moderado?")
        self.resultado_tree.column("idx", width=70, anchor="center")
        self.resultado_tree.column("moderado", width=90, anchor="center")
        self.resultado_tree.column("costo", width=120, anchor="center")
        self.resultado_tree.column("aporte", width=120, anchor="center")
        self.resultado_tree.column("estado", width=120, anchor="center")
        self.resultado_tree.pack(fill="both", expand=True, padx=10, pady=(0, 10))

    def _build_comparacion_tab(self):
        top = ttk.Frame(self.comparacion_tab)
        top.pack(fill="x", padx=10, pady=10)

        ttk.Button(top, text="Comparar FB/Voraz/PD", command=self.comparar_todos).pack(side="left", padx=(0, 10))
        ttk.Button(top, text="Exportar CSV", command=self.exportar_tabla_comparacion).pack(side="left")

        self.comparacion_tree = ttk.Treeview(
            self.comparacion_tab,
            columns=("algoritmo", "ext", "esfuerzo", "tiempo", "aplicable", "optimo"),
            show="headings",
        )
        self.comparacion_tree.heading("algoritmo", text="Algoritmo")
        self.comparacion_tree.heading("ext", text="Ext")
        self.comparacion_tree.heading("esfuerzo", text="Esfuerzo")
        self.comparacion_tree.heading("tiempo", text="Tiempo (s)")
        self.comparacion_tree.heading("aplicable", text="Aplicable")
        self.comparacion_tree.heading("optimo", text="¿Óptimo?")
        self.comparacion_tree.pack(fill="both", expand=True, padx=10, pady=(0, 10))

    def _build_generador_tab(self):
        frame = ttk.Frame(self.generador_tab)
        frame.pack(fill="both", expand=True, padx=10, pady=10)

        campos = [
            ("n:", "n", "50"),
            ("Opinión min:", "opin_min", "-100"),
            ("Opinión max:", "opin_max", "100"),
            ("Receptividad min:", "recep_min", "0.0"),
            ("Receptividad max:", "recep_max", "1.0"),
            ("Influencia min:", "infl_min", "1.0"),
            ("Influencia max:", "infl_max", "3.0"),
            ("R_max:", "rmax", "100"),
            ("Semilla:", "seed", "123"),
        ]

        self.generador_vars = {}
        for i, (label, key, default) in enumerate(campos):
            ttk.Label(frame, text=label).grid(row=i, column=0, sticky="e", padx=5, pady=5)
            entry = ttk.Entry(frame, width=18)
            entry.insert(0, default)
            entry.grid(row=i, column=1, sticky="w", padx=5, pady=5)
            self.generador_vars[key] = entry

        ttk.Label(frame, text="Tipo:").grid(row=len(campos), column=0, sticky="e", padx=5, pady=8)
        self.tipo_var = tk.StringVar(value="aleatorio_uniforme")
        combo = ttk.Combobox(frame, textvariable=self.tipo_var, values=["aleatorio_uniforme", "dificil_para_voraz", "facil"], state="readonly", width=18)
        combo.grid(row=len(campos), column=1, sticky="w", padx=5)

        buttons = ttk.Frame(frame)
        buttons.grid(row=len(campos) + 1, column=0, columnspan=2, pady=(15, 0), sticky="w")
        ttk.Button(buttons, text="Generar caso", command=self.generar_caso).pack(side="left", padx=(0, 10))
        ttk.Button(buttons, text="Guardar caso", command=self.guardar_caso_actual).pack(side="left", padx=(0, 10))
        ttk.Button(buttons, text="Cargar caso generado", command=self.cargar_caso_generado).pack(side="left")

        self.generador_info = tk.StringVar(value="Sin caso generado.")
        ttk.Label(frame, textvariable=self.generador_info, justify="left", wraplength=700).grid(row=len(campos) + 2, column=0, columnspan=2, sticky="w", padx=5, pady=10)

    def _build_bateria_tab(self):
        frame = ttk.Frame(self.bateria_tab)
        frame.pack(fill="both", expand=True, padx=10, pady=10)

        top = ttk.Frame(frame)
        top.pack(fill="x", pady=(0, 10))

        self.umbral_fb = tk.StringVar(value="25")
        ttk.Label(top, text="Umbral FB:").pack(side="left", padx=(0, 8))
        ttk.Entry(top, textvariable=self.umbral_fb, width=8).pack(side="left", padx=(0, 10))
        ttk.Button(top, text="Ejecutar batería (35 pruebas)", command=self.ejecutar_bateria).pack(side="left")
        ttk.Button(top, text="Exportar CSV de batería", command=self.exportar_bateria_csv).pack(side="left", padx=(10, 0))

        self.bateria_tree = ttk.Treeview(frame, columns=("n", "r_max", "ext_v", "ext_pd", "t_v", "t_pd", "brecha"), show="headings")
        self.bateria_tree.heading("n", text="n")
        self.bateria_tree.heading("r_max", text="R_max")
        self.bateria_tree.heading("ext_v", text="Ext Voraz")
        self.bateria_tree.heading("ext_pd", text="Ext PD")
        self.bateria_tree.heading("t_v", text="t_v (s)")
        self.bateria_tree.heading("t_pd", text="t_pd (s)")
        self.bateria_tree.heading("brecha", text="Brecha")
        self.bateria_tree.pack(fill="both", expand=True)

    def _mostrar_entrada(self):
        if self.red is None:
            self.entrada_tree.delete(*self.entrada_tree.get_children())
            self.input_info.set("Ninguna entrada cargada.")
            return

        self.input_info.set(f"n={self.red.n}, R_max={self.red.r_max}, extremismo inicial={extremismo(self.red):.6f}")
        self.entrada_tree.delete(*self.entrada_tree.get_children())

        max_rows = 2000 if self.red.n > 2000 else self.red.n
        for i, agente in enumerate(self.red.agentes[:max_rows]):
            self.entrada_tree.insert(
                "",
                "end",
                values=(i, agente.opinion, agente.receptividad, agente.influencia, costo_agente(agente), aporte_agente(agente)),
            )
        if self.red.n > max_rows:
            self.entrada_tree.insert("", "end", values=("-", "-", "-", "-", "-", "..."))

    def abrir_archivo(self):
        ruta = filedialog.askopenfilename(
            title="Abrir archivo ModEx",
            filetypes=[("Archivos de texto", "*.txt"), ("Todos", "*.*")],
        )
        if not ruta:
            return
        try:
            self.red = cargar_red_social(ruta)
            self._mostrar_entrada()
            self._limpiar_resultado()
            messagebox.showinfo("Entrada cargada", f"Se cargó la red desde: {ruta}")
        except Exception as exc:
            messagebox.showerror("Error al cargar", str(exc))

    def abrir_prueba(self):
        if not os.path.isdir(CARPETA_PRUEBAS):
            messagebox.showerror("Error", f"No existe la carpeta de pruebas: {CARPETA_PRUEBAS}")
            return
        ruta = filedialog.askopenfilename(
            initialdir=CARPETA_PRUEBAS,
            title="Abrir prueba predefinida",
            filetypes=[("Archivos de texto", "*.txt"), ("Todos", "*.*")],
        )
        if not ruta:
            return
        try:
            self.red = cargar_red_social(ruta)
            self._mostrar_entrada()
            self._limpiar_resultado()
        except Exception as exc:
            messagebox.showerror("Error", str(exc))

    def _limpiar_resultado(self):
        self.resultado_actual = None
        self.resumen_var.set("")
        self.detalle_text.delete("1.0", "end")
        self.resultado_tree.delete(*self.resultado_tree.get_children())
        self.estado_label.set("Sin cálculo aún.")
        self.comparacion_tree.delete(*self.comparacion_tree.get_children())

    def ejecutar_algoritmo_seleccionado(self):
        if self.red is None:
            messagebox.showwarning("Sin entrada", "Primero carga una red social.")
            return

        nombre = self.alg_sel.get()
        fn = self.algoritmos[nombre]

        if nombre == "Fuerza bruta" and self.red.n > self.limite_fb:
            confirmar = messagebox.askyesno(
                "Confirmación",
                f"Fuerza bruta es O(2^n) y con n={self.red.n} puede tardar mucho. ¿Continuar?",
            )
            if not confirmar:
                return

        if nombre == "Programación dinámica":
            messagebox.showinfo(
                "PD pendiente",
                "La programación dinámica aún no está implementada en esta versión. Deja este punto listo para que la implementes más adelante.",
            )
            return

        self.estado_label.set("Calculando...")
        self._ejecutar_en_hilo(fn, nombre)

    def _ejecutar_en_hilo(self, fn, nombre_alg):
        def tarea():
            inicio = time.perf_counter()
            try:
                resultado = fn(self.red)
            except Exception as exc:
                self.after(0, lambda: self._on_error(f"{nombre_alg}: {exc}"))
                return
            elapsed = time.perf_counter() - inicio
            self.after(0, lambda: self._mostrar_resultado(nombre_alg, resultado, elapsed))

        threading.Thread(target=tarea, daemon=True).start()

    def _on_error(self, msg):
        self.estado_label.set("Error")
        messagebox.showerror("Error de ejecución", msg)

    def _mostrar_resultado(self, nombre_alg, resultado, elapsed):
        self.estado_label.set(f"{nombre_alg} terminado en {elapsed:.4f}s")
        E, esf, ext = resultado
        if not isinstance(E, list):
            E = list(E)

        self.resultado_actual = {
            "algoritmo": nombre_alg,
            "E": E,
            "Esf": esf,
            "Ext": ext,
            "time": elapsed,
            "ext_inicial": extremismo(self.red),
        }

        ext_inicial = extremismo(self.red)
        reduccion = 0.0 if ext_inicial == 0 else ((ext_inicial - ext) / ext_inicial) * 100.0
        aplicable = es_aplicable(self.red, E)
        total_moderados = sum(E)

        resumen = (
            f"Algoritmo: {nombre_alg}\n"
            f"Ext inicial: {ext_inicial:.6f}\n"
            f"Ext resultante: {ext:.6f}\n"
            f"Reducción: {reduccion:.2f}%\n"
            f"Esfuerzo: {esf} / R_max={self.red.r_max}\n"
            f"Agentes moderados: {total_moderados}\n"
            f"Aplicable: {'Sí' if aplicable else 'No'}"
        )
        self.resumen_var.set(resumen)

        verif = verificar_estrategia(self.red, E, esfuerzo_reportado=esf, ext_reportado=ext)
        self.detalle_text.delete("1.0", "end")
        self.detalle_text.insert("1.0", verif["texto"])

        self.resultado_tree.delete(*self.resultado_tree.get_children())
        for i, (agente, e) in enumerate(zip(self.red.agentes, E)):
            costo = costo_agente(agente)
            aporte = aporte_agente(agente)
            self.resultado_tree.insert("", "end", values=(i, e, costo, aporte, "Sí" if e == 1 else "No"))

        for child in self.resultado_tree.get_children():
            vals = self.resultado_tree.item(child, "values")
            if vals and vals[1] == 1:
                self.resultado_tree.item(child, tags=("moderado",))
        self.resultado_tree.tag_configure("moderado", background="#d9f7be")

    def comparar_con_optimo(self):
        if self.red is None or self.resultado_actual is None:
            messagebox.showwarning("Sin resultado", "Primero ejecuta un algoritmo sobre una red.")
            return

        try:
            _, _, ext_pd = modexPD(self.red)
        except NotImplementedError:
            messagebox.showinfo(
                "PD no implementada",
                "La programación dinámica sigue sin implementarse. Este botón queda preparado para cuando la implementes.",
            )
            return

        ext_alg = self.resultado_actual["Ext"]
        brecha = comparar_optimalidad(ext_alg, ext_pd)
        info = (
            f"Ext algoritmo: {ext_alg:.6f}\n"
            f"Ext óptimo (PD): {ext_pd:.6f}\n"
            f"Brecha: {brecha:.2f}%\n"
            f"¿Óptimo?: {'Sí' if abs(ext_alg - ext_pd) < 1e-9 else 'No'}"
        )
        messagebox.showinfo("Comparación con óptimo", info)

    def guardar_entrada_actual(self):
        if self.red is None:
            messagebox.showwarning("Sin entrada", "Primero carga una red social.")
            return
        ruta = filedialog.asksaveasfilename(defaultextension=".txt", title="Guardar entrada ModEx")
        if not ruta:
            return
        guardar_entrada(self.red, ruta)
        messagebox.showinfo("Guardado", f"Entrada guardada en: {ruta}")

    def guardar_salida_actual(self):
        if self.red is None or self.resultado_actual is None:
            messagebox.showwarning("Sin resultado", "Primero ejecuta un algoritmo.")
            return
        ruta = filedialog.asksaveasfilename(defaultextension=".txt", title="Guardar salida ModEx")
        if not ruta:
            return
        guardar_salida(ruta, self.resultado_actual["Ext"], self.resultado_actual["Esf"], self.resultado_actual["E"])
        messagebox.showinfo("Guardado", f"Salida guardada en: {ruta}")

    def cargar_salida_verificar(self):
        if self.red is None:
            messagebox.showwarning("Sin entrada", "Primero carga una red social.")
            return
        ruta = filedialog.askopenfilename(
            title="Abrir archivo de salida",
            filetypes=[("Text", "*.txt"), ("Todos", "*.*")],
        )
        if not ruta:
            return
        try:
            ext, esf, estrategia = leer_salida(ruta)
            ver = verificar_estrategia(self.red, estrategia, esfuerzo_reportado=esf, ext_reportado=ext)
            messagebox.showinfo("Verificación", ver["texto"])
        except Exception as exc:
            messagebox.showerror("Error", str(exc))

    def comparar_todos(self):
        if self.red is None:
            messagebox.showwarning("Sin entrada", "Primero carga una red social.")
            return

        self.comparacion_tree.delete(*self.comparacion_tree.get_children())
        filas = []

        for nombre, fn in [("Fuerza bruta", modexFB), ("Voraz", modexV)]:
            if nombre == "Fuerza bruta" and self.red.n > self.limite_fb:
                continue
            inicio = time.perf_counter()
            try:
                E, es, ext = fn(self.red)
            except NotImplementedError:
                continue
            elapsed = time.perf_counter() - inicio
            apl = es_aplicable(self.red, E)
            filas.append((nombre, f"{ext:.6f}", es, f"{elapsed:.4f}", "Sí" if apl else "No", "-"))

        try:
            _, _, ext_pd = modexPD(self.red)
        except NotImplementedError:
            filas.append(("Programación dinámica", "No implementada", "-", "-", "-", "-"))
        else:
            filas.append(("Programación dinámica", f"{ext_pd:.6f}", "-", "-", "-", "-"))

        for row in filas:
            self.comparacion_tree.insert("", "end", values=row)

    def exportar_tabla_comparacion(self):
        if not self.comparacion_tree.get_children():
            messagebox.showwarning("Sin datos", "Primero compara los algoritmos.")
            return
        ruta = filedialog.asksaveasfilename(defaultextension=".csv", title="Guardar CSV de comparación")
        if not ruta:
            return
        filas = [self.comparacion_tree.item(child, "values") for child in self.comparacion_tree.get_children()]
        guardar_csv(ruta, ["algoritmo", "ext", "esfuerzo", "tiempo", "aplicable", "optimo"], filas)
        messagebox.showinfo("CSV", f"CSV exportado a {ruta}")

    def generar_caso(self):
        try:
            n = int(self.generador_vars["n"].get())
            opinion_min = float(self.generador_vars["opin_min"].get())
            opinion_max = float(self.generador_vars["opin_max"].get())
            receptividad_min = float(self.generador_vars["recep_min"].get())
            receptividad_max = float(self.generador_vars["recep_max"].get())
            influencia_min = float(self.generador_vars["infl_min"].get())
            influencia_max = float(self.generador_vars["infl_max"].get())
            rmax = int(self.generador_vars["rmax"].get())
            seed = int(self.generador_vars["seed"].get())
        except ValueError as exc:
            messagebox.showerror("Datos inválidos", f"Revisa los campos numéricos.\n{exc}")
            return

        tipo = self.tipo_var.get()
        if n <= 0:
            messagebox.showerror("Error", "n debe ser un entero positivo.")
            return
        if not (0.0 <= receptividad_min <= 1.0 and 0.0 <= receptividad_max <= 1.0):
            messagebox.showerror("Error", "La receptividad debe estar en [0, 1].")
            return
        if not (1.0 <= influencia_min <= 3.0 and 1.0 <= influencia_max <= 3.0):
            messagebox.showerror("Error", "La influencia debe estar en [1, 3].")
            return
        if rmax < 0:
            messagebox.showerror("Error", "R_max no puede ser negativo.")
            return

        red = generar_caso(
            tipo=tipo,
            n=n,
            opinion_min=opinion_min,
            opinion_max=opinion_max,
            receptividad_min=receptividad_min,
            receptividad_max=receptividad_max,
            influencia_min=influencia_min,
            influencia_max=influencia_max,
            r_max=rmax,
            seed=seed,
        )
        self.red = red
        self._mostrar_entrada()
        self.generador_info.set(f"Caso generado: tipo={tipo}, n={n}, R_max={rmax}, semilla={seed}.")
        messagebox.showinfo("Caso generado", "Se ha generado la red.")

    def guardar_caso_actual(self):
        if self.red is None:
            messagebox.showwarning("Sin entrada", "Genera o carga una red antes de guardar.")
            return
        ruta = filedialog.asksaveasfilename(defaultextension=".txt", title="Guardar caso generado")
        if not ruta:
            return
        guardar_entrada(self.red, ruta)
        with open(ruta, "a", encoding="utf-8") as f:
            f.write("\n# Caso generado por la interfaz ModEx\n")
        messagebox.showinfo("Guardado", f"Caso guardado en {ruta}")

    def cargar_caso_generado(self):
        ruta = filedialog.askopenfilename(
            title="Abrir caso generado",
            filetypes=[("Archivos de texto", "*.txt"), ("Todos", "*.*")],
        )
        if not ruta:
            return
        try:
            self.red = cargar_red_social(ruta)
            self._mostrar_entrada()
            self._limpiar_resultado()
            self.generador_info.set(f"Caso cargado desde: {ruta}")
        except Exception as exc:
            messagebox.showerror("Error", str(exc))

    def ejecutar_bateria(self):
        if not os.path.isdir(CARPETA_PRUEBAS):
            messagebox.showwarning("Sin batería", f"No existe: {CARPETA_PRUEBAS}")
            return

        self.bateria_tree.delete(*self.bateria_tree.get_children())
        fb_limite = int(self.umbral_fb.get())

        for i in range(1, 36):
            ruta = os.path.join(CARPETA_PRUEBAS, f"Prueba{i}.txt")
            if not os.path.exists(ruta):
                continue
            try:
                red = cargar_red_social(ruta)
            except Exception:
                continue

            inicio = time.perf_counter()
            _, _, ext_v = modexV(red)
            t_v = time.perf_counter() - inicio

            try:
                _, _, ext_pd = modexPD(red)
            except NotImplementedError:
                ext_pd = float("nan")
                t_pd = float("nan")
            else:
                t_pd = 0.0

            brecha = "-"
            if not (ext_pd != ext_pd):
                brecha = f"{((ext_v - ext_pd) / ext_pd) * 100.0:.2f}%" if ext_pd != 0 else "0.00%"

            self.bateria_tree.insert(
                "",
                "end",
                values=(red.n, red.r_max, f"{ext_v:.6f}", "PD" if str(ext_pd) == "nan" else f"{ext_pd:.6f}", f"{t_v:.4f}", "-" if str(t_pd) == "nan" else f"{t_pd:.4f}", brecha),
            )

        messagebox.showinfo("Batería", "Se ejecutó la batería de 35 pruebas.")

    def exportar_bateria_csv(self):
        if not self.bateria_tree.get_children():
            messagebox.showwarning("Sin datos", "Primero ejecuta la batería.")
            return
        ruta = filedialog.asksaveasfilename(defaultextension=".csv", title="Guardar CSV de batería")
        if not ruta:
            return
        filas = [self.bateria_tree.item(child, "values") for child in self.bateria_tree.get_children()]
        guardar_csv(ruta, ["n", "r_max", "ext_v", "ext_pd", "t_v", "t_pd", "brecha"], filas)
        messagebox.showinfo("CSV", f"CSV exportado en {ruta}")


def main():
    app = ModExApp()
    app.mainloop()


if __name__ == "__main__":
    main()

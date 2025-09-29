import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import json
import requests
import config
from supabase_client import SupabaseClient
from config import USERS

class SupabaseGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Supabase API Client - Sistema de Ventas")
        self.root.geometry("1200x800")
        
        # Cliente de Supabase
        self.client = SupabaseClient()
        self.current_user = None
        
        # Crear interfaz
        self.setup_ui()
        
    def setup_ui(self):
        """Configurar la interfaz de usuario"""
        # Frame principal
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configurar grid weights
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        main_frame.rowconfigure(1, weight=1)
        
        # Frame de login
        self.setup_login_frame(main_frame)
        
        # Notebook para pestañas
        self.notebook = ttk.Notebook(main_frame)
        self.notebook.grid(row=1, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(10, 0))
        
        # Crear pestañas
        self.setup_config_tab()
        self.setup_reports_tab()
        self.setup_authorization_tab()
        self.setup_advanced_tab()
        self.setup_admin_tab()
        
        # Deshabilitar pestañas inicialmente (excepto configuración)
        self.toggle_tabs(False)
        
    def setup_login_frame(self, parent):
        """Configurar frame de login"""
        login_frame = ttk.LabelFrame(parent, text="Autenticación", padding="10")
        login_frame.grid(row=0, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))
        
        # Usuario dropdown
        ttk.Label(login_frame, text="Usuario:").grid(row=0, column=0, sticky=tk.W, padx=(0, 5))
        self.user_var = tk.StringVar()
        user_combo = ttk.Combobox(login_frame, textvariable=self.user_var, values=list(USERS.keys()), state="readonly")
        user_combo.grid(row=0, column=1, sticky=(tk.W, tk.E), padx=(0, 10))
        user_combo.set(list(USERS.keys())[0])
        
        # Botón login
        self.login_btn = ttk.Button(login_frame, text="Iniciar Sesión", command=self.login)
        self.login_btn.grid(row=0, column=2, padx=(0, 10))
        
        # Botón logout
        self.logout_btn = ttk.Button(login_frame, text="Cerrar Sesión", command=self.logout, state="disabled")
        self.logout_btn.grid(row=0, column=3)
        
        # Estado de login
        self.status_label = ttk.Label(login_frame, text="No autenticado", foreground="red")
        self.status_label.grid(row=0, column=4, padx=(10, 0))
        
        login_frame.columnconfigure(1, weight=1)
        
    def setup_config_tab(self):
        """Configurar pestaña de configuración"""
        config_frame = ttk.Frame(self.notebook)
        self.notebook.add(config_frame, text="⚙️ Configuración")
        
        # Frame principal con scroll
        canvas = tk.Canvas(config_frame)
        scrollbar = ttk.Scrollbar(config_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Instrucciones
        instructions_frame = ttk.LabelFrame(scrollable_frame, text="Instrucciones", padding="10")
        instructions_frame.pack(fill=tk.X, padx=10, pady=10)
        
        instructions_text = """
🔧 Configuración de Credenciales de Supabase

1. Obtén tus credenciales desde tu proyecto en supabase.com
2. Ve a Settings > API en tu dashboard de Supabase
3. Copia la URL del proyecto y las API Keys
4. Pega las credenciales en los campos de abajo
5. Haz clic en "Guardar Configuración"
6. Las credenciales se aplicarán inmediatamente

⚠️ Importante: 
- La Service Role Key es opcional (solo para funciones admin)
- Nunca compartas estas credenciales públicamente
- Los valores por defecto son de ejemplo, usa los tuyos propios
        """
        
        ttk.Label(instructions_frame, text=instructions_text, justify=tk.LEFT).pack()
        
        # Frame de configuración
        cred_frame = ttk.LabelFrame(scrollable_frame, text="Credenciales de Supabase", padding="10")
        cred_frame.pack(fill=tk.X, padx=10, pady=10)
        
        # URL de Supabase
        ttk.Label(cred_frame, text="URL del Proyecto Supabase:").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.supabase_url_var = tk.StringVar(value=config.SUPABASE_URL)
        url_entry = ttk.Entry(cred_frame, textvariable=self.supabase_url_var, width=70)
        url_entry.grid(row=0, column=1, sticky=(tk.W, tk.E), padx=(10, 0), pady=5)
        
        # API Key (anon/public)
        ttk.Label(cred_frame, text="API Key (anon/public):").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.api_key_var = tk.StringVar(value=config.SUPABASE_KEY)
        api_entry = ttk.Entry(cred_frame, textvariable=self.api_key_var, width=70, show="*")
        api_entry.grid(row=1, column=1, sticky=(tk.W, tk.E), padx=(10, 0), pady=5)
        
        # Botón para mostrar/ocultar API Key
        self.show_api_key = tk.BooleanVar()
        api_check = ttk.Checkbutton(cred_frame, text="Mostrar", variable=self.show_api_key, 
                                   command=lambda: api_entry.config(show="" if self.show_api_key.get() else "*"))
        api_check.grid(row=1, column=2, padx=(5, 0), pady=5)
        
        # Service Role Key
        ttk.Label(cred_frame, text="Service Role Key (Admin):").grid(row=2, column=0, sticky=tk.W, pady=5)
        self.service_key_var = tk.StringVar(value=config.SERVICE_ROLE_KEY)
        service_entry = ttk.Entry(cred_frame, textvariable=self.service_key_var, width=70, show="*")
        service_entry.grid(row=2, column=1, sticky=(tk.W, tk.E), padx=(10, 0), pady=5)
        
        # Botón para mostrar/ocultar Service Key
        self.show_service_key = tk.BooleanVar()
        service_check = ttk.Checkbutton(cred_frame, text="Mostrar", variable=self.show_service_key,
                                       command=lambda: service_entry.config(show="" if self.show_service_key.get() else "*"))
        service_check.grid(row=2, column=2, padx=(5, 0), pady=5)
        
        # Botones de acción
        button_frame = ttk.Frame(cred_frame)
        button_frame.grid(row=3, column=0, columnspan=3, pady=20)
        
        ttk.Button(button_frame, text="💾 Guardar Configuración", command=self.save_config).pack(side=tk.LEFT, padx=(0, 10))
        ttk.Button(button_frame, text="🔄 Restaurar Valores por Defecto", command=self.restore_defaults).pack(side=tk.LEFT, padx=(0, 10))
        ttk.Button(button_frame, text="🧪 Probar Conexión", command=self.test_connection).pack(side=tk.LEFT)
        
        # Estado de configuración
        self.config_status_label = ttk.Label(cred_frame, text="Configuración actual cargada", foreground="blue")
        self.config_status_label.grid(row=4, column=0, columnspan=3, pady=10)
        
        # Configurar grid weights
        cred_frame.columnconfigure(1, weight=1)
        
        # Frame de usuarios personalizados
        users_frame = ttk.LabelFrame(scrollable_frame, text="Usuarios de Prueba (Opcional)", padding="10")
        users_frame.pack(fill=tk.X, padx=10, pady=10)
        
        # Agregar usuario personalizado
        ttk.Label(users_frame, text="Email:").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.custom_email_var = tk.StringVar()
        ttk.Entry(users_frame, textvariable=self.custom_email_var, width=30).grid(row=0, column=1, padx=(5, 10), pady=5)
        
        ttk.Label(users_frame, text="Password:").grid(row=0, column=2, sticky=tk.W, pady=5)
        self.custom_password_var = tk.StringVar()
        ttk.Entry(users_frame, textvariable=self.custom_password_var, width=20, show="*").grid(row=0, column=3, padx=(5, 10), pady=5)
        
        ttk.Button(users_frame, text="Agregar Usuario", command=self.add_custom_user).grid(row=0, column=4, pady=5)
        
        # Lista de usuarios personalizados
        self.custom_users_listbox = tk.Listbox(users_frame, height=4)
        self.custom_users_listbox.grid(row=1, column=0, columnspan=5, sticky=(tk.W, tk.E), pady=10)
        
        users_frame.columnconfigure(1, weight=1)
        users_frame.columnconfigure(3, weight=1)
        
        # Configurar canvas
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
    def setup_reports_tab(self):
        """Configurar pestaña de reportes"""
        reports_frame = ttk.Frame(self.notebook)
        self.notebook.add(reports_frame, text="Reportes")
        
        # Frame de botones
        btn_frame = ttk.Frame(reports_frame)
        btn_frame.pack(fill=tk.X, padx=10, pady=10)
        
        ttk.Button(btn_frame, text="Sales Fact View", command=self.get_sales_fact).pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(btn_frame, text="Sales by Category", command=self.get_sales_by_category).pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(btn_frame, text="Sales by Country (CR)", command=self.get_sales_by_country).pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(btn_frame, text="Top Products (30d)", command=self.get_top_products).pack(side=tk.LEFT, padx=(0, 5))
        
        # Área de resultados
        self.reports_text = scrolledtext.ScrolledText(reports_frame, height=35, wrap=tk.WORD)
        self.reports_text.pack(fill=tk.BOTH, expand=True, padx=10, pady=(0, 10))
        
    def setup_authorization_tab(self):
        """Configurar pestaña de autorización"""
        auth_frame = ttk.Frame(self.notebook)
        self.notebook.add(auth_frame, text="Autorización")
        
        # Frame de botones
        btn_frame = ttk.Frame(auth_frame)
        btn_frame.pack(fill=tk.X, padx=10, pady=10)
        
        ttk.Button(btn_frame, text="Mis Países Permitidos", command=self.get_allowed_countries).pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(btn_frame, text="Mis Categorías Permitidas", command=self.get_allowed_categories).pack(side=tk.LEFT, padx=(0, 5))
        
        # Área de resultados
        self.auth_text = scrolledtext.ScrolledText(auth_frame, height=35, wrap=tk.WORD)
        self.auth_text.pack(fill=tk.BOTH, expand=True, padx=10, pady=(0, 10))
        
    def setup_advanced_tab(self):
        """Configurar pestaña de consultas avanzadas"""
        advanced_frame = ttk.Frame(self.notebook)
        self.notebook.add(advanced_frame, text="Consultas Avanzadas")
        
        # Frame de controles
        controls_frame = ttk.Frame(advanced_frame)
        controls_frame.pack(fill=tk.X, padx=10, pady=10)
        
        # Productos por precio
        price_frame = ttk.LabelFrame(controls_frame, text="Productos por Rango de Precio", padding="5")
        price_frame.pack(fill=tk.X, pady=(0, 10))
        
        ttk.Label(price_frame, text="Precio Mín:").grid(row=0, column=0, sticky=tk.W)
        self.min_price_var = tk.StringVar(value="100")
        ttk.Entry(price_frame, textvariable=self.min_price_var, width=10).grid(row=0, column=1, padx=(5, 10))
        
        ttk.Label(price_frame, text="Precio Máx:").grid(row=0, column=2, sticky=tk.W)
        self.max_price_var = tk.StringVar(value="1000")
        ttk.Entry(price_frame, textvariable=self.max_price_var, width=10).grid(row=0, column=3, padx=(5, 10))
        
        ttk.Button(price_frame, text="Buscar Productos", command=self.search_products_by_price).grid(row=0, column=4, padx=(10, 0))
        
        # Búsqueda de clientes
        customer_frame = ttk.LabelFrame(controls_frame, text="Búsqueda de Clientes", padding="5")
        customer_frame.pack(fill=tk.X, pady=(0, 10))
        
        ttk.Label(customer_frame, text="Nombre:").grid(row=0, column=0, sticky=tk.W)
        self.customer_name_var = tk.StringVar(value="María")
        ttk.Entry(customer_frame, textvariable=self.customer_name_var, width=20).grid(row=0, column=1, padx=(5, 10))
        
        ttk.Button(customer_frame, text="Buscar Clientes", command=self.search_customers).grid(row=0, column=2, padx=(10, 0))
        
        # Otras consultas
        other_frame = ttk.LabelFrame(controls_frame, text="Otras Consultas", padding="5")
        other_frame.pack(fill=tk.X)
        
        ttk.Button(other_frame, text="Facturas Este Mes", command=self.get_invoices_this_month).pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(other_frame, text="Líneas Alto Valor (>1000)", command=self.get_high_value_lines).pack(side=tk.LEFT, padx=(0, 5))
        
        # Área de resultados
        self.advanced_text = scrolledtext.ScrolledText(advanced_frame, height=25, wrap=tk.WORD)
        self.advanced_text.pack(fill=tk.BOTH, expand=True, padx=10, pady=(0, 10))
        
    def setup_admin_tab(self):
        """Configurar pestaña de administración"""
        admin_frame = ttk.Frame(self.notebook)
        self.notebook.add(admin_frame, text="Administración")
        
        # Frame de controles
        controls_frame = ttk.Frame(admin_frame)
        controls_frame.pack(fill=tk.X, padx=10, pady=10)
        
        # Gestión de usuarios
        user_frame = ttk.LabelFrame(controls_frame, text="Gestión de Usuarios", padding="5")
        user_frame.pack(fill=tk.X, pady=(0, 10))
        
        ttk.Button(user_frame, text="Ver Todos los Usuarios", command=self.admin_get_users).pack(side=tk.LEFT, padx=(0, 5))
        
        # Crear usuario
        create_frame = ttk.LabelFrame(controls_frame, text="Crear Usuario", padding="5")
        create_frame.pack(fill=tk.X, pady=(0, 10))
        
        ttk.Label(create_frame, text="Email:").grid(row=0, column=0, sticky=tk.W)
        self.new_email_var = tk.StringVar()
        ttk.Entry(create_frame, textvariable=self.new_email_var, width=25).grid(row=0, column=1, padx=(5, 10))
        
        ttk.Label(create_frame, text="Password:").grid(row=0, column=2, sticky=tk.W)
        self.new_password_var = tk.StringVar(value="password123")
        ttk.Entry(create_frame, textvariable=self.new_password_var, width=15, show="*").grid(row=0, column=3, padx=(5, 10))
        
        ttk.Button(create_frame, text="Crear Usuario", command=self.admin_create_user).grid(row=0, column=4, padx=(10, 0))
        
        # Asignar permisos
        perm_frame = ttk.LabelFrame(controls_frame, text="Asignar Permisos", padding="5")
        perm_frame.pack(fill=tk.X)
        
        ttk.Label(perm_frame, text="User ID:").grid(row=0, column=0, sticky=tk.W)
        self.perm_user_id_var = tk.StringVar()
        ttk.Entry(perm_frame, textvariable=self.perm_user_id_var, width=35).grid(row=0, column=1, padx=(5, 10))
        
        ttk.Label(perm_frame, text="País:").grid(row=0, column=2, sticky=tk.W)
        self.country_var = tk.StringVar(value="CR")
        ttk.Entry(perm_frame, textvariable=self.country_var, width=5).grid(row=0, column=3, padx=(5, 10))
        
        ttk.Button(perm_frame, text="Asignar País", command=self.admin_assign_country).grid(row=0, column=4, padx=(5, 0))
        
        ttk.Label(perm_frame, text="Cat ID:").grid(row=1, column=2, sticky=tk.W, pady=(5, 0))
        self.category_var = tk.StringVar(value="1")
        ttk.Entry(perm_frame, textvariable=self.category_var, width=5).grid(row=1, column=3, padx=(5, 10), pady=(5, 0))
        
        ttk.Button(perm_frame, text="Asignar Categoría", command=self.admin_assign_category).grid(row=1, column=4, padx=(5, 0), pady=(5, 0))
        
        # Área de resultados
        self.admin_text = scrolledtext.ScrolledText(admin_frame, height=20, wrap=tk.WORD)
        self.admin_text.pack(fill=tk.BOTH, expand=True, padx=10, pady=(0, 10))
        
    def login(self):
        """Iniciar sesión"""
        selected_user = self.user_var.get()
        if selected_user in USERS:
            user_data = USERS[selected_user]
            result = self.client.login(user_data["email"], user_data["password"])
            
            if result["success"]:
                self.current_user = selected_user
                self.status_label.config(text=f"Autenticado como: {selected_user}", foreground="green")
                self.login_btn.config(state="disabled")
                self.logout_btn.config(state="normal")
                self.toggle_tabs(True)
                messagebox.showinfo("Éxito", f"Conectado como {user_data['description']}")
            else:
                messagebox.showerror("Error", result["message"])
        
    def logout(self):
        """Cerrar sesión"""
        self.client.jwt_token = None
        self.client.user_id = None
        self.current_user = None
        self.status_label.config(text="No autenticado", foreground="red")
        self.login_btn.config(state="normal")
        self.logout_btn.config(state="disabled")
        self.toggle_tabs(False)
        
        # Limpiar todas las áreas de texto
        self.reports_text.delete(1.0, tk.END)
        self.auth_text.delete(1.0, tk.END)
        self.advanced_text.delete(1.0, tk.END)
        self.admin_text.delete(1.0, tk.END)
        
    def toggle_tabs(self, enable):
        """Habilitar/deshabilitar pestañas (excepto configuración)"""
        state = "normal" if enable else "disabled"
        # Empezar desde 1 para saltar la pestaña de configuración (índice 0)
        for i in range(1, self.notebook.index("end")):
            self.notebook.tab(i, state=state)
            
    def display_result(self, text_widget, result, title="Resultado"):
        """Mostrar resultado en el widget de texto"""
        text_widget.delete(1.0, tk.END)
        text_widget.insert(tk.END, f"=== {title} ===\n\n")
        
        if result["success"]:
            if "data" in result:
                # Formatear JSON de manera legible
                formatted_data = json.dumps(result["data"], indent=2, ensure_ascii=False)
                text_widget.insert(tk.END, formatted_data)
            else:
                text_widget.insert(tk.END, "Operación exitosa")
        else:
            text_widget.insert(tk.END, f"Error: {result.get('error', 'Error desconocido')}")
            if "status" in result:
                text_widget.insert(tk.END, f"\nCódigo de estado: {result['status']}")
                
    # Métodos para reportes
    def get_sales_fact(self):
        result = self.client.get_sales_fact()
        self.display_result(self.reports_text, result, "Sales Fact View")
        
    def get_sales_by_category(self):
        result = self.client.get_sales_by_category()
        self.display_result(self.reports_text, result, "Sales by Category")
        
    def get_sales_by_country(self):
        result = self.client.get_sales_by_country()
        self.display_result(self.reports_text, result, "Sales by Country (CR)")
        
    def get_top_products(self):
        result = self.client.get_top_products()
        self.display_result(self.reports_text, result, "Top Products (30 días)")
        
    # Métodos para autorización
    def get_allowed_countries(self):
        result = self.client.get_my_allowed_countries()
        self.display_result(self.auth_text, result, "Mis Países Permitidos")
        
    def get_allowed_categories(self):
        result = self.client.get_my_allowed_categories()
        self.display_result(self.auth_text, result, "Mis Categorías Permitidas")
        
    # Métodos para consultas avanzadas
    def search_products_by_price(self):
        try:
            min_price = float(self.min_price_var.get())
            max_price = float(self.max_price_var.get())
            result = self.client.get_products_by_price_range(min_price, max_price)
            self.display_result(self.advanced_text, result, f"Productos entre ${min_price} y ${max_price}")
        except ValueError:
            messagebox.showerror("Error", "Por favor ingrese precios válidos")
            
    def search_customers(self):
        name = self.customer_name_var.get().strip()
        if name:
            result = self.client.search_customers(name)
            self.display_result(self.advanced_text, result, f"Clientes con nombre '{name}'")
        else:
            messagebox.showerror("Error", "Por favor ingrese un nombre para buscar")
            
    def get_invoices_this_month(self):
        result = self.client.get_invoices_this_month()
        self.display_result(self.advanced_text, result, "Facturas Este Mes")
        
    def get_high_value_lines(self):
        result = self.client.get_high_value_invoice_lines()
        self.display_result(self.advanced_text, result, "Líneas de Factura Alto Valor (>$1000)")
        
    # Métodos administrativos
    def admin_get_users(self):
        result = self.client.admin_get_all_users()
        self.display_result(self.admin_text, result, "Todos los Usuarios (Admin)")
        
    def admin_create_user(self):
        email = self.new_email_var.get().strip()
        password = self.new_password_var.get().strip()
        
        if email and password:
            result = self.client.admin_create_user(email, password)
            self.display_result(self.admin_text, result, f"Crear Usuario: {email}")
            if result["success"]:
                self.new_email_var.set("")
                messagebox.showinfo("Éxito", f"Usuario {email} creado exitosamente")
        else:
            messagebox.showerror("Error", "Por favor complete email y password")
            
    def admin_assign_country(self):
        user_id = self.perm_user_id_var.get().strip()
        country = self.country_var.get().strip()
        
        if user_id and country:
            result = self.client.admin_assign_country_permission(user_id, country)
            self.display_result(self.admin_text, result, f"Asignar País {country} a Usuario {user_id[:8]}...")
            if result["success"]:
                messagebox.showinfo("Éxito", f"Permiso de país {country} asignado")
        else:
            messagebox.showerror("Error", "Por favor complete User ID y País")
            
    def admin_assign_category(self):
        user_id = self.perm_user_id_var.get().strip()
        category_id = self.category_var.get().strip()
        
        if user_id and category_id:
            try:
                cat_id = int(category_id)
                result = self.client.admin_assign_category_permission(user_id, cat_id)
                self.display_result(self.admin_text, result, f"Asignar Categoría {cat_id} a Usuario {user_id[:8]}...")
                if result["success"]:
                    messagebox.showinfo("Éxito", f"Permiso de categoría {cat_id} asignado")
            except ValueError:
                messagebox.showerror("Error", "ID de categoría debe ser un número")
        else:
            messagebox.showerror("Error", "Por favor complete User ID y Category ID")

    # Métodos para configuración
    def save_config(self):
        """Guardar configuración de credenciales"""
        try:
            # Validar URL
            url = self.supabase_url_var.get().strip()
            if not url.startswith("https://"):
                messagebox.showerror("Error", "La URL debe comenzar con https://")
                return
                
            # Validar API Key
            api_key = self.api_key_var.get().strip()
            if len(api_key) < 50:
                messagebox.showerror("Error", "La API Key parece muy corta")
                return
                
            # Validar Service Key (opcional)
            service_key = self.service_key_var.get().strip()
            if service_key and len(service_key) < 50:
                messagebox.showerror("Error", "La Service Role Key parece muy corta")
                return
            
            # Actualizar configuración
            config.SUPABASE_URL = url
            config.SUPABASE_KEY = api_key
            if service_key:
                config.SERVICE_ROLE_KEY = service_key
            
            # Actualizar cliente existente
            self.client.update_credentials()
            
            # Actualizar estado
            self.config_status_label.config(text="✅ Configuración guardada exitosamente", foreground="green")
            
            # Si hay una sesión activa, cerrarla para forzar re-autenticación
            if self.current_user:
                self.logout()
                messagebox.showinfo("Configuración Guardada", 
                                  "Configuración actualizada. Por favor, inicia sesión nuevamente.")
            else:
                messagebox.showinfo("Configuración Guardada", 
                                  "Configuración actualizada correctamente.")
                
        except Exception as e:
            messagebox.showerror("Error", f"Error guardando configuración: {str(e)}")
    
    def restore_defaults(self):
        """Restaurar valores por defecto"""
        self.supabase_url_var.set(config.DEFAULT_SUPABASE_URL)
        self.api_key_var.set(config.DEFAULT_SUPABASE_KEY)
        self.service_key_var.set(config.DEFAULT_SERVICE_ROLE_KEY)
        self.config_status_label.config(text="Valores por defecto restaurados", foreground="blue")
    
    def test_connection(self):
        """Probar conexión con las credenciales actuales"""
        try:
            # Guardar temporalmente credenciales actuales
            original_url = config.SUPABASE_URL
            original_key = config.SUPABASE_KEY
            
            # Usar credenciales del formulario
            config.SUPABASE_URL = self.supabase_url_var.get().strip()
            config.SUPABASE_KEY = self.api_key_var.get().strip()
            
            # Crear cliente temporal
            test_client = SupabaseClient()
            
            # Intentar una llamada simple (obtener users admin)
            url = f"{test_client.base_url}/auth/v1/admin/users"
            headers = {"apikey": test_client.api_key}
            
            response = requests.get(url, headers=headers, timeout=10)
            
            if response.status_code in [200, 401, 403]:
                # 200 = éxito, 401/403 = sin permisos pero conexión OK
                self.config_status_label.config(text="✅ Conexión exitosa", foreground="green")
                messagebox.showinfo("Prueba de Conexión", 
                                  "¡Conexión exitosa! Las credenciales son válidas.")
            else:
                self.config_status_label.config(text="❌ Error de conexión", foreground="red")
                messagebox.showerror("Error de Conexión", 
                                   f"Error {response.status_code}: {response.text[:200]}")
            
            # Restaurar credenciales originales
            config.SUPABASE_URL = original_url
            config.SUPABASE_KEY = original_key
            
        except Exception as e:
            self.config_status_label.config(text="❌ Error de conexión", foreground="red")
            messagebox.showerror("Error de Conexión", f"No se pudo conectar: {str(e)}")
            
            # Restaurar credenciales originales en caso de error
            config.SUPABASE_URL = original_url
            config.SUPABASE_KEY = original_key
    
    def add_custom_user(self):
        """Agregar usuario personalizado a la lista"""
        email = self.custom_email_var.get().strip()
        password = self.custom_password_var.get().strip()
        
        if email and password:
            user_info = f"{email} (password: {password})"
            self.custom_users_listbox.insert(tk.END, user_info)
            self.custom_email_var.set("")
            self.custom_password_var.set("")
            messagebox.showinfo("Usuario Agregado", 
                              f"Usuario {email} agregado a la lista.\n\n" +
                              "Nota: Para usar este usuario, debe existir en tu base de datos de Supabase.")
        else:
            messagebox.showerror("Error", "Por favor complete email y password")

def main():
    root = tk.Tk()
    app = SupabaseGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()
import requests
import json
import config

class SupabaseClient:
    def __init__(self):
        self.update_credentials()
        self.jwt_token = None
        self.user_id = None
        
    def update_credentials(self):
        """Actualizar credenciales desde config"""
        self.base_url = config.SUPABASE_URL
        self.api_key = config.SUPABASE_KEY
        self.service_key = config.SERVICE_ROLE_KEY
        
    def login(self, email, password):
        """Autenticar usuario y obtener JWT token"""
        url = f"{self.base_url}/auth/v1/token"
        headers = {
            "apikey": self.api_key,
            "Content-Type": "application/json"
        }
        data = {
            "email": email,
            "password": password
        }
        params = {"grant_type": "password"}
        
        try:
            response = requests.post(url, headers=headers, json=data, params=params)
            if response.status_code == 200:
                result = response.json()
                self.jwt_token = result.get("access_token")
                self.user_id = result.get("user", {}).get("id")
                return {"success": True, "message": "Login exitoso"}
            else:
                return {"success": False, "message": f"Error de login: {response.text}"}
        except Exception as e:
            return {"success": False, "message": f"Error de conexión: {str(e)}"}
    
    def get_headers(self, use_service_role=False):
        """Obtener headers para requests"""
        headers = {
            "apikey": self.service_key if use_service_role else self.api_key,
            "Content-Type": "application/json"
        }
        
        if not use_service_role and self.jwt_token:
            headers["Authorization"] = f"Bearer {self.jwt_token}"
        elif use_service_role:
            headers["Authorization"] = f"Bearer {self.service_key}"
            
        return headers
    
    def get_sales_fact(self):
        """Obtener datos de Sales Fact View"""
        url = f"{self.base_url}/rest/v1/v_sales_fact"
        params = {"select": "*"}
        response = requests.get(url, headers=self.get_headers(), params=params)
        return self._handle_response(response)
    
    def get_sales_by_category(self):
        """Obtener ventas por categoría"""
        url = f"{self.base_url}/rest/v1/v_sales_by_category"
        params = {"select": "*"}
        response = requests.get(url, headers=self.get_headers(), params=params)
        return self._handle_response(response)
    
    def get_sales_by_country(self, country_code="CR"):
        """Obtener ventas por país"""
        url = f"{self.base_url}/rest/v1/v_sales_by_country"
        params = {
            "select": "*",
            "country_code": f"eq.{country_code}"
        }
        response = requests.get(url, headers=self.get_headers(), params=params)
        return self._handle_response(response)
    
    def get_top_products(self, limit=10):
        """Obtener top productos (30 días)"""
        url = f"{self.base_url}/rest/v1/v_top_products_30d"
        params = {
            "select": "*",
            "limit": limit
        }
        response = requests.get(url, headers=self.get_headers(), params=params)
        return self._handle_response(response)
    
    def get_my_allowed_countries(self):
        """Obtener países permitidos para el usuario actual"""
        url = f"{self.base_url}/rest/v1/user_allowed_country"
        params = {
            "select": "*,countries(*)",
            "user_id": f"eq.{self.user_id}"
        }
        response = requests.get(url, headers=self.get_headers(), params=params)
        return self._handle_response(response)
    
    def get_my_allowed_categories(self):
        """Obtener categorías permitidas para el usuario actual"""
        url = f"{self.base_url}/rest/v1/user_allowed_category"
        params = {
            "select": "*,categories(*)",
            "user_id": f"eq.{self.user_id}"
        }
        response = requests.get(url, headers=self.get_headers(), params=params)
        return self._handle_response(response)
    
    def get_products_by_price_range(self, min_price=100, max_price=1000):
        """Obtener productos por rango de precio"""
        url = f"{self.base_url}/rest/v1/products"
        url += f"?select=*,categories(*)&unit_price=gte.{min_price}&unit_price=lte.{max_price}"
        response = requests.get(url, headers=self.get_headers())
        return self._handle_response(response)
    
    def get_invoices_this_month(self, start_date="2024-12-01"):
        """Obtener facturas del mes actual"""
        url = f"{self.base_url}/rest/v1/invoices"
        params = {
            "select": "*,customers(*)",
            "invoice_date": f"gte.{start_date}",
            "order": "invoice_date.desc"
        }
        response = requests.get(url, headers=self.get_headers(), params=params)
        return self._handle_response(response)
    
    def search_customers(self, name_filter):
        """Buscar clientes por nombre"""
        url = f"{self.base_url}/rest/v1/customers"
        params = {
            "select": "*",
            "name": f"ilike.*{name_filter}*"
        }
        response = requests.get(url, headers=self.get_headers(), params=params)
        return self._handle_response(response)
    
    def get_high_value_invoice_lines(self, min_total=1000):
        """Obtener líneas de factura con total alto"""
        url = f"{self.base_url}/rest/v1/invoice_lines"
        params = {
            "select": "*,products(*),invoices(customers(*))",
            "line_total": f"gte.{min_total}"
        }
        response = requests.get(url, headers=self.get_headers(), params=params)
        return self._handle_response(response)
    
    # Funciones administrativas
    def admin_get_all_users(self):
        """ADMIN - Obtener todos los usuarios"""
        url = f"{self.base_url}/auth/v1/admin/users"
        response = requests.get(url, headers=self.get_headers(use_service_role=True))
        return self._handle_response(response)
    
    def admin_create_user(self, email, password):
        """ADMIN - Crear nuevo usuario"""
        url = f"{self.base_url}/auth/v1/admin/users"
        data = {
            "email": email,
            "password": password,
            "email_confirm": True
        }
        response = requests.post(url, headers=self.get_headers(use_service_role=True), json=data)
        return self._handle_response(response)
    
    def admin_assign_country_permission(self, user_id, country_code):
        """ADMIN - Asignar permiso de país"""
        url = f"{self.base_url}/rest/v1/user_allowed_country"
        data = {
            "user_id": user_id,
            "country_code": country_code
        }
        response = requests.post(url, headers=self.get_headers(use_service_role=True), json=data)
        return self._handle_response(response)
    
    def admin_assign_category_permission(self, user_id, category_id):
        """ADMIN - Asignar permiso de categoría"""
        url = f"{self.base_url}/rest/v1/user_allowed_category"
        data = {
            "user_id": user_id,
            "category_id": category_id
        }
        response = requests.post(url, headers=self.get_headers(use_service_role=True), json=data)
        return self._handle_response(response)
    
    def _handle_response(self, response):
        """Manejar respuesta de la API"""
        try:
            if response.status_code == 200:
                return {"success": True, "data": response.json()}
            else:
                return {"success": False, "error": response.text, "status": response.status_code}
        except Exception as e:
            return {"success": False, "error": str(e)}
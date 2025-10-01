# Configuración de la aplicación - Valores por defecto
DEFAULT_SUPABASE_URL = "https://roliajiiiipsxdpanyrl.supabase.co"
DEFAULT_SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InJvbGlhamlpaWlwc3hkcGFueXJsIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTg4MzQ0MjgsImV4cCI6MjA3NDQxMDQyOH0.uw2hkNDCt36iYPFBUsUe1CrdiCuL7B5FPjt9ymB7cuQ"
DEFAULT_SERVICE_ROLE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InJvbGlhamlpaWlwc3hkcGFueXJsIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc1ODgzNDQyOCwiZXhwIjoyMDc0NDEwNDI4fQ.em8_9gu47jH7f8FqyjnybnCD41Y4y_vT33EMY-gMlQY"

# Variables que serán configuradas desde la UI
SUPABASE_URL = DEFAULT_SUPABASE_URL
SUPABASE_KEY = DEFAULT_SUPABASE_KEY
SERVICE_ROLE_KEY = DEFAULT_SERVICE_ROLE_KEY

# Usuarios predefinidos
USERS = {
    "Usuario 1 - brianramirez0farias@gmail.com": {
        "email": "brianramirez0farias@gmail.com",
        "password": "password123",
        "description": "Brian Ramirez"
    },
    "Usuario 2 - usertest@email.com": {
        "email": "usertest@email.com", 
        "password": "{Bases@1234}",
        "description": "User Test"
    },
    "Usuario 3 - adbyb.es@gmail.com": {
        "email": "adbyb.es@gmail.com",
        "password": "{Dep@2022}",
        "description": "ADBYB ES"
    }
}
"""
Script de prueba para verificar que la aplicación GUI funciona correctamente
"""
import sys
import os

def test_imports():
    """Probar que todas las importaciones funcionan"""
    try:
        import tkinter as tk
        print("✓ tkinter importado correctamente")
        
        from tkinter import ttk, messagebox, scrolledtext
        print("✓ tkinter widgets importados correctamente")
        
        import requests
        print("✓ requests importado correctamente")
        
        import json
        print("✓ json importado correctamente")
        
        # Importar módulos locales
        from config import SUPABASE_URL, USERS
        print("✓ config.py importado correctamente")
        
        from supabase_client import SupabaseClient
        print("✓ supabase_client.py importado correctamente")
        
        return True
        
    except ImportError as e:
        print(f"❌ Error de importación: {e}")
        return False

def test_config():
    """Probar que la configuración es válida"""
    try:
        from config import SUPABASE_URL, SUPABASE_KEY, USERS
        
        assert SUPABASE_URL.startswith("https://"), "URL de Supabase debe comenzar con https://"
        print("✓ URL de Supabase válida")
        
        assert len(SUPABASE_KEY) > 100, "API Key de Supabase debe ser una cadena larga"
        print("✓ API Key de Supabase válida")
        
        assert len(USERS) == 2, "Debe haber exactamente 2 usuarios configurados"
        print("✓ Usuarios configurados correctamente")
        
        for user_name, user_data in USERS.items():
            assert "email" in user_data and "password" in user_data
            print(f"✓ Usuario '{user_name}' configurado correctamente")
            
        return True
        
    except Exception as e:
        print(f"❌ Error en configuración: {e}")
        return False

def test_client_creation():
    """Probar que el cliente se puede crear"""
    try:
        from supabase_client import SupabaseClient
        
        client = SupabaseClient()
        assert client.base_url is not None
        assert client.api_key is not None
        print("✓ Cliente de Supabase creado correctamente")
        
        return True
        
    except Exception as e:
        print(f"❌ Error creando cliente: {e}")
        return False

def main():
    """Ejecutar todas las pruebas"""
    print("=== Pruebas de la Aplicación GUI de Supabase ===\n")
    
    tests = [
        ("Importaciones", test_imports),
        ("Configuración", test_config),
        ("Creación de Cliente", test_client_creation)
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"Ejecutando prueba: {test_name}")
        if test_func():
            passed += 1
            print(f"✅ {test_name} - PASÓ\n")
        else:
            print(f"❌ {test_name} - FALLÓ\n")
    
    print("=== Resumen ===")
    print(f"Pruebas pasadas: {passed}/{total}")
    
    if passed == total:
        print("🎉 ¡Todas las pruebas pasaron! La aplicación está lista para ejecutar.")
        print("\nPara ejecutar la aplicación GUI, usa:")
        print("python main.py")
    else:
        print("⚠️ Algunas pruebas fallaron. Revisa los errores arriba.")
        
    return passed == total

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
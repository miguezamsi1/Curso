# Instrucciones para crear superusuario

Para crear el superusuario de Django, ejecuta el siguiente comando:

```powershell
python manage.py createsuperuser
```

Te pedirá:
1. Username (nombre de usuario)
2. Email (correo electrónico)
3. Password (contraseña - debe tener al menos 8 caracteres)
4. Password (again) (confirmar contraseña)

Ejemplo:
```
Username: admin
Email address: admin@eea.gob.ec
Password: ********
Password (again): ********
Superuser created successfully.
```

Este usuario podrá acceder al panel de administración en:
http://localhost:8000/admin/

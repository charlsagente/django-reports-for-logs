# Reportes para logs
## Instalación
1. Crear una variable de entorno llamada SECRET_KEY y asignarle un valor como:
    
    ```
    2lg7tgdpdycq__j_g#rpil80s*!29_=+xvs(cr655c=3%k2%2h
    ```
    
2. Tener instalado python 2.7

3. Tener instalada la librería pip

4. Con el archivo requirements.txt escribir:
 
    ``` 
    pip install -r requirements.txt
    ```


5. Una vez teniendo el código, entrar a la carpeta y escribir:
    
    ```
    python manage.py migrate
    ```
    

6. Para ejecutar el servidor y que se pueda acceder desde internet, escribir:
    
    ```
    python manage.py runserver 0.0.0.0:8000
    ```
    
    
6. Si todo salió bien desde el navegador visitar:
    
    ```
    http://{ip}:8000/logs/
    ```
    
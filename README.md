## API para consulta de efemérides
Se provee una API con autenticación para la consulta de efemérides.
La aplicación se despliega sobre un servidor self-hosted _nginx_.


### Obtención del proyecto

Clonar el repositorio:

```git clone https://github.com/fabionazzi/deepvision-coding-challenge.git>```


### Cómo ejecutar el servicio

Ubicarse en el directorio donde se encuentra el proyecto clonado:  

```cd /deepvision-coding-challenge```

Para construir el proyecto, ejecutar el siguiente comando:  

```docker-compose build```

Para ejecutar la solución:  

```docker-compose up```


### Ejecución de la aplicación
1. Desde un navegador acceder a la documentación interactiva de la API en: 

```localhost/docs```

Antes de realizar cualquier operación sobre la API, es necesario
autenticarse utilizando las credenciales: 

```user: user1```  
```password: pass1```

2. Realizar una petición:

```GET localhost/login```

La API responderá con un token que se utilizará para auntenticar las siguientes peticiones.

3. Para consultar las efemérides de un determinado día, realizar una petición:

```GET localhost/efemerides```

que incluya la consulta en formato _YYYY:MM:DD_ y la cabecera HTTP un campo _x-access-token_ cuyo valor
será el token devuelto en el paso anterior.


### Casos de prueba

Para correr el _test suite_, ubicarse en el directorio clonado y ejecutar:

```py.test```
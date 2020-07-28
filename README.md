## API para consulta de efemérides
Se provee una API con autenticación para la consulta de efemérides.
La aplicación se despliega sobre un servidor self-hosted _nginx_.


### Obtención del proyecto

Clonar el repositorio

```git clone https://github.com/fabionazzi/deepvision-coding-challenge.git>```


### Cómo ejecutar el servicio

Ubicarse en el directorio donde se encuentra el proyecto clonado:  
```cd /deepvision-coding-challenge```

Para construir e proyecto, ejecutar el siguiente comando:  
```docker-compose build```

Para ejecutar la solución:  
```docker-compose up```


### Ejecución de la aplicación
1. Desde una aplicación (e.g Insomnia o Postman) realizar una solicitud:  
```GET localhost/login```

que incluya en la cabecera HTTP un campo __Authorization: Basic__ con las credenciales 

```user: user1```  
```password: pass1```

La API responderá con un token que se utilizará para auntenticar las siguientes peticiones.

2. Para consultar las efemérides de un determinado día, realizar una petición

```GET localhost/efemerides?day=YYYY:MM:DD```

que incluya en la cabecera HTTP un campo __x-access-token__ cuyo valor
será el token devuelto en el paso anterior.



### Casos de prueba

Para correr el _test suite_, ubicarse en el directorio clonado y ejecutar:

```py.test```
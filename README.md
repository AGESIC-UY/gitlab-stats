# GitLab Stats

Es un script para obtener estadísticas de acceso y descarga de los proyectos de GitLab. Con base en los archivos de log de GitLab, este script obtiene estadísticas de la cantidad de accesos y descargas en cada proyecto y 
envía un email con los resultados. 

Características técnicas:
Escrito en Python, se ejecuta en cualquier entorno que tenga Python instalado y con acceso a los logs de GitLab.
Licencia compatible con Software Público Uruguayo

---------------------------------

This Python script (`counter.py`) parses gitLab's log files and count those lines which define a download / clone / pull / fetch in a project.

The results are sent by email using the settings defined in `local_settings.py`.

## Dependencies

* Python 2.7.3+

## Testing

You can test the script starting a SMTP daemon with Python with any user on a port greater than 1024, example:

```
$ python -m smtpd -n -c DebuggingServer localhost:1025
```

After setting the correct values in `local_settings.py` you can execute the script `counter.py` in another shell and return to the python command with the running SMTP daemon to see the email generated.

--
Software Público Uruguayo.
Aníbal Pacheco, AGESIC
April 2014


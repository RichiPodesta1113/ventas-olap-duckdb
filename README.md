# Explorador OLAP de ventas con DuckDB

Demostración de procesamiento analítico sobre 120 000 pedidos sintéticos. DuckDB genera un cubo de 144 celdas con tres dimensiones (mes, región y categoría) y tres medidas aditivas (pedidos, unidades e ingresos en centavos). El explorador permite filtrar una dimensión (slice), combinar filtros (dice) y cambiar el nivel de agrupación (roll-up y desglose).

El navegador carga solo las celdas agregadas. La aplicación se publica como HTML estático en GitHub Pages. GitHub Actions genera el cubo, comprueba que sus totales coincidan con los pedidos originales, valida los agregados de cada dimensión y despliega el HTML.

Con Python 3.12, desde la raíz del proyecto:

```sh
python -m pip install -r requirements.txt
python build.py
```

Abra `site/index.html`. El SQL en `cube.sql` genera las transacciones de forma determinista con la versión fijada de DuckDB. Los datos son simulados y no describen ventas reales.

Para desplegar un fork, active GitHub Actions como origen en Settings → Pages y ejecute el workflow Build and deploy OLAP.

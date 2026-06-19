import os
import re

# Configuración
API_KEY = "AIzaSyBXefNIPS3AJO-2sMmkXe2DiOSl_yISBI0"
SEARCH_ENGINE_ID = "8188dd1a84ecb4c08"
CARPETA_NOTICIAS = "noticias"

# Bloque de imágenes que se inserta en cada artículo
BLOQUE_IMAGENES = '''
<!-- Galería de imágenes Google Custom Search -->
<div class="galeria-imagenes" style="margin:2rem 0;">
  <h3 style="font-family:'Playfair Display',serif;color:#0f3d26;margin-bottom:1rem;">Fotos del lugar</h3>
  <div id="galeria-grid" style="display:grid;grid-template-columns:repeat(auto-fill,minmax(200px,1fr));gap:0.75rem;"></div>
</div>
<script>
(function() {
  var titulo = document.querySelector('.art-title') || document.querySelector('h1');
  var query = titulo ? titulo.textContent.trim() : 'Santa Fe Argentina';
  query = query + ' Santa Fe Argentina';
  var url = 'https://www.googleapis.com/customsearch/v1?key=''' + API_KEY + '''&cx=''' + SEARCH_ENGINE_ID + '''&q=' + encodeURIComponent(query) + '&searchType=image&num=6&imgSize=medium&safe=active';
  fetch(url)
    .then(function(r){ return r.json(); })
    .then(function(data) {
      var grid = document.getElementById('galeria-grid');
      if (!data.items || !grid) return;
      data.items.forEach(function(item) {
        var a = document.createElement('a');
        a.href = item.image.contextLink;
        a.target = '_blank';
        a.rel = 'noopener';
        var img = document.createElement('img');
        img.src = item.link;
        img.alt = item.title;
        img.loading = 'lazy';
        img.style.cssText = 'width:100%;height:160px;object-fit:cover;border-radius:8px;display:block;';
        img.onerror = function(){ this.parentElement.parentElement.removeChild(this.parentElement); };
        a.appendChild(img);
        grid.appendChild(a);
      });
      if (grid.children.length === 0) {
        document.querySelector('.galeria-imagenes').style.display = 'none';
      }
    })
    .catch(function(){ 
      var g = document.querySelector('.galeria-imagenes');
      if (g) g.style.display = 'none';
    });
})();
</script>
'''

def ya_tiene_galeria(contenido):
    return 'galeria-imagenes' in contenido

def agregar_galeria(contenido):
    # Insertar antes del cierre del article o antes del </main> o antes del primer <h2> del body
    patrones = ['</article>', '</main>', '</body>']
    for patron in patrones:
        if patron in contenido:
            return contenido.replace(patron, BLOQUE_IMAGENES + patron, 1)
    return contenido

def procesar():
    if not os.path.exists(CARPETA_NOTICIAS):
        print(f"ERROR: No se encontró la carpeta '{CARPETA_NOTICIAS}'")
        return

    archivos = [f for f in os.listdir(CARPETA_NOTICIAS) if f.endswith('.html')]
    print(f"Encontrados {len(archivos)} archivos HTML\n")

    modificados = 0
    saltados = 0

    for archivo in sorted(archivos):
        ruta = os.path.join(CARPETA_NOTICIAS, archivo)
        with open(ruta, 'r', encoding='utf-8') as f:
            contenido = f.read()

        if ya_tiene_galeria(contenido):
            print(f"  SALTADO (ya tiene galería): {archivo}")
            saltados += 1
            continue

        nuevo = agregar_galeria(contenido)
        if nuevo != contenido:
            with open(ruta, 'w', encoding='utf-8') as f:
                f.write(nuevo)
            print(f"  ✓ Modificado: {archivo}")
            modificados += 1
        else:
            print(f"  ! No se encontró punto de inserción: {archivo}")

    print(f"\nListo: {modificados} modificados, {saltados} saltados.")

if __name__ == '__main__':
    procesar()

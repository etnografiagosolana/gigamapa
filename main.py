from PIL import Image
import os
import xml.etree.ElementTree as ET
import math

def generate_zoomify_tiles_and_xml(image_path, tile_size=256, output_dir='Zoomify'):
    # Abrir la imagen
    image = Image.open(image_path)
    image_width, image_height = image.size
    
    # Crear el directorio de salida si no existe
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Calcular el número de niveles de zoom
    max_zoom_level = int(math.log2(max(image_width, image_height) / tile_size))
    
    # Variables para generar ImageProperties.xml
    num_tiles_total = 0
    num_images = 1  # Solo una imagen
    version = '1.8'

    # Generar las carpetas de tiles por nivel de zoom
    for zoom_level in range(max_zoom_level + 1):
        zoom_dir = os.path.join(output_dir, str(zoom_level))
        if not os.path.exists(zoom_dir):
            os.makedirs(zoom_dir)

        # Determinar las dimensiones de la imagen para este nivel de zoom
        zoom_factor = 2 ** zoom_level
        zoom_width = math.ceil(image_width / zoom_factor)
        zoom_height = math.ceil(image_height / zoom_factor)

        # Dividir la imagen en tiles
        tile_number = 0
        num_tiles = 0
        for top in range(0, zoom_height, tile_size):
            for left in range(0, zoom_width, tile_size):
                # Definir el área del tile (recorte)
                right = min(left + tile_size, zoom_width)
                bottom = min(top + tile_size, zoom_height)
                
                # Recortar el tile de la imagen original y redimensionarlo según el zoom
                tile = image.crop((left * zoom_factor, top * zoom_factor, right * zoom_factor, bottom * zoom_factor))
                tile = tile.resize((right - left, bottom - top), Image.LANCZOS)

                # Guardar el tile en el directorio correspondiente
                tile.save(os.path.join(zoom_dir, f'{top // tile_size}_{left // tile_size}.jpg'))
                tile_number += 1
                num_tiles += 1
                num_tiles_total += 1

        # Imprimir información de los tiles generados para este nivel
        print(f"Generados {num_tiles} tiles en el nivel {zoom_level} (Total: {num_tiles_total})")

    # Crear el archivo ImageProperties.xml
    image_properties = ET.Element('IMAGE_PROPERTIES')
    image_properties.set('WIDTH', str(image_width))
    image_properties.set('HEIGHT', str(image_height))
    image_properties.set('NUMTILES', str(num_tiles_total))
    image_properties.set('NUMIMAGES', str(num_images))
    image_properties.set('VERSION', version)
    image_properties.set('TILESIZE', str(tile_size))

    # Crear el árbol XML y guardarlo
    tree = ET.ElementTree(image_properties)
    xml_output_path = os.path.join(output_dir, 'ImageProperties.xml')
    tree.write(xml_output_path)

    print(f"Archivo ImageProperties.xml guardado en '{xml_output_path}'")

# Ejemplo de uso
image_path = 'portada.jpg'  # Ruta a tu imagen
generate_zoomify_tiles_and_xml(image_path, tile_size=256)  # Ajusta el tamaño del tile según sea necesario

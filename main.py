from PIL import Image
import os
import xml.etree.ElementTree as ET

def generate_tiles_and_xml(image_path, tile_size=256, output_dir='tiles'):
    # Abrir la imagen
    image = Image.open(image_path)
    image_width, image_height = image.size
    
    # Crear el directorio de salida si no existe
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Contadores para los tiles
    tile_number = 0
    num_tiles = 0  # Para contar el total de tiles
    
    # Dividir la imagen en tiles
    for top in range(0, image_height, tile_size):
        for left in range(0, image_width, tile_size):
            # Definir el área del tile (recorte)
            right = min(left + tile_size, image_width)
            bottom = min(top + tile_size, image_height)
            
            # Recortar el tile de la imagen original
            tile = image.crop((left, top, right, bottom))
            
            # Guardar el tile en el directorio de salida
            tile.save(os.path.join(output_dir, f'tile_{tile_number}.png'))
            tile_number += 1
            num_tiles += 1

    # Crear el archivo XML ImageProperties.xml
    image_properties = ET.Element('IMAGE_PROPERTIES')
    image_properties.set('WIDTH', str(image_width))
    image_properties.set('HEIGHT', str(image_height))
    image_properties.set('NUMTILES', str(num_tiles))
    image_properties.set('NUMIMAGES', '1')
    image_properties.set('VERSION', '1.8')
    image_properties.set('TILESIZE', str(tile_size))

    # Crear el árbol XML y guardarlo
    tree = ET.ElementTree(image_properties)
    xml_output_path = os.path.join(output_dir, 'ImageProperties.xml')
    tree.write ('ImageProperties.xml') #(xml_output_path)

    print(f"Generados {num_tiles} tiles en el directorio '{output_dir}'")
    print(f"Archivo ImageProperties.xml guardado en '{xml_output_path}'")

# Ejemplo de uso
image_path = 'portada.jpg'  # Ruta a tu imagen
generate_tiles_and_xml(image_path, tile_size=256)  # Ajusta el tamaño del tile según sea necesario
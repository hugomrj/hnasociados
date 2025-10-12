# views.py
from django.http import HttpResponse
from django.views import View
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from io import BytesIO
from docx import Document

from copy import deepcopy
import re

from io import BytesIO
import zipfile
import os

from lxml import etree as ET
import random


W_NS = "http://schemas.openxmlformats.org/wordprocessingml/2006/main"
XML_NS = "http://www.w3.org/XML/1998/namespace"
NS = {"w": W_NS}


@method_decorator(csrf_exempt, name='dispatch')
class MemoView(View):
    def get(self, request):
        return HttpResponse('''

<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Procesador de Memos</title>

    <!-- Bootstrap 5 -->
    <link 
        href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css" 
        rel="stylesheet">

    <!-- MDBootstrap -->
    <link 
        href="https://cdnjs.cloudflare.com/ajax/libs/mdb-ui-kit/7.3.2/mdb.min.css" 
        rel="stylesheet">

</head>
<body class="bg-light">
    <div class="container mt-5">
        <div class="card shadow-3">
            <div class="card-body">
                <h3 class="text-center mb-4">📄 Procesador de Memos</h3>

                <form method="post" enctype="multipart/form-data">
                    <div class="mb-4">
                        <label class="form-label" for="archivo">Archivo .docx:</label>
                        <input class="form-control" type="file" id="archivo" name="archivo" accept=".docx" required>
                    </div>
                        


                    <div class="text-center">
                        <button class="btn btn-primary btn-rounded" type="submit">
                            <i class="fas fa-cogs me-2"></i>Procesar
                        </button>
                    </div>
                </form>
            </div>
        </div>
    </div>

    <!-- Bootstrap JS -->
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/js/bootstrap.bundle.min.js"></script>

    <!-- MDBootstrap JS -->
    <script src="https://cdnjs.cloudflare.com/ajax/libs/mdb-ui-kit/7.3.2/mdb.min.js"></script>

    <!-- Font Awesome (para íconos MDB) -->
    <script src="https://kit.fontawesome.com/a2d9d6c6f5.js" crossorigin="anonymous"></script>
</body>
</html>



        ''')

    def post(self, request):
        file = request.FILES.get("archivo")
        motivo = request.POST.get("motivo")

        if not file:
            return HttpResponse("Sube un archivo .docx", status=400)

        try:
            # Leer archivo original
            docx_bytes = file.read()


            # Aplicar reemplazos
            # docx_bytes = reemplazar_linea_memo(BytesIO(docx_bytes), cambios)


            texto_extraido = obtener_texto(BytesIO(docx_bytes))
            print(texto_extraido)
            

            docx_bytes = marcar_bloque(docx_bytes, texto_extraido, "CUERPO_MEMO")


            marcadores = listar_marcadores(docx_bytes)
            print(marcadores)


            nuevo = "Este es el nuevo texto generado dinámicamente."
            docx_bytes = reemplazar_texto(docx_bytes, nuevo, "CUERPO_MEMO")


            guardar_xml_docx(BytesIO(docx_bytes))




        except Exception as e:
            return HttpResponse(f"Error procesando: {e}", status=500)

        resp = HttpResponse(
            docx_bytes,
            content_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
        )
        resp["Content-Disposition"] = f'attachment; filename="memo_prueba.docx"'
        return resp




def obtener_texto(docx_bytes_io):
    """
    Extrae el texto dentro del bloque que comienza con 'Me dirijo a Usted,'
    y termina con 'Atentamente,' (inclusive).
    """
    doc = Document(docx_bytes_io)
    texto = "\n".join(p.text.strip() for p in doc.paragraphs if p.text.strip())

    # Buscar el bloque entre las dos frases
    patron = r"(Me dirijo a Usted,.*?Atentamente,)"
    match = re.search(patron, texto, re.DOTALL)
    
    return match.group(1).strip() if match else ""






def guardar_xml_docx(docx_bytes_io, salida="/home/hugo/Descargas/xml/document.xml"):
    """
    Extrae el archivo word/document.xml de un .docx (en memoria)
    y lo guarda en la ruta especificada.
    """
    # Asegura que la carpeta exista
    os.makedirs(os.path.dirname(salida), exist_ok=True)

    # Abre el .docx como un ZIP y lee el XML principal
    with zipfile.ZipFile(docx_bytes_io, "r") as docx_zip:
        xml_data = docx_zip.read("word/document.xml")

    # Guarda el XML en el archivo de salida
    with open(salida, "wb") as f:
        f.write(xml_data)

    print(f"✅ Archivo XML guardado en: {salida}")








def marcar_bloque(docx_bytes, texto_base, marcador="MARCADOR"):
    def normalizar_texto(t):
        return re.sub(r"\s+", "", t or "")

    mem_in = BytesIO(docx_bytes)
    mem_out = BytesIO()

    with zipfile.ZipFile(mem_in, "r") as zin, zipfile.ZipFile(mem_out, "w") as zout:
        for item in zin.infolist():
            data = zin.read(item.filename)
            if item.filename != "word/document.xml":
                zout.writestr(item, data)
                continue

            root = ET.fromstring(data)
            textos = root.findall(".//w:t", NS)

            # Construir cadena unificada y mapa de índices
            mapping = []
            cadena = ""
            for i, t in enumerate(textos):
                txt = t.text or ""
                for j, c in enumerate(txt):
                    if not c.isspace():
                        cadena += c
                        mapping.append((i, j))

            base = normalizar_texto(texto_base)
            doc = normalizar_texto(cadena)

            # Buscar posición del texto base
            pos_base = 0
            start_idx = None
            end_idx = None
            for idx_doc, c in enumerate(doc):
                if c == base[pos_base]:
                    if pos_base == 0:
                        start_idx = idx_doc
                    pos_base += 1
                    if pos_base == len(base):
                        end_idx = idx_doc
                        break
                else:
                    pos_base = 0
                    start_idx = None
            if start_idx is None or end_idx is None:
                print(f"⚠️ No se encontró el bloque para '{texto_base}'.")
                zout.writestr(item.filename, data)
                continue

            start_node, _ = mapping[start_idx]
            end_node, _ = mapping[end_idx]

     
            nuevo_id = str(random.randint(1,999))

            print(f"🆔 ID generado para marcador '{marcador}': {nuevo_id}")




            w_id = f"{{{W_NS}}}id"
            w_name = f"{{{W_NS}}}name"

            bm_start = ET.Element(f"{{{W_NS}}}bookmarkStart", {w_id: nuevo_id, w_name: marcador})
            bm_end = ET.Element(f"{{{W_NS}}}bookmarkEnd", {w_id: nuevo_id})

            # Insertar marcadores
            start_parent = textos[start_node].getparent()
            start_parent.addprevious(bm_start)

            end_parent = textos[end_node].getparent()
            end_parent.addnext(bm_end)

            # Guardar
            nuevo_xml = ET.tostring(root, encoding="utf-8", xml_declaration=True)
            zout.writestr(item.filename, nuevo_xml)

    return mem_out.getvalue()






def listar_marcadores(docx_bytes):
    """
    Devuelve una lista con todos los nombres de marcadores (<w:bookmarkStart>)
    presentes en el archivo DOCX.
    """
    marcadores = []
    try:
        with zipfile.ZipFile(BytesIO(docx_bytes)) as docx:
            xml_content = docx.read("word/document.xml")
            tree = ET.fromstring(xml_content)

        for bmk in tree.findall(".//w:bookmarkStart", NS):
            nombre = bmk.attrib.get(f"{{{W_NS}}}name")
            if nombre:
                marcadores.append(nombre)

    except Exception as e:
        print(f"Error procesando: {e}")

    return marcadores





def reemplazar_texto(docx_bytes, nuevo_texto, marcador):
    mem_in = BytesIO(docx_bytes)
    mem_out = BytesIO()



    nuevo_texto = "texto agreagao desde la funcion remplazar texto"


    with zipfile.ZipFile(mem_in, "r") as zin, zipfile.ZipFile(mem_out, "w") as zout:
        for item in zin.infolist():
            data = zin.read(item.filename)

            if item.filename != "word/document.xml":
                zout.writestr(item, data)
                continue

            xml = data.decode("utf-8")

            # Expresión para encontrar el bloque del marcador
            patron = (
                rf'(<w:bookmarkStart[^>]*w:name="{marcador}"[^>]*/>)'
                r'(.*?)'
                rf'(<w:bookmarkEnd[^>]*w:id="\d+"[^>]*/>)'
            )

            # Reemplaza el contenido entre los marcadores
            nuevo_xml = re.sub(
                patron,
                rf'\1<w:r><w:t>{nuevo_texto}</w:t></w:r>\3',
                xml,
                flags=re.DOTALL
            )

            zout.writestr(item.filename, nuevo_xml.encode("utf-8"))

    return mem_out.getvalue()
import tkinter as tk
from tkinter import messagebox
import random
import string
import csv
import json
from xml.etree.ElementTree import Element, SubElement, tostring
from xml.dom.minidom import parseString

class DummyDataGenerator:
    def export_html(self, records, file):
        file.write("<!DOCTYPE html>\n<html>\n<head>\n<title>Registros de Alumnos</title>\n")
        file.write("<link rel=\"stylesheet\" type=\"text/css\" href=\"styles.css\">\n")
        file.write("</head>\n<body>\n<table>\n")
        file.write("<tr><th>Matricula</th><th>Apellido 1</th><th>Apellido 2</th><th>Nombres</th><th>Correo</th><th>Fecha de nacimiento</th></tr>\n")
        for record in records:
            file.write("<tr>")
            for field, value in record.items():
                file.write(f"<td>{value}</td>")
            file.write("</tr>\n")
        file.write("</table>\n</body>\n</html>")

    def __init__(self, master):
        self.master = master
        master.title("Generador de Datos Ficticios")

        self.label = tk.Label(master, text="Cantidad de Registros:")
        self.label.pack()

        self.entry = tk.Entry(master)
        self.entry.pack()

        self.generate_button = tk.Button(master, text="Generar", command=self.generate_data)
        self.generate_button.pack()

    def generate_data(self):
        input_value = self.entry.get()
        if not input_value:
            messagebox.showerror("Error", "Por favor, ingresa la cantidad de registros.")
            return

        try:
            num_records = int(input_value)
        except ValueError:
            messagebox.showerror("Error", "Por favor, ingresa un valor numérico válido.")
            return

        records = []

        # Listas de apellidos y nombres en diferentes idiomas
        apellidos = {
            'es': ['García', 'Martínez', 'López', 'González', 'Rodríguez', 'Fernández', 'Pérez', 'Gómez', 'Sánchez', 'Díaz'],
            'en': ['Smith', 'Johnson', 'Brown', 'Davis', 'Miller', 'Wilson', 'Moore', 'Taylor', 'Anderson', 'Thomas'],
            'fr': ['Dupont', 'Martin', 'Lefevre', 'Dubois', 'Laurent', 'Michel', 'Leroy', 'Simon', 'Moreau', 'Lefebvre'],
            'it': ['Rossi', 'Russo', 'Ferrari', 'Esposito', 'Bianchi', 'Romano', 'Colombo', 'Ricci', 'Marino', 'Greco']
            }
        nombres = {
            'es': ['Juan', 'María', 'José', 'Ana', 'Pedro', 'Lucía', 'Carlos', 'Laura', 'Miguel', 'Elena'],
            'en': ['John', 'Mary', 'James', 'Elizabeth', 'William', 'Patricia', 'Michael', 'Jennifer', 'David', 'Linda'],
            'fr': ['Pierre', 'Marie', 'Jean', 'Anne', 'Jacques', 'Michelle', 'Philippe', 'Isabelle', 'David', 'Sylvie'],
            'it': ['Mario', 'Giuseppe', 'Anna', 'Maria', 'Luigi', 'Rosa', 'Giovanni', 'Sofia', 'Antonio', 'Francesca']
}


        for _ in range(num_records):
            matricula = ''.join(random.choices(string.digits, k=8))
            apellido1 = random.choice(apellidos['es'])
            apellido2 = random.choice(apellidos['en'])
            nombre = random.choice(nombres['es'])
            correo = f"{nombre.lower()}@example.com"
            fecha_nacimiento = f"{random.randint(1, 28)}/{random.randint(1, 12)}/{random.randint(1990, 2010)}"

            record = {
                'Matricula': matricula,
                'Apellido 1': apellido1,
                'Apellido 2': apellido2,
                'Nombres': nombre,
                'Correo': correo,
                'Fecha de nacimiento': fecha_nacimiento
            }

            records.append(record)

        self.export_data(records)

    def export_data(self, records):
        export_format = {
            'SQL': self.export_sql,
            'CSV': self.export_csv,
            'XML': self.export_xml,
            'JSON': self.export_json,
            'HTML': self.export_html
        }

        for format, exporter in export_format.items():
            filename = f'data.{format.lower()}'
            with open(filename, 'w', encoding='utf-8') as f:  # Agregar encoding='utf-8' aquí
                exporter(records, f)

        messagebox.showinfo("Exportación Exitosa", "Datos exportados exitosamente")


    def export_sql(self, records, file):
        file.write("INSERT INTO sistema_escolar (Matricula, Apellido1, Apellido2, Nombres, Correo, Fecha_Nacimiento) VALUES\n")
        for record in records:
            file.write(f"('{record['Matricula']}', '{record['Apellido 1']}', '{record['Apellido 2']}', '{record['Nombres']}', '{record['Correo']}', '{record['Fecha de nacimiento']}'),\n")

    def export_csv(self, records, file):
        writer = csv.DictWriter(file, fieldnames=['Matricula', 'Apellido 1', 'Apellido 2', 'Nombres', 'Correo', 'Fecha de nacimiento'])
        writer.writeheader()
        writer.writerows(records)

    def export_xml(self, records, file):
        root = Element('alumnos')
        for record in records:
            alumno = SubElement(root, 'alumno')
            for field, value in record.items():
                SubElement(alumno, field.replace(' ', '_')).text = value

        xml_str = tostring(root, 'utf-8')
        parsed_xml = parseString(xml_str)
        file.write(parsed_xml.toprettyxml(indent="  "))

    def export_json(self, records, file):
        json.dump(records, file, indent=4)

    def export_html(self, records, file):
        file.write("<html>\n<head>\n<title>Registros de Alumnos</title>\n")
        file.write("<link rel='stylesheet' type='text/css' href='styles.css'>\n")  # Agrega esta línea
        file.write("</head>\n<body>\n<table>\n")
        file.write("<tr><th>Matricula</th><th>Apellido 1</th><th>Apellido 2</th><th>Nombres</th><th>Correo</th><th>Fecha de nacimiento</th></tr>\n")
        for record in records:
            file.write("<tr>")
            for field, value in record.items():
                file.write(f"<td>{value}</td>")
        file.write("</tr>\n")
        file.write("</table>\n</body>\n</html>")


def main():
    root = tk.Tk()
    app = DummyDataGenerator(root)
    root.mainloop()

if __name__ == "__main__":
    main()

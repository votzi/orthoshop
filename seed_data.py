"""Script para poblar la base de datos con el catalogo inicial de productos."""
import os
from dotenv import load_dotenv
from models import db, Product
from app import create_app

load_dotenv()


def seed_products():
    """Agrega productos iniciales al catalogo de ortodoncia."""
    app = create_app()

    with app.app_context():
        # Verificar si ya hay productos
        if Product.query.first():
            print("La base de datos ya tiene productos. Saltando seed.")
            return

        products = []

        # ==================== LIGAS (25 colores) ====================
        ligas_data = [
            ("Liga Roja", "Liga elastica de color rojo intenso para brackets ortodonticos. Material de alta calidad con excelente elasticidad y resistencia. Compatible con todos los sistemas de brackets estandar.", "Ligas"),
            ("Liga Azul Oscuro", "Liga elastica azul marino profesional. Color sobrio y elegante, muy popular entre pacientes adultos. Excelente fuerza de retencion.", "Ligas"),
            ("Liga Azul Claro", "Liga elastica en tono azul cielo. Color fresco y juvenil que mantiene su intensidad durante todo el tratamiento.", "Ligas"),
            ("Liga Verde", "Liga elastica verde brillante. Color vibrante y energetico, ideal para pacientes jovenes que buscan un look divertido.", "Ligas"),
            ("Liga Rosa", "Liga elastica rosa pastel. Color suave y delicado, especialmente popular entre pacientes adolescentes.", "Ligas"),
            ("Liga Rosa Fuerte", "Liga elastica en tono rosa fuerte/fucsia. Color llamativo y moderno con excelente durabilidad.", "Ligas"),
            ("Liga Naranja", "Liga elastica naranja brillante. Color energetico y divertido, perfecto para combinar con tematicas festivas.", "Ligas"),
            ("Liga Amarilla", "Liga elastica amarilla brillante. Color alegre y luminoso que aporta un toque de alegria a la sonrisa.", "Ligas"),
            ("Liga Morada", "Liga elastica morada/violeta. Uno de los colores mas populares, combina bien con todos los tonos de piel.", "Ligas"),
            ("Liga Blanca", "Liga elastica blanca translucida. Color discreto y limpio que simula la apariencia de brackets ceramicos.", "Ligas"),
            ("Liga Negra", "Liga elastica negra. Color elegante y discreto que hace que los dientes se vean mas blancos por contraste.", "Ligas"),
            ("Liga Gris", "Liga elastica gris plateado. Color neutro y profesional, excelente alternativa al negro.", "Ligas"),
            ("Liga Turquesa", "Liga elastica turquesa. Color tropical y vibrante, muy popular entre adolescentes.", "Ligas"),
            ("Liga Dorada", "Liga elastica color dorado/oro. Color premium y sofisticado que aporta un toque de lujo.", "Ligas"),
            ("Liga Plateada", "Liga elastica color plata. Discreta y elegante, combina perfectamente con brackets metalicos.", "Ligas"),
            ("Liga Verde Lima", "Liga elastica verde lima neon. Color fluorescente y llamativo, ideal para pacientes atrevidos.", "Ligas"),
            ("Liga Lavanda", "Liga elastica lavanda suave. Color pastel tranquilo y elegante, muy estetico.", "Ligas"),
            ("Liga Coral", "Liga elastica color coral. Tono calido entre rosa y naranja, muy popular y favorecedor.", "Ligas"),
            ("Liga Celeste", "Liga elastica celeste claro. Color suave y relajante, alternativa delicada al azul intenso.", "Ligas"),
            ("Liga Fucsia", "Liga elastica fucsia intenso. Color vibrante y atrevido con gran poder de expresion.", "Ligas"),
            ("Liga Cafe", "Liga elastica color cafe/marron. Color neutro y discreto, poco comun pero elegante.", "Ligas"),
            ("Liga Vino", "Liga elastica color vino/borgona. Color elegante y maduro, muy sofisticado.", "Ligas"),
            ("Liga Verde Bosque", "Liga elastica verde bosque oscuro. Color natural y profundo, alternative al verde brillante.", "Ligas"),
            ("Liga Arcoiris", "Liga elastica con colores tornasolados efecto arcoiris. Color especial y unico que cambia con la luz.", "Ligas"),
            ("Liga Transparente", "Liga elastica transparente/cristal. La mas discreta de todas, practicamente invisible.", "Ligas"),
        ]

        for name, desc, category in ligas_data:
            products.append(Product(name=name, description=desc, category=category))

        # ==================== CADENETAS (25 colores) ====================
        cadenetas_data = [
            ("Cadeneta Roja", "Cadena elastica roja para ortodoncia de cierre continuo. Excelente para cerrar espacios y mantener fuerza constante. Paquete de una cadena completa.", "Cadenetas"),
            ("Cadeneta Azul Oscuro", "Cadena elastica azul marino de cierre continuo. Color profesional y sobrio, ideal para adultos. Alta resistencia a la decoloracion.", "Cadenetas"),
            ("Cadeneta Azul Claro", "Cadena elastica azul cielo. Color fresco y juvenil con fuerza de cierre optima para tratamiento ortodontico.", "Cadenetas"),
            ("Cadeneta Verde", "Cadena elastica verde brillante. Color energetico con excelente memoria elastica y durabilidad.", "Cadenetas"),
            ("Cadeneta Rosa", "Cadena elastica rosa pastel. Color suave y popular entre adolescentes. Cierre espaciado uniforme.", "Cadenetas"),
            ("Cadeneta Rosa Fuerte", "Cadena elastica fucsia intensa. Color atrevido y llamativo con fuerza de cierre constante.", "Cadenetas"),
            ("Cadeneta Naranja", "Cadena elastica naranja brillante. Color vibrante y divertido para pacientes con personalidad.", "Cadenetas"),
            ("Cadeneta Amarilla", "Cadena elastica amarilla. Color alegre y luminoso que aporta energia a la sonrisa.", "Cadenetas"),
            ("Cadeneta Morada", "Cadena elastica morada/violeta. Color popular y versatil que favorece a todo tipo de pacientes.", "Cadenetas"),
            ("Cadeneta Blanca", "Cadena elastica blanca translucida. Discreta y limpia, ideal para brackets ceramicos.", "Cadenetas"),
            ("Cadeneta Negra", "Cadena elastica negra. Elegante y discreta, hace que los dientes resalten mas blancos.", "Cadenetas"),
            ("Cadeneta Gris", "Cadena elastica gris. Color neutro y profesional, excelente balance entre discrecion y estilo.", "Cadenetas"),
            ("Cadeneta Turquesa", "Cadena elastica turquesa. Color tropical y moderno con excelente fuerza de retencion.", "Cadenetas"),
            ("Cadeneta Dorada", "Cadena elastica dorada. Color premium y sofisticado para un look diferenciado.", "Cadenetas"),
            ("Cadeneta Plateada", "Cadena elastica plateada. Discreta y elegante, combina con brackets metalicos.", "Cadenetas"),
            ("Cadeneta Verde Lima", "Cadena elastica verde lima neon. Color fluorescente atrevido para pacientes expresivos.", "Cadenetas"),
            ("Cadeneta Lavanda", "Cadena elastica lavanda. Color pastel suave y elegante, muy estetico.", "Cadenetas"),
            ("Cadeneta Coral", "Cadena elastica coral. Tono calido y favorecedor entre rosa y naranja.", "Cadenetas"),
            ("Cadeneta Celeste", "Cadena elastica celeste. Color suave y delicado, alternativa al azul intenso.", "Cadenetas"),
            ("Cadeneta Fucsia", "Cadena elastica fucsia. Color intenso y vibrante con gran impacto visual.", "Cadenetas"),
            ("Cadeneta Cafe", "Cadena elastica cafe. Color neutro y poco comun pero elegante.", "Cadenetas"),
            ("Cadeneta Vino", "Cadena elastica vino/borgona. Color maduro y sofisticado.", "Cadenetas"),
            ("Cadeneta Verde Bosque", "Cadena elastica verde oscuro. Color profundo y natural.", "Cadenetas"),
            ("Cadeneta Arcoiris", "Cadena elastica con efecto tornasol. Color especial que cambia con la luz.", "Cadenetas"),
            ("Cadeneta Transparente", "Cadena elastica transparente/cristal. La mas discreta, practicamente invisible.", "Cadenetas"),
        ]

        for name, desc, category in cadenetas_data:
            products.append(Product(name=name, description=desc, category=category))

        # ==================== KIT DE HIGIENE ====================
        kit_higiene_data = [
            ("Kit de Higiene Basico", "Kit completo de higiene para pacientes de ortodoncia. Incluye cepillo dental de cabezal pequeno, cepillo interproximal, hilo dental especial para brackets y cera ortodontica protectora. Todo lo esencial para mantener una limpieza optima durante el tratamiento.", "Kit de Higiene"),
            ("Kit de Higiene Premium", "Kit premium de higiene ortodontica con accesorios avanzados. Incluye cepillo electrico compatible con brackets, irrigador bucal de viaje, cepillos interproximales de varios tamanos, hilo dental Super Floss, cera ortodontica con sabor y estuche de transporte. Ideal para viajeros.", "Kit de Higiene"),
            ("Kit de Higiene de Viaje", "Kit compacto de higiene ortodontica para llevar. Estuche portatil con cepillo plegable, mini pasta dental, cepillo interproximal y cera ortodontica. Perfecto para llevar al colegio, trabajo o viajes. Cabe en cualquier bolsillo.", "Kit de Higiene"),
            ("Kit de Higiene Infantil", "Kit de higiene disenado para ninos en ortodoncia. Incluye cepillo de mangos ergonomicos para manos pequenas, cepillo interproximal suave, hilo dental con guia para ninos, cera con sabores divertidos y guia ilustrada de cepillado. Hace que la higiene sea divertida.", "Kit de Higiene"),
        ]

        for name, desc, category in kit_higiene_data:
            products.append(Product(name=name, description=desc, category=category))

        # ==================== ELASTICOS ====================
        elasticos_data = [
            ("Elásticos 1/4 - Ligeros", "Elásticos ortodonticos medida 1/4 de pulgada (6.35mm). Fuerza ligera de 2oz. Ideales para movimientos dentales suaves y correcciones menores de mordida. Paquete de 100 unidades. Latex-free.", "Elásticos"),
            ("Elásticos 1/4 - Medianos", "Elásticos ortodonticos medida 1/4 de pulgada (6.35mm). Fuerza mediana de 3.5oz. Para correcciones estandar de mordida clase II y III. Excelente elasticidad y fuerza consistente. Paquete de 100 unidades.", "Elásticos"),
            ("Elásticos 1/4 - Fuertes", "Elásticos ortodonticos medida 1/4 de pulgada (6.35mm). Fuerza fuerte de 4.5oz. Para correcciones avanzadas de mordida que requieren mayor presion. Duracion prolongada. Paquete de 100 unidades.", "Elásticos"),
            ("Elásticos 1/8 - Ligeros", "Elásticos ortodonticos medida 1/8 de pulgada (3.17mm). Fuerza ligera de 2oz. Diseno compacto para movimientos precisos en espacios reducidos. Alta resistencia a la rotura. Paquete de 100 unidades.", "Elásticos"),
            ("Elásticos 1/8 - Medianos", "Elásticos ortodonticos medida 1/8 de pulgada (3.17mm). Fuerza mediana de 3.5oz. Para correcciones de mordida en espacios reducidos con fuerza moderada. Calidad premium. Paquete de 100 unidades.", "Elásticos"),
            ("Elásticos 1/8 - Fuertes", "Elásticos ortodonticos medida 1/8 de pulgada (3.17mm). Fuerza fuerte de 4.5oz. Maxima potencia en tamano reducido para correcciones exigentes. Paquete de 100 unidades.", "Elásticos"),
            ("Elásticos 3/16 - Ligeros", "Elásticos ortodonticos medida 3/16 de pulgada (4.76mm). Fuerza ligera de 2oz. Tamano intermedio versatil para multiples aplicaciones ortodonticas. Excelente relacion tamano-fuerza. Paquete de 100 unidades.", "Elásticos"),
            ("Elásticos 3/16 - Medianos", "Elásticos ortodonticos medida 3/16 de pulgada (4.76mm). Fuerza mediana de 3.5oz. El tamano mas versatil para correcciones de mordida estandar. Fuerza constante y duradera. Paquete de 100 unidades.", "Elásticos"),
            ("Elásticos 3/16 - Fuertes", "Elásticos ortodonticos medida 3/16 de pulgada (4.76mm). Fuerza fuerte de 4.5oz. Para correcciones de mordida que requieren fuerza significativa. Alta durabilidad. Paquete de 100 unidades.", "Elásticos"),
        ]

        for name, desc, category in elasticos_data:
            products.append(Product(name=name, description=desc, category=category))

        # ==================== ARCOS ORTODONTICOS ====================
        arcos_data = [
            ("Arco Nitinol 0.012", "Arco ortodontico de Nitinol (NiTi) super elastico calibre 0.012 pulgadas. Ideal para nivelacion inicial. Memoria de forma excepcional y fuerza constante. Longitud: arco superior e inferior. Unidad.", "Arcos Ortodónticos"),
            ("Arco Nitinol 0.014", "Arco ortodontico de Nitinol calibre 0.014 pulgadas. Segunda fase de nivelacion. Excelente relacion flexibilidad-fuerza. Compatible con brackets de ranura 0.018 y 0.022. Unidad.", "Arcos Ortodónticos"),
            ("Arco Nitinol 0.016", "Arco ortodontico de Nitinol calibre 0.016 pulgadas. Versatil para multiples fases del tratamiento. Fuerza suave y continua para movimiento dental eficiente. Unidad.", "Arcos Ortodónticos"),
            ("Arco Nitinol 0.018", "Arco ortodontico de Nitinol calibre 0.018 pulgadas. Para fases intermedias de alineacion. Mayor rigidez que calibres menores manteniendo la super elasticidad. Unidad.", "Arcos Ortodónticos"),
            ("Arco Nitinol 0.020", "Arco ortodontico de Nitinol calibre 0.020 pulgadas. Para fases avanzadas de nivelacion. Alta resistencia con elasticidad controlada. Unidad.", "Arcos Ortodónticos"),
            ("Arco Acero 0.012", "Arco ortodontico de acero inoxidable calibre 0.012 pulgadas. Para fases de finished y detalado. Maximo control y precision en los movimientos finales. Unidad.", "Arcos Ortodónticos"),
            ("Arco Acero 0.014", "Arco ortodontico de acero inoxidable calibre 0.014 pulgadas. Excelente para control de torque y cierre de espacios. Rigidez superior al Nitinol. Unidad.", "Arcos Ortodónticos"),
            ("Arco Acero 0.016", "Arco ortodontico de acero inoxidable calibre 0.016 pulgadas. Versatil para detallado y acabados. Alta estabilidad dimensional. Unidad.", "Arcos Ortodónticos"),
            ("Arco Acero 0.018", "Arco ortodontico de acero inoxidable calibre 0.018 pulgadas. Para fases de finished con brackets de ranura 0.018. Maxima precision. Unidad.", "Arcos Ortodónticos"),
            ("Arco Acero 0.020", "Arco ortodontico de acero inoxidable calibre 0.020 pulgadas. Ideal para arcos de trabajo y finalizacion. Excelente control tridimensional. Unidad.", "Arcos Ortodónticos"),
            ("Arco Acero 0.022", "Arco ortodontico de acero inoxidable calibre 0.022 pulgadas. Para brackets de ranura 0.022 en fase final. Maxima rigidez y control. Unidad.", "Arcos Ortodónticos"),
            ("Arco Nitinol Termico 0.016", "Arco ortodontico de Nitinol termico-activado calibre 0.016 pulgadas. Se activa con la temperatura bucal para ejercer fuerza progresiva. Tecnologia de ultima generacion. Unidad.", "Arcos Ortodónticos"),
            ("Arco Nitinol Termico 0.018", "Arco ortodontico de Nitinol termico-activado calibre 0.018 pulgadas. Activacion termica para fuerza constante y suave. Comodidad superior para el paciente. Unidad.", "Arcos Ortodónticos"),
            ("Arco Nitinol Termico 0.020", "Arco ortodontico de Nitinol termico-activado calibre 0.020 pulgadas. Tecnologia termica avanzada para movimientos eficientes. Menos visitas de ajuste necesarias. Unidad.", "Arcos Ortodónticos"),
        ]

        for name, desc, category in arcos_data:
            products.append(Product(name=name, description=desc, category=category))

        # Insertar todos los productos
        db.session.add_all(products)
        db.session.commit()

        print(f"✅ {len(products)} productos insertados exitosamente:")
        print(f"   - Ligas: {len(ligas_data)}")
        print(f"   - Cadenetas: {len(cadenetas_data)}")
        print(f"   - Kit de Higiene: {len(kit_higiene_data)}")
        print(f"   - Elasticos: {len(elasticos_data)}")
        print(f"   - Arcos Ortodonticos: {len(arcos_data)}")


if __name__ == '__main__':
    seed_products()

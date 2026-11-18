import os
from grafos import (grafoMalla, grafoErdosRenyi, grafoGilbert, grafoGeografico, grafoBarabasiAlbert, grafoDorogovtsevMendes)

def generar_entregables_mst():
    carpeta_base = "entregables_mst"
    os.makedirs(f"{carpeta_base}/generados", exist_ok=True)
    os.makedirs(f"{carpeta_base}/calculados", exist_ok=True)

    # Dos tamaños: pocos (30) y muchos (300) nodos
    configuraciones = {
        "pocos": 30,
        "muchos": 300
    }

    dimensiones_malla = {
        30: (6, 5),     # 6x5 = 30 nodos
        300: (20, 15)   # 20x15 = 300 nodos
    }

    print("=" * 75)
    print(f"{'GRAFO':<22} | {'NODOS':<5} | {'KRUSKAL D':<10} | {'KRUSKAL I':<10} | {'PRIM':<10}")
    print("=" * 75)

    for etiqueta, n in configuraciones.items():
        m, cols = dimensiones_malla[n]
        p = 0.15 if n == 30 else 0.03
        r = 0.30 if n == 30 else 0.12

        modelos = {
            "malla": grafoMalla(m, cols),
            "erdos_renyi": grafoErdosRenyi(n, n * 3),
            "gilbert": grafoGilbert(n, p),
            "geografico": grafoGeografico(n, r),
            "barabasi": grafoBarabasiAlbert(n, 4),
            "dorogovtsev": grafoDorogovtsevMendes(n)
        }

        for nombre_modelo, g in modelos.items():
            id_archivo = f"{nombre_modelo}_{etiqueta}_{n}"
            
            # 1. Guardar grafo original generado
            g.guardar_graphviz(f"{carpeta_base}/generados/{id_archivo}.gv")

            # 2. Calcular MST con los 3 algoritmos
            mst_kd = g.KruskalD()
            mst_ki = g.KruskalI()
            mst_prim = g.Prim()

            # 3. Guardar grafos calculados (.gv)
            mst_kd.guardar_graphviz(f"{carpeta_base}/calculados/{id_archivo}_KruskalD.gv")
            mst_ki.guardar_graphviz(f"{carpeta_base}/calculados/{id_archivo}_KruskalI.gv")
            mst_prim.guardar_graphviz(f"{carpeta_base}/calculados/{id_archivo}_Prim.gv")

            # 4. Imprimir valores del MST en consola (para tus capturas de pantalla)
            costo_kd = mst_kd.peso_total()
            costo_ki = mst_ki.peso_total()
            costo_prim = mst_prim.peso_total()

            print(f"{id_archivo:<22} | {n:<5} | {costo_kd:<10} | {costo_ki:<10} | {costo_prim:<10}")

    print("=" * 75)
    print("Proceso finalizado. Archivos guardados en la carpeta 'entregables_mst/'.")

if __name__ == '__main__':
    generar_entregables_mst()

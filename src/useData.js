import { useEffect, useState } from "react";
import Papa from "papaparse";

export default function useData() {
  const [data, setData] = useState([]);

  useEffect(() => {
    Papa.parse("/ventas.csv", {
      download: true,
      header: true,
      skipEmptyLines: true,
      complete: (results) => {

        const parsed = results.data
          .filter(d => d.IdTienda && d.SKU)
          .map(d => ({
            tienda: Number(d.IdTienda),
            sku: Number(d.SKU),
            unidades: Number(d["Unidades Vendidas"]) || 0,
            ingreso: Number(d.Ingreso) || 0,
            tipo: d["Tipo de venta"]?.trim()
          }));

        setData(parsed);
      }
    });
  }, []);

  return data;
}
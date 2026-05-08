import { Treemap } from "recharts";

export default function TreeMapChart({ data }) {

  const grouped = Object.values(
    data.reduce((acc, curr) => {
      if (!acc[curr.sku]) {
        acc[curr.sku] = { name: "SKU " + curr.sku, size: 0 };
      }
      acc[curr.sku].size += curr.ingreso;
      return acc;
    }, {})
  );

  return (
    <Treemap
      width={400}
      height={250}
      data={grouped}
      dataKey="size"
      stroke="#0f172a"
      fill="#60a5fa"
    />
  );
}
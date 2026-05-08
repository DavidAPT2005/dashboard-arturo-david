import { Sankey } from "recharts";

export default function SankeyChart({ data }) {

  const nodes = [];
  const links = [];
  const nodeMap = {};

  function getIndex(name) {
    if (!(name in nodeMap)) {
      nodeMap[name] = nodes.length;
      nodes.push({ name });
    }
    return nodeMap[name];
  }

  data.slice(0, 30).forEach(d => {
    if (!d.tienda || !d.sku) return;

    const tienda = "Tienda " + d.tienda;
    const producto = "SKU " + d.sku;

    links.push({
      source: getIndex(tienda),
      target: getIndex(producto),
      value: d.unidades || 1
    });
  });

  return (
    <Sankey
      width={400}
      height={250}
      data={{ nodes, links }}
    />
  );
}
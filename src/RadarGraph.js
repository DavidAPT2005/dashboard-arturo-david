import { RadarChart, PolarGrid, PolarAngleAxis, Radar } from "recharts";

export default function RadarGraph({ data }) {

  const counts = { Alta: 0, Media: 0, Baja: 0 };

  data.forEach(d => {
    const tipo = d.tipo?.trim();
    if (counts[tipo] !== undefined) {
      counts[tipo]++;
    }
  });

  const formatted = Object.keys(counts).map(key => ({
    tipo: key,
    valor: counts[key]
  }));

  return (
    <RadarChart width={400} height={250} data={formatted}>
      <PolarGrid />
      <PolarAngleAxis dataKey="tipo" />
      <Radar dataKey="valor" fill="#22c55e" />
    </RadarChart>
  );
}
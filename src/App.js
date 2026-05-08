import SankeyChart from "./SankeyChart";
import TreeMapChart from "./TreeMapChart";
import RadarGraph from "./RadarGraph";
import ForceGraph from "./ForceGraph";
import useData from "./useData";

function App() {
  const data = useData();

  if (data.length === 0) {
    return <p style={{ textAlign: "center" }}>Cargando datos...</p>;
  }

  return (
    <div style={styles.container}>
      <h1 style={styles.title}>Base de datos Arturo y David</h1>

      <div style={styles.grid}>
        <div style={styles.card}>
          <h2 style={styles.cardTitle}>Flujo de Ventas</h2>
          <SankeyChart data={data} />
        </div>

        <div style={styles.card}>
          <h2 style={styles.cardTitle}>Distribución por Producto</h2>
          <TreeMapChart data={data} />
        </div>

        <div style={styles.card}>
          <h2 style={styles.cardTitle}>Tipos de Venta</h2>
          <RadarGraph data={data} />
        </div>

        <div style={styles.card}>
          <h2 style={styles.cardTitle}>Relación Tienda - Producto</h2>
          <ForceGraph data={data} />
        </div>
      </div>
    </div>
  );
}

const styles = {
  container: {
    background: "#0f172a",
    minHeight: "100vh",
    padding: "40px",
    color: "white"
  },
  title: {
    textAlign: "center",
    fontSize: "2rem",
    marginBottom: "30px"
  },
  grid: {
    display: "grid",
    gridTemplateColumns: "1fr 1fr",
    gap: "20px"
  },
  card: {
    background: "#1e293b",
    padding: "20px",
    borderRadius: "10px"
  },
  cardTitle: {
    marginBottom: "10px"
  }
};

export default App;
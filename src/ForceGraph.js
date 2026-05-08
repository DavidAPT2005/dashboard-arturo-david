import * as d3 from "d3";
import { useEffect, useRef } from "react";

export default function ForceGraph({ data }) {
  const ref = useRef();

  useEffect(() => {
    const svg = d3.select(ref.current);
    svg.selectAll("*").remove();

    const nodes = [];
    const links = [];

    data.slice(0, 10).forEach(d => {
      if (!d.tienda || !d.sku) return;

      nodes.push({ id: "T" + d.tienda });
      nodes.push({ id: "S" + d.sku });

      links.push({
        source: "T" + d.tienda,
        target: "S" + d.sku
      });
    });

    const simulation = d3.forceSimulation(nodes)
      .force("link", d3.forceLink(links).id(d => d.id))
      .force("charge", d3.forceManyBody())
      .force("center", d3.forceCenter(200, 125));

    const link = svg.append("g")
      .selectAll("line")
      .data(links)
      .enter()
      .append("line")
      .attr("stroke", "white");

    const node = svg.append("g")
      .selectAll("circle")
      .data(nodes)
      .enter()
      .append("circle")
      .attr("r", 6)
      .attr("fill", "yellow");

    simulation.on("tick", () => {
      link
        .attr("x1", d => d.source.x)
        .attr("y1", d => d.source.y)
        .attr("x2", d => d.target.x)
        .attr("y2", d => d.target.y);

      node
        .attr("cx", d => d.x)
        .attr("cy", d => d.y);
    });

  }, [data]);

  return <svg ref={ref} width={400} height={250} />;
}
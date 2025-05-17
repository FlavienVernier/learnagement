"use client";

import axios from "axios";
import React, { useEffect, useState } from "react";
import { MarkerType, Position, ReactFlowProvider } from "@xyflow/react";

import MaquetteFlow from "@/app/modules/maquetteModule/maquetteFlow";
import Loader from "@/app/indicators/loading";

export default function maquetteModule({code_module}: {code_module: string; }) {
  const [maquette, setMaquette] = useState([]);
  const [nodes, setNodes] = useState<object[]>([]);
  const [edges, setEdges] = useState<object[]>([]);
  const [width, setWidth] = useState(-1);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    setIsLoading(true);

    let form_data = new FormData();

    form_data.append("code_module", code_module);
    axios.post("/api/proxy/select/selectMaquette", form_data, {withCredentials: true})
        .then((response) => {
          if (response.status == 200) {
            setMaquette(response.data);
            setIsLoading(false);
          } else {
            console.error(response.data);
            setTimeout(() => {
              setIsLoading(false);
            }, 2000);
          }
        });
  }, [code_module]);

  /* création des nodes des edges (besoins de la largeur d'écran pour placer les nodes */
  useEffect(() => {
    if (maquette.length > 0) {
      createNodes(maquette);
      createEdges(maquette);
    } else {
      setNodes([]);
      setEdges([]);
    }
  }, [maquette, width]);

  function getSeances(maquette: any) {
    /* liste des séances de cours dans le bon ordre */
    let tmpSeances = [];

    let index = 0;
    let i = 0;
    let seancePred = maquette[i]["séance précédente"];
    let seanceSuiv = maquette[i]["séance suivante"];

    tmpSeances.push(seancePred);
    tmpSeances.push(seanceSuiv);

    while (i < maquette.length) {
      index = maquette.findIndex(
        (obj: any) => obj["séance précédente"] === seanceSuiv
      );

      if (index != -1) {
        seanceSuiv = maquette[index]["séance suivante"];
        tmpSeances.push(seanceSuiv);
      } else {
        /* Traitement du cas où il y a une rupture dans les liens de tous les cours */
        seancePred = maquette[i]["séance précédente"];
        seanceSuiv = maquette[i]["séance suivante"];
        tmpSeances.push(seancePred, seanceSuiv);
      }

      i++;
    }

    return [...new Set(tmpSeances)];
  }

  function createNodes(edges: any) {
    let seances = getSeances(edges); // Liste des séances dans le bon ordre (selon les liens)
    let nodes = [];

    let x = 0;
    let y = 0;

    for (let i = 0; i < seances.length; i++) {
      let color;
      let seance = seances[i];
      let type = seance.slice(0, 2);

      if (type === "CM") {
        color = "bg-cm-red";
      } else if (type === "TD") {
        color = "bg-td-green";
      } else if (type === "TP") {
        color = "bg-tp-yellow";
      } else if (type === "Ex") {
        color = "bg-exam-blue";
      } else {
        color = "bg-other-pink";
      }

      let node = {
        id: seance,
        type: "customNode",
        position: { x: x, y: y },
        data: { label: seance, color: color },
        sourcePosition: Position.Right, // Les liens sortent par la droite
        targetPosition: Position.Left, // Les liens entrent par la gauche
      };

      nodes.push(node);

      if (x >= width && width != -1) {
        y += 200;
        x = 0;
      } else {
        x += 200;
      }
    }
    setNodes(nodes);
  }

  function createEdges(maquette: any) {
    let edges = [];

    for (let i = 0; i < maquette.length; i++) {
      let pred = maquette[i]["séance précédente"];
      let suiv = maquette[i]["séance suivante"];

      let link = {
        id: pred + "-" + suiv,
        source: pred,
        target: suiv,
        animated: true,
        markerEnd: {
          type: MarkerType.ArrowClosed,
          width: 30,
          height: 30,
        },
        type: "floating",
      };
      edges.push(link);
    }
    setEdges(edges);
  }

  return (
    <div className={"h-screen w-full"}>
      {!isLoading ? (
        <ReactFlowProvider>
          <MaquetteFlow
            initialNodes={nodes}
            initialEdges={edges}
            setWidth={setWidth}
          />
        </ReactFlowProvider>
      ) : (
        <div className={"h-full w-full flex items-center justify-center"}>
          <Loader />
        </div>
      )}
    </div>
  );
}

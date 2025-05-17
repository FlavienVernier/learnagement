import { memo, useEffect } from "react";
import { Handle, Position } from "@xyflow/react";
import axios from "axios";
import { useInfosModuleStore } from "@/app/store/useInfosModuleStore";

function CustomNode({data, setDisplayCardCourse}: { data: any, setDisplayCardCourse: (course: any) => void}){
  const { module } = useInfosModuleStore();

  const handleClick = (e: any) => {
    e.stopPropagation();
    
    const formData = new FormData();
    formData.append("input", data.label);
    formData.append("module", module.code_module);

    axios.post("/api/proxy/select/selectSeance", formData, {withCredentials: true})
        .then((response) => {
          setDisplayCardCourse({
            label: data.label,
            moduleCode: response.data.moduleCode,
            session: data.session,
            duration: response.data.duree_h,
            color: data.color,
            typeCourse: response.data.typeCourse,
            currentNumber: response.data.currentNumber,
            totalNumber: response.data.totalNumber,
          });
      })
      .catch((error) => {
        console.error("API Error:", error);
      });
  };

  return (
    <div
      className={`px-10 py-2.5 shadow-md rounded-md border-2 border-stone-400 ${data.color}`}
      onClick={handleClick}
    >
      <div className={"text-lg font-bold"}>{data.label}</div>

      <Handle type="target" position={Position.Left} className={"opacity-0"} />
      <Handle type="source" position={Position.Right} className={"opacity-0"} />
    </div>
  );
}

export default memo(CustomNode);

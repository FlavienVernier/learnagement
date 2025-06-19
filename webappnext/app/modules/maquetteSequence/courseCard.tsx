import React from "react";

interface CourseCardProps {
  label: string,
  type: string;
  moduleCode: string;
  session: string;
  duration: string;
  bgColor: string;
}

const CourseCard: React.FC<CourseCardProps> = ({
  label,
  type,
  moduleCode,
  session,
  duration,
  bgColor,
}) => {
  return (
    <div
      className={`w-48 p-4 rounded-md shadow-md border border-gray-300 ${bgColor}`}
    >
      <h2 className="text-lg font-bold">{label}</h2>
      <p className="text-sm">{type}</p>
      <p className="text-xs text-gray-700">{moduleCode}</p>
      <p>{session}</p>
      <p className="text-md font-semibold">{duration}</p>
    </div>
  );
};

export default CourseCard;

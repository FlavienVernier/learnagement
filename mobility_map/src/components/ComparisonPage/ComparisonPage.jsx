import ComparisonTable from "./ComparisonTable";

export default function ComparisonPage({ selectedUnivs }) {
  return (
    <div>
      <ComparisonTable universities={selectedUnivs} />
    </div>
  );
}
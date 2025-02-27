import PropTypes from "prop-types";
import CountUp from "react-countup";

const InfoCard = ({ title, value, description }) => {
  return (
    <div className="bg-white p-6 rounded-lg shadow-lg hover:shadow-xl transition-shadow duration-300">
      <h1 className="text-xl font-bold mb-2">{title}</h1>
      <p className="text-3xl font-semibold mb-4">
        <CountUp end={value} duration={2.5} />
      </p>
      <p className="text-gray-600">{description}</p>
    </div>
  );
};

InfoCard.propTypes = {
  title: PropTypes.string.isRequired,
  value: PropTypes.number.isRequired,
  description: PropTypes.string.isRequired,
};

export default InfoCard;
import { Spinner } from "react-bootstrap";

const Loader = ({ size = 40 }) => {
  return (
    <Spinner
      animation="border"
      role="status"
      style={{
        width: `${size}px`,
        height: `${size}px`,
        position: "fixed", // Use 'fixed' instead of 'absolute' to position relative to the viewport
        top: "50%", // Position halfway down the viewport
        left: "50%", // Position halfway across the viewport
        display: "block",
      }}
    ></Spinner>
  );
};

export default Loader;

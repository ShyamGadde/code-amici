import { useState } from "react";
import { Badge, CloseButton, Form } from "react-bootstrap";

const PillInputList = ({ list, setList }) => {
  const [inputValue, setInputValue] = useState("");

  const handleAddPill = () => {
    if (inputValue.trim()) {
      const cleanedInput = inputValue.toLowerCase().replace(/[.-]/g, "");
      setList([...list, cleanedInput]);
      setInputValue("");
    }
  };

  const handleRemovePill = (index) => {
    const updatedList = list.filter((_, i) => i !== index);
    setList(updatedList);
  };

  return (
    <>
      <Form.Control
        type="text"
        placeholder="Enter full name"
        value={inputValue}
        onChange={(e) => setInputValue(e.target.value)}
        onKeyDown={(e) => {
          if (e.key === "Enter") {
            e.preventDefault();
            handleAddPill();
          }
        }}
      ></Form.Control>

      <div style={{ marginTop: "10px" }}>
        {list.map((item, index) => (
          <Badge
            key={index}
            pill
            bg="success"
            style={{
              margin: "5px",
              display: "inline-flex",
              alignItems: "center",
              justifyContent: "space-between",
            }}
          >
            {item}
            <CloseButton
              style={{ marginLeft: "5px" }}
              onClick={() => handleRemovePill(index)}
            />
          </Badge>
        ))}
      </div>
    </>
  );
};
export default PillInputList;

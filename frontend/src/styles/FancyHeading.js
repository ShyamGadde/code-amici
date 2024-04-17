import styled from "styled-components";

export const FancyHeading = styled.span`
  position: relative;
  &:after {
    content: "";
    position: absolute;
    bottom: -10px;
    left: 0;
    width: 100%;
    height: 8px;
    background: #ffd200;
    border-radius: 10px;
  }
`;

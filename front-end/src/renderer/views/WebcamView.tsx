import { MenuItem } from "electron";
import * as React from "react";
import styled from "styled-components";
import MenuItem_ from "../MenuItem_";

const WebcamViewStyled = styled.div`
  margin: 0 8px;
`;

const WebcamView = () => {
  const greeting = "Hello Function Component!";

  return (
    <WebcamViewStyled>
      <MenuItem_
        optionName={"Option name"}
        optionDescription={"This is a description of the feature"}
        toggled={false}
      />
    </WebcamViewStyled>
  );
};

export default WebcamView;

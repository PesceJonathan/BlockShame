import { MenuItem } from "electron";
import * as React from "react";
import styled from "styled-components";
import { ActionType, store } from "_/utils/store";
import MenuItem_ from "../MenuItem_";

const WebcamViewStyled = styled.div`
  margin: 0 8px;
  width: 100%;
`;

const Title = styled.h1`
  margin: 15px 15px 0px 15px;
  font-size: 24px;
`;

const WebcamView = () => {
  const greeting = "Hello Function Component!";
  const context = React.useContext(store);
  return (
    <WebcamViewStyled>
      <Title>
          Webcam
      </Title>
      <MenuItem_
        optionName={"Option name"}
        optionDescription={"This is a description of the feature"}
        toggled={false}
        onToggle={(value: boolean) => {
          if(context && context.dispatch){
            context.dispatch({
              type: ActionType.toggleVideoAwayDetection,
              payload: value
            })
          }
        }}
      />
    </WebcamViewStyled>
  );
};

export default WebcamView;

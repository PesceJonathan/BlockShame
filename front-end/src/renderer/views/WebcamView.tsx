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
        optionName={"Detect User is away"}
        optionDescription={"Turns the camera off when the user is no longer on the camera"}
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
      <MenuItem_
        optionName={"Show custom image"}
        optionDescription={"Show a custom image when the user is away"}
        toggled={false}
        filePicker={true}
        onToggle={(value: boolean) => {
          if(context && context.dispatch){
            context.dispatch({
              type: ActionType.toggleCustomAwayImage,
              payload: value
            })
          }
        }}
        onFileChoose={(path: string) => {
          if(context && context.dispatch){
            context.dispatch({
              type: ActionType.setAwayBackgroundPath,
              payload: path
            })
          }
        }}
      />
    </WebcamViewStyled>
  );
};

export default WebcamView;

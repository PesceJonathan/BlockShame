import * as React from "react";
import styled from "styled-components";
import { store, ActionType, View } from "_utils/store";
import AudioView from "./views/AudioView";
import WebcamView from "./views/WebcamView";

const MainViewStyled = styled.div`
  height: 612px;
  display: flex;
  flex-direction: column;
  align-items: center;
`;
const viewMap = {
  [View.Webcam]: <WebcamView />,
  [View.Audio]: <AudioView />,
};

const MainView = (props: any) => {
  const { currentView } = React.useContext(store);
  return <MainViewStyled>{currentView && viewMap[currentView]}</MainViewStyled>;
};

export default MainView;

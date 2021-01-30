import * as React from "react";
import styled from "styled-components";
import { connect, sendMessage } from "_/utils/controller";
import { store, ActionType, View } from "_utils/store";
import AudioView from "./views/AudioView";
import WebcamView from "./views/WebcamView";
import AccessiblityView from "./views/AccessiblityView";

const MainViewStyled = styled.div`
  height: 612px;
  width: 100%;
  display: flex;
  flex-direction: column;
  align-items: center;
`;
const viewMap = {
  [View.Webcam]: <WebcamView />,
  [View.Audio]: <AudioView />,
  [View.Accessiblity]: <AccessiblityView />,
};

const MainView = (props: any) => {
  const {
    currentView,
    videoSettings,
    accessibilitySettings,
  } = React.useContext(store);

  React.useEffect(() => {
    connect().then(() => {
      console.log("Successfully connected");
    });
  }, []);

  React.useEffect(() => {
    console.log("Sending video config", videoSettings);
    sendMessage({ webcam: videoSettings }, "setting_change");
  }, [videoSettings]);

  React.useEffect(() => {
    console.log("Sending access config", accessibilitySettings);
    sendMessage({ accessibility: accessibilitySettings }, "setting_change");
  }, [accessibilitySettings]);

  return <MainViewStyled>{currentView && viewMap[currentView]}</MainViewStyled>;
};

export default MainView;

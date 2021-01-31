import * as React from "react";
import styled from "styled-components";
import { connect, sendMessage } from "_/utils/controller";
import { store, ActionType, View } from "_utils/store";
import AudioView from "./views/AudioView";
import WebcamView from "./views/WebcamView";
import AccessiblityView from "./views/AccessiblityView";
import Concentration from "./views/ConcentrationView";
import ConcentrationView from "./views/ConcentrationView";

const MainViewStyled = styled.div`
  width: 100%;
  display: flex;
  flex-direction: column;
  align-items: center;
  background: #f1f0e7;
  border-bottom-right-radius: 5px;
`;
const viewMap = {
  [View.Webcam]: <WebcamView />,
  [View.Audio]: <AudioView />,
  [View.Accessiblity]: <AccessiblityView />,
  [View.Concentration]: <ConcentrationView />
};

const MainView = (props: any) => {
  const {
    currentView,
    videoSettings,
    accessibilitySettings,
    audioSettings
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
    console.log("Sending audio config", audioSettings);
    sendMessage({ audio: audioSettings }, "setting_change");
  }, [audioSettings]);

  React.useEffect(() => {
    console.log("Sending access config", accessibilitySettings);
    sendMessage({ accessibility: accessibilitySettings }, "setting_change");
  }, [accessibilitySettings]);

  return <MainViewStyled>{currentView && viewMap[currentView]}</MainViewStyled>;
};

export default MainView;

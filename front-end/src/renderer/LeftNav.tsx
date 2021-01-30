import * as React from "react";
import styled from "styled-components";
import { store, ActionType, View } from "_utils/store";
import VideocamIcon from "@material-ui/icons/Videocam";
import SettingsVoiceIcon from "@material-ui/icons/Mic";
import HearingIcon from "@material-ui/icons/Hearing";

const LeftNavStyled = styled.div`
  background-color: #3c3c3c;
  width: 80px;
  height: 612px;
  padding: 8px 0px; /* this */
  display: flex;
  flex-direction: column;
  align-items: center;
`;

const ViewIconBackground = styled.div`
  display: flex;
  align-items: center;
  justify-content: center;
  margin-bottom: 8px;
  width: 50px;
  height: 50px;
  border-radius: 10px;
  background-color: ${(props: { primary: boolean }) =>
    props.primary ? "palevioletred" : "white"};
`;

interface ViewIconProps {
  onClick: () => void;
  children?: React.ReactNode;
  primary: boolean;
  icon: any;
}

const ViewIcon = ({ icon, primary, onClick }: ViewIconProps) => {
  return (
    <ViewIconBackground primary={primary} onClick={onClick}>
      {icon}
    </ViewIconBackground>
  );
};

const LeftNav = (props: any) => {
  const { currentView, dispatch } = React.useContext(store);

  return (
    <LeftNavStyled>
      {[
        {
          icon: <VideocamIcon fontSize="large" />,
          view: View.Webcam,
          primary: currentView === View.Webcam,
        },
        {
          icon: <SettingsVoiceIcon fontSize="large" />,
          view: View.Audio,
          primary: currentView === View.Audio,
        },
        {
          icon: <HearingIcon fontSize="large" />,
          view: View.Accessiblity,
          primary: currentView === View.Accessiblity,
        },
      ].map((el, index) => (
        <ViewIcon
          key={index}
          icon={el.icon}
          primary={el.primary}
          onClick={() => {
            if (dispatch) {
              dispatch({
                type: ActionType.SwitchView,
                payload: {
                  currentView: el.view.valueOf(),
                },
              });
            }
          }}
        />
      ))}
    </LeftNavStyled>
  );
};

export default LeftNav;

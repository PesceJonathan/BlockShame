import * as React from 'react';
import {WebcamViewStyled, Title} from './WebcamView';

import MenuItem_ from "../MenuItem_";
import { ActionType, store } from '_/utils/store';
const AudioView = () => {
  const greeting = 'Hello Function Component!';
  const context = React.useContext(store);
  return <WebcamViewStyled>
  <Title>Audio</Title>
  <MenuItem_
    optionName={"Mute microphone when video is off"}
    optionDescription={"Turns your microphone off when the user is no longer being showed on the camera"}
    toggled={false}
    onToggle={(value: boolean) => {
      if (context && context.dispatch) {
        context.dispatch({
          type: ActionType.toggleMuteAudioWhenVideoDisabled,
          payload: value,
        });
      }
    }}
  />
</WebcamViewStyled>
}
 
export default AudioView;
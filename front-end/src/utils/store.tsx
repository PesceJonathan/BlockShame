import * as React from "react";

export enum View {
  Webcam = "Webcam",
  Audio = "Audio",
  Accessiblity = "Accessiblity",
  Concentration = "Concentration",
}

export enum ActionType {
  SwitchView,
  toggleVideoAwayDetection,
  setAwayBackgroundPath,
  toggleCustomAwayImage,
  toggleAccesibilityConfig,
  toggleVideoSleepingDetection,
  toggleNotUserDetection,
  toggleMuteAudioWhenVideoDisabled,
}

interface Action {
  type: ActionType;
  payload?: any;
}

interface StoreState {
  currentView?: View;
  dispatch?: React.Dispatch<Action>;
  videoSettings: {
    videoAwaydetection: Boolean,
    useCustomAwayImage: Boolean,
    customImagePath: string,
    videoSleepingDetection: Boolean,
    videoNotUserDetection: Boolean,
  };
  audioSettings:{
    muteAudioWhenVideoIsDisabled: Boolean,
  }
  accessibilitySettings: {
    aslTranslation: Boolean;
    audioTranscriber: Boolean;
  };
}

const initialState: StoreState = {
  currentView: View.Webcam,
  videoSettings: {
    useCustomAwayImage: false,
    customImagePath: 'E:\Hackathon\BlockShame\VirtualWebcam\ErrorImage.png',
    videoAwaydetection: true,
    videoSleepingDetection: false,
    videoNotUserDetection: false,
  },
  audioSettings: {
    muteAudioWhenVideoIsDisabled: false
  },
  accessibilitySettings: {
    aslTranslation: false,
    audioTranscriber: false
  },
};

const store = React.createContext<StoreState>(initialState);
console.log(store);
const { Provider } = store;

const StateProvider = (props: { children: any }) => {
  const [state, dispatch] = React.useReducer((state: any, action: Action) => {
    switch (action.type) {
      case ActionType.SwitchView:
        console.log(state, action, { ...state, ...action.payload }  );
        const newState = { ...state, ...action.payload }; // do something with the action
        return { ...state, ...action.payload };;
      case ActionType.toggleVideoAwayDetection:
        console.log(state, action);
        return {
          ...state,
          videoSettings: {
            ...state.videoSettings,
            videoAwaydetection: action.payload,
          },
        };
      case ActionType.toggleAccesibilityConfig:
        console.log(state, action);
        return {
          ...state,
          accessibilitySettings: {
            ...state.accessibilitySettings,
            ...action.payload,
          },
        };
      case ActionType.toggleCustomAwayImage:
        console.log(state, action);
        return {
          ...state,
          videoSettings: {
            ...state.videoSettings,
            useCustomAwayImage: action.payload,
          },
        };
      case ActionType.setAwayBackgroundPath:
        console.log(state, action);
        return {
          ...state,
          videoSettings: {
            ...state.videoSettings,
            customImagePath: action.payload,
          },
        };

        case ActionType.toggleVideoSleepingDetection:
        console.log(state, action);
        return {
          ...state,
          videoSettings: {
            ...state.videoSettings,
            videoSleepingDetection: action.payload,
          },
        };

        case ActionType.toggleNotUserDetection:
        console.log(state, action);
        return {
          ...state,
          videoSettings: {
            ...state.videoSettings,
            videoNotUserDetection: action.payload,
          },
        };

        case ActionType.toggleMuteAudioWhenVideoDisabled:
        console.log(state, action);
        return {
          ...state,
          audioSettings: {
            ...state.audioSettings,
            muteAudioWhenVideoIsDisabled: action.payload,
          },
        };
      default:
        throw new Error();
    }
  }, initialState);
  return <Provider value={{ ...state, dispatch }}>{props.children}</Provider>;
};

export { store, StateProvider };

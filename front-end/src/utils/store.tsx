import * as React from "react";

export enum View {
  Webcam = "Webcam",
  Audio = "Audio",
  Accessiblity = "Accessiblity",
}

export enum ActionType {
  SwitchView,
  toggleVideoAwayDetection,
  toggleAccesibilityConfig,
}

interface Action {
  type: ActionType;
  payload?: any;
}

interface StoreState {
  currentView?: View;
  dispatch?: React.Dispatch<Action>;
  videoSettings: {
    videoAwaydetection: Boolean;
  };
  accessibilitySettings: {
    aslTranslation: Boolean;
  };
}

const initialState: StoreState = {
  currentView: View.Webcam,
  videoSettings: {
    videoAwaydetection: true,
  },
  accessibilitySettings: {
    aslTranslation: false,
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
      default:
        throw new Error();
    }
  }, initialState);
  return <Provider value={{ ...state, dispatch }}>{props.children}</Provider>;
};

export { store, StateProvider };

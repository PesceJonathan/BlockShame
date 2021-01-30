import * as React from 'react';

export enum View {
  Webcam = "Webcam",
  Audio = "Audio",
}

export enum ActionType {
  SwitchView,
  toggleVideoAwayDetection,
  setAwayBackgroundPath,
  toggleCustomAwayImage
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
  }
}

const initialState: StoreState = {
  currentView: View.Webcam,
  videoSettings: {
    videoAwaydetection: true,
    useCustomAwayImage: false,
    customImagePath: ''
  }
};

const store = React.createContext<StoreState>(initialState);
console.log(store)
const { Provider } = store;

const StateProvider = (props: { children: any }) => {
  const [state, dispatch] = React.useReducer((state: any, action: Action) => {
    switch (action.type) {
      case ActionType.SwitchView:
        const newState = { ...initialState, ...action.payload }; // do something with the action
        return newState;
      case ActionType.toggleVideoAwayDetection:
        console.log(initialState, action);
        return {...initialState, videoSettings: {...initialState.videoSettings, videoAwaydetection: action.payload}}
      default:
        throw new Error();
    }
  }, initialState);
  return (<Provider value={{ ...state, dispatch }}>{props.children}</Provider>);
};

export { store, StateProvider };

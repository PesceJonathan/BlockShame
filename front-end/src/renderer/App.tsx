import * as React from "react";
import styled from "styled-components";
import { createMuiTheme, ThemeProvider } from "@material-ui/core/styles";
import LeftNav from "./LeftNav";
import MainView from "./MainView";
import { startProgram } from "_utils/controller";

const AppStyled = styled.div`
  display: flex;
  flex-direction: row;
  height: 100%;
`;
const App = (props: any) => {
  let theme = createMuiTheme();
  // {palette: {
  //   primary: {
  //     main: '#E33E7F'
  //   }
  // }
  React.useEffect(() => {}, []);
  
  
  return (
    <ThemeProvider theme={theme}>
      <AppStyled>
        <LeftNav />
        <MainView />
      </AppStyled>
    </ThemeProvider>
  );
};

const Boom = styled.div`
  display: block;
  line-height: 32px;
  font-size: 28px;
  font-weight: bold;
`;

const Motto = styled.div`
  line-height: 32px;
  font-size: 14px;
  font-weight: light;
`;
export default App;

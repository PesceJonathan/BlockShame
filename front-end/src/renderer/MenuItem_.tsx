import * as React from "react";
import styled from "styled-components";
import Switch from "@material-ui/core/Switch";
import boomSwitchStyle from "_utils/boomSwitchStyle";
import { makeStyles } from "@material-ui/core/styles";
let dialog = require('electron').remote.dialog
const MenuItemStyled = styled.div`
  display: flex;
  width: 100%;
  flex-direction: row;
  align-items: center;
  padding: 0px 15px;
  box-sizing: border-box;
  /* background: red; */
`;

const Item = styled.div`
  display: flex;
  flex-direction: column;
  justify-content: center;
  height: 75px;  
`;

const Title = styled.h3`
  font-size: 18px;
  margin: 0;
`;

const Desc = styled.h4`
  font-weight: 400;
  font-size: 15px;
  margin: 0;
`;

const SwitchContainer = styled.div`
  display: flex;
  flex-direction: column;
  justify-content: flex-end;
  margin-left: auto;
`;

const StyledSwitch = styled(Switch)`
  margin-left: auto;
`
// @ts-ignore
const useStyles = makeStyles(boomSwitchStyle);
const Button = styled.a`
  text-align: center;
  font-size: 12px;
  :hover{
    cursor: pointer;
  }
`;
interface Props {
  optionName: string;
  optionDescription?: string;
  toggled?: boolean;
  onToggle: (value: boolean) => void;
  filePicker?: boolean;
  onFileChoose?: (value: string) => void;
}
const MenuItem = (props: Props) => {
  const classes = useStyles(props);
  const [toggled, setToggled] = React.useState(false);

  return (
    <MenuItemStyled>
      <Item>
        <Title>{props.optionName}</Title>
        {props.optionDescription && <Desc>{props.optionDescription}</Desc>}
      </Item>
      <SwitchContainer>
        <StyledSwitch
          classes={classes}
          checked={toggled}
          onChange={(e) => {
            setToggled(e.target.checked)
            props.onToggle(e.target.checked)
          }}
        />
        {props.filePicker == true && <Button onClick={() => {
          dialog.showOpenDialog({filters: [
            { name: 'Images', extensions: ['jpg', 'png', 'gif'] }], properties: ['openFile']}).then((val) => {
                if(val?.filePaths[0]){
                  if(props.onFileChoose)
                    props.onFileChoose(val?.filePaths[0]);
                }
            })
        }}> Pick image </Button>}
      </SwitchContainer>
    </MenuItemStyled>
  );
};

export default MenuItem;

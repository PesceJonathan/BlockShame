import * as React from "react";
import styled from "styled-components";
import Switch from "@material-ui/core/Switch";
import boomSwitchStyle from "_utils/boomSwitchStyle";
import { makeStyles } from "@material-ui/core/styles";

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
  margin: 0;
`;

const Desc = styled.h4`
  font-weight: 300;
  margin: 0;
`;

const SwitchContainer = styled.div`
  margin-left: auto;
`;

// @ts-ignore
const useStyles = makeStyles(boomSwitchStyle);

interface Props {
  optionName: string;
  optionDescription?: string;
  toggled?: boolean;
  onToggle: (value: boolean) => void;
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
        <Switch
          classes={classes}
          checked={toggled}
          onChange={(e) => {
            setToggled(e.target.checked)
            props.onToggle(e.target.checked)
          }}
        />
      </SwitchContainer>
    </MenuItemStyled>
  );
};

export default MenuItem;
